
import os
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc.source.json import CiteProcJSON
import json

def render_bibliography(csl_path, bib_entries):
    with open(csl_path, 'r', encoding='utf-8') as f:
        style = CitationStylesStyle(f, validate=False)
    bib_source = CiteProcJSON(bib_entries)
    bibliography = CitationStylesBibliography(style, bib_source, formatter='text')
    citation = Citation([CitationItem(bib_entries[0]['id'])])
    bibliography.register(citation)
    return list(bibliography.bibliography())
