# test_zotero_upload.py

"""
Test script for uploading a single CSL-JSON entry to Zotero.
Requires: test_csl_input.json, config.py, zotero_writer.py
"""

import json
from zotero_writer import send_to_zotero, validate_zotero_response
from csl_mapper import csl_to_zotero
from config import ZOTERO_USERNAME

# Load CSL-JSON test data from file
with open("test_csl_input.json", "r", encoding="utf-8") as f:
    csl_item = json.load(f)

# Convert to Zotero-compatible JSON
zotero_item = csl_to_zotero(csl_item)

# Attempt Zotero upload
status_code, response = send_to_zotero(zotero_item)

# Print raw result
print(f"\nStatus Code: {status_code}")
print("Raw Zotero Response:\n", json.dumps(response, indent=2) if isinstance(response, dict) else response)

# Parse Zotero API response
success = response.get("success", {})
failed = response.get("failed", {})
zotero_key = list(success.values())[0] if success else None

print(f"\nSuccess? {bool(success) and not failed}")
if success and not failed:
    print("Message: Upload successful")
    print(f"Zotero Key: {zotero_key}")
    print(f"Zotero URL: https://www.zotero.org/users/{ZOTERO_USERNAME}/items/{zotero_key}")
elif failed:
    failure = list(failed.values())[0]
    print("Message: Upload failed")
    print(f"Zotero Error: {failure.get('message', 'Unknown error')}")
else:
    print("Message: Upload status unclear")

