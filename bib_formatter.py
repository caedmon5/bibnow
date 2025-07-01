import os
import json
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc.source.json import CiteProcJSON
from author_utils import parse_responsible_parties
from lxml import etree


# 🔽 Path to the folder where your CSL files live (relative to this script)
STYLE_DIR = os.path.join(os.path.dirname(__file__), "csl")

def patch_csl_quotes(style):
    """
    Ensures that standard quote terms are present in CSL styles,
    preventing citeproc rendering errors.
    """
    root = style.root
# patch root terms
    if root.terms is None:
            root.terms = {}
    root.terms.setdefault("open-quote", {"long": "“", "short": "‘"}) # check if openquote is set; if not use provided values
    root.terms.setdefault("close-quote", {"long": "”", "short": "’"}) # ditto, except for close quote.

# Patch locale terms (used during rendering)
    for locale in root.locales:
        if not hasattr(locale, "terms") or locale.terms is None:
            locale.terms = []

        term_names = {t.get("name") for t in locale.terms if isinstance(t, dict)}
        if "open-quote" not in term_names:
            term_el = etree.Element("term")
            term_el.set("name", "open-quote")
            term_el.set("form", "long")
            term_el.text = "“"
            locale.terms.append(term_el)
        if "close-quote" not in term_names:
            term_el = etree.Element("term")
            term_el.set("name", "close-quote")
            term_el.set("form", "long")
            term_el.text = "”"
            locale.terms.append(term_el)

def render_bibliography(entry_csl_json, style_name="chicago-author-date"):
    """
    Renders a full formatted bibliography string for a CSL JSON item.
    :param entry_csl_json: A single-item CSL JSON dictionary (e.g. from BibTeX conversion).
    :param style_name: A CSL style string (default: chicago-author-date).
    :return: A formatted bibliography string.
    """
    style_path = os.path.join(STYLE_DIR, f"{style_name}.csl")
    style = CitationStylesStyle(style_path, validate=False)
    patch_csl_quotes(style)  # ← Add this line to ensure quote terms are present
    print(json.dumps(entry_csl_json, indent=2))
    bib_source = CiteProcJSON([entry_csl_json])
    bibliography = CitationStylesBibliography(style, bib_source, formatter="text")

    bib_id = entry_csl_json.get("id")
    if not bib_id:
        raise ValueError("Missing 'id' in CSL JSON")

    citation = Citation([CitationItem(entry_csl_json.get("id"))])
    bibliography.register(citation)
    entries = list(bibliography.bibliography())
    return str(entries[0]) if entries else "⟨No bibliography entry generated⟩"

def bib_to_csl(entry, citekey=None):
    """
    Converts a BibTeX-like entry into CSL-JSON format for citeproc.
    Adds fallbacks for required fields.
    """
    # Fallbacks for mandatory CSL fields
    if not entry.get("title"):
        entry["title"] = "Untitled"
    if not entry.get("container-title"):
        entry["container-title"] = ""
    if not entry.get("publisher"):
        entry["publisher"] = ""
    if not entry.get("issued") and entry.get("year"):
        try:
            entry["issued"] = {"date-parts": [[int(entry["year"])]]}
        except ValueError:
            entry["issued"] = {"date-parts": [[1900]]}

    return {
        "id": citekey or entry.get("ID", "missing-id"),
        "type": entry.get("ENTRYTYPE", "article-journal"),
        "title": entry["title"],
        "author": parse_responsible_parties(entry),
        "issued": entry.get("issued", {"date-parts": [[1900]]}),
        "container-title": entry.get("container-title", ""),
        "publisher": entry.get("publisher", ""),
        "DOI": entry.get("doi", ""),
    }


# Command-line test
if __name__ == "__main__":
    import json

    test_entry = {
        "id": "item1",
        "type": "book",
        "title": "Interfaces of the Archive",
        "editor": [
            {"family": "Lopez", "given": "Carmen"},
            {"family": "Wei", "given": "Yuxin"},
            {"family": "Kline", "given": "David"}
        ],
        "issued": {"date-parts": [[2022]]},
        "publisher": "Archivum Universalis"
    }

    print("Chicago Author-Date:")
    print(render_bibliography(test_entry, "chicago-author-date"))

    print("\nAPA:")
    print(render_bibliography(test_entry, "apa"))

    print("\nMLA:")
    print(render_bibliography(test_entry, "modern-language-association"))
