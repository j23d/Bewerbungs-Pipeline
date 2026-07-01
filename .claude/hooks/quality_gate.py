# -*- coding: utf-8 -*-
"""Quality-Gate + Human-Freigabe Hook (PreToolUse).

Greift, bevor eine finale Bewerbungsdatei geschrieben wird:
  runs/**/anschreiben_*.docx  oder  runs/**/lebenslauf_*.docx

Prueft:
  1) Im selben Run-Verzeichnis existiert 05_qa.json mit "bestanden": true.
  2) Eine Freigabe des Menschen liegt vor (freigabe.txt im Run-Verzeichnis).

Andernfalls Exit-Code 2 -> harter Stop; die Begruendung geht an stderr.
Der Hook liest den Tool-Payload als JSON von stdin (Claude-Code-Konvention).
"""
import json
import os
import re
import sys


def fail(msg):
    sys.stderr.write("QUALITY-GATE BLOCKIERT: " + msg + "\n")
    sys.exit(2)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # Kein gueltiger Payload -> nicht blockieren (Hook ist tolerant).
        sys.exit(0)

    ti = payload.get("tool_input", {}) or {}
    path = ti.get("file_path") or ti.get("path") or ""
    norm = path.replace("\\", "/")

    # Nur finale Bewerbungsdateien unter runs/ betreffen.
    if not re.search(r"(^|/)runs/.+/(anschreiben|lebenslauf)_.+\.docx$", norm):
        sys.exit(0)

    run_dir = os.path.dirname(path)

    # 1) QA muss bestanden sein.
    qa = os.path.join(run_dir, "05_qa.json")
    if not os.path.exists(qa):
        fail(f"05_qa.json fehlt in {run_dir}. Stufe 5 (QA) muss zuerst laufen.")
    try:
        with open(qa, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        fail(f"05_qa.json nicht lesbar: {e}")
    if data.get("bestanden") is not True:
        fail("QA nicht bestanden (bestanden != true). Zurueck zu Stufe 4.")

    # 2) Human-Freigabe muss vorliegen.
    freigabe = os.path.join(run_dir, "freigabe.txt")
    if not os.path.exists(freigabe) or not open(freigabe, encoding="utf-8").read().strip():
        fail("Keine Freigabe. Lege freigabe.txt im Run-Verzeichnis mit der "
             "ausdruecklichen Bestaetigung des Menschen an (Human-in-the-Loop).")

    # Alles ok -> Schreiben erlauben.
    sys.exit(0)


if __name__ == "__main__":
    main()
