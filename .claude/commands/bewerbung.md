---
description: Startet die Bewerbungs-Pipeline für eine Stellenanzeige (Dateipfad, URL oder Text) und führt die Stufen 1–6 aus.
argument-hint: <Stellenanzeige = Dateipfad | URL | Text>
---

Aktiviere den Skill `bewerbung` (Orchestrator der Bewerbungs-Pipeline) und führe
ihn mit folgender Stellenanzeige aus:

$ARGUMENTS

Halte dich an `CLAUDE.md` (Wahrheitstreue-Regel, Deutsch). Lege das Run-Verzeichnis
an, arbeite die Stufen 1–6 der Reihe nach ab, persistiere nach jeder Stufe den
Zwischenstand, respektiere die QA-Rücksprung-Schleife (5→4, max. 3 Iterationen) und
halte für den Lücken-Dialog (Stufe 3) und die finale Freigabe (vor Stufe 6) an.
