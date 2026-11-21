"""Baut game/index.html aus spiel.html und den eingebetteten Zeichnungen."""
from pathlib import Path
here = Path(__file__).parent
html = (here / "spiel.html").read_text(encoding="utf-8")
html = html.replace("{{SOFA}}", (here / "sofa.b64").read_text().strip()).replace("{{KLEID}}", (here / "kleid.b64").read_text().strip())
(here / "index.html").write_text(html, encoding="utf-8")
print("index.html", len(html) // 1024, "KB")
