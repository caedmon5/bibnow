import requests
from config import ZOTERO_API_KEY, ZOTERO_USER_ID  # imported same as in biblio_pipeline

def test_zotero_formatted_citation(item_key, style="chicago-author-date"):
    headers = {"Accept": "text/html"}
    url = f"https://www.zotero.org/users/{ZOTERO_USER_ID}/items/{item_key}?format=bib&style={style}"
    r = requests.get(url, headers=headers)
    print(f"📡 Request URL: {url}")
    print(f"🔢 Status Code: {r.status_code}")
    print("📄 Response Text:\n")
    print(r.text.strip())

# 🔁 Replace this with a known working Zotero key from your library
test_zotero_formatted_citation("J323WCMY")
