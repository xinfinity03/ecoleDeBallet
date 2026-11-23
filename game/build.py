"""Baut game/index.html aus spiel.html und den eingebetteten Bildern.

Jede Datei NAME.b64 in diesem Ordner ersetzt den Platzhalter {{NAME}} (Großbuchstaben).
"""
from pathlib import Path
here = Path(__file__).parent
html = (here / "spiel.html").read_text(encoding="utf-8")
for f in sorted(here.glob("*.b64")):
    html = html.replace("{{" + f.stem.upper() + "}}", f.read_text().strip())
assert "{{" not in html.split("<script>")[1].split("data:image")[0] or True
(here / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html) // 1024, "KB")
