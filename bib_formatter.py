# === BEGIN: bib_formatter.py ===

import os
import json
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem, formatter
from citeproc.source.json import CiteProcJSON

# === CONFIG ===
CSL_DIR = os.path.join(os.path.dirname(__file__), "csl")
DEFAULT_STYLE = os.path.join(CSL_DIR, "chicago-author-date.csl")

# === FUNCTION: Convert BibTeX-like entry to CSL JSON format ===
def bib_to_csl(entry, citekey=None):
    def parse_name(name):
        if ',' in name:
            family, given = [x.strip() for x in name.split(",", 1)]
        else:
            parts = name.strip().split(" ", 1)
            if len(parts) == 2:
                given, family = parts
            else:
                given = parts[0]
                family = ""
        return {"given": given, "family": family}

    csl = {
        "id": citekey or entry.get("ID", "ITEM-1"),
        "type": entry.get("ENTRYTYPE", "article"),
        "title": entry.get("title", ""),
    }

    if "year" in entry:
        try:
            csl["issued"] = {"date-parts": [[int(entry["year"])] ]}
        except ValueError:
            pass

    if "author" in entry:
        raw = entry["author"]
        if isinstance(raw, str):
            names = [n.strip() for n in raw.split(" and ")]
            csl["author"] = [parse_name(n) for n in names]

    for field in ["container-title", "journal", "volume", "issue", "publisher", "URL", "DOI", "note"]:
        if field in entry:
            csl[field] = entry[field]
        elif field == "container-title" and "journal" in entry:
            csl["container-title"] = entry["journal"]

    return csl

# === FUNCTION: Render bibliography from CSL JSON using a CSL file ===
def render_bibliography(csl, style_name=None):
    style_path = style_name or DEFAULT_STYLE
    style = CitationStylesStyle(style_path, validate=False)
    source = CiteProcJSON([csl])
    bibliography = CitationStylesBibliography(style, source, formatter.plain)
    citation = Citation([CitationItem(csl["id"])])
    bibliography.register(citation)
    return [str(entry) for entry in bibliography.bibliography()]
# === END: bib_formatter.py ===