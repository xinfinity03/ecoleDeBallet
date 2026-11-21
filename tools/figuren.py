"""Zeichnet die Figuren der École de Ballet Étoile (Vorderansicht) als Übersichtsbild.

Die Figuren werden aus Teilen zusammengesetzt (Haut, Frisur, Haarfarbe, Kleidung, Größe,
Haltung, Gesichtsausdruck). Dasselbe Baukastensystem dient später für den Avatar-Editor.

Aufruf: python3 figuren.py -> assets/konzept/figuren.svg
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "konzept" / "figuren.svg"
LINE = "#5b3d4a"
LW = 2.2

SKIN = {"hell": "#f6d2b8", "mittel": "#e2ad84", "dunkel": "#8a5636"}
HAIR = {"braun": "#7a4a2b", "blond": "#f0cc6e", "hellblond": "#f6dc8f", "schwarz": "#2a2030", "dunkelbraun": "#4a2c1c"}

# Kopf-Mittelpunkt und Maße (Figur steht bei y=0, Höhe ca. 300 bei Größe 1.0)
HX, HY, HR = 0, -236, 35


def outlined(d, color, width, outline=LINE):
    """Dicker Strich mit Kontur (für Arme und Beine)."""
    return (f'<path d="{d}" fill="none" stroke="{outline}" stroke-width="{width + LW * 2}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ Frisuren
def hair_back(style, c):
    if style == "lang_glatt":
        return (f'<path d="M-40 -238 C-46 -286 46 -286 40 -238 L46 -150 Q48 -128 40 -122 Q0 -112 -40 -122 '
                f'Q-48 -128 -46 -150 Z" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>')
    if style == "schulter":
        return (f'<path d="M-40 -238 C-46 -286 46 -286 40 -238 L44 -196 Q46 -182 34 -180 Q0 -176 -34 -180 '
                f'Q-46 -182 -44 -196 Z" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>')
    if style == "locken_lang":
        pts = [(-40, -250), (-44, -228), (-46, -206), (-44, -184), (-38, -166), (40, -250), (44, -228),
               (46, -206), (44, -184), (38, -166), (-30, -270), (30, -270), (0, -280), (-16, -278), (16, -278)]
        circles = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>' for x, y in pts)
        fill = f'<path d="M-44 -250 Q0 -300 44 -250 L42 -170 Q0 -160 -42 -170 Z" fill="{c}"/>'
        return circles + fill
    if style == "dutt":
        return f'<circle cx="0" cy="-282" r="17" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>'
    return ""


def hair_front(style, c):
    if style in ("lang_glatt", "schulter"):
        part = "M0 -270 Q-4 -258 -2 -250" if style == "lang_glatt" else ""
        bangs = ("M-37 -236 C-40 -284 40 -284 37 -236 Q28 -262 4 -262 Q-2 -256 -10 -252 Q-28 -248 -37 -236 Z"
                 if style == "schulter" else
                 "M-37 -234 C-40 -284 40 -284 37 -234 Q30 -258 2 -264 Q-30 -258 -37 -234 Z")
        return (f'<path d="{bangs}" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>'
                + (f'<path d="{part}" stroke="{LINE}" stroke-width="1.5" fill="none" opacity=".5"/>' if part else ""))
    if style == "locken_lang":
        cs = [(-26, -262, 12), (-8, -268, 12), (10, -268, 12), (27, -261, 12), (-36, -246, 10), (36, -246, 10)]
        return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>' for x, y, r in cs)
    if style == "dutt":
        return (f'<path d="M-36 -234 C-38 -280 38 -280 36 -234 Q30 -262 0 -266 Q-30 -262 -36 -234 Z" fill="{c}" '
                f'stroke="{LINE}" stroke-width="{LW}"/>'
                f'<path d="M-2 -268 Q-14 -256 -30 -246" stroke="{LINE}" stroke-width="1.3" fill="none" opacity=".5"/>')
    if style == "kurz":
        return (f'<path d="M-37 -230 C-42 -286 42 -286 37 -230 Q34 -250 26 -256 Q6 -248 -12 -258 Q-30 -252 -37 -230 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>')
    if style == "locken_kurz":
        cs = [(-30, -250), (-20, -266), (-4, -273), (13, -271), (27, -261), (35, -244), (-36, -236), (36, -232)]
        base = f'<path d="M-36 -236 C-38 -284 38 -284 36 -236 Z" fill="{c}"/>'
        return base + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>' for x, y in cs)
    if style == "stachelig":
        return (f'<path d="M-37 -232 C-40 -262 -34 -270 -30 -274 L-26 -290 L-16 -278 L-8 -296 L2 -280 L12 -296 L18 -278 '
                f'L30 -288 L30 -270 C38 -262 40 -248 37 -232 Q30 -252 14 -254 Q0 -246 -14 -254 Q-30 -250 -37 -232 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>')
    if style == "wellig":
        return (f'<path d="M-37 -230 C-42 -288 42 -288 37 -230 Q36 -250 28 -256 Q20 -246 10 -256 Q0 -246 -10 -256 '
                f'Q-20 -246 -28 -256 Q-36 -250 -37 -230 Z" fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>')
    if style == "seitenscheitel":
        return (f'<path d="M-37 -230 C-42 -286 42 -286 37 -230 Q35 -248 28 -254 Q10 -262 -14 -262 Q-30 -254 -37 -230 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="{LW}"/>'
                f'<path d="M-14 -262 Q-4 -276 6 -278" stroke="{LINE}" stroke-width="1.4" fill="none" opacity=".55"/>'
                f'<path d="M-12 -262 Q8 -266 30 -252" stroke="{LINE}" stroke-width="1.2" fill="none" opacity=".35"/>')
    if style == "gegelt":
        return (f'<path d="M-37 -232 C-40 -268 -26 -284 -4 -292 Q20 -300 34 -286 Q26 -284 22 -280 C36 -272 40 -252 37 -232 '
                f'Q32 -258 4 -262 Q-26 -258 -37 -232 Z" fill="{c}" stroke="{LINE}" stroke-width="{LW}" stroke-linejoin="round"/>'
                f'<path d="M-20 -266 Q-6 -284 18 -288 M-28 -254 Q-14 -272 6 -276" stroke="#fff" stroke-width="3" '
                f'fill="none" stroke-linecap="round" opacity=".75"/>'
                f'<circle cx="24" cy="-276" r="2.4" fill="#fff" opacity=".9"/>')
    return ""


# ------------------------------------------------------------------ Gesicht
def face(expr, eye_color="#4a3528"):
    out = []
    ey = HY + 2
    if expr == "eingebildet":
        for sx in (-1, 1):
            x = sx * 13
            out.append(f'<path d="M{x - 7} {ey} q7 7 14 0" fill="{eye_color}" stroke="{LINE}" stroke-width="1.5"/>')
            out.append(f'<path d="M{x - 8} {ey} h16" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round"/>')
        out.append(f'<path d="M-20 {ey - 14} q7 -4 14 0" stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M6 {ey - 19} q8 -5 15 1" stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M-6 {ey + 20} q10 4 16 -4" stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    else:
        look = (-2, 2) if expr == "schuechtern" else (0, 0)
        for sx in (-1, 1):
            x = sx * 13
            out.append(f'<ellipse cx="{x}" cy="{ey}" rx="6" ry="7.5" fill="#fff" stroke="{LINE}" stroke-width="1.4"/>')
            out.append(f'<ellipse cx="{x + look[0]}" cy="{ey + 1 + look[1]}" rx="4.6" ry="5.8" fill="{eye_color}"/>')
            out.append(f'<circle cx="{x + look[0] + 1.6}" cy="{ey - 1.5 + look[1]}" r="1.8" fill="#fff"/>')
            if expr == "streng":
                out.append(f'<path d="M{x + 9 * sx} {ey - 17} L{x - 7 * sx} {ey - 11}" stroke="{LINE}" stroke-width="2.6" stroke-linecap="round"/>')
            elif expr == "schuechtern":
                out.append(f'<path d="M{x - 7} {ey - 12} q7 -4 14 0" transform="rotate({8 * sx} {x} {ey - 12})" stroke="{LINE}" stroke-width="2" fill="none" stroke-linecap="round"/>')
            else:
                out.append(f'<path d="M{x - 7} {ey - 13} q7 -6 14 0" stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        if expr == "froh":
            out.append(f'<path d="M-9 {ey + 15} q9 13 18 0 z" fill="#b8475c" stroke="{LINE}" stroke-width="1.6" stroke-linejoin="round"/>'
                       f'<path d="M-4 {ey + 21} q4 -3 8 0" fill="#f28a9b"/>')
        elif expr == "streng":
            out.append(f'<path d="M-7 {ey + 19} h14" stroke="{LINE}" stroke-width="2.2" stroke-linecap="round"/>')
        elif expr == "schuechtern":
            out.append(f'<path d="M-4 {ey + 18} q4 3 8 0" stroke="{LINE}" stroke-width="2" fill="none" stroke-linecap="round"/>')
        else:
            out.append(f'<path d="M-8 {ey + 16} q8 8 16 0" stroke="{LINE}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    blush = .75 if expr == "schuechtern" else .45
    out.append(f'<ellipse cx="-22" cy="{ey + 12}" rx="6.5" ry="4" fill="#f28a9b" opacity="{blush}"/>'
               f'<ellipse cx="22" cy="{ey + 12}" rx="6.5" ry="4" fill="#f28a9b" opacity="{blush}"/>')
    out.append(f'<path d="M-1 {ey + 8} q2 3 4 0" stroke="{LINE}" stroke-width="1.4" fill="none" opacity=".6"/>')
    return "".join(out)


# ------------------------------------------------------------------ Arme
SH = 23, -186  # Schulter


def arm(pose, side, sleeve):
    sx = side
    x0, y0 = sx * SH[0], SH[1]
    paths = {
        "unten": f"M{x0} {y0} Q{sx * 36} {-150} {sx * 37} {-112}",
        "offen": f"M{x0} {y0} Q{sx * 52} {-184} {sx * 84} {-170}",
        "oben": f"M{x0} {y0} Q{sx * 52} {-236} {sx * 16} {-292}",
        "huefte": f"M{x0} {y0} L{sx * 48} {-156} L{sx * 24} {-128}",
        "winken": f"M{x0} {y0} Q{sx * 52} {-210} {sx * 54} {-258}",
        "buch": f"M{x0} {y0} Q{sx * 32} {-150} {sx * 12} {-146}",
    }
    ends = {"unten": (37, -112), "offen": (84, -170), "oben": (16, -292), "huefte": (24, -128),
            "winken": (54, -258), "buch": (12, -146)}
    d = paths[pose]
    hx, hy = ends[pose]
    s = outlined(d, sleeve, 11)
    if pose != "huefte":
        s += f'<circle cx="{sx * hx}" cy="{hy}" r="7.5" fill="var(--skin)" stroke="{LINE}" stroke-width="{LW}"/>'
    return s


def figure(p):
    """p: dict mit skin, hair_style, hair, eyes, kind ('m'/'w'/'lehrerin'), color, height, arms(l,r), expr, extra."""
    skin = SKIN[p["skin"]]
    hc = HAIR[p["hair"]]
    kind = p["kind"]
    col = p["color"]
    s = p.get("height", 1.0)
    g = [f'<g transform="translate({p["x"]},{p["y"]}) scale({s})" style="--skin:{skin}">']
    g.append(f'<ellipse cx="0" cy="2" rx="{52 / s:.0f}" ry="8" fill="#000" opacity=".12"/>')
    g.append(hair_back(p["hair_style"], hc))
    # Beine
    leg = "#f3cfd6" if kind == "w" else ("#2f2838" if kind == "lehrerin" else "#3a3550")
    g.append(outlined("M-11 -116 L-13 -10", leg, 15))
    g.append(outlined("M11 -116 L13 -10", leg, 15))
    shoe = {"w": "#f7b6c8", "m": "#f4f0ea", "lehrerin": "#f7b6c8"}[kind]
    g.append(f'<ellipse cx="-15" cy="-5" rx="11" ry="6" fill="{shoe}" stroke="{LINE}" stroke-width="{LW}"/>'
             f'<ellipse cx="15" cy="-5" rx="11" ry="6" fill="{shoe}" stroke="{LINE}" stroke-width="{LW}"/>')
    # Hals
    g.append(f'<rect x="-8" y="-206" width="16" height="22" fill="var(--skin)" stroke="{LINE}" stroke-width="{LW}"/>')
    # Oberkörper
    if kind == "w":
        g.append(f'<path d="M-23 -190 Q0 -184 23 -190 L19 -150 Q16 -130 20 -116 L-20 -116 Q-16 -130 -19 -150 Z" '
                 f'fill="{col}" stroke="{LINE}" stroke-width="{LW}" stroke-linejoin="round"/>')
        g.append(f'<path d="M-15 -190 Q0 -178 15 -190" fill="var(--skin)" stroke="{LINE}" stroke-width="1.6"/>')
        light = p.get("tutu", col)
        g.append(f'<ellipse cx="0" cy="-120" rx="64" ry="13" fill="{light}" stroke="{LINE}" stroke-width="{LW}" opacity=".9"/>')
        g.append(f'<path d="M-64 -121 Q-46 -100 -34 -111 Q-22 -98 -11 -109 Q0 -97 11 -109 Q22 -98 34 -111 Q46 -100 64 -121 '
                 f'Q0 -140 -64 -121 Z" fill="{light}" stroke="{LINE}" stroke-width="{LW}" stroke-linejoin="round"/>')
        g.append(f'<path d="M-40 -116 l-4 8 M-14 -112 l-2 9 M14 -112 l2 9 M40 -116 l4 8" stroke="#fff" stroke-width="2" opacity=".7"/>')
    elif kind == "m":
        g.append(f'<path d="M-25 -190 Q0 -184 25 -190 L23 -150 L21 -110 L-21 -110 L-23 -150 Z" '
                 f'fill="{col}" stroke="{LINE}" stroke-width="{LW}" stroke-linejoin="round"/>')
        g.append(f'<path d="M-9 -190 Q0 -180 9 -190" fill="var(--skin)" stroke="{LINE}" stroke-width="1.6"/>')
        g.append(f'<rect x="-22" y="-118" width="44" height="8" fill="#3a3550" stroke="{LINE}" stroke-width="1.6"/>')
    else:  # Lehrerin: schwarzer Body, Wickelrock
        g.append(f'<path d="M-22 -190 Q0 -184 22 -190 L18 -150 Q15 -132 19 -118 L-19 -118 Q-15 -132 -18 -150 Z" '
                 f'fill="{col}" stroke="{LINE}" stroke-width="{LW}"/>')
        g.append(f'<path d="M-13 -190 Q0 -170 13 -190" fill="var(--skin)" stroke="{LINE}" stroke-width="1.6"/>')
        g.append(f'<path d="M-22 -124 Q0 -130 22 -124 L36 -62 Q0 -52 -36 -62 Z" fill="#3b3346" stroke="{LINE}" stroke-width="{LW}"/>'
                 f'<path d="M12 -124 Q20 -96 30 -63" stroke="{LINE}" stroke-width="1.4" fill="none" opacity=".6"/>')
        for k in range(7):  # Perlenkette
            g.append(f'<circle cx="{-12 + k * 4}" cy="{-186 + abs(3 - k) * -1.6 + 6}" r="2.2" fill="#fff" stroke="#c9c2cc" stroke-width=".8"/>')
    sleeve = "var(--skin)" if kind in ("w",) else (col if kind == "m" else "#2f2838")
    # Arme hinter dem Kopf zuerst? Erhobene Arme werden nach dem Kopf gezeichnet
    la, ra = p["arms"]
    behind = [(la, -1), (ra, 1)]
    for pose, side in behind:
        if pose != "oben":
            g.append(arm(pose, side, sleeve))
    # Kopf
    g.append(f'<ellipse cx="-35" cy="{HY + 2}" rx="6" ry="8" fill="var(--skin)" stroke="{LINE}" stroke-width="{LW}"/>'
             f'<ellipse cx="35" cy="{HY + 2}" rx="6" ry="8" fill="var(--skin)" stroke="{LINE}" stroke-width="{LW}"/>')
    g.append(f'<ellipse cx="{HX}" cy="{HY}" rx="{HR}" ry="{HR + 2}" fill="var(--skin)" stroke="{LINE}" stroke-width="{LW}"/>')
    g.append(face(p.get("expr", "nett"), p.get("eyes", "#4a3528")))
    g.append(hair_front(p["hair_style"], hc))
    # Extras
    ex = p.get("extra")
    if ex == "kopfhoerer":
        g.append(f'<path d="M-30 -184 Q0 -164 30 -184" fill="none" stroke="#e85d8a" stroke-width="5"/>'
                 f'<rect x="-36" y="-192" width="13" height="18" rx="5" fill="#e85d8a" stroke="{LINE}" stroke-width="1.6"/>'
                 f'<rect x="23" y="-192" width="13" height="18" rx="5" fill="#e85d8a" stroke="{LINE}" stroke-width="1.6"/>')
    if ex == "diadem":
        g.append(f'<path d="M-20 -266 L-14 -280 L-6 -270 L0 -286 L6 -270 L14 -280 L20 -266 Z" fill="#f6c64b" stroke="{LINE}" stroke-width="1.6"/>'
                 f'<circle cx="0" cy="-277" r="3" fill="#f28ab0"/>')
    if ex == "buch":
        g.append(f'<g transform="rotate(-6 0 -150)"><rect x="-26" y="-170" width="52" height="36" rx="3" fill="#7fa6e0" stroke="{LINE}" stroke-width="{LW}"/>'
                 f'<line x1="0" y1="-170" x2="0" y2="-134" stroke="{LINE}" stroke-width="1.6"/>'
                 f'<path d="M-20 -160 h14 M-20 -152 h12 M6 -160 h14 M6 -152 h10" stroke="#fff" stroke-width="2"/></g>')
    if ex == "notenblatt":
        g.append(f'<g transform="translate(60,-286) rotate(12)"><path d="M0 0 v-16 l10 -3 v16" fill="none" stroke="{LINE}" stroke-width="2"/>'
                 f'<ellipse cx="-3" cy="1" rx="4" ry="3" fill="{LINE}"/><ellipse cx="7" cy="-2" rx="4" ry="3" fill="{LINE}"/></g>')
    if ex == "herz":
        g.append(f'<path d="M64 -300 c-6 -10 -20 -4 -14 6 l14 12 l14 -12 c6 -10 -8 -16 -14 -6 z" fill="#f28ab0" stroke="{LINE}" stroke-width="1.6"/>')
    if ex == "stern":
        g.append(f'<path d="M-70 -300 l5 11 12 1 -9 8 3 12 -11 -6 -11 6 3 -12 -9 -8 12 -1 z" fill="#f6c64b" stroke="{LINE}" stroke-width="1.4"/>')
    for pose, side in behind:
        if pose == "oben":
            g.append(arm(pose, side, sleeve))
    g.append('</g>')
    return "".join(g)


# ------------------------------------------------------------------ Die Figuren
FIGUREN = [
    dict(name="Elisabeth", traits=["normal groß", "kann schon gut tanzen", "hilfsbereit"], kind="w", skin="hell",
         hair="braun", hair_style="locken_lang", color="#b9a2e6", tutu="#d8c9f5", arms=("unten", "oben"), expr="nett", extra="herz"),
    dict(name="Johanna", traits=["normal groß", "chillig, redet gern", "hört gern Musik"], kind="w", skin="hell",
         hair="blond", hair_style="schulter", color="#8fd3b6", tutu="#bfe8d4", arms=("unten", "winken"), expr="froh", extra="kopfhoerer"),
    dict(name="Marie", traits=["normal groß", "zickig", "tanzt sehr gut"], kind="w", skin="hell", hair="hellblond",
         hair_style="lang_glatt", color="#f6f0f4", tutu="#fff7fb", arms=("huefte", "oben"), expr="eingebildet", extra="diadem", eyes="#3f6fb0"),
    dict(name="Nora", traits=["etwas kleiner", "schüchtern, liest gern", "sehr nett"], kind="w", skin="mittel",
         hair="schwarz", hair_style="lang_glatt", color="#9ad1f5", tutu="#c9e8fa", arms=("buch", "buch"), expr="schuechtern",
         extra="buch", height=.9),
    dict(name="Madame Colletin", traits=["Ballettlehrerin · groß", "streng, perfekte Tänzerin", "Star der großen Bühnen"],
         kind="lehrerin", skin="hell", hair="schwarz", hair_style="dutt", color="#2a2430", arms=("unten", "offen"),
         expr="streng", height=1.12, teacher=True),
    dict(name="Leon", traits=["groß", "nett und lustig", "sehr guter Tänzer"], kind="m", skin="hell", hair="schwarz",
         hair_style="kurz", color="#4b6fb5", arms=("offen", "offen"), expr="froh", height=1.08, extra="stern"),
    dict(name="Levi", traits=["mittelgroß, braune Haare", "freundlich", "liebt Ballett über alles"], kind="m", skin="hell", hair="braun",
         hair_style="seitenscheitel", color="#5aa58a", arms=("unten", "oben"), expr="froh", extra="herz"),
    dict(name="Tom", traits=["klein", "gegelte blonde Haare", "Angeber"], kind="m", skin="hell", hair="blond", hair_style="gegelt",
         color="#e0574f", arms=("huefte", "huefte"), expr="eingebildet", height=.9),
    dict(name="Samy", traits=["groß", "freundlich", "braune Haare"], kind="m", skin="dunkel", hair="dunkelbraun",
         hair_style="wellig", color="#f2b84b", arms=("unten", "winken"), expr="nett", height=1.08),
]


def build():
    W, H = 1960, 860
    FLOOR = 560
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', STYLE]
    # Ballettsaal-Hintergrund
    parts.append(f'<rect width="{W}" height="{H}" fill="#fdf3e4"/>')
    for i in range(9):
        parts.append(f'<rect x="{40 + i * 210}" y="90" width="196" height="{FLOOR - 140}" rx="6" fill="url(#mirror)" opacity=".55"/>')
    parts.append(f'<line x1="30" y1="{FLOOR - 170}" x2="{W - 30}" y2="{FLOOR - 170}" stroke="#c9955f" stroke-width="8" stroke-linecap="round" opacity=".8"/>')
    parts.append(f'<rect x="0" y="{FLOOR}" width="{W}" height="{H - FLOOR}" fill="#e2b98c"/>')
    for i in range(0, W, 120):
        parts.append(f'<line x1="{i}" y1="{FLOOR}" x2="{i - 60}" y2="{H}" stroke="#d4a676" stroke-width="2"/>')
    parts.append(f'<text x="{W / 2}" y="56" class="title">Die Figuren der École de Ballet Étoile</text>')
    for i, f in enumerate(FIGUREN):
        x = 120 + i * 215
        f = dict(f, x=x, y=FLOOR)
        parts.append(figure(f))
        # Namenskarte
        teacher = f.get("teacher")
        col = "#2a2430" if teacher else ("#c2456e" if f["kind"] == "w" else "#3f5f9f")
        parts.append(f'<rect x="{x - 100}" y="{FLOOR + 30}" width="200" height="{128}" rx="16" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
        parts.append(f'<text x="{x}" y="{FLOOR + 62}" class="name" style="fill:{col}">{f["name"]}</text>')
        for k, t in enumerate(f["traits"]):
            parts.append(f'<text x="{x}" y="{FLOOR + 88 + k * 20}" class="trait">{t}</text>')
    parts.append('</svg>')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(parts), encoding="utf-8")
    print(OUT)


STYLE = '''<defs><linearGradient id="mirror" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#e6f3fb"/><stop offset=".45" stop-color="#c9e2f2"/><stop offset=".5" stop-color="#f4fbff"/><stop offset="1" stop-color="#bcd8ec"/>
</linearGradient></defs>
<style>text{font-family:Inter,'DejaVu Sans',sans-serif;text-anchor:middle}
.title{font-size:30px;font-weight:800;fill:#7a3e5c}.name{font-size:21px;font-weight:800}
.trait{font-size:13.5px;font-weight:500;fill:#5b3d4a}</style>'''

if __name__ == "__main__":
    build()
