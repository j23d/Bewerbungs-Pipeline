---
name: analyse-stellenanzeige
description: Stufe 1 der Bewerbungs-Pipeline. Extrahiert aus einer Stellenanzeige die Must-haves, Nice-to-haves, relevanten Keywords und den Ton/Stil. Nutze diesen Skill, wenn eine Stellenanzeige analysiert werden soll, bevor Bewerbungsunterlagen erstellt werden.
---

# Stufe 1: Analyse der Stellenanzeige

Input: die Stellenanzeige (`runs/<lauf>/stellenanzeige.txt`).
Output: `01_analyse.md` im Run-Verzeichnis. Sprache: Deutsch.

## Vorgehen
Lies die Stellenanzeige sorgfältig und extrahiere strukturiert:

1. **Eckdaten:** Firma, Rollenbezeichnung, Standort/Remote, ggf. Ansprechpartner.
2. **Must-haves** (harte Anforderungen): jede als eigener, prüfbarer Punkt.
3. **Nice-to-haves** (wünschenswert, nicht zwingend).
4. **Keywords für ATS:** konkrete Begriffe, Tools, Technologien, Zertifikate,
   Methoden — genau in der Schreibweise der Anzeige (für spätere Keyword-Abdeckung).
5. **Ton & Stil:** förmlich/locker, „Du"/„Sie", Werte/Kultur-Signale.
6. **Zwischen-den-Zeilen:** implizite Erwartungen, priorisierte Kompetenzen.

Erfinde keine Anforderungen. Nur was in der Anzeige steht.

## Ausgabeformat (`01_analyse.md`)
```markdown
# Analyse der Stellenanzeige

## Eckdaten
- Firma / Rolle / Standort / Ansprechpartner

## Must-haves
- ...

## Nice-to-haves
- ...

## Keywords (ATS)
- ...

## Ton & Stil
- Ansprache (Du/Sie), Formalität, Kultur-Signale

## Zwischen den Zeilen
- ...
```
