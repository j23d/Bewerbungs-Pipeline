# -*- coding: utf-8 -*-
"""Stufe 6: Rendert die Inhalte aus 04_entwurf.md in die DOCX-Vorlagen und
schreibt anschreiben_<firma>.docx und lebenslauf_<firma>.docx ins Run-Verzeichnis.

Das Parsen von 04_entwurf.md ist bewusst einfach gehalten und sollte bei Bedarf
an die konkrete Struktur des Entwurfs angepasst werden. Grundprinzip: Der Skill
'output-docx' baut das Kontext-Dict; dieses Skript ist die technische Render-Hilfe.

Aufruf:
  python .claude/scripts/render_docx.py \
    --entwurf runs/<lauf>/04_entwurf.md --firma acme --out runs/<lauf>
"""
import argparse
import os
import re
from docxtpl import DocxTemplate

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TPL_AN = os.path.join(ROOT, "vorlagen", "anschreiben.dotx")
TPL_LB = os.path.join(ROOT, "vorlagen", "lebenslauf.dotx")


def section(text, title):
    """Extrahiert den Inhalt einer Markdown-Ueberschrift bis zur naechsten gleicher/hoeherer Ebene."""
    m = re.search(rf"^#+\s*{re.escape(title)}\s*$(.*?)(?=^#+\s|\Z)",
                  text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--entwurf", required=True)
    p.add_argument("--firma", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    with open(args.entwurf, encoding="utf-8") as f:
        txt = f.read()

    anschreiben = section(txt, "Anschreiben")
    kurzprofil = section(txt, "Kurzprofil")
    erfahrung = [l.lstrip("- ").strip()
                 for l in section(txt, "Berufserfahrung").splitlines() if l.strip()]
    ausbildung = [l.lstrip("- ").strip()
                  for l in section(txt, "Ausbildung").splitlines() if l.strip()]
    skills = section(txt, "Skills")

    # --- Anschreiben rendern ---
    ctx_an = {
        "absender_name": "[Name aus Masterprofil]",
        "absender_kontakt": "[Kontakt aus Masterprofil]",
        "firma_name": args.firma,
        "firma_adresse": "[Adresse]",
        "ort": "[Ort]",
        "datum": "[Datum]",
        "betreff": "Bewerbung",
        "anrede": "Sehr geehrte Damen und Herren,",
        "anschreiben_text": anschreiben,
        "gruss": "Mit freundlichen Gruessen",
    }
    d_an = DocxTemplate(TPL_AN)
    d_an.render(ctx_an)
    out_an = os.path.join(args.out, f"anschreiben_{args.firma}.docx")
    d_an.save(out_an)

    # --- Lebenslauf rendern ---
    ctx_lb = {
        "name": "[Name aus Masterprofil]",
        "kontakt": "[Kontakt aus Masterprofil]",
        "kurzprofil": kurzprofil,
        "erfahrung": erfahrung,
        "ausbildung": ausbildung,
        "skills": skills,
    }
    d_lb = DocxTemplate(TPL_LB)
    d_lb.render(ctx_lb)
    out_lb = os.path.join(args.out, f"lebenslauf_{args.firma}.docx")
    d_lb.save(out_lb)

    print(f"Erstellt:\n  {out_an}\n  {out_lb}")


if __name__ == "__main__":
    main()
