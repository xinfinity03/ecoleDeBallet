# École de Ballet Étoile – Spielkonzept

Stand: 21.11.2026. Diese Datei sammelt alle Entscheidungen. Sie wird laufend ergänzt.

## Grundidee
- Ballettschule in **Paris**. Die Spielerin oder der Spieler lässt sich dort zum Ballettprofi ausbilden.
- **Ziel:** die Ausbildung bestehen. Dafür sammelt man Punkte, vor allem Lob-Punkte von Madame Colletin, aber auch auf anderen Wegen.
- Es gibt verschiedene **Aufführungen** auf der Bühne des Théâtre.
- Für Kinder von **6 bis 14 Jahren**: viele Bilder, wenig Text, Vorlesefunktion, kein frustrierendes Scheitern.

## Technik
- Läuft im **Browser auf dem iPad** (Safari, Querformat) und lässt sich als Web-App auf den Startbildschirm legen.
- Bedienung nur mit Tippen und Wischen.
- **Grafik:** gezeichnete Vektorgrafik, keine Pixelgrafik. Dazu kommen eigene Buntstiftzeichnungen (freigestellt und ausgemalt, siehe `tools/zeichnung_freistellen.py`).
- **Ansicht:** von der Seite, wie ein aufgeschnittenes Puppenhaus.

## Phasen
1. **Einzelspieler** (jetzt): Alle anderen Figuren werden vom Spiel gesteuert.
2. **Mehrspieler** (später, wenn uns das Spiel gut genug gefällt): Echte Spielerinnen und Spieler an ihren eigenen Tablets ziehen nach und nach in die freien Betten ein.
   - Dafür braucht es später einen Server und Spielerkonten mit Zustimmung der Eltern.
   - Gesprochen wird **mit vorgegebenen Sätzen statt freiem Chat**. Das schützt die Kinder.
   - Das Spiel wird schon jetzt so gebaut, dass jedes Bett einen „Bewohner" hat. Der ist entweder eine Spielfigur oder später ein echter Spieler.

## Das Gebäude (siehe `schule_aufbau.png`)
| Stockwerk | Räume |
|---|---|
| Dach | Boutique (Kleider für Lob-Punkte), Büro der Direktorin (Prüfungen, Zeugnisse), **Dachterrasse** (Treffpunkt mit Blick über Paris) |
| 3. Stock | Jungen: Zimmer 6–10 |
| 2. Stock | Mädchen: Zimmer 1–5 |
| 1. Stock | Großer Ballettsaal (Unterricht, Üben für Auftritte), Umkleide ♀ und Umkleide ♂ |
| Erdgeschoss | Entrée (Eingangshalle, Schwarzes Brett), Café (später: Macarons selbst gestalten) |
| Théâtre (Anbau) | Bühne mit Publikum, Garderobe & Maske, Kulissenlager |

