import requests
from config import ZOTERO_API_KEY, ZOTERO_USERNAME, ZOTERO_USER_ID, ZOTERO_GROUP_ID

# === SETTINGS ===
GROUP_ID = ZOTERO_GROUP_ID
ITEM_KEY = "35IXIHJC"
STYLE = "chicago-author-date"

def fetch_formatted_citation(group_id, item_key, style="chicago-author-date"):
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}?format=bib&style={style}"
    headers = {"Accept": "text/html"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print("✅ Citation fetched:\n")
        print(r.text.strip())
        return True
    else:
        print(f"❌ Failed to fetch citation. Status: {r.status_code}")
        return False

def fetch_item_version(group_id, item_key):
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}"
    headers = {"Zotero-API-Key": ZOTERO_API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        version = r.json().get("version")
        print(f"✅ Item version fetched: {version}")
        return version
    else:
        print(f"❌ Failed to fetch item version: {r.status_code}")
        return None

def delete_item(group_id, item_key, version):
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}"
    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "If-Unmodified-Since-Version": str(version)
    }
    r = requests.delete(url, headers=headers)
    if r.status_code == 204:
        print(f"🗑️ Item {item_key} successfully deleted.")
    else:
        print(f"❌ Deletion failed: {r.status_code} — {r.text}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("📚 Testing Zotero citation and delete sequence via group...\n")
    success = fetch_formatted_citation(GROUP_ID, ITEM_KEY, STYLE)
    if success:
        version = fetch_item_version(GROUP_ID, ITEM_KEY)
        if version:
            delete_item(GROUP_ID, ITEM_KEY, version)
