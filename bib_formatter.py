
import os
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc.source.json import CiteProcJSON
import json

def render_bibliography(csl, style_name=None):
    from citeproc import CitationStylesBibliography, Citation, CitationItem
    from citeproc.source.json import CiteProcJSON
    style = CitationStylesStyle(style_name, validate=False)
    bib_source = CiteProcJSON([csl])
    bibliography = CitationStylesBibliography(style, bib_source, formatter="text")
    citation = Citation([CitationItem(csl["id"])])
    bibliography.register(citation)
    return [str(entry) for entry in bibliography.bibliography()]

def bib_to_csl(entry, citekey=None):
    """
    Convert a basic BibTeX dictionary to a CSL-compatible dictionary.
    Only supports 'author' for now.
    """
    def parse_name(name):
        parts = name.split(", ")
        if len(parts) == 2:
            family, given = parts
        else:
            given, family = name.split(" ", 1)
        return {"given": given.strip(), "family": family.strip()}

    csl = {
        "id": entry.get("ID", "ITEM-1"),
        "type": entry.get("ENTRYTYPE", "article"),
        "title": entry.get("title", ""),
        "issued": {"date-parts": [[int(entry.get("year", 0))]]},
    }

    if "author" in entry:
        raw = entry["author"]
        if isinstance(raw, str):
            names = [n.strip() for n in raw.split(" and ")]
            csl["author"] = [parse_name(n) for n in names]

    return csl

