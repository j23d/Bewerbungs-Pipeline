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
5b. **ATS-Check** (Simulator) → liest die fertigen DOCX zurück, **misst** die
   Keyword-Abdeckung gegen die Must-haves und meldet Parsing-Probleme

- **Rücksprung 5→4** bei durchgefallener QA (max. 3 Iterationen).
- **Quality-Gate-Hook** verhindert finalen Output ohne bestandene QA + Freigabe.
- **Human-in-the-Loop:** finaler Output erst nach deiner ausdrücklichen Freigabe.
- **ATS-Check (5b): Warnung-und-Freigabe** – kein hartes Gate; ein niedriger
  gemessener Score oder Parsing-Warnungen werden dir vorgelegt, du entscheidest.

### Warum die KI-Vorauswahl überwinden?
Viele Bewerbungen scheitern schon an der maschinellen Vorauswahl (ATS), bevor ein
Mensch sie sieht. Ursache ist meist **Format** (Parsing zerlegt zweispaltige
Layouts, Kopfzeilen, Textboxen falsch), nicht fehlende Qualifikation. Stufe 5b
simuliert dieses Parsen: Sie liest die fertige DOCX so zurück, wie ein ATS es tut,
und liefert einen **gemessenen** statt geschätzten Score plus konkrete
Format-Warnungen. `ats_extrakt.txt` zeigt, was das ATS tatsächlich „sieht".
**Grenze:** Optimiert wird nur die Darstellung wahrer Fakten – keine versteckten
Keywords, kein weißer Text (fliegt bei modernen Rankern/HR auf).

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
  scripts/                    Hilfsskripte (Rückschreiben, DOCX-Rendering, ATS-Check)
  settings.json               Hook-Konfiguration
```

## Datenschutz (PII bleibt lokal)
Personenbezogene Daten dürfen **nicht** ins Repository gelangen. Dafür gibt es drei
Verteidigungslinien:
1. **`.gitignore`** (restriktive Whitelist): `profil/**` und `runs/**` werden pauschal
   ignoriert; nur Struktur-/Hinweisdateien und die leeren `vorlagen/*.dotx` sind
   freigegeben. Dokument-/Bildformate (`*.docx`, `*.pdf`, `*.jpg`, `*.csv`, …) sind
   baumweit gesperrt. Zusätzlich lokale `.gitignore` in `profil/` und `runs/`.
2. **`.githooks/pre-commit`** (aktiver Wächter): blockiert jeden Commit, der
   PII-verdächtige Dateien enthält — **auch** bei `git add -f`. Aktiv über
   `git config core.hooksPath .githooks` (bei frischem Clone einmalig setzen).
3. **`.gitattributes`**: behandelt Office-Dateien als Binär (kein versehentliches
   Diffen von Inhalten).

**Nach einem frischen `git clone` einmalig ausführen:**
```
git config core.hooksPath .githooks
```
Notfall-Umgehung des Hooks nur bewusst mit `git commit --no-verify`.

## Voraussetzungen
Python mit `python-docx` und `docxtpl` (bereits installiert). Vor dem ersten Lauf
`profil/lebenslauf.docx` mit echten Fakten füllen und Nachweise in
`profil/nachweise/` ablegen.