- Alle Zimmer sind **Zweibettzimmer mit eigenem Bad**.
- Man läuft frei durch das Haus. Eine Treppe verbindet alle Stockwerke.
- Jedes Stockwerk hat einen **Gang**. Von dort betritt man die Räume durch **Türen mit Namensschildern** (z. B. „Zimmer 1 · Elisabeth").
- Alle Zimmer haben ein **französisches Fenster bis zum Boden** (so hoch wie die Tür, mit kleinem Balkongitter) und **Blick auf den Eiffelturm**. Der Himmel richtet sich nach der Uhrzeit: Morgen (6–9 Uhr), Tag (9–17), Abend (17–21), Nacht (21–6 Uhr, der Eiffelturm glitzert).
- Jedes Bad hat Dusche, Toilette und Waschbecken. Bei den Jungen sind Vorhänge und Duschvorhang blau.
- **Dachterrasse:** Je nach Tageszeit sind dort Figuren (morgens Levi oder Elisabeth, tagsüber Nora und Samy oder Marie und Tom, abends Johanna mit Leon oder mit Elisabeth und Levi, nachts niemand). Wer oben ist, fehlt so lange im eigenen Zimmer. Treffpunkt (später auch für echte Mitspieler), mit Fernrohr und den Sehenswürdigkeiten Eiffelturm, Sacré-Cœur, Opéra Garnier, Arc de Triomphe und Notre-Dame.

## Zimmer und Mitbewohner
- Man **sucht sich sein Zimmer selbst aus** (Mädchen im 2. Stock, Jungen im 3. Stock).
- **Vorschlag:** Jede Figur wohnt in einem eigenen Zimmer, das zweite Bett ist frei. Wer ein Zimmer aussucht, sucht sich damit auch die Mitbewohnerin bzw. den Mitbewohner aus. Zimmer 5 und Zimmer 10 sind leer, dort wohnt man allein und ist später offen für echte Mitspieler.

| Zimmer | Bewohner | | Zimmer | Bewohner |
|---|---|---|---|---|
| 1 | Elisabeth | | 6 | Leon |
| 2 | Johanna | | 7 | Levi |
| 3 | Marie | | 8 | Tom |
| 4 | Nora | | 9 | Samy |
| 5 | frei | | 10 | frei |

- Das eigene Zimmer kann man einrichten, zum Beispiel mit dem roten Sofa.

## Figuren (siehe `assets/konzept/figuren.svg`)
**Tänzerinnen**
- **Elisabeth**: normal groß, braune gelockte Haare, kann schon gut tanzen, hilfsbereit
- **Johanna**: normal groß, blond, schulterlange Haare, chillig, redet gern, hört gern Musik
- **Marie**: normal groß, lange blonde Haare, zickig, tanzt sehr gut
- **Nora**: kleiner, lange schwarze Haare, schüchtern, liest gern, sehr nett

**Tänzer**
- **Leon**: groß, schwarze Haare, nett, lustig, sehr guter Tänzer
- **Levi**: mittelgroß, braune Haare (glatt, Seitenscheitel), freundlich, tanzt für sein Leben gern Ballett
- **Tom**: klein, gegelte blonde Haare, Angeber
- **Samy**: groß, dunkelhäutig, braune Haare, freundlich

**Lehrerin**
- **Madame Colletin**: groß, schwarze Haare, streng, sehr gute Lehrerin, perfekte Tänzerin, hat an allen großen Theatern getanzt

## Spielfunktionen
- **Sprechen:** Figur antippen, dann erscheint eine Sprechblase mit Antworten zum Auswählen. Jede Figur spricht passend zu ihrem Charakter.
- **Avatar selbst gestalten:** Tänzerin oder Tänzer, Hautfarbe, Haarfarbe, Frisur, Augenfarbe, Körperform, Kleidung. Grundlage ist dasselbe Baukastensystem wie bei den Figuren (`tools/figuren.py`).
- **Anziehen:** am Kleiderschrank im Zimmer und in der Umkleide. Am Anfang gibt es ein paar Kleider (darunter das rosa Tutu), weitere kauft man in der Boutique mit Lob-Punkten.
- **Punkte:** Lob-Punkte von Madame Colletin, weitere Punktearten folgen.
- **Später:** Macarons im Café selbst gestalten, Mehrspieler.

## Ballettunterricht (Rhythmus-Spiel)
- Im Ballettsaal Madame Colletin ansprechen → „Ich möchte üben!"
- Oben laufen Karten mit Positionen zum Kreis „Jetzt!". Ist eine Karte im Kreis, tippt man im Takt der Klaviermusik unten auf die passende Position. Madame Colletin zeigt die nächste Position vor, Elisabeth und Levi tanzen mit.
- Positionen: Bras bas (Arme rund nach unten), Seconde (Arme zur Seite), En haut (Arme rund nach oben), Plié (Knie beugen), Relevé (auf die Zehenspitzen), Arabesque (ein Bein nach hinten).
- Stufen: **Leicht** (2 Positionen, 12 Karten, langsam), **Mittel** (4 Positionen, 16 Karten), **Schwer** (alle 6, 20 Karten, schneller).
- Bewertung: Perfekt = 2, Gut = 1 Punkt. Am Ende 0–3 Sterne (ab 30 / 60 / 85 %). **Jeder Stern = 1 Lob-Punkt.** Die beste Sternzahl je Stufe wird gespeichert.
- Offen: Soll es Lob-Punkte bei jeder Wiederholung geben oder z. B. nur einmal am Tag / nur für neue Rekorde?

## Zimmer einrichten
- Im eigenen Zimmer gibt es den Knopf **„Einrichten"**. Unten öffnet sich ein Katalog, die Szene wird so lange verkleinert, damit das ganze Zimmer zu sehen ist.
- Antippen stellt den Gegenstand ins Zimmer. Mit dem Finger verschieben: Wandsachen frei an der Wand, Möbel am Boden entlang. **×** räumt weg.
- Gratis: **unsere eigenen Bilder** („Ballerina im Licht", „Wal im Sonnenuntergang", „Der alte Turm", „Spaziergang im Park", „Stillleben mit Früchten", „Straße in der Stadt"), das rote Sofa (unsere Zeichnung), eine Zimmerpflanze.
- Mit Lob-Punkten: Poster Schwanensee (1), Teddybär, Stehlampe (leuchtet abends), runder Teppich, Sitzkissen (je 2), Bücherregal, Goldspiegel (je 3), Tutu am Haken, Lichterkette (je 4).
- Nach dem ersten Einrichten sagt die Mitbewohnerin bzw. der Mitbewohner etwas dazu (wenn sie/er gerade im Zimmer ist).
- Neue eigene Bilder: Foto mit `python3 tools/bild_vorbereiten.py foto.jpg bild_name --licht` vorbereiten (ganzes Blatt, Licht ausgeglichen) und im Katalog `DECOR` in `game/spiel.html` eintragen.

## Für später gemerkt
- **Bilder in den Rahmen malen wir selbst.** Die Ballettbilder über den Betten (und später weitere Bilder im Haus) sind im Moment nur Platzhalter. Sie werden durch eigene Zeichnungen ersetzt, die wie Sofa und Kleid freigestellt werden (`tools/zeichnung_freistellen.py`). Am besten im Querformat zeichnen, ungefähr im Seitenverhältnis 4:3.

## Prototyp 1 (21.11.2026)
Spielbar unter https://claude.ai/artifact/75v5SbU8dhCx72YkYJ1aBg (Quelltext: `game/spiel.html`, bauen mit `python3 game/build.py`).
- Avatar-Editor: Tänzerin/Tänzer, Name, Hautfarbe, Haarfarbe, Frisur, Augenfarbe, Farbe des Outfits
- Alle Stockwerke mit Gang und Treppe, alle 10 Zimmer mit eigenem Bad und Eiffelturm-Blick
- Zimmer aussuchen und einziehen (Türschild zeigt danach beide Namen)
- Gespräche mit allen 8 Tänzerinnen und Tänzern und mit Madame Colletin (erster Lob-Punkt fürs „Bonjour")
- Vorlesefunktion, Aufgaben-Hinweise, Spielstand wird auf dem Gerät gespeichert
- Café, Théâtre, Boutique, Büro und Umkleiden sind schon begehbar, aber noch Platzhalter

## Offene Fragen
- Weitere Punktearten (außer Lob)?
- Welche Aufführungen gibt es (z. B. Schwanensee, Nussknacker) und in welcher Reihenfolge?
- Wie läuft die Ausbildung ab (Jahre/Level, Prüfungen)?
- Wie heißt die Direktorin?
