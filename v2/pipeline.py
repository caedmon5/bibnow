# pipeline.py
# bibnow v2 pipeline prototype
#
# This script loads CSL-JSON from `input.txt` and converts each entry to a Zotero-compatible
# JSON dictionary using the `csl_to_zotero()` function from `csl_mapper.py`.
#
# Initially designed to handle one or more entries stored in `input.txt`, this parser serves
# as the entry point for clipboard-based ingestion. Upload to Zotero will be added later.

import json
from csl_mapper import csl_to_zotero

def load_csl_items_from_input_file(filepath="input.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept both a single dict and a list of dicts
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Input file must contain a JSON object or a list of objects.")


if __name__ == "__main__":
    items = load_csl_items_from_input_file("input.txt")

    for csl_item in items:
        zotero_item = csl_to_zotero(csl_item)
        print(json.dumps(zotero_item, indent=2))
