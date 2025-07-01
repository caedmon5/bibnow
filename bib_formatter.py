import os
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc.source.json import CiteProcJSON

# 🔽 Path to the folder where your CSL files live (relative to this script)
STYLE_DIR = os.path.join(os.path.dirname(__file__), "csl")


def render_bibliography(entry_csl_json, style_name="chicago-author-date"):
    """
    Renders a full formatted bibliography string for a CSL JSON item.
    :param entry_csl_json: A single-item CSL JSON dictionary (e.g. from BibTeX conversion).
    :param style_name: A CSL style string (default: chicago-author-date).
    :return: A formatted bibliography string.
    """
    style_path = os.path.join(STYLE_DIR, f"{style_name}.csl")
    style = CitationStylesStyle(style_path, validate=False)
    bib_source = CiteProcJSON([entry_csl_json])
    bibliography = CitationStylesBibliography(style, bib_source, formatter="text")

    bib_id = entry_csl_json.get("id")
    if not bib_id:
        raise ValueError("Missing 'id' in CSL JSON")

    citation = Citation([CitationItem(entry_csl_json.get("id"))])
    bibliography.register(citation)
    entries = list(bibliography.bibliography())
    return str(entries[0]) if entries else "⟨No bibliography entry generated⟩"


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
