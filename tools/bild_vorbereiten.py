"""Bereitet ein fotografiertes Bild für einen Bilderrahmen im Spiel vor.

Anders als zeichnung_freistellen.py wird nichts freigestellt: Das ganze Blatt kommt in den Rahmen.
- gleicht ungleichmäßiges Licht vom Foto aus (Papier wird gleichmäßig hell)
- schneidet einen schmalen Rand ab (Tischkante, Schatten)
- speichert eine große Version (assets/bearbeitet) und eine kleine eingebettete Version fürs Spiel

Aufruf: python3 tools/bild_vorbereiten.py foto.jpg name [--licht]
  name      Dateiname ohne Endung, z. B. bild_wal  → Platzhalter {{BILD_WAL}} im Spiel
  --licht   Licht ausgleichen (für Bleistift-/Buntstiftbilder auf Papier; nicht für dunkle Gemälde)
"""
import base64
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from zeichnung_freistellen import background_estimate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def prepare(src, name, licht=False, rand=0.025):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * rand), int(h * rand), int(w * (1 - rand)), int(h * (1 - rand))))
    if licht:
        rgb = np.asarray(im).astype(np.float32)
        bg = background_estimate(np.asarray(im))
        paper = np.array([250, 246, 238], np.float32)        # warmes Papierweiß
        norm = np.clip(rgb / np.maximum(bg, 1) * paper, 0, 255)
        im = Image.fromarray(norm.astype(np.uint8))
        im = ImageEnhance.Contrast(im).enhance(1.12)
        im = ImageEnhance.Color(im).enhance(1.2)
    im.save(ROOT / "assets" / "bearbeitet" / f"{name}.jpg", quality=90)
    small = im.resize((300, int(im.height * 300 / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    small.save(buf, "WEBP", quality=80)
    (ROOT / "game" / f"{name}.b64").write_text(base64.b64encode(buf.getvalue()).decode())
    print(name, small.size, len(buf.getvalue()) // 1024, "KB")


if __name__ == "__main__":
    prepare(sys.argv[1], sys.argv[2], "--licht" in sys.argv)
