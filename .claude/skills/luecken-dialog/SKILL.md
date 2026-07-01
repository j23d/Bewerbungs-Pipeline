---
name: luecken-dialog
description: Stufe 3 der Bewerbungs-Pipeline (Human Input). Führt einen sokratischen Dialog mit dem Menschen zu jeder im Profilabgleich gefundenen Lücke, wartet auf die Antworten und erfindet nichts. Schreibt die Antworten sofort nach profil/ergaenzungen.docx zurück, damit dieselbe Lücke bei der nächsten Bewerbung nicht erneut abgefragt wird. Nutze diesen Skill nach dem Profilabgleich, wenn Lücken zu klären sind.
---

# Stufe 3: Lücken-Dialog (Human-in-the-Loop)

Inputs: `02_abgleich.md` (Abschnitte „Teilweise gedeckt" und „Lücken").
Outputs: `03_dialog.md` (Frage-Antwort-Protokoll) **und** Fortschreibung von
`profil/ergaenzungen.docx`. Sprache: Deutsch.

## Vorgehen (sokratisch, ehrlich)
1. Formuliere zu **jeder** Lücke gezielte, offene Fragen, die dem Menschen helfen,
   vorhandene — aber im Profil fehlende — Erfahrung zu erinnern und zu präzisieren.
   Beispiele: „Hast du X schon einmal in einem Projekt eingesetzt? Wenn ja: wo,
   wie lange, mit welchem Ergebnis?"
2. **Stelle die Fragen und warte** auf die Antworten des Menschen. Fahre nicht
   selbstständig fort und fülle keine Antworten aus.
3. **Erfinde nichts.** Wenn der Mensch eine Lücke nicht schließen kann, wird sie als
   „offen" markiert und im Anschreiben/Lebenslauf **nicht** behauptet.
4. Frage bei vagen Antworten nach, bis die Aussage konkret und belegbar ist
   (Zahlen, Zeiträume, Kontext).

## Rückschreiben (wichtig)
Nach Erhalt der Antworten:
- Ergänze `profil/ergaenzungen.docx` um jede neue, gesicherte Aussage — mit Datum
  und Verweis auf den Lauf. So wird dieselbe Lücke künftig nicht erneut abgefragt.
- Nutze dafür das Hilfsskript (python-docx):

```bash
python .claude/scripts/append_ergaenzung.py \
  --datum "<YYYY-MM-DD>" --lauf "<run-verzeichnis>" \
  --frage "<Frage>" --antwort "<Antwort des Menschen>"
```

## Ausgabeformat (`03_dialog.md`)
```markdown
# Lücken-Dialog

## [Lücke 1]
**Frage:** ...
**Antwort (Mensch):** ...
**Status:** geschlossen / offen
**In ergaenzungen.docx geschrieben:** ja/nein

## [Lücke 2]
...
```
