# === BEGIN: bib_formatter.py ===

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
import json
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem, formatter
from citeproc.source.json import CiteProcJSON
import inflect
import xml.etree.ElementTree as ET
from tempfile import NamedTemporaryFile
p = inflect.engine()

# === CONFIG ===
CSL_DIR = os.path.join(os.path.dirname(__file__), "csl")
DEFAULT_STYLE = os.path.join(CSL_DIR, "chicago-author-date.csl")

# === FUNCTION: Convert BibTeX-like entry to CSL JSON format ===
def bib_to_csl(entry, citekey=None):
    bibtex_to_csl_type = {
        "article": "article-journal",
        "book": "book",
        "inbook": "chapter",
        "incollection": "chapter",
        "inproceedings": "paper-conference",
        "conference": "paper-conference",
        "thesis": "thesis",
        "phdthesis": "thesis",
        "mastersthesis": "thesis",
        "report": "report",
        "webpage": "webpage",
        "misc": "document",
        "manual": "book",
    }

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
        "type": bibtex_to_csl_type.get(entry.get("ENTRYTYPE", "article"), "document"),
        "title": entry.get("title", ""),
    }

    if entry["ENTRYTYPE"] in ["phdthesis", "mastersthesis", "thesis"]:
        csl["genre"] = "PhD thesis" if "phd" in entry["ENTRYTYPE"] else "Master's thesis"
        if "publisher" not in csl:
            csl["publisher"] = entry.get("school", entry.get("institution", ""))

    if "booktitle" in entry:
        csl["container-title"] = entry["booktitle"]

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

    # === Additional CSL field mappings ===

    if "pages" in entry:
        csl["page"] = entry["pages"]

    if "editor" in entry:
        from author_utils import parse_responsible_parties
        csl["editor"] = parse_responsible_parties({"editor": entry["editor"]})

    if "series" in entry:
        csl["collection-title"] = entry["series"]

    if "collection" in entry and "collection-title" not in csl:
        csl["collection-title"] = entry["collection"]

    if "number" in entry:
        csl["number"] = entry["number"]

    if "edition" in entry:
        try:
            edition_number = int(entry["edition"])
            csl["edition"] = p.ordinal(edition_number)
        except ValueError:
            csl["edition"] = entry["edition"]

    if "language" in entry:
        csl["language"] = entry["language"]

    if "callnumber" in entry:
        csl["callnumber"] = entry["callnumber"]

    if "abstract" in entry:
        csl["abstract"] = entry["abstract"]

    if "keywords" in entry:
        csl["keyword"] = entry["keywords"]

    if "booktitle" in entry:
        csl["event"] = entry["booktitle"]

    if "event" in entry and "event" not in csl:
        csl["event"] = entry["event"]

    if "address" in entry:
        csl["event-place"] = entry["address"]

    if "location" in entry and "event-place" not in csl:
        csl["event-place"] = entry["location"]

    if "urldate" in entry:
        csl["accessed"] = {"raw": entry["urldate"]}

    if "access-date" in entry and "accessed" not in csl:
        csl["accessed"] = {"raw": entry["access-date"]}

    # Fallback for issued if date is available
    if "issued" not in csl and "date" in entry:
        csl["issued"] = {"raw": entry["date"]}

    # === Remove unsupported fields for citeproc Reference ===
    # These are kept in entry for Markdown generation, but CSL engine will warn on them
    unsupported_fields = ["journal", "callnumber", "abstract", "keywords"]
    for field in unsupported_fields:
        csl.pop(field, None)


    return csl

# === FUNCTION: Render bibliography from CSL JSON using a CSL file ===
def render_bibliography(csl, style_name=None):
    original_style_path = style_name or DEFAULT_STYLE
    force_us_punctuation_styles = [
        "chicago-author-date",  # add more as needed
    ]

    # Extract basename of CSL file to determine style
    style_basename = os.path.splitext(os.path.basename(original_style_path))[0]

    # Patch CSL file if needed
    patched_style_path = original_style_path
    if style_basename in force_us_punctuation_styles:
        tree = ET.parse(original_style_path)
        root = tree.getroot()
        if not any(e.tag.endswith("style-options") for e in root):
            style_options = ET.Element("style-options")
            style_options.attrib["punctuation-in-quote"] = "true"
            root.insert(1, style_options)
            tmp = NamedTemporaryFile(delete=False, suffix=".csl", mode="w", encoding="utf-8")
            tree.write(tmp.name, encoding="unicode")
            patched_style_path = tmp.name

    style = CitationStylesStyle(patched_style_path, validate=False)
    source = CiteProcJSON([csl])
    bibliography = CitationStylesBibliography(style, source)
    citation = Citation([CitationItem(csl["id"])])
    bibliography.register(citation)
    entries = bibliography.bibliography()
    return str(entries[0]) if entries else ""
# === END: bib_formatter.py ===
