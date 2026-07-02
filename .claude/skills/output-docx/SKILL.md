---
name: output-docx
description: Stufe 6 der Bewerbungs-Pipeline. Rendert die freigegebenen Inhalte aus 04_entwurf.md in die DOCX-Vorlagen aus ./vorlagen/ und schreibt die finalen Dateien (anschreiben_<firma>.docx, lebenslauf_<firma>.docx) ins Run-Verzeichnis. Nutze diesen Skill erst nach bestandener QA und ausdrücklicher Freigabe durch den Menschen.
---

# Stufe 6: Output DOCX

**Vorbedingung:** `05_qa.json` → `bestanden: true` **und** Freigabe des Menschen
(`freigabe.txt` im Run-Verzeichnis). Der Hook erzwingt dies zusätzlich; ohne
Freigabe wird der Schreibvorgang hart gestoppt (Exit-Code 2).

Inputs:
- `04_entwurf.md` (freigegebener Inhalt)
- Vorlagen: `vorlagen/anschreiben.dotx`, `vorlagen/lebenslauf.dotx`
- Absenderdaten aus `profil/lebenslauf.docx`

Outputs (im Run-Verzeichnis):
- `anschreiben_<firma>.docx`
- `lebenslauf_<firma>.docx`

## Vorgehen
1. Parse `04_entwurf.md` in die Platzhalter-Felder der Vorlagen (Jinja-Syntax:
   `{{ ... }}`, `{% for ... %}`).
2. Rendere mit `docxtpl` (siehe Hilfsskript). Übergib ein Kontext-Dict mit allen
   Feldern (absender_name, firma_name, betreff, anschreiben_text, kurzprofil,
   erfahrung[], ausbildung[], skills, …).
3. Schreibe die finalen Dateien ins Run-Verzeichnis. Verändere die Vorlagen selbst
   nicht.

## Hilfsskript
```bash
python .claude/scripts/render_docx.py \
  --entwurf "<run>/04_entwurf.md" \
  --firma "<firma>" \
  --out "<run>"
```
Das Skript liest die Vorlagen, füllt den Kontext und schreibt beide DOCX-Dateien.
Passe den Kontextaufbau bei Bedarf an die konkrete Struktur von `04_entwurf.md` an.

## Abschluss
Melde dem Menschen die Pfade der erzeugten Dateien und einen kurzen Hinweis, die
DOCX in Word/LibreOffice final zu prüfen.

## Danach: Stufe 5b (ATS-Check)
Nach dem Rendering läuft der ATS-Simulator (Skill `ats-check`) über die eben
erzeugten DOCX und misst die Keyword-Abdeckung/Parsing-Tauglichkeit. Halte die
Vorlagen daher ATS-freundlich: einspaltig, Standard-Überschriften
(„Berufserfahrung", „Ausbildung", „Kenntnisse"), Kontaktdaten im Fließtext,
keine kritischen Inhalte in Tabellen/Kopfzeilen/Textboxen.
