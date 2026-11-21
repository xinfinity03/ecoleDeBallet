"""Stellt eine fotografierte Buntstift-Zeichnung frei und verschönert sie.

- gleicht ungleichmäßige Beleuchtung / Papierfarbe aus
- entfernt den Papierhintergrund (transparentes PNG)
- verstärkt die Farben und glättet die Buntstift-Lücken leicht

Aufruf: python3 zeichnung_freistellen.py eingabe.jpg ausgabe.png [--crop l,o,r,u] [--schwelle 190,55]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance


def background_estimate(rgb, scale=8):
    """Papierfarbe schätzen: Bild verkleinern, Striche wegfiltern (Max), weichzeichnen."""
    h, w = rgb.shape[:2]
    small = Image.fromarray(rgb).resize((w // scale, h // scale), Image.BILINEAR)
    for _ in range(3):
        small = small.filter(ImageFilter.MaxFilter(9))
    small = small.filter(ImageFilter.GaussianBlur(12))
    return np.asarray(small.resize((w, h), Image.BILINEAR)).astype(np.float32)


def fill_holes(mask):
    """Löcher in der Maske schließen (Flood-Fill vom Rand aus)."""
    m = Image.fromarray((mask * 255).astype(np.uint8))
    padded = ImageOps.expand(m, border=2, fill=0)
    from PIL import ImageDraw
    ImageDraw.floodfill(padded, (0, 0), 128)
    arr = np.asarray(padded)[2:-2, 2:-2]
    return arr != 128


def largest_component(mask, scale=4):
    """Größte zusammenhängende Fläche finden (auf verkleinerter Maske, BFS)."""
    from collections import deque
    h, w = mask.shape
    small = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                       .resize((w // scale, h // scale), Image.NEAREST)) > 127
    sh, sw = small.shape
    labels = np.zeros((sh, sw), np.int32)
    best, best_size, cur = 0, 0, 0
    for y in range(sh):
        for x in range(sw):
            if small[y, x] and not labels[y, x]:
                cur += 1
                q = deque([(y, x)]); labels[y, x] = cur; size = 0
                while q:
                    cy, cx = q.popleft(); size += 1
                    for ny, nx in ((cy+1,cx),(cy-1,cx),(cy,cx+1),(cy,cx-1)):
                        if 0 <= ny < sh and 0 <= nx < sw and small[ny, nx] and not labels[ny, nx]:
                            labels[ny, nx] = cur; q.append((ny, nx))
                if size > best_size:
                    best, best_size = cur, size
    keep = Image.fromarray(((labels == best) * 255).astype(np.uint8)).resize((w, h), Image.NEAREST)
    keep = keep.filter(ImageFilter.MaxFilter(9))
    return mask & (np.asarray(keep) > 127)


def clip_to_outline(norm, mask, close=8, s=4):
    """Bereich innerhalb der Bleistift-Umrisslinie bestimmen und die Maske darauf begrenzen.
    Rechnet auf verkleinertem Bild; close = Lückenbreite (in kleinen Pixeln), die überbrückt wird."""
    lum = norm.mean(axis=2)
    sat = norm.max(axis=2) - norm.min(axis=2)
    line = (lum < 170) & (sat < 40) & mask
    h, w = mask.shape
    m = Image.fromarray((line * 255).astype(np.uint8)).resize((w // s, h // s), Image.BILINEAR)
    m = m.point(lambda v: 255 if v > 40 else 0)
    k = 2 * close + 1
    m = m.filter(ImageFilter.MaxFilter(k))                # Lücken in der Linie schließen
    core = Image.fromarray((mask * 255).astype(np.uint8)).resize((w // s, h // s), Image.BILINEAR)
    core = core.filter(ImageFilter.MinFilter(21))          # Innenbereich der Form
    inside = fill_holes((np.asarray(m) > 127) | (np.asarray(core) > 127))
    m = Image.fromarray((inside * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k))
    band = m.filter(ImageFilter.MaxFilter(5))              # schmaler Streifen um den Innenbereich
    tight = np.asarray(m.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))) > 127
    band = np.asarray(band.resize((w, h), Image.BILINEAR)) > 127
    # Bleistiftlinie im Randstreifen behalten, blasse übermalte Farbe wegschneiden
    soft_line = (lum < 185) & (sat < 50)
    soft_line = np.asarray(Image.fromarray((soft_line * 255).astype(np.uint8))
                           .filter(ImageFilter.MaxFilter(3))) > 127
    # breite Flächen der Form behalten, auch wo der Umriss offen ist (nur dünne Fransen fallen weg)
    body = Image.fromarray((mask * 255).astype(np.uint8)).resize((w // s, h // s), Image.BILINEAR)
    body = body.filter(ImageFilter.MinFilter(13)).filter(ImageFilter.MaxFilter(9))
    body = np.asarray(body.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))) > 127
    inside = tight | body | (band & soft_line)
    if inside.sum() > 0.6 * mask.sum():
        return mask & inside
    print("  Hinweis: Umriss nicht geschlossen, Begrenzung übersprungen")
    return mask


def _box(a, r, axis):
    """Box-Weichzeichner (Breite 2r+1) entlang einer Achse, Ränder gespiegelt."""
    if r < 1:
        return a
    pad = [(0, 0), (0, 0)]; pad[axis] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="reflect"), axis=axis, dtype=np.float64)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return ((hi - lo) / (2 * r + 1)).astype(np.float32)


def _blur_small(a, radius, s=4):
    """Gauß-ähnliches Weichzeichnen in Fließkomma auf verkleinerter Kopie (schnell, ohne Streifen)."""
    h, w = a.shape
    hs, ws = h // s, w // s
    small = a[:hs * s, :ws * s].reshape(hs, s, ws, s).mean(axis=(1, 3)).astype(np.float32)
    sigma = radius / s
    r = int(round((np.sqrt(4 * sigma * sigma + 1) - 1) / 2))
    for _ in range(3):
        small = _box(_box(small, r, 0), r, 1)
    up = Image.fromarray(small, "F").resize((w, h), Image.BILINEAR)
    return np.asarray(up)


def _normconv(color, w, radius):
    num = np.stack([_blur_small(color[..., c] / 255 * w, radius) for c in range(3)], -1) * 255
    den = _blur_small(w, radius)
    return np.clip(num / np.maximum(den[..., None], 1e-4), 0, 255), den


def _kmeans(x, k, iters=20, seed=1):
    rng = np.random.default_rng(seed)
    c = x[rng.choice(len(x), k, replace=False)]
    for _ in range(iters):
        lab = ((x[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        c = np.array([x[lab == i].mean(0) if (lab == i).any() else c[i] for i in range(k)])
    return c


def _hue(c):
    import colorsys
    return colorsys.rgb_to_hsv(*(np.asarray(c) / 255))[0] * 360


def fill_gaps(norm, mask, k=4):
    """Fläche ganz ausmalen.
    1. Buntstiftfarben in Gruppen einteilen (gleicher Farbton = eine Gruppe).
    2. Jede Stelle gehört zu der Gruppe, die in der Umgebung am häufigsten ist -> klare Flächen.
    3. Innerhalb der Gruppe wird die Farbe der kräftigen Striche in der Nähe genommen
       (so bleiben z.B. braune Sofabeine braun). Bleistiftlinien bleiben erhalten."""
    lum = norm.mean(axis=2)
    sat = norm.max(axis=2) - norm.min(axis=2)
    line = np.clip((192 - lum) / 35, 0, 1) * np.clip((60 - sat) / 25, 0, 1) * mask
    dense = _blur_small((line > 0.5).astype(np.float32), 6, s=2)
    line = line * np.clip((dense - 0.12) / 0.15, 0, 1)
    painted = (sat > 30) & (lum < 238) & mask & (line < 0.3)

    px = norm[painted]
    sample = px[np.random.default_rng(0).choice(len(px), min(len(px), 20000), replace=False)]
    centers = _kmeans(sample, k)
    lab = ((norm[..., None, :] - centers[None, None]) ** 2).sum(-1).argmin(-1)
    hues = [_hue(c) for c in centers]
    for i in range(k):
        for j in range(i):
            d = abs(hues[i] - hues[j]); d = min(d, 360 - d)
            if d < 12:
                lab[lab == i] = j
    groups = [g for g in np.unique(lab[painted]) if (painted & (lab == g)).sum() > 200]

    strength = np.clip((sat - 30) / 50, 0, 1) ** 2
    votes, fills = [], []
    for g in groups:
        sel = painted & (lab == g)
        selw = sel.astype(np.float32)
        votes.append(_blur_small(selw, 18) + 0.3 * _blur_small(selw, 80))
        w = selw * strength
        cp = norm[sel]; ss = cp.max(1) - cp.min(1)
        base = np.median(cp[ss >= np.percentile(ss, 85)], axis=0)
        near, d1 = _normconv(norm, w, 15)
        far, d2 = _normconv(norm, w, 60)
        t1 = np.clip(d1 / 0.04, 0, 1)[..., None]
        t2 = np.clip(d2 / 0.01, 0, 1)[..., None]
        f = near * t1 + (far * t2 + base * (1 - t2)) * (1 - t1)
        fills.append(f * 0.6 + base * 0.4)   # gleichmäßiger, aber mit lokaler Farbe
    cls = np.stack(votes, -1).argmax(-1)
    fill = np.zeros_like(norm)
    for i in range(len(groups)):
        fill[cls == i] = fills[i][cls == i]

    fill = fill * 0.9 + np.minimum(norm, fill) * 0.1   # Hauch Buntstift-Struktur
    line_col = np.full(3, 95.0)
    out = fill * (1 - line[..., None]) + line_col * line[..., None]
    out = np.where(mask[..., None], out, norm)
    return np.clip(out, 0, 255)


LUM, SAT = 190, 55

def process(src, dst, crop=None):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    rgb = np.asarray(im).astype(np.float32)

    bg = background_estimate(np.asarray(im))
    # Beleuchtung ausgleichen: Papier -> weiß
    norm = np.clip(rgb / np.maximum(bg, 1) * 255.0, 0, 255)

    # Vordergrund: dunkler als Papier oder farbig
    lum = norm.mean(axis=2)
    sat = norm.max(axis=2) - norm.min(axis=2)
    fg = (lum < LUM) | (sat > SAT)

    # Maske säubern: schließen, Löcher füllen, kleine Krümel entfernen
    m = Image.fromarray((fg * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
    m = m.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))
    mask = fill_holes(np.asarray(m) > 127)

    # nur die größte zusammenhängende Form behalten (entfernt Papierreste/Schatten)
    mask = largest_component(mask)

    # Fransen entfernen: dünne Ausläufer wegschneiden, Umriss glätten
    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MinFilter(13)).filter(ImageFilter.MaxFilter(13))
    m = m.filter(ImageFilter.GaussianBlur(6)).point(lambda v: 255 if v > 127 else 0)
    mask = np.asarray(m) > 127
    alpha = m.filter(ImageFilter.GaussianBlur(1.5))

    # Farbe, die über den Bleistift-Umriss hinausgemalt wurde, abschneiden
    mask = clip_to_outline(norm, mask)
    m = Image.fromarray((mask * 255).astype(np.uint8))
    alpha = m.filter(ImageFilter.GaussianBlur(1.5))

    # Fläche ganz ausmalen: weiße Papierlücken mit der Farbe der Umgebung füllen
    norm = fill_gaps(norm, mask)

    # Farben verschönern
    out = Image.fromarray(norm.astype(np.uint8))
    out = out.filter(ImageFilter.GaussianBlur(0.8))
    out = ImageEnhance.Color(out).enhance(1.3)
    out = ImageEnhance.Contrast(out).enhance(1.08)

    out.putalpha(alpha)
    bbox = alpha.point(lambda v: 255 if v > 20 else 0).getbbox()
    if bbox:
        pad = 10
        bbox = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
                min(bbox[2] + pad, out.width), min(bbox[3] + pad, out.height))
        out = out.crop(bbox)
    out.save(dst, optimize=True)
    print(dst, out.size)


if __name__ == "__main__":
    crop = None
    if "--crop" in sys.argv:
        i = sys.argv.index("--crop")
        crop = tuple(int(v) for v in sys.argv[i + 1].split(","))
    if "--schwelle" in sys.argv:  # z.B. --schwelle 200,40 (Helligkeit, Farbigkeit)
        i = sys.argv.index("--schwelle")
        LUM, SAT = (int(v) for v in sys.argv[i + 1].split(","))
    process(sys.argv[1], sys.argv[2], crop)
