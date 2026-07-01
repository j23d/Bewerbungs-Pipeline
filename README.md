# Bewerbungs-Pipeline

Agentische Pipeline zur Erstellung von Bewerbungsunterlagen (Anschreiben +
Lebenslauf) auf Deutsch — wahrheitstreu, ATS-orientiert, mit Human-in-the-Loop.

## Start
Im Projekt-Root aufrufen:

```
/bewerbung <Stellenanzeige>
```

`<Stellenanzeige>` ist ein Dateipfad, eine URL oder direkt eingefügter Text.
Die Pipeline legt automatisch ein Run-Verzeichnis an und führt dich durch die Stufen.

## Pipeline
1. **Analyse** der Stellenanzeige → Must-haves, Nice-to-haves, Keywords, Ton
2. **Profilabgleich** → Stärken & Lücken
3. **Lücken-Dialog** (Human Input) → sokratische Fragen; Antworten werden nach
   `profil/ergaenzungen.docx` zurückgeschrieben
4. **Erstellung** → Anschreiben + Lebenslauf-Inhalt (keyword-orientiert, faktentreu)
5. **QA** (isolierter Subagent `qa-reviewer`) → ATS, Ton, Vollständigkeit, Halluzinations-Check
6. **Output DOCX** → finale Dateien in die Vorlagen gerendert

- **Rücksprung 5→4** bei durchgefallener QA (max. 3 Iterationen).
- **Quality-Gate-Hook** verhindert finalen Output ohne bestandene QA + Freigabe.
- **Human-in-the-Loop:** finaler Output erst nach deiner ausdrücklichen Freigabe.

## Struktur
```
CLAUDE.md                     Projektkonstitution (Wahrheitstreue-Regel, Pfade, Ablauf)
profil/
  lebenslauf.docx             Masterprofil (Single Source of Truth)  ← ausfüllen
  ergaenzungen.docx           automatisch fortgeschriebene Dialog-Antworten
  nachweise/*.pdf             Zeugnisse, Zertifikate                 ← ablegen
vorlagen/
  anschreiben.dotx            Layout-Vorlage (docxtpl / Jinja-Felder)
  lebenslauf.dotx             Layout-Vorlage
runs/<datum>-<firma>/         Arbeitsverzeichnis pro Lauf (Zwischenstände + finale DOCX)
.claude/
  skills/                     je Pipeline-Stufe ein Skill (+ Orchestrator 'bewerbung')
  agents/qa-reviewer.md       QA-Subagent (Stufe 5)
  hooks/quality_gate.py       Quality-Gate + Freigabe-Prüfung
  scripts/                    Hilfsskripte (Rückschreiben, DOCX-Rendering)
  settings.json               Hook-Konfiguration
```

## Voraussetzungen
Python mit `python-docx` und `docxtpl` (bereits installiert). Vor dem ersten Lauf
`profil/lebenslauf.docx` mit echten Fakten füllen und Nachweise in
`profil/nachweise/` ablegen.
