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
from clipboard_loader import load_clipboard_or_file
from obsidian_writer import build_markdown_from_zotero, generate_filename, generate_citekey, write_obsidian_note
import sys

def _extract_first_key(response: dict):
    """
    Return the first successful item's key from a Zotero write response, or None.
    Response format: {"successful": {"0": { "key": "...", ...}, ...}, ...}
    """
    if not isinstance(response, dict):
        return None
    successful = response.get("successful", {})
    if not isinstance(successful, dict) or not successful:
        return None
    first = next(iter(successful.values()))
    return first.get("key")

def _extract_all_keys(response: dict):
    """
    Return a list of all successful item keys from a Zotero write response.
    """
    if not isinstance(response, dict):
        return []
    successful = response.get("successful", {})
    if not isinstance(successful, dict) or not successful:
        return []
    return [v.get("key") for v in successful.values() if isinstance(v, dict) and v.get("key")]



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
    input_text = load_clipboard_or_file("input.txt")
    t = (input_text or "").lstrip()
    if not (t.startswith("{") or t.startswith("[")):
        raise ValueError("Input is not JSON. v2 expects CSL JSON. If you have BibTeX, switch back to v1 or refactor the input as CSL.")
    data = json.loads(input_text)
    items = [data] if isinstance(data, dict) else data

    for csl_item in items:
        zotero_item = csl_to_zotero(csl_item)
        # Generate markdown and filename
        citekey = generate_citekey(zotero_item)
        filename = generate_filename(zotero_item)

        if "--commit" in sys.argv:
            status_code, response = send_to_zotero(zotero_item)
            if 200 <= status_code < 300:
                successful = response.get("successful", {})
                zotero_key = None
                if successful:
                    first_item = next(iter(successful.values()))
                    zotero_key = first_item.get("key")

                if zotero_key:
                    print(f"✅ Upload successful. Zotero Key: {zotero_key}")
                    print(f"🔗 Zotero URL: https://www.zotero.org/users/{ZOTERO_USERNAME}/items/{zotero_key}")
                else:
                    print(f"⚠️ Upload succeeded but no key returned.\n{json.dumps(response, indent=2)}")
            else:
                print(f"❌ Upload failed. Status: {status_code}")
                print(json.dumps(response, indent=2))
            # ✅ Markdown generation after upload (using zotero_key if present)
            markdown = build_markdown_from_zotero(zotero_item, citekey, zotero_key)

            write_obsidian_note(markdown, filename)
            print(f"📄 Markdown written to: {filename}")

        else:
            # Dry-run mode
            markdown = build_markdown_from_zotero(zotero_item, citekey)
            print("[DRY-RUN] No upload. Final mapped Zotero item:\n")
            print(json.dumps(zotero_item, indent=2))
            print(f"\n📄 Would write: {filename}")
            print(markdown)
