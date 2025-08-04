# pipeline.py

# Usage:
#   python3 pipeline.py             → Dry-run: parse and display CSL JSON
#   python3 pipeline.py --commit   → Upload entry to Zotero




# bibnow v2 pipeline prototype
#
# This script loads CSL-JSON from `input.txt` and converts each entry to a Zotero-compatible
# JSON dictionary using the `csl_to_zotero()` function from `csl_mapper.py`.
#
# Initially designed to handle one or more entries stored in `input.txt`, this parser serves
# as the entry point for clipboard-based ingestion. Upload to Zotero will be added later.

import json
from csl_mapper import csl_to_zotero
from config import ZOTERO_USERNAME
from zotero_writer import send_to_zotero


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

        zotero_item = csl_to_zotero(csl_item)
        if "--commit" in sys.argv:
            status_code, response = send_to_zotero(zotero_item)
            if 200 <= status_code < 300:
                key = next(iter(response.get("success", {}).values()), None)
                if key:
                    print(f"✅ Upload successful. Zotero Key: {key}")
                    print(f"🔗 Zotero URL: https://www.zotero.org/users/{ZOTERO_USERNAME}/items/{key}")
                else:
                    print(f"⚠️ Upload succeeded but no key returned.\n{json.dumps(response, indent=2)}")
            else:
                print(f"❌ Upload failed. Status: {status_code}")
                print(json.dumps(response, indent=2))
        else:
            print("[DRY-RUN] No upload. Final mapped Zotero item:\n")
            print(json.dumps(zotero_item, indent=2))

