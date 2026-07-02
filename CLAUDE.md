# Projektkonstitution — Bewerbungs-Pipeline

Dieses Projekt ist eine agentische Pipeline zur Erstellung von Bewerbungsunterlagen
(Anschreiben + Lebenslauf). Diese Datei ist verbindlich für **alle** Läufe.

## Sprache
Alle Ausgaben, Zwischenstände, Fragen und finalen Dokumente sind auf **Deutsch**.

## Wahrheitstreue-Regel (HART, nicht verhandelbar)
Es werden **NIEMALS** Qualifikationen, Erfahrungen, Zahlen, Titel, Zeiträume oder
Kompetenzen erfunden, geschätzt oder „plausibel ergänzt".

Jede einzelne Aussage im Anschreiben oder Lebenslauf **muss** ihre Quelle haben in:
1. dem Masterprofil (`profil/lebenslauf.docx`) und den Ergänzungen
   (`profil/ergaenzungen.docx`), oder
2. den Nachweisen (`profil/nachweise/*.pdf`), oder
3. einer Antwort, die der Mensch im sokratischen Lücken-Dialog (Stufe 3)
   ausdrücklich gegeben hat.

Im Zweifel gilt: **nachfragen statt ausschmücken.** Lieber eine Lücke offen
benennen als eine unbelegte Behauptung aufstellen. Diese Regel steht über allen
anderen Zielen (auch über ATS-Score oder Vollständigkeit).

## Datenquellen (lokal, kein MCP)
- **Masterprofil:** `./profil/lebenslauf.docx` — gesicherte Fakten, Erfahrungen, Skills.
- **Ergänzungen:** `./profil/ergaenzungen.docx` — automatisch fortgeschriebene
  Antworten aus früheren Lücken-Dialogen.
- **Nachweise:** `./profil/nachweise/*.pdf` — Zeugnisse, Zertifikate.
- **DOCX-Vorlagen:** `./vorlagen/anschreiben.dotx`, `./vorlagen/lebenslauf.dotx`
  — nur Layout/Struktur, werden erst beim Rendern (Stufe 6) gebraucht.
- **Stellenanzeige:** Trigger pro Lauf, als Argument übergeben
  (Dateipfad, URL oder direkt eingefügter Text).

## Output-Konvention
- Arbeitsverzeichnis pro Lauf: `./runs/<YYYY-MM-DD-HHMM>-<firma>/`
- Finale Dateien: `anschreiben_<firma>.docx` und `lebenslauf_<firma>.docx`
- `<firma>` wird kleingeschrieben, ohne Leer-/Sonderzeichen (z. B. `acme-gmbh`).

## Pipeline-Reihenfolge
1. **Analyse der Stellenanzeige** → `01_analyse.md`
   (Must-haves, Nice-to-haves, Keywords, Ton)
2. **Profilabgleich** → `02_abgleich.md`
   (Stärken & Lücken explizit)
3. **Lücken-Dialog (Human Input)** → `03_dialog.md`
   (sokratische Fragen; Antworten werden nach `profil/ergaenzungen.docx` zurückgeschrieben)
4. **Erstellung** → `04_entwurf.md`
   (Anschreiben + Lebenslauf-Inhalt, keyword-orientiert, wahrheitstreu)
5. **Qualitätsprüfung** → `05_qa.json`
   (durch separaten, isolierten Subagenten `qa-reviewer`)
6. **Output DOCX** → finale Dateien im Run-Verzeichnis
5b. **ATS-Check** → `05b_ats.json` + `ats_extrakt.txt`
   (ATS-Simulator; läuft **nach** Stufe 6, weil er die fertigen DOCX zurückliest;
   misst überprüfbar die Keyword-Abdeckung und meldet Parsing-Probleme)

## Kontrollfluss
- **Rücksprung-Schleife 5→4:** Fällt die QA durch (`bestanden: false`), geht es
  mit den QA-Findings zurück zu Stufe 4. Maximal **3 Iterationen**, danach Stop
  mit Bericht an den Menschen.
- **Wiederaufnahme:** Nach jeder Stufe wird der Zwischenstand als Datei im
  Run-Verzeichnis persistiert. Ein nach der Human-Wartezeit (Stufe 3 oder
  Freigabe) unterbrochener Lauf kann anhand der vorhandenen Dateien fortgesetzt werden.
- **Human-in-the-Loop:** Nach bestandener QA hält der Orchestrator an und legt die
  Entwürfe zur Prüfung/Freigabe/Änderung vor. Ohne ausdrückliche Freigabe läuft
  Stufe 6 nicht. Ein Quality-Gate-Hook erzwingt dies zusätzlich technisch.
- **ATS-Check (Stufe 5b, Warnung-und-Freigabe):** Nach dem Rendering prüft der
  ATS-Simulator die fertigen DOCX und misst die Keyword-Abdeckung. Dies ist **kein
  hartes Gate** – ein Score unter Schwelle oder Parsing-Warnungen führen zu einer
  deutlichen Warnung, die der Mensch bewusst übersteuern kann. ATS-Optimierung
  bedeutet ausschließlich, Wahres maschinenlesbar/relevant darzustellen, niemals
  Täuschung (kein versteckter Text, keine erfundenen Keywords).
