---
name: ats-check
description: Stufe 5b der Bewerbungs-Pipeline (ATS-Simulator). Liest die fertig gerenderten DOCX-Dateien eines Laufs zurück – wie ein Applicant Tracking System – und liefert eine ÜBERPRÜFBARE (gemessene, nicht geschätzte) Keyword-Abdeckung gegen die Must-haves sowie Parsing-Warnungen (Text in Tabellen/Kopfzeilen/Textboxen, fehlende Standard-Überschriften, Kontaktdaten nicht im Fließtext). Nutze diesen Skill nach dem DOCX-Rendering (Stufe 6), um zu prüfen, ob die Unterlagen die KI-Vorauswahl überstehen.
---

# Stufe 5b: ATS-Simulator (Warnung-und-Freigabe)

Ziel: die häufigste Hürde vor dem ersten Menschen bei HR überwinden – die
maschinelle Vorauswahl. Zwei Filter existieren: **Parsing** (Format, mechanisch)
und **Ranking** (semantische Relevanz). Diese Stufe adressiert vor allem Parsing
und misst die Keyword-Abdeckung überprüfbar.

**Wichtig – Kontrollfluss:** Dies ist ein **WARNUNG-UND-FREIGABE**-Schritt, **kein
hartes Gate**. Liegt der gemessene ATS-Score unter der Schwelle, wird deutlich
gewarnt – blockiert wird **nichts**. Der Mensch entscheidet bei der Freigabe.

**Rote Linie:** ATS-Optimierung heißt, Wahres maschinenlesbar und relevant
darzustellen – niemals täuschen (kein versteckter/weißer Text, keine erfundenen
Keywords). Das steht im Einklang mit der Wahrheitstreue-Regel in `CLAUDE.md`.

## Inputs
- `01_analyse.md` (Must-haves + Keywords des Laufs)
- die fertigen DOCX im Run-Verzeichnis (`anschreiben_<firma>.docx`,
  `lebenslauf_<firma>.docx`) – daher läuft diese Stufe **nach** Stufe 6.

## Ausführung
```bash
python .claude/scripts/ats_check.py \
  --analyse "<run>/01_analyse.md" \
  --run "<run>" \
  --schwelle 75
```

## Outputs (im Run-Verzeichnis)
- `05b_ats.json` – gemessener ATS-Score, Must-have-/Keyword-Abdeckung im Detail,
  Parsing-Warnungen, Liste der geprüften Dateien.
- `ats_extrakt.txt` – das, was ein ATS aus den Dateien „liest" (Fließtext-Zone +
  Risiko-Zone). Nützlich, um Parsing-Verluste mit eigenen Augen zu sehen.
- Exit-Code: `0` = über Schwelle, `3` = unter Schwelle (Signal, **nicht** blockierend).

## Umgang mit dem Ergebnis
1. **Score über Schwelle, keine Warnungen:** alles gut, weiter zur Freigabe.
2. **Parsing-Warnungen (Tabellen/Kopfzeilen/Textboxen, fehlende Überschriften,
   keine E-Mail im Fließtext):** Format in `vorlagen/` korrigieren (einspaltig,
   Standard-Überschriften, Kontakt im Fließtext), Stufe 6 neu rendern, erneut prüfen.
3. **Keyword-Lücken:** nur schließen, wenn belegbar (aus Masterprofil/Dialog).
   Fehlende, unbelegte Keywords bleiben offen – nicht erfinden. Ggf. Stufe 4
   nutzen, um belegtes Vokabular exakt an die Anzeige anzugleichen.
4. **Score unter Schwelle:** Warnung dem Menschen im Freigabe-Schritt vorlegen; er
   kann bewusst freigeben oder zu Stufe 4/6 zurückgehen.
```
