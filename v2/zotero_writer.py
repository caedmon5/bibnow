# zotero_writer.py

"""
Handles uploading CSL-JSON bibliographic entries to the Zotero web API.

Assumptions:
1. Input is a single clean and validated CSL-JSON dict.
2. API credentials are available in config.py.
3. This module focuses strictly on Zotero upload logic — field mapping from CSL to Zotero
   should be done in a separate utility (csl_mapper.py) for clarity and reuse.
"""

import requests
import json
from config import ZOTERO_API_KEY, ZOTERO_USER_ID, ZOTERO_GROUP_ID, LIBRARY_TYPE

# Choose correct API base (user vs group)
if LIBRARY_TYPE == "group":
    API_BASE = f"https://api.zotero.org/groups/{ZOTERO_GROUP_ID}"
else:
    API_BASE = f"https://api.zotero.org/users/{ZOTERO_USER_ID}"

# Define base URL for Zotero item upload
ZOTERO_BASE_URL = f"{API_BASE}/items"

def send_to_zotero(csl_item):
    """
    Send a zotero-mapped bibliographic item to Zotero via their API.

    Parameters:
        csl_item (dict): A CSL-JSON bibliographic entry.

    Returns:
        tuple: (status_code, response JSON or text)
    """
    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "Content-Type": "application/json"
    }

    # Wrap CSL item in array — Zotero expects an array of items
    payload = csl_item if isinstance(csl_item, list) else [csl_item]

#debug
#    print("[DEBUG] Final payload:\n", json.dumps(payload, indent=2))


    try:
        response = requests.post(ZOTERO_BASE_URL, headers=headers, json=payload)
    except requests.exceptions.RequestException as e:
        return 0, {"error": "Network or connection error", "exception": str(e)}

    # Attempt to parse response JSON or return raw text if malformed
    try:
        content = response.json()
    except json.JSONDecodeError:
        content = response.text

    return response.status_code, content

def create_fulltext_note(parent_key, fulltext, title_prefix="Full text (user provided via bibnow)"):
    """
    Create a Zotero child note containing user-provided full text.

    - parent_key: Zotero key of the parent bibliographic item.
    - fulltext: plain-text content supplied by the user (UTF-8).
    - title_prefix: optional label shown in the note title.

    Zotero notes are stored as simple HTML. Here we:
      - escape basic HTML-sensitive characters,
      - convert newlines to <br> to preserve paragraph breaks.
    """
    if not parent_key or not fulltext:
        return 0, {"error": "Missing parent_key or fulltext; note not created."}

    # Basic HTML escaping and newline handling
    def _html_escape(s: str) -> str:
        return (
            s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
        )

    escaped = _html_escape(str(fulltext))
    # Preserve line breaks
    escaped = escaped.replace("\r\n", "\n").replace("\r", "\n")
    note_html = "<p>" + escaped.replace("\n", "<br />\n") + "</p>"

    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "Content-Type": "application/json"
    }

    note_item = {
        "itemType": "note",
        "parentItem": parent_key,
        "note": note_html
    }

    payload = [note_item]

    try:
        response = requests.post(ZOTERO_BASE_URL, headers=headers, json=payload)
    except requests.exceptions.RequestException as e:
        return 0, {"error": "Network or connection error while creating note", "exception": str(e)}

    try:
        content = response.json()
    except json.JSONDecodeError:
        content = response.text

    return response.status_code, content



def validate_zotero_response(status_code, response_data):
    """
    Interpret a Zotero API response and determine success or failure.

    Parameters:
        status_code (int): HTTP status code.
        response_data (dict or str): Response body from Zotero.

    Returns:
        tuple: (bool success, str explanation, str zotero_key or None)
    """
    if 200 <= status_code < 300:
        if isinstance(response_data, dict) and "successful" in response_data:
            success_key = next(iter(response_data["successful"].values()), {})
            zotero_key = success_key.get("key", None)
            return True, "Upload successful", zotero_key
        return True, "Upload accepted", None

    # If not successful, extract error info
    explanation = "Unknown error"
    if isinstance(response_data, dict) and "message" in response_data:
        explanation = response_data["message"]
    elif isinstance(response_data, str):
        explanation = response_data

    return False, f"Upload failed: {explanation}", None
