---
name: bewerbung
description: Orchestrator und Einstiegspunkt der Bewerbungs-Pipeline. Nutze diesen Skill, wenn der Nutzer Bewerbungsunterlagen (Anschreiben + Lebenslauf) zu einer Stellenanzeige erstellen will, /bewerbung aufruft, oder eine Stellenanzeige (Datei, URL, Text) zur Bewerbung übergibt. Steuert die Stufen 1-6, persistiert Zwischenstände und implementiert die QA-Rücksprung-Schleife und Human-in-the-Loop-Freigabe.
---

# Orchestrator: Bewerbungs-Pipeline

Einstieg: `/bewerbung $ARGUMENTS` — `$ARGUMENTS` ist die Stellenanzeige
(Dateipfad, URL oder direkt eingefügter Text).

Lies zuerst `CLAUDE.md` und halte dich strikt an die **Wahrheitstreue-Regel**.
Alle Ausgaben auf Deutsch.

## Ablauf

### Setup
1. Bestimme `<firma>` aus der Stellenanzeige (kleingeschrieben, ohne Sonderzeichen;
   falls unklar, frage kurz nach).
2. Bestimme den Zeitstempel `<YYYY-MM-DD-HHMM>` (heute/jetzt).
3. Lege das Run-Verzeichnis an: `runs/<YYYY-MM-DD-HHMM>-<firma>/`.
4. Speichere die Stellenanzeige dort als `stellenanzeige.txt` (bei URL: Inhalt
   abrufen und Text sichern; bei Datei: hineinkopieren).

### Wiederaufnahme-Prüfung
Prüfe vor jeder Stufe, ob ihre Ausgabedatei im Run-Verzeichnis schon existiert.
Wenn ja und gültig: überspringe die Stufe (Wiederaufnahme nach Unterbrechung).
Persistiere nach **jeder** Stufe den Zwischenstand als Datei.

### Stufen
1. **Analyse** (Skill `analyse-stellenanzeige`) → schreibe `01_analyse.md`.
2. **Profilabgleich** (Skill `profilabgleich`) → schreibe `02_abgleich.md`.
3. **Lücken-Dialog** (Skill `luecken-dialog`, **Human Input**) → schreibe
   `03_dialog.md`. Der Skill stellt Fragen und **wartet** auf die Antworten des
   Menschen; erfinde nichts. Antworten werden zusätzlich nach
   `profil/ergaenzungen.docx` zurückgeschrieben. Danach hält der Lauf ggf. an,
   bis der Mensch antwortet (wiederaufnehmbar).
4. **Erstellung** (Skill `erstellung`) → schreibe `04_entwurf.md`
   (Anschreiben + Lebenslauf-Inhalt). Bei Rücksprung aus Stufe 5: übergib die
   QA-Findings aus `05_qa.json` als zusätzlichen Input.
5. **Qualitätsprüfung** (Subagent `qa-reviewer`, isolierter Kontext) → schreibe
   `05_qa.json`. Übergib dem Subagenten **nur** `01_analyse.md` und `04_entwurf.md`
   sowie lesenden Zugriff auf das Masterprofil für den Halluzinations-Check.
   **Nicht** die Generierungshistorie.

### QA-Rücksprung-Schleife (5 → 4)
- Ist `05_qa.json` → `bestanden: false`: gehe zurück zu Stufe 4 mit den `findings`
  als Input, erzeuge einen neuen `04_entwurf.md`, dann erneut Stufe 5.
- Zähle Iterationen. Nach **max. 3** fehlgeschlagenen Durchläufen: **Stop** und
  Bericht an den Menschen (welche Findings blieben offen, Empfehlung).
- Bei `bestanden: true`: weiter zum Human-in-the-Loop.

### Human-in-the-Loop (Inhalts-Freigabe, vor Stufe 6)
- Lege dem Menschen die Entwürfe (`04_entwurf.md`) und den QA-Bericht
  (`05_qa.json`, ats_score) zur **Prüfung/Freigabe/Änderung** vor.
- **Warte** auf explizite Freigabe. Bei Änderungswunsch: zurück zu Stufe 4.
- Kein finaler Output ohne Freigabe (wird zusätzlich durch den Hook erzwungen).

### Stufe 6 (nach Inhalts-Freigabe)
- **Output** (Skill `output-docx`) → rendert `04_entwurf.md` in die Vorlagen und
  schreibt `anschreiben_<firma>.docx` und `lebenslauf_<firma>.docx` ins
  Run-Verzeichnis.

### Stufe 5b: ATS-Check (nach Stufe 6, Warnung-und-Freigabe)
- **ATS-Simulator** (Skill `ats-check`) → liest die eben gerenderten DOCX zurück
  und schreibt `05b_ats.json` + `ats_extrakt.txt`.
- Dies ist **kein hartes Gate**: Liegt der gemessene Score unter der Schwelle
  oder gibt es Parsing-Warnungen, lege beides dem Menschen **deutlich** vor.
  - Bei Parsing-Warnungen (Tabellen/Kopfzeilen/Textboxen etc.): Empfehlung,
    `vorlagen/` zu korrigieren und Stufe 6 neu zu rendern.
  - Bei belegbaren Keyword-Lücken: optional zurück zu Stufe 4 (nur belegtes
    Vokabular angleichen, nichts erfinden).
  - Der Mensch kann die Warnung **bewusst übersteuern** und die Unterlagen so
    belassen. Die endgültige Entscheidung liegt bei ihm.

## Zustandsdateien im Run-Verzeichnis
```
stellenanzeige.txt   01_analyse.md   02_abgleich.md   03_dialog.md
04_entwurf.md        05_qa.json      freigabe.txt (nach Freigabe)
anschreiben_<firma>.docx   lebenslauf_<firma>.docx
05b_ats.json   ats_extrakt.txt   (ATS-Check, nach Rendering)
```
`freigabe.txt` enthält den Freigabe-Vermerk des Menschen (dient dem Hook als Nachweis).
