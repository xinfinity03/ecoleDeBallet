"""Erzeugt den Entwurf für den Aufbau der Ballettschule (Seitenansicht, Puppenhaus-Schnitt).

Version 2: 10 Zweibettzimmer mit eigenem Bad (5 Mädchen, 5 Jungen), Paris, Café mit Macaron-Theke.
Aufruf: python3 schule_aufbau.py  -> assets/konzept/schule_aufbau.svg
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "konzept" / "schule_aufbau.svg"
W, H = 1820, 1290
LINE = "#6b4a55"
WALL = "#ead8c4"
SLAB = "#c9ad94"
ROOF = "#7f90ad"            # Pariser Zinkdach

# Geschosse: (oben, unten)
DACH = 150, 305
OG3 = 319, 515              # Jungen
OG2 = 529, 725              # Mädchen
OG1 = 739, 935              # Ballettsaal
EG = 949, 1145              # Eingang + Café
X0, X1 = 110, 1370          # Hauptgebäude außen
TX0, TX1 = 1370, 1750       # Theaterflügel
TROOF = OG3[0]              # Dachkante Theater
STAIR = 125, 240            # Treppenhaus

parts = []
add = parts.append


def label(x, y, text, sub=None, color="#7a3e5c"):
    text = text.replace("&", "&amp;")
    sub = sub.replace("&", "&amp;") if sub else sub
    w = max(len(text) * 10.5 + 28, (len(sub) * 7.6 + 24) if sub else 0)
    h = 30 if not sub else 46
    add(f'<g><rect x="{x - w / 2:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="15" fill="#fff" '
        f'fill-opacity=".92" stroke="{color}" stroke-width="2"/>'
        f'<text x="{x}" y="{y + 21}" class="lb" fill="{color}">{text}</text>')
    if sub:
        add(f'<text x="{x}" y="{y + 38}" class="sub">{sub}</text>')
    add('</g>')


def person(x, y, kind="girl", s=1.0, skin="#f2c9a5", hair="#6b3e26", dress="#f59ab8", flip=False):
    sx = -s if flip else s
    add(f'<use href="#{kind}" transform="translate({x},{y}) scale({sx},{s})" '
        f'style="--skin:{skin};--hair:{hair};--dress:{dress}"/>')


def room(x0, y0, x1, y1, color, floor="#d8b48c"):
    add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{color}"/>')
    # Fußleiste + Boden
    add(f'<rect x="{x0}" y="{y1 - 14}" width="{x1 - x0}" height="14" fill="{floor}"/>')
    add(f'<rect x="{x0}" y="{y1 - 18}" width="{x1 - x0}" height="4" fill="#fff" opacity=".6"/>')


def partition(x, y0, y1, door=True):
    """Innenwand mit offenem Durchgang (man kann frei hindurchlaufen)."""
    if door:
        top = y1 - 130
        add(f'<rect x="{x - 6}" y="{y0}" width="12" height="{top - y0}" fill="{WALL}"/>')
        add(f'<path d="M{x - 6} {top} q6 -10 12 0" fill="none" stroke="{SLAB}" stroke-width="3"/>')
    else:
        add(f'<rect x="{x - 6}" y="{y0}" width="12" height="{y1 - y0}" fill="{WALL}"/>')


def window(x, y, w=60, h=70, curtain="#f7b6c8"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#sky)" stroke="#fff" stroke-width="5"/>')
    add(f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="#fff" stroke-width="3"/>')
    add(f'<path d="M{x - 6} {y - 4} h18 q-6 {h / 2} 4 {h + 8} h-22 z" fill="{curtain}"/>')
    add(f'<path d="M{x + w + 6} {y - 4} h-18 q6 {h / 2} -4 {h + 8} h22 z" fill="{curtain}"/>')


def bed(x, y, color="#f59ab8", w=110):
    add(f'<g><rect x="{x}" y="{y - 52}" width="12" height="52" rx="4" fill="#b98a63"/>'
        f'<rect x="{x}" y="{y - 30}" width="{w}" height="20" rx="6" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
        f'<rect x="{x + 34}" y="{y - 34}" width="{w - 34}" height="20" rx="8" fill="{color}" stroke="{LINE}" stroke-width="1.5"/>'
        f'<ellipse cx="{x + 24}" cy="{y - 36}" rx="13" ry="8" fill="#fff" stroke="{LINE}" stroke-width="1.5"/>'
        f'<rect x="{x + 4}" y="{y - 12}" width="8" height="12" fill="#b98a63"/>'
        f'<rect x="{x + w - 10}" y="{y - 12}" width="8" height="12" fill="#b98a63"/></g>')


def wardrobe(x, y, color="#e9c9a8"):
    add(f'<g><rect x="{x}" y="{y - 110}" width="56" height="110" rx="5" fill="{color}" stroke="{LINE}" stroke-width="1.5"/>'
        f'<line x1="{x + 28}" y1="{y - 104}" x2="{x + 28}" y2="{y - 6}" stroke="{LINE}" stroke-width="1.5"/>'
        f'<circle cx="{x + 23}" cy="{y - 56}" r="2.5" fill="{LINE}"/><circle cx="{x + 33}" cy="{y - 56}" r="2.5" fill="{LINE}"/></g>')


def plant(x, y, s=1):
    add(f'<g transform="translate({x},{y}) scale({s})"><path d="M-12 0 l3 -22 h18 l3 22 z" fill="#d98b5f"/>'
        f'<path d="M0 -22 q-22 -20 -10 -44 q6 18 10 44 q4 -30 16 -40 q6 24 -16 40" fill="#7fb77e"/></g>')


def dress_icon(x, y, color, s=1):
    add(f'<g transform="translate({x},{y}) scale({s})"><line x1="0" y1="-62" x2="0" y2="-52" stroke="#8a7" stroke-width="2"/>'
        f'<path d="M-8 -52 q8 6 16 0 v18 h-16 z" fill="{color}" stroke="{LINE}" stroke-width="1.2"/>'
        f'<path d="M-9 -34 q-14 4 -18 22 q9 6 18 2 q9 4 18 0 q9 4 18 -2 q-4 -18 -18 -22 z" '
        f'transform="translate(0,0)" fill="{color}" stroke="{LINE}" stroke-width="1.2"/></g>')


# ---------------------------------------------------------------- Hintergrund
add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
for cx, cy, s in [(260, 70, 1), (900, 50, .8), (1250, 95, .9)]:
    add(f'<g transform="translate({cx},{cy}) scale({s})" fill="#fff" opacity=".9">'
        f'<ellipse cx="0" cy="0" rx="50" ry="22"/><ellipse cx="35" cy="-12" rx="34" ry="24"/>'
        f'<ellipse cx="-30" cy="-6" rx="28" ry="18"/></g>')
# Eiffelturm im Hintergrund
ex, ey = (TX0 + TX1) / 2 + 20, TROOF - 10
add(f'<g transform="translate({ex},{ey}) scale(.6)" fill="#c9b8d8" stroke="#b3a0c6" stroke-width="2" opacity=".85">'
    '<path d="M-95 0 Q-40 -120 -14 -300 L-6 -420 L6 -420 L14 -300 Q40 -120 95 0 L60 0 Q30 -60 0 -62 Q-30 -60 -60 0 z"/>'
    '<rect x="-52" y="-120" width="104" height="10" rx="2"/><rect x="-26" y="-260" width="52" height="8" rx="2"/>'
    '<line x1="0" y1="-420" x2="0" y2="-450" stroke-width="3"/></g>')
# Boden
GY = EG[1] + 15
add(f'<path d="M0 {GY} Q450 {GY - 20} 900 {GY} T1820 {GY - 5} V{H} H0 z" fill="#a8d5a2"/>')
add(f'<path d="M0 {GY + 30} Q450 {GY + 15} 900 {GY + 33} T1820 {GY + 27} V{H} H0 z" fill="#93c78c"/>')
add(f'<path d="M330 {GY} L300 {H} H520 L470 {GY} z" fill="#ead9c0"/>')
for bx in (30, 75):
    add(f'<g fill="#7ab673"><circle cx="{bx}" cy="{EG[1] + 5}" r="22"/><circle cx="{bx + 18}" cy="{EG[1] + 10}" r="16"/></g>')
add(f'<g transform="translate({TX1 + 38},{GY})"><rect x="-8" y="-90" width="16" height="90" rx="6" fill="#a47551"/>'
    '<circle cx="0" cy="-130" r="48" fill="#86c17f"/><circle cx="-26" cy="-100" r="30" fill="#7ab673"/>'
    '<circle cx="26" cy="-104" r="32" fill="#93cb8a"/><circle cx="-12" cy="-150" r="6" fill="#f7a8c4"/>'
    '<circle cx="18" cy="-118" r="6" fill="#f7a8c4"/></g>')

# ---------------------------------------------------------------- Theaterflügel
add(f'<rect x="{TX0}" y="{TROOF}" width="{TX1 - TX0}" height="{EG[1] - TROOF + 20}" fill="{WALL}" stroke="{LINE}" stroke-width="3"/>')
add(f'<path d="M{TX0 - 10} {TROOF + 4} L{TX0 + 40} {TROOF - 46} H{TX1 - 30} L{TX1 + 12} {TROOF + 4} z" fill="{ROOF}" stroke="{LINE}" stroke-width="3"/>')
add(f'<text x="{(TX0 + TX1) / 2}" y="{TROOF - 14}" class="sign" fill="#fff" style="fill:#fff">★ Théâtre ★</text>')
# Frankreich-Fähnchen
fx = TX1 - 40
add(f'<line x1="{fx}" y1="{TROOF - 46}" x2="{fx}" y2="{TROOF - 100}" stroke="#3d3f52" stroke-width="3"/>'
    f'<rect x="{fx}" y="{TROOF - 100}" width="14" height="24" fill="#2f5aa8"/><rect x="{fx + 14}" y="{TROOF - 100}" width="14" height="24" fill="#fff"/>'
    f'<rect x="{fx + 28}" y="{TROOF - 100}" width="14" height="24" fill="#d8344a"/>')
# Garderobe & Maske (auf Höhe 2. Stock)
room(TX0 + 12, OG2[0], TX1 - 12, OG2[1], "#f6e1ea")
add(f'<rect x="{TX0}" y="{OG2[1]}" width="{TX1 - TX0}" height="14" fill="{SLAB}"/>')
for i in range(2):
    mx = TX0 + 40 + i * 120
    add(f'<rect x="{mx}" y="{OG2[0] + 75}" width="80" height="60" rx="6" fill="#dceefb" stroke="#d9b36c" stroke-width="5"/>')
    for k in range(5):
        add(f'<circle cx="{mx + 8 + k * 16}" cy="{OG2[0] + 70}" r="4.5" fill="#ffe28a"/>')
    add(f'<rect x="{mx - 6}" y="{OG2[0] + 140}" width="92" height="10" rx="3" fill="#d9b8a0"/>')
add(f'<line x1="{TX1 - 120}" y1="{OG2[0] + 100}" x2="{TX1 - 30}" y2="{OG2[0] + 100}" stroke="#9a7" stroke-width="4"/>')
for i, c in enumerate(["#9ad1f5", "#f6d26b", "#c7a2f0"]):
    dress_icon(TX1 - 105 + i * 30, OG2[0] + 160, c, .9)
person(TX0 + 300, OG2[1] - 14, "girl", .95, skin="#8d5a3b", hair="#1e1410", dress="#f6d26b", flip=True)
label((TX0 + TX1) / 2, OG2[0] + 6, "Garderobe & Maske", "Schminken vor dem Auftritt")
# Dachboden des Theaters (Höhe 3. Stock): Kulissenlager
room(TX0 + 12, TROOF + 14, TX1 - 12, OG3[1], "#efe3d3")
add(f'<rect x="{TX0}" y="{OG3[1]}" width="{TX1 - TX0}" height="14" fill="{SLAB}"/>')
add(f'<path d="M{TX0 + 40} {OG3[1] - 14} v-90 h110 v90" fill="#cfe6c9" stroke="{LINE}" stroke-width="1.5"/>'
    f'<circle cx="{TX0 + 95}" cy="{OG3[1] - 60}" r="22" fill="#f6d26b" stroke="{LINE}" stroke-width="1.5"/>'
    f'<path d="M{TX0 + 190} {OG3[1] - 14} l40 -100 l40 100 z" fill="#b8d0ec" stroke="{LINE}" stroke-width="1.5"/>'
    f'<rect x="{TX0 + 290} " y="{OG3[1] - 54}" width="50" height="40" rx="4" fill="#c99b74" stroke="{LINE}" stroke-width="1.5"/>')
label((TX0 + TX1) / 2, TROOF + 20, "Kulissenlager")
# Bühne (doppelt hoch: 1. Stock + EG)
BT = OG1[0]
add(f'<rect x="{TX0 + 12}" y="{BT}" width="{TX1 - TX0 - 24}" height="{EG[1] - BT}" fill="#3d2b4f"/>')
SB = BT + 290  # Bühnenkante
add(f'<path d="M{TX0 + 120} {BT + 6} L{TX0 + 70} {SB} H{TX0 + 250} z" fill="#fff6c9" opacity=".18"/>')
add(f'<path d="M{TX1 - 120} {BT + 6} L{TX1 - 250} {SB} H{TX1 - 70} z" fill="#fff6c9" opacity=".18"/>')
add(f'<rect x="{TX0 + 12}" y="{SB}" width="{TX1 - TX0 - 24}" height="34" fill="#b5835a"/>')
add(f'<rect x="{TX0 + 12}" y="{SB - 4}" width="{TX1 - TX0 - 24}" height="6" fill="#e0b182"/>')
add(f'<path d="M{TX0 + 12} {BT} H{TX1 - 12} V{BT + 46} Q{(TX0 + TX1) / 2} {BT + 76} {TX0 + 12} {BT + 46} z" fill="#c8324a"/>')
add(f'<path d="M{TX0 + 12} {BT} h70 q-20 140 30 {SB - BT} h-100 z" fill="url(#curtain)"/>')
add(f'<path d="M{TX1 - 12} {BT} h-70 q20 140 -30 {SB - BT} h100 z" fill="url(#curtain)"/>')
person(TX0 + 190, SB - 2, "girl", 1.15, skin="#f2c9a5", hair="#e8c15a", dress="#9ad1f5")
person(TX0 + 240, SB - 2, "boy", 1.15, skin="#c68a5e", hair="#2b1a12", dress="#4b6fb5", flip=True)
for row in range(2):
    for i in range(8):
        cx = TX0 + 45 + i * 42 + row * 20
        cy = SB + 84 + row * 40
        add(f'<g fill="#{"5a466e" if row else "4a3a5c"}"><circle cx="{cx}" cy="{cy - 26}" r="11"/>'
            f'<path d="M{cx - 16} {cy + 4} q0 -24 16 -24 q16 0 16 24 z"/></g>')
label((TX0 + TX1) / 2, BT + 86, "Bühne", "Hier sind die Aufführungen")

# ---------------------------------------------------------------- Hauptgebäude
add(f'<rect x="{X0}" y="{DACH[1]}" width="{X1 - X0}" height="{EG[1] - DACH[1] + 20}" fill="{WALL}" stroke="{LINE}" stroke-width="3"/>')
# Pariser Mansarddach (Zink-Blau) mit Schornsteinen
for cx in (X0 + 200, X1 - 260):
    add(f'<g><rect x="{cx}" y="72" width="44" height="50" fill="#c97b5a" stroke="{LINE}" stroke-width="2"/>'
        f'<rect x="{cx - 4}" y="66" width="52" height="10" fill="#b5694a" stroke="{LINE}" stroke-width="2"/>'
        + "".join(f'<rect x="{cx + 6 + k * 12}" y="54" width="8" height="12" rx="2" fill="#d98b5f" stroke="{LINE}" stroke-width="1.2"/>' for k in range(3))
        + '</g>')
add(f'<path d="M{X0 - 22} {DACH[1] + 6} L{X0 + 55} 118 H{X1 - 55} L{X1 + 22} {DACH[1] + 6} z" fill="{ROOF}" stroke="{LINE}" stroke-width="3"/>')
for i in range(15):
    add(f'<line x1="{X0 + 90 + i * 72}" y1="120" x2="{X0 + 90 + i * 72}" y2="140" stroke="#6f7f99" stroke-width="2" opacity=".7"/>')
add(f'<rect x="{X0 + 50}" y="112" width="{X1 - X0 - 100}" height="8" rx="3" fill="#d9b36c"/>')
SX = (X0 + X1) / 2
add(f'<path d="M{SX - 330} 84 h660 l22 30 h-704 z" fill="#f4ead9" stroke="{LINE}" stroke-width="3"/>')
add(f'<text x="{SX}" y="106" class="sign">École de Ballet Étoile · Paris</text>')
# Dachgeschoss-Innenraum
add(f'<path d="M{X0 + 18} {DACH[1]} L{X0 + 82} {DACH[0]} H{X1 - 82} L{X1 - 18} {DACH[1]} z" fill="#fbe3ef"/>')
add(f'<rect x="{X0 + 18}" y="{DACH[1] - 14}" width="{X1 - X0 - 36}" height="14" fill="#d8b48c"/>')
for y in (DACH[1], OG3[1], OG2[1], OG1[1]):
    add(f'<rect x="{X0}" y="{y}" width="{X1 - X0}" height="14" fill="{SLAB}"/>')
add(f'<rect x="{X0 - 6}" y="{EG[1]}" width="{TX1 - X0 + 12}" height="20" fill="{SLAB}" stroke="{LINE}" stroke-width="2"/>')

# --- Dach: Boutique + Büro
DB = DACH[1] - 14
partition(820, DACH[0], DACH[1])
for rx, colors in [(285, ["#f59ab8", "#9ad1f5", "#f6d26b", "#c7a2f0"]),
                   (470, ["#ffffff", "#ff8c7a", "#8fd3b6", "#f59ab8"])]:
    add(f'<line x1="{rx}" y1="{DB - 70}" x2="{rx + 150}" y2="{DB - 70}" stroke="#b39070" stroke-width="5"/>')
    add(f'<line x1="{rx + 6}" y1="{DB - 70}" x2="{rx + 6}" y2="{DB}" stroke="#b39070" stroke-width="4"/>')
    add(f'<line x1="{rx + 144}" y1="{DB - 70}" x2="{rx + 144}" y2="{DB}" stroke="#b39070" stroke-width="4"/>')
    for i, c in enumerate(colors):
        dress_icon(rx + 22 + i * 36, DB - 8, c, .9)
add(f'<rect x="700" y="{DB - 96}" width="44" height="92" rx="22" fill="#dceefb" stroke="#d9b36c" stroke-width="5"/>')
person(670, DB, "girl", .9, skin="#f2c9a5", hair="#b5532c", dress="#c7a2f0", flip=True)
label(520, DACH[0] + 10, "Boutique (Kleiderladen)", "Kleider kaufen mit Lob-Punkten ★")
add(f'<rect x="900" y="{DB - 36}" width="140" height="16" rx="4" fill="#b98a63"/>'
    f'<rect x="910" y="{DB - 20}" width="10" height="20" fill="#b98a63"/><rect x="1020" y="{DB - 20}" width="10" height="20" fill="#b98a63"/>')
add(f'<path d="M960 {DB - 64} l5 11 12 1 -9 8 3 12 -11 -6 -11 6 3 -12 -9 -8 12 -1 z" fill="#f6c64b" stroke="#6b4a55" stroke-width="1.2"/>')
add(f'<rect x="1080" y="{DB - 82}" width="70" height="80" fill="#c99b74" stroke="#6b4a55" stroke-width="1.5"/>')
for i, c in enumerate(["#e77", "#7ae", "#ec6", "#8c8", "#c7a2f0", "#e77"]):
    add(f'<rect x="{1086 + (i % 3) * 21}" y="{DB - 75 + (i // 3) * 38}" width="16" height="30" fill="{c}"/>')
person(1000, DB, "teacher", 1.0, skin="#e0b08a", hair="#9a9a9a", dress="#6d5a8c", flip=True)
label(1030, DACH[0] + 10, "Büro der Direktorin", "Zeugnisse & Prüfungen")

# --- Zimmer-Etagen: je 5 Zweibettzimmer mit eigenem Bad
RW = (X1 - STAIR[1]) / 5
BATH = 66
wall_cols = ["#fde2e4", "#e6f0ea", "#fff1df", "#efe4f7", "#e3eefb"]
bed_cols = [("#f59ab8", "#9ad1f5"), ("#8fd3b6", "#f6d26b"), ("#c7a2f0", "#ff8c7a"),
            ("#7fa6e0", "#e98b6f"), ("#f6d26b", "#8fd3b6")]


def bath(x0, y0, y1):
    room(x0, y0, x0 + BATH, y1, "#dff3f6", floor="#bfdfe6")
    for k in range(4):  # Fliesen
        add(f'<line x1="{x0}" y1="{y1 - 40 - k * 22}" x2="{x0 + BATH}" y2="{y1 - 40 - k * 22}" stroke="#fff" stroke-width="1.5"/>')
    # Dusche
    add(f'<path d="M{x0 + 8} {y1 - 14} v-110 h28 v110" fill="none" stroke="#9fb7c4" stroke-width="2"/>'
        f'<path d="M{x0 + 22} {y1 - 124} q8 0 8 8" fill="none" stroke="#9aa" stroke-width="3"/>'
        f'<path d="M{x0 + 6} {y1 - 120} q8 30 0 60 q8 30 0 46 h10 q-6 -50 0 -106 z" fill="#f7b6c8" opacity=".9"/>')
    # Waschbecken + Spiegel
    add(f'<rect x="{x0 + 42}" y="{y1 - 98}" width="18" height="24" rx="4" fill="#dceefb" stroke="#d9b36c" stroke-width="2"/>'
        f'<path d="M{x0 + 40} {y1 - 64} h22 q0 12 -11 12 q-11 0 -11 -12 z" fill="#fff" stroke="{LINE}" stroke-width="1.2"/>'
        f'<rect x="{x0 + 49}" y="{y1 - 52}" width="4" height="38" fill="#fff" stroke="{LINE}" stroke-width="1"/>')
    add(f'<text x="{x0 + BATH / 2}" y="{y0 + 20}" class="small">Bad</text>')


def dorm_floor(fl, title, kind, mine=None):
    y0, y1 = fl
    for i in range(5):
        x0 = STAIR[1] + i * RW
        room(x0, y0, x0 + RW - BATH, y1, wall_cols[i], floor="#d6b089")
        bath(x0 + RW - BATH, y0, y1)
        partition(x0 + RW - BATH, y0, y1)
        if i:
            partition(x0, y0, y1)
        window(x0 + (RW - BATH) / 2 - 24, y0 + 50, 48, 54, wall_cols[(i + 2) % 5].replace("f", "c", 1))
        c1, c2 = bed_cols[i]
        bed(x0 + 6, y1 - 14, c1, 74)
        bed(x0 + RW - BATH - 80, y1 - 14, c2, 74)
        name = "Dein Zimmer ♥" if mine == i else f"Zimmer {i + 1 + (5 if kind == 'boy' else 0)}"
        label(x0 + (RW - BATH) / 2, y0 + 6, name, None, "#c2456e" if mine == i else "#7a3e5c")
    # Etagenschild
    add(f'<text x="{X0 - 30}" y="{(y0 + y1) / 2}" class="floor" transform="rotate(-90 {X0 - 30} {(y0 + y1) / 2})">{title}</text>')


dorm_floor(OG3, "3. Stock · Jungen", "boy")
dorm_floor(OG2, "2. Stock · Mädchen", "girl", mine=0)
# Figuren auf den Zimmer-Etagen
person(STAIR[1] + 60, OG2[1] - 14, "girl", .85, skin="#f2c9a5", hair="#6b3e26", dress="#f59ab8")
person(STAIR[1] + 115, OG2[1] - 14, "girl", .85, skin="#7a4a2e", hair="#1e1410", dress="#9ad1f5", flip=True)
add(f'<g><path d="M{STAIR[1] + 30} {OG2[0] + 66} h150 a12 12 0 0 1 12 12 v6 a12 12 0 0 1 -12 12 h-46 l-6 12 l-6 -12 h-92 a12 12 0 0 1 -12 -12 v-6 a12 12 0 0 1 12 -12 z" '
    f'fill="#fff" stroke="#6b4a55" stroke-width="2"/>'
    f'<text x="{STAIR[1] + 105}" y="{OG2[0] + 86}" class="bubble">Salut! Ich bin Lina!</text></g>')
person(STAIR[1] + 2 * RW + 70, OG2[1] - 14, "girl", .85, skin="#f0c39d", hair="#e8c15a", dress="#c7a2f0")
person(STAIR[1] + 1 * RW + 75, OG3[1] - 14, "boy", .85, skin="#f0c39d", hair="#c98a3b", dress="#4b6fb5")
person(STAIR[1] + 3 * RW + 60, OG3[1] - 14, "boy", .85, skin="#7a4a2e", hair="#1e1410", dress="#e98b6f", flip=True)

# --- 1. Stock: Ballettsaal + Umkleiden
SAAL1 = 1000
room(STAIR[1], OG1[0], SAAL1, OG1[1], "#fdf0d8", floor="#c98f5b")
room(SAAL1, OG1[0], X1, OG1[1], "#ebe4f6", floor="#d6b089")
partition(SAAL1, OG1[0], OG1[1])
partition(SAAL1 + (X1 - SAAL1) / 2, OG1[0], OG1[1])
for i in range(6):
    add(f'<rect x="{300 + i * 112}" y="{OG1[0] + 36}" width="104" height="120" fill="url(#mirror)" stroke="#e6cf9e" stroke-width="3"/>')
add(f'<line x1="270" y1="{OG1[0] + 116}" x2="{SAAL1 - 30}" y2="{OG1[0] + 116}" stroke="#a87449" stroke-width="7" stroke-linecap="round"/>')
for x in (290, 600, SAAL1 - 50):
    add(f'<line x1="{x}" y1="{OG1[0] + 116}" x2="{x}" y2="{OG1[1] - 14}" stroke="#a87449" stroke-width="4"/>')
add(f'<g><rect x="{SAAL1 - 120}" y="{OG1[1] - 70}" width="80" height="50" rx="4" fill="#3b2f3a"/>'
    f'<rect x="{SAAL1 - 120}" y="{OG1[1] - 78}" width="80" height="10" fill="#4b3d4a"/>'
    f'<rect x="{SAAL1 - 116}" y="{OG1[1] - 56}" width="72" height="8" fill="#fff"/></g>')
FL1 = OG1[1] - 14
person(320, FL1, "teacher", 1.1, skin="#e9bf98", hair="#2b1a12", dress="#2f2a3a")
add(f'<path d="M352 {OG1[0] + 62} l5 11 12 1 -9 8 3 12 -11 -6 -11 6 3 -12 -9 -8 12 -1 z" fill="#f6c64b" stroke="#6b4a55" stroke-width="1.2"/>')
for i, (k, sk, hr, dr) in enumerate([("girl", "#f2c9a5", "#6b3e26", "#f59ab8"), ("girl", "#7a4a2e", "#1e1410", "#9ad1f5"),
                                     ("boy", "#f0c39d", "#c98a3b", "#4b6fb5"), ("girl", "#f0c39d", "#e8c15a", "#c7a2f0"),
                                     ("boy", "#c68a5e", "#2b1a12", "#5aa58a")]):
    person(430 + i * 95, FL1, k, 1.0, skin=sk, hair=hr, dress=dr)
label(620, OG1[0] + 6, "Großer Ballettsaal", "Unterricht · Üben für den Auftritt · Lob-Punkte ★")
for j, (title, col) in enumerate([("Umkleide ♀", "#f2b8cc"), ("Umkleide ♂", "#b9c8e8")]):
    ux = SAAL1 + j * (X1 - SAAL1) / 2
    for i in range(3):
        add(f'<rect x="{ux + 20 + i * 42}" y="{OG1[1] - 134}" width="38" height="120" rx="4" fill="{col}" stroke="#6b4a55" stroke-width="1.5"/>'
            f'<rect x="{ux + 32 + i * 42}" y="{OG1[1] - 120}" width="14" height="4" rx="2" fill="#6b4a55"/>')
    label(ux + (X1 - SAAL1) / 4, OG1[0] + 6, title)
add(f'<text x="{X0 - 30}" y="{(OG1[0] + OG1[1]) / 2}" class="floor" transform="rotate(-90 {X0 - 30} {(OG1[0] + OG1[1]) / 2})">1. Stock</text>')

# --- EG: Eingangshalle + Café
CAFE = 700
room(STAIR[1], EG[0], CAFE, EG[1], "#f7e8cf", floor="#cfae8c")
room(CAFE, EG[0], X1, EG[1], "#fbeef2", floor="#d6b089")
partition(CAFE, EG[0], EG[1])
FL0 = EG[1] - 14
add(f'<g><path d="M300 {FL0 + 2} v-120 a50 50 0 0 1 100 0 v120 z" fill="#3f5f8f" stroke="#6b4a55" stroke-width="2"/>'
    f'<path d="M310 {FL0 + 2} v-118 a40 40 0 0 1 80 0 v118" fill="none" stroke="#6f8fbf" stroke-width="3"/>'
    f'<circle cx="380" cy="{FL0 - 54}" r="4" fill="#f6d26b"/></g>')
add(f'<g><line x1="500" y1="{EG[0] + 14}" x2="500" y2="{EG[0] + 36}" stroke="#b39070" stroke-width="2"/>'
    f'<path d="M470 {EG[0] + 42} q30 18 60 0" fill="none" stroke="#d9b36c" stroke-width="4"/>'
    f'<circle cx="470" cy="{EG[0] + 40}" r="5" fill="#ffe28a"/><circle cx="500" cy="{EG[0] + 50}" r="5" fill="#ffe28a"/>'
    f'<circle cx="530" cy="{EG[0] + 40}" r="5" fill="#ffe28a"/></g>')
person(495, FL0, "teacher", .95, skin="#f2c9a5", hair="#c98a3b", dress="#8fbf9f")
add(f'<rect x="440" y="{FL0 - 56}" width="110" height="56" rx="6" fill="#c99b74" stroke="#6b4a55" stroke-width="1.5"/>')
add(f'<rect x="590" y="{FL0 - 116}" width="74" height="56" rx="4" fill="#c69c6d" stroke="#6b4a55" stroke-width="1.5"/>')
for i, c in enumerate(["#fff", "#f7b6c8", "#ffe28a", "#bfe3f5"]):
    xx, yy = 596 + (i % 2) * 34, FL0 - 110 + (i // 2) * 24
    add(f'<rect x="{xx}" y="{yy}" width="28" height="20" fill="{c}" transform="rotate({(-3, 4, 2, -4)[i]} {xx + 14} {yy + 10})"/>')
label(465, EG[0] + 6, "Entrée (Eingangshalle)", "Empfang · Schwarzes Brett (Termine)")
# Café mit Macaron-Theke
add(f'<path d="M{CAFE + 20} {EG[0] + 14} h{X1 - CAFE - 40} v26 q-{(X1 - CAFE - 40) / 16} 14 -{(X1 - CAFE - 40) / 8} 0 '
    + " ".join(f"q-{(X1 - CAFE - 40) / 16} 14 -{(X1 - CAFE - 40) / 8} 0" for _ in range(7)) + ' z" fill="#f59ab8" opacity=".55"/>')
for tx in (760, 920):
    add(f'<g><ellipse cx="{tx + 50}" cy="{FL0 - 50}" rx="50" ry="8" fill="#c99b74"/>'
        f'<rect x="{tx + 46}" y="{FL0 - 50}" width="8" height="50" fill="#b98a63"/>'
        f'<path d="M{tx - 6} {FL0} v-40 h8 v20 h22 v20" fill="none" stroke="#3d3f52" stroke-width="4"/>'
        f'<path d="M{tx + 106} {FL0} v-40 h-8 v20 h-22 v20" fill="none" stroke="#3d3f52" stroke-width="4"/></g>')
    plant(tx + 50, FL0 - 58, .45)
# Macaron-Vitrine
VX = X1 - 250
add(f'<rect x="{VX}" y="{FL0 - 90}" width="230" height="90" rx="8" fill="#f3d3b5" stroke="{LINE}" stroke-width="1.5"/>')
add(f'<rect x="{VX + 10}" y="{FL0 - 130}" width="210" height="44" rx="6" fill="#eaf6fb" stroke="{LINE}" stroke-width="1.5" opacity=".9"/>')
mac = ["#f59ab8", "#9ad1f5", "#f6d26b", "#8fd3b6", "#c7a2f0", "#ff8c7a", "#f59ab8", "#9ad1f5", "#f6d26b", "#c7a2f0"]
for i, c in enumerate(mac):
    mx, my = VX + 26 + (i % 5) * 44, FL0 - 120 + (i // 5) * 18
    add(f'<g><ellipse cx="{mx}" cy="{my}" rx="11" ry="5" fill="{c}" stroke="{LINE}" stroke-width=".8"/>'
        f'<rect x="{mx - 10}" y="{my + 3}" width="20" height="3" fill="#fff"/>'
        f'<ellipse cx="{mx}" cy="{my + 8}" rx="11" ry="5" fill="{c}" stroke="{LINE}" stroke-width=".8"/></g>')
person(VX + 120, FL0 - 88, "teacher", .8, skin="#f0c39d", hair="#6b3e26", dress="#ffffff")
add(f'<g><rect x="{VX + 40}" y="{FL0 - 64}" width="150" height="38" rx="8" fill="#fff" stroke="#c2456e" stroke-width="2" stroke-dasharray="5 4"/>'
    f'<text x="{VX + 115}" y="{FL0 - 49}" class="small" style="fill:#c2456e">Macaron-Werkstatt</text>'
    f'<text x="{VX + 115}" y="{FL0 - 34}" class="small" style="fill:#c2456e;font-weight:500">kommt später</text></g>')
person(800, FL0, "girl", .95, skin="#f2c9a5", hair="#e8c15a", dress="#c7a2f0")
person(1010, FL0, "boy", .95, skin="#7a4a2e", hair="#1e1410", dress="#e98b6f", flip=True)
add(f'<g><path d="M820 {FL0 - 126} h126 a12 12 0 0 1 12 12 v6 a12 12 0 0 1 -12 12 h-96 l-14 12 l2 -12 h-18 a12 12 0 0 1 -12 -12 v-6 a12 12 0 0 1 12 -12 z" '
    f'fill="#fff" stroke="#6b4a55" stroke-width="2"/><text x="883" y="{FL0 - 106}" class="bubble">Übst du heute mit?</text></g>')
label(900, EG[0] + 6, "Café", "Treffen · plaudern · Macarons")
add(f'<text x="{X0 - 30}" y="{(EG[0] + EG[1]) / 2}" class="floor" transform="rotate(-90 {X0 - 30} {(EG[0] + EG[1]) / 2})">Erdgeschoss</text>')
add(f'<text x="{X0 - 30}" y="{(DACH[0] + DACH[1]) / 2 + 20}" class="floor" transform="rotate(-90 {X0 - 30} {(DACH[0] + DACH[1]) / 2 + 20})">Dach</text>')

# --- Treppenhaus
add(f'<rect x="{STAIR[0] - 15}" y="{OG3[0]}" width="{STAIR[1] - STAIR[0] + 15}" height="{EG[1] - OG3[0]}" fill="#efe4d6"/>')
for y in (OG3[1], OG2[1], OG1[1]):
    add(f'<rect x="{STAIR[0] - 15}" y="{y}" width="{STAIR[1] - STAIR[0] + 15}" height="14" fill="{SLAB}"/>')
flights = [(DACH[1], OG3[1]), (OG3[1] + 14, OG2[1]), (OG2[1] + 14, OG1[1]), (OG1[1] + 14, EG[1])]
for i, (ytop, ybot) in enumerate(flights):
    steps = 9
    pts = []
    for k in range(steps + 1):
        t = k / steps
        pts.append((STAIR[0] + (t if i % 2 == 0 else 1 - t) * (STAIR[1] - STAIR[0] - 10), ybot - t * (ybot - ytop)))
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for k in range(1, len(pts)):
        d += f" V{pts[k][1]:.0f} H{pts[k][0]:.0f}"
    add(f'<path d="{d} V{pts[0][1]:.0f} z" fill="#d7b996" stroke="#b08a66" stroke-width="2"/>')

add(f'<rect x="{X0}" y="{DACH[1]}" width="{X1 - X0}" height="{EG[1] - DACH[1]}" fill="none" stroke="{LINE}" stroke-width="3"/>')
add(f'<rect x="{TX0}" y="{TROOF}" width="{TX1 - TX0}" height="{EG[1] - TROOF}" fill="none" stroke="{LINE}" stroke-width="3"/>')

DEFS = '''
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#cfe8f7"/><stop offset=".75" stop-color="#fbe9f0"/><stop offset="1" stop-color="#fbe9f0"/>
  </linearGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd0f0"/><stop offset="1" stop-color="#dff1fb"/></linearGradient>
  <linearGradient id="mirror" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#e6f3fb"/><stop offset=".45" stop-color="#c9e2f2"/><stop offset=".5" stop-color="#f4fbff"/><stop offset="1" stop-color="#bcd8ec"/>
  </linearGradient>
  <linearGradient id="curtain" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#a51f37"/><stop offset=".3" stop-color="#d9405a"/><stop offset=".6" stop-color="#b52640"/><stop offset="1" stop-color="#d9405a"/>
  </linearGradient>
  <!-- Figuren: Ursprung = Fußpunkt; Farben über CSS-Variablen -->
  <g id="girl" stroke="#6b4a55" stroke-width="1.4" stroke-linejoin="round">
    <path d="M-5 -34 L-7 -2 M5 -34 L7 -2" stroke="var(--skin)" stroke-width="5" stroke-linecap="round"/>
    <ellipse cx="-8" cy="-1" rx="5" ry="3" fill="#f7b6c8"/><ellipse cx="8" cy="-1" rx="5" ry="3" fill="#f7b6c8"/>
    <path d="M-8 -57 Q-20 -66 -22 -82 M8 -57 Q18 -54 22 -46" fill="none" stroke="var(--skin)" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M-8 -60 q8 -4 16 0 v24 h-16 z" fill="var(--dress)"/>
    <path d="M-22 -36 q22 -10 44 0 q-4 7 -11 6 q-5 4 -11 1 q-6 3 -11 -1 q-7 1 -11 -6 z" fill="var(--dress)"/>
    <rect x="-3" y="-66" width="6" height="7" fill="var(--skin)" stroke="none"/>
    <circle cx="0" cy="-75" r="10.5" fill="var(--skin)"/>
    <path d="M-10.5 -76 q1 -12 10.5 -12 q9.5 0 10.5 12 q-5 -6 -10.5 -6 q-6 0 -10.5 6 z" fill="var(--hair)"/>
    <circle cx="0" cy="-90" r="5.5" fill="var(--hair)"/>
    <circle cx="-3.5" cy="-75" r="1.3" fill="#3b2a30" stroke="none"/><circle cx="3.5" cy="-75" r="1.3" fill="#3b2a30" stroke="none"/>
    <path d="M-3 -70 q3 2.5 6 0" fill="none" stroke-width="1.2"/>
    <circle cx="-6" cy="-71" r="2" fill="#f49cb0" stroke="none" opacity=".6"/><circle cx="6" cy="-71" r="2" fill="#f49cb0" stroke="none" opacity=".6"/>
  </g>
  <g id="boy" stroke="#6b4a55" stroke-width="1.4" stroke-linejoin="round">
    <path d="M-5 -36 L-7 -2 M5 -36 L7 -2" stroke="#3d3550" stroke-width="6" stroke-linecap="round"/>
    <ellipse cx="-8" cy="-1" rx="5" ry="3" fill="#eee"/><ellipse cx="8" cy="-1" rx="5" ry="3" fill="#eee"/>
    <path d="M-9 -58 Q-18 -52 -22 -44 M9 -58 Q20 -66 22 -80" fill="none" stroke="var(--skin)" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M-10 -61 q10 -4 20 0 l1 26 h-22 z" fill="var(--dress)"/>
    <rect x="-3" y="-67" width="6" height="7" fill="var(--skin)" stroke="none"/>
    <circle cx="0" cy="-76" r="10.5" fill="var(--skin)"/>
    <path d="M-11 -76 q0 -13 11 -13 q11 0 11 13 q-3 -5 -6 -6 q-4 3 -11 2 q-3 1 -5 4 z" fill="var(--hair)"/>
    <circle cx="-3.5" cy="-76" r="1.3" fill="#3b2a30" stroke="none"/><circle cx="3.5" cy="-76" r="1.3" fill="#3b2a30" stroke="none"/>
    <path d="M-3 -71 q3 2.5 6 0" fill="none" stroke-width="1.2"/>
  </g>
  <g id="teacher" stroke="#6b4a55" stroke-width="1.4" stroke-linejoin="round">
    <path d="M-4 -30 L-5 -2 M4 -30 L5 -2" stroke="var(--skin)" stroke-width="4.5" stroke-linecap="round"/>
    <ellipse cx="-6" cy="-1" rx="5" ry="3" fill="#3b2f3a"/><ellipse cx="6" cy="-1" rx="5" ry="3" fill="#3b2f3a"/>
    <path d="M-8 -60 Q-16 -50 -18 -42 M8 -60 Q20 -64 26 -72" fill="none" stroke="var(--skin)" stroke-width="4.5" stroke-linecap="round"/>
    <path d="M-9 -63 q9 -4 18 0 l1 22 h-20 z" fill="var(--dress)"/>
    <path d="M-10 -42 h20 l7 18 h-34 z" fill="var(--dress)" opacity=".85"/>
    <rect x="-3" y="-69" width="6" height="7" fill="var(--skin)" stroke="none"/>
    <circle cx="0" cy="-78" r="10.5" fill="var(--skin)"/>
    <path d="M-10.5 -79 q1 -12 10.5 -12 q9.5 0 10.5 12 q-5 -6 -10.5 -6 q-6 0 -10.5 6 z" fill="var(--hair)"/>
    <ellipse cx="9" cy="-88" rx="6" ry="5" fill="var(--hair)"/>
    <circle cx="-3.5" cy="-78" r="1.3" fill="#3b2a30" stroke="none"/><circle cx="3.5" cy="-78" r="1.3" fill="#3b2a30" stroke="none"/>
    <path d="M-3 -73 q3 2.5 6 0" fill="none" stroke-width="1.2"/>
  </g>
</defs>
<style>
  text { font-family: Inter, 'DejaVu Sans', sans-serif; }
  .lb { font-size: 17px; font-weight: 700; text-anchor: middle; }
  .sub { font-size: 12.5px; font-weight: 500; fill: #6b4a55; text-anchor: middle; }
  .sign { font-size: 21px; font-weight: 800; fill: #7a3e5c; text-anchor: middle; letter-spacing: .5px; }
  .bubble { font-size: 13px; font-weight: 600; fill: #5a3a48; text-anchor: middle; }
  .small { font-size: 12px; font-weight: 700; fill: #5a7f8a; text-anchor: middle; }
  .floor { font-size: 15px; font-weight: 700; fill: #7a3e5c; text-anchor: middle; opacity: .75; }
</style>
'''

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       + DEFS + "\n".join(parts) + "</svg>")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print(OUT)
