# test_zotero_upload.py

"""
Test script for uploading a single CSL-JSON entry to Zotero.
Requires: test_csl_input.json, config.py, zotero_writer.py
"""

import json
from zotero_writer import send_to_zotero, validate_zotero_response

from csl_mapper import csl_to_zotero

# Load CSL-JSON test data from file
with open("test_csl_input.json", "r", encoding="utf-8") as f:
    csl_item = json.load(f)

# Load CSL-JSON test data from file
zotero_item = csl_to_zotero(csl_item)

# Attempt Zotero upload
status_code, response = send_to_zotero(csl_item)

# Print raw result
print(f"\nStatus Code: {status_code}")
print("Raw Zotero Response:\n", json.dumps(response, indent=2) if isinstance(response, dict) else response)

# Interpret and summarize result
success, message, zotero_key = validate_zotero_response(status_code, response)
print(f"\nSuccess? {success}")
print(f"Message: {message}")
print(f"Zotero Key: {zotero_key}")
if zotero_key:
    print(f"Zotero URL: https://www.zotero.org/users/{ZOTERO_USER_ID}/items/{zotero_key}")
