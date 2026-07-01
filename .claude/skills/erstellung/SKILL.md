---
name: erstellung
description: Stufe 4 der Bewerbungs-Pipeline. Erstellt die Inhalte für Anschreiben und Lebenslauf, integriert die Keywords aus der Stellenanzeigen-Analyse und hält sich strikt an die Wahrheitstreue-Regel (nur belegte Aussagen). Verarbeitet auch QA-Findings bei Rücksprung aus Stufe 5. Nutze diesen Skill, wenn die Bewerbungsinhalte verfasst oder überarbeitet werden sollen.
---

# Stufe 4: Erstellung der Inhalte

Inputs:
- `01_analyse.md` (Keywords, Ton, Must-haves)
- `02_abgleich.md` (Stärken, geklärte Punkte)
- `03_dialog.md` und `profil/ergaenzungen.docx` (im Dialog gesicherte Antworten)
- Masterprofil `profil/lebenslauf.docx`
- **Bei Rücksprung:** `05_qa.json` (Findings, die behoben werden müssen)

Output: `04_entwurf.md` im Run-Verzeichnis. Sprache: Deutsch.

## Wahrheitstreue-Regel (hart)
Jeder Satz muss aus Masterprofil, Ergänzungen, Nachweisen oder dem Dialog stammen.
**Nichts erfinden.** Offene Lücken werden nicht als Kompetenz behauptet. Im Zweifel:
weglassen oder ehrlich als Entwicklungsfeld formulieren, nicht ausschmücken.

## Vorgehen
1. **Anschreiben:** individuell auf die Firma/Rolle, im Ton der Anzeige (Du/Sie
   übernehmen). Struktur: Aufhänger → Passung (belegte Stärken zu Must-haves) →
   Motivation/Kulturfit → Abschluss. Keywords natürlich einbauen, nicht stapeln.
2. **Lebenslauf-Inhalt:** relevante Erfahrungen zuerst; Formulierungen auf die
   Must-haves und Keywords ausrichten, aber faktentreu.
3. **Keyword-Abdeckung:** decke die Must-have-Keywords aus Stufe 1 ab, soweit sie
   tatsächlich belegt sind.
4. **Bei Rücksprung (5→4):** arbeite jedes Finding aus `05_qa.json` gezielt ab
   (Halluzinationen entfernen, Keyword-Lücken schließen, Ton anpassen). Notiere am
   Ende kurz, welche Findings wie behoben wurden.

## Ausgabeformat (`04_entwurf.md`)
```markdown
# Entwurf

## Anschreiben
[vollständiger Fließtext, inkl. Betreff, Anrede, Gruß]

## Lebenslauf
### Kurzprofil
...
### Berufserfahrung
- ...
### Ausbildung
- ...
### Skills
...

## Behobene QA-Findings (nur bei Rücksprung)
- Finding → Maßnahme
```
