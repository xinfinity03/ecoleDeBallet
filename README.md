# École de Ballet Étoile

Ein Ballettschul-Spiel für Kinder von 6 bis 14 Jahren, das auf dem iPad im Browser läuft.
Die Spielerin oder der Spieler lässt sich an einer Ballettschule in Paris zum Ballettprofi ausbilden.

- **Spielen:** https://claude.ai/artifact/75v5SbU8dhCx72YkYJ1aBg
- **Spielkonzept mit allen Entscheidungen:** [SPIELKONZEPT.md](SPIELKONZEPT.md)

## Ordner
| Ordner/Datei | Inhalt |
|---|---|
| `game/spiel.html` | Das Spiel (Quelltext) |
| `game/build.py` | Baut `game/index.html` mit eingebetteten Zeichnungen |
| `assets/original/` | Eigene Zeichnungen (Fotos) |
| `assets/bearbeitet/` | Freigestellte und ausgemalte Zeichnungen |
| `assets/konzept/` | Gebäudeplan und Figuren als SVG |
| `tools/zeichnung_freistellen.py` | Zeichnung freistellen und ausmalen |
| `tools/schule_aufbau.py` | Zeichnet den Gebäudeplan |
| `tools/figuren.py` | Zeichnet die Figurenübersicht |

## Spiel bauen
```bash
python3 game/build.py
```
