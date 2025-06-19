import requests, json, os, re, time
from config import ZOTERO_API_KEY, ZOTERO_USER_ID, ZOTERO_USERNAME

# Dynamic base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OBSIDIAN_PATH = os.path.join(BASE_PATH, "output", "LN Literature Notes")
LOG_PATH = os.path.join(BASE_PATH, "output", "biblio-log")

# Ensure output directories exist
os.makedirs(OBSIDIAN_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)

def extract_blocks(text, start_marker, end_marker):
    pattern = rf"{start_marker}(.*?){end_marker}"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None

def parse_bibtex(bibtex):
    entry = {}
    lines = bibtex.splitlines()
    for line in lines:
        if '=' in line:
            k, v = line.split('=', 1)
            entry[k.strip()] = v.strip().strip('{}",')
    entry["ID"] = re.search(r'@\w+\{([^,]+),', bibtex).group(1)
    return entry

def zotero_upload(entry):
    headers = {'Zotero-API-Key': ZOTERO_API_KEY, 'Content-Type': 'application/json'}
    metadata = {
        "items": [{
            "itemType": "journalArticle",
            "title": entry.get("title", ""),
            "creators": [{"creatorType": "author", "name": entry.get("author", "Unknown")}],
            "publicationTitle": entry.get("journal", ""),
            "date": entry.get("date", ""),
            "url": entry.get("url", ""),
            "abstractNote": entry.get("abstract", ""),
            "tags": [{"tag": k.strip()} for k in entry.get("keywords", "").split(',')]
        }]
    }

    r = requests.post(
        f"https://api.zotero.org/users/{ZOTERO_USER_ID}/items",
        headers=headers,
        data=json.dumps(metadata)
    )

    try:
        return r.status_code, r.json()
    except requests.exceptions.JSONDecodeError:
        return r.status_code, {"error": "No JSON returned", "body": r.text}

def build_markdown(entry, zotero_key):
    zotero_url = f"https://www.zotero.org/{ZOTERO_USERNAME}/items/{zotero_key}"
    md = f"""---
citekey: "{entry.get('ID')}"
type: "article"
zotero_key: "{zotero_key}"
zotero_url: "{zotero_url}"
zotero_library_id: {ZOTERO_USER_ID}
autoupdate: true
---
# Chicago Author-Year  Bibliography
{entry.get('author', '')}. {entry.get('date', '')}. "{entry.get('title', '')}." *{entry.get('journal', '')}*. {entry.get('url', '')}

# Abstract  
{entry.get('abstract', 'TBD')}

# Keywords
{', '.join(f"[[{k.strip()}]]" for k in entry.get("keywords", "").split(','))}

# Notes  
TBD

# Related Files and URLs.  
{zotero_url}
"""
    return md

def save_file(content, filename, path):
    full_path = os.path.join(path, filename)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def log_run(data, citekey):
    ts = time.strftime("%Y%m%d-%H%M%S")
    log_filename = f"biblio_log_{citekey}_{ts}.json"
    save_file(json.dumps(data, indent=2), log_filename, LOG_PATH)

def main(text, commit=False):
    bibtex_raw = extract_blocks(text, "@bibtex", "@end")
    if not bibtex_raw:
        print("❌ Could not find @bibtex block.")
        return

    bib = parse_bibtex(bibtex_raw)
    citekey = bib.get("ID", "unknown")

    print(f"✅ Parsed citekey: {citekey}")
    if not commit:
        print("🟡 Dry-run mode. No Zotero upload or file write.")
        print(json.dumps(bib, indent=2))
    else:
        status, resp = zotero_upload(bib)
        if status == 201:
            zotero_item = resp['successful']['0']
            key = zotero_item['key']
            print(f"✅ Zotero upload successful (Key: {key})")
            md = build_markdown(bib, key)
            filename = f"{citekey}.md"
            save_file(md, filename, OBSIDIAN_PATH)
            print(f"✅ Markdown saved: {filename}")
            log_run({"bibtex": bib, "zotero_response": zotero_item}, citekey)
        else:
            print(f"❌ Zotero upload failed: {status}")
            print(json.dumps(resp, indent=2))

if __name__ == "__main__":
    with open("viking_sample.txt", encoding='utf-8') as f:
        input_text = f.read()
    main(input_text, commit=True)
