---
name: profilabgleich
description: Stufe 2 der Bewerbungs-Pipeline. Gleicht das Masterprofil (Lebenslauf + Ergänzungen + Nachweise) gegen die Stellenanzeigen-Analyse ab und benennt Stärken (belegte Treffer) und Lücken (unbelegte oder fehlende Anforderungen) explizit. Nutze diesen Skill nach der Stellenanzeigen-Analyse.
---

# Stufe 2: Profilabgleich

Inputs:
- `01_analyse.md` (Must-haves, Nice-to-haves, Keywords)
- Masterprofil: `profil/lebenslauf.docx`, `profil/ergaenzungen.docx`
- Nachweise: `profil/nachweise/*.pdf` (Existenz/Belege)

Output: `02_abgleich.md` im Run-Verzeichnis. Sprache: Deutsch.

## Vorgehen
Gehe jede Anforderung aus Stufe 1 durch und ordne sie einer Kategorie zu:

- **Stärke (belegt):** Anforderung ist durch eine konkrete Stelle im Masterprofil
  oder einen Nachweis gedeckt. Notiere die Belegquelle.
- **Teilweise gedeckt:** verwandte Erfahrung vorhanden, aber nicht exakt — notiere,
  was fehlt.
- **Lücke:** keine Deckung im Masterprofil. Diese Punkte gehen in Stufe 3
  (Lücken-Dialog).

**Wahrheitstreue-Regel:** Ein Punkt gilt nur als „belegt", wenn es tatsächlich eine
Quelle gibt. Nichts wohlwollend als vorhanden markieren.

## Ausgabeformat (`02_abgleich.md`)
```markdown
# Profilabgleich

## Stärken (belegt)
- [Anforderung] — Beleg: [Quelle im Masterprofil / Nachweis]

## Teilweise gedeckt
- [Anforderung] — vorhanden: [...] / fehlt: [...]

## Lücken (für Stufe 3)
- [Anforderung] — keine Deckung gefunden

## Keyword-Abdeckung
- Abgedeckte Keywords: ...
- Fehlende Keywords: ...
```
