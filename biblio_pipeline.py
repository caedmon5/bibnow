import requests, json, os, re, time, bibtexparser
from config import (
    ZOTERO_API_KEY,
    ZOTERO_USER_ID,
    ZOTERO_USERNAME,
    OBSIDIAN_VAULT_PATH,
    ZOTERO_GROUP_ID,
    ZOTERO_GROUP_SLUG,
)
from bibtexparser.bparser import BibTexParser

def detect_platform():
    """
    Returns one of: 'windows', 'macos', 'ios', 'ipad', 'android-termux', 'android', 'linux', 'unknown'
    """
    import platform, os

    sysname = platform.system()
    machine = platform.machine()
    env_home = os.environ.get("HOME", "")

    if sysname == "Windows":
        return "windows"
    elif sysname == "Darwin":
        plat = platform.platform()
        if "iPhone" in plat:
            return "ios"
        if "iPad" in plat:
            return "ipad"
        return "macos"
    elif sysname == "Linux":
        if "com.termux" in env_home:
            return "android-termux"
        if "ANDROID_STORAGE" in os.environ:
            return "android"
        return "linux"
    else:
        return "unknown"


# Expanded BibTeX to Zotero type map
BIBTEX_TO_ZOTERO_TYPE = {
    "article": "journalArticle",
    "book": "book",
    "inbook": "bookSection",
    "incollection": "bookSection",
    "inproceedings": "conferencePaper",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "report",
    "report": "report",
    "manual": "document",
    "misc": "webpage",  # Catch-all fallback
    "unpublished": "manuscript",
    "online": "webpage",
    "webpage": "webpage",
    "dataset": "dataset",
    "thesis": "thesis",
    "proceedings": "conferencePaper",
    "booklet": "book",
    "lecture": "presentation",
    "presentation": "presentation",
    "film": "film",
    "broadcast": "tvBroadcast",
    "hearing": "hearing",
    "case": "case",
    "bill": "bill",
    "legal": "case",
    "document": "document",  # Explicit fallback
}

def load_bibtex_entries(bibtex_str):
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = False
    parser.interpolate_strings = True
    db = bibtexparser.loads(bibtex_str, parser=parser)
    return db.entries  # list of dicts

def extract_year(entry):
    date_str = entry.get("date", "")
    match = re.search(r'\b(\d{4})\b', date_str)
    if match:
        return match.group(1)
    year_str = entry.get("year", "")
    match = re.search(r'\b(\d{4})\b', year_str)
    if match:
        return match.group(1)
    return "XXXX"

def get_responsible_party(entry):
    for field in ["author", "editor", "court", "institution", "organization", "legislativebody", "director", "producer"]:
        value = entry.get(field)
        if value:
            return value
    return "Unknown"

def parse_responsible_party(entry):
    party = get_responsible_party(entry)
    party_list = [p.strip() for p in party.split(" and ")]
    first = party_list[0]

    if "," in first:
        lastname = first.split(",")[0].strip()
    else:
        lastname = first.split()[-1].strip()

    clean_lastname = re.sub(r"[^\w\s]", "", lastname).capitalize()

    return {
        "raw": party,
        "party_list": party_list,
        "first_lastname": clean_lastname,
        "multiple": len(party_list) > 1
    }


def generate_citekey(entry):
    info = parse_responsible_party(entry)
    lastname = info["first_lastname"]
    title = entry.get("title", "")
    year = extract_year(entry)

    # First four words of title
    title_words = re.findall(r'\b\w+\b', title)
    slug = ''.join(word.capitalize() for word in title_words[:4])

    return f"{lastname}{year}{slug}"

def generate_filename(entry):
    info = parse_responsible_party(entry)
    lastname = info["first_lastname"]
    if info["multiple"]:
        lastname += " et al"
    title = entry.get("title", "")
    year = extract_year(entry)

    title_words = re.findall(r'\b\w+\b', title)
    title_part = ' '.join(re.sub(r"[^\w\s]", "", w).capitalize() for w in title_words[:4])
    return f"LN {lastname} {year} {title_part}.md"


# Dynamic base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
if not OBSIDIAN_VAULT_PATH:
    raise ValueError("❌ OBSIDIAN_VAULT_PATH is not set in config.py — please set it to your local Obsidian vault path.")

OBSIDIAN_PATH = os.path.abspath(OBSIDIAN_VAULT_PATH)

platform_type = detect_platform()

if platform_type == "linux":
    import pyperclip
    input_text = pyperclip.paste()
    print("📋 Clipboard input (Linux) detected and loaded.")
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(input_text)

elif platform_type == "android-termux":
    import subprocess
    try:
        clipboard = subprocess.check_output(["termux-clipboard-get"]).decode("utf-8")
        print("📋 Android clipboard detected via termux-clipboard-get.")
        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(clipboard)
        print("📋 Clipboard input (Android/Termux) saved to input.txt.")
        input_text = clipboard
    except Exception as e:
        print(f"❌ Failed to read clipboard: {e}")
        exit(1)

else:
    with open("input.txt", encoding="utf-8") as f:
        input_text = f.read()
    print("📄 Loaded input from file.")

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
    entry["ENTRYTYPE"] = re.search(r'@(\w+)\{', bibtex).group(1).lower()
    lines = bibtex.splitlines()
    for line in lines:
        if '=' in line:
            k, v = line.split('=', 1)
            entry[k.strip()] = v.strip().strip('{}",')
            entry_type_match = re.search(r'@(\w+)\{([^,]+),', bibtex)
            entry["ENTRYTYPE"] = entry_type_match.group(1).lower() if entry_type_match else "misc"
            entry["ID"] = entry_type_match.group(2) if entry_type_match else "unknown"
# Normalize institution to school for Zotero compatibility
    if entry["ENTRYTYPE"] in ["phdthesis", "mastersthesis"]:
        entry["school"] = entry.get("school", "") or entry.get("institution", "")
    return entry

def fetch_formatted_citation_from_group(group_id, item_key, style="chicago-author-date", retries=3, delay=1.5):
    import time
    from html import unescape
    import re

    headers = {"Accept": "text/html"}
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}?format=bib&style={style}"

    for attempt in range(retries):
        r = requests.get(url, headers=headers)
        body = r.text.strip()

        # Step 1: detect fallback HTML
        if "<html" in body.lower():
            print(f"⏳ CSL citation not ready (attempt {attempt + 1}), retrying in {delay}s...")
            time.sleep(delay)
            continue

        # Step 2: try to extract formatted citation
        if r.status_code == 200:
            match = re.search(r'<div class="csl-entry">(.*?)</div>', body, re.DOTALL)
            if match:
                return unescape(match.group(1).strip())
            return unescape(body)

        elif r.status_code == 404:
            if attempt < retries - 1:
                print(f"⏳ Citation not yet available from group (attempt {attempt + 1}), retrying in {delay}s...")
                time.sleep(delay)
        else:
            print(f"⚠️ Group citation fetch failed with status: {r.status_code}")
            return None

    print("⚠️ Group citation not available after retries.")
    return None


def generate_citation(entry, mode="minimal", zotero_key=None, zotero_group_key=None):
    if mode == "zotero":
        citation = None
        if zotero_group_key:
            citation = fetch_formatted_citation_from_group(ZOTERO_GROUP_ID, zotero_group_key)
        elif zotero_key:
            citation = fetch_formatted_citation(ZOTERO_USER_ID, zotero_key)
        if citation:
            return citation
        else:
            print("⚠️ No formatted citation returned — falling back to minimal style.")

    if mode == "citeproc":
        return f"{get_responsible_party(entry)} ({extract_year(entry)}). *{entry.get('title', '')}*"
    return f"{get_responsible_party(entry)} ({extract_year(entry)}). {entry.get('title', '')}"



def zotero_upload(entry):
    headers = {'Zotero-API-Key': ZOTERO_API_KEY, 'Content-Type': 'application/json'}
    item_type = BIBTEX_TO_ZOTERO_TYPE.get(entry.get("ENTRYTYPE", "misc"), "document")
    creators = [{"creatorType": "author", "name": entry.get("author", "")}]

    metadata = [{
        "itemType": item_type,
        "title": entry.get("title", ""),
        "creators": creators,
        "date": entry.get("date", entry.get("year", "")),
        # "year": extract_year(entry),
        "url": entry.get("url", ""),
        "abstractNote": entry.get("abstract", ""),
        "extra": entry.get("note", ""),
        "tags": [{"tag": k.strip()} for k in entry.get("keywords", "").split(",") if k.strip()],
        "publicationTitle": entry.get("journal", ""),
        "volume": entry.get("volume", ""),
        "issue": entry.get("number", entry.get("issue", "")),
        "pages": entry.get("pages", ""),
        "publisher": entry.get("publisher", ""),
        "DOI": entry.get("doi", entry.get("DOI", "")),
        "reportType": entry.get("type", "") if item_type == "report" else "",
        "thesisType": "PhD Thesis" if entry.get("ENTRYTYPE") == "phdthesis" else (
            "Master's Thesis" if entry.get("ENTRYTYPE") == "mastersthesis" else ""
        ),
        "institution": entry.get("institution", "") if item_type == "report" else "",
        "university": entry.get("school", "") if item_type == "thesis" else "",
        "court": entry.get("court", "") if item_type == "case" else "",
        "reporter": entry.get("reporter", "") if item_type == "case" else "",
        "committee": entry.get("committee", "") if item_type == "hearing" else "",
        "billNumber": entry.get("billnumber", "") if item_type == "bill" else "",
        "session": entry.get("session", "") if item_type == "bill" else "",
        "legislativeBody": entry.get("legislativebody", "") if item_type == "bill" else ""
}]

    # Additional fields for custom types
    item_type = BIBTEX_TO_ZOTERO_TYPE.get(entry.get("ENTRYTYPE", "misc"), "document")
    metadata[0]["itemType"] = item_type

    if item_type == "case":
        metadata[0]["reporter"] = entry.get("reporter", "")
        metadata[0]["court"] = entry.get("court", "")
    elif item_type == "hearing":
        metadata[0]["institution"] = entry.get("institution", "")
        metadata[0]["committee"] = entry.get("committee", "")
    elif item_type == "bill":
        metadata[0]["billNumber"] = entry.get("billnumber", "")
        metadata[0]["session"] = entry.get("session", "")
        metadata[0]["legislativeBody"] = entry.get("legislativebody", "")



    r = requests.post(
        f"https://api.zotero.org/users/{ZOTERO_USER_ID}/items",
        headers=headers,
        data=json.dumps(metadata)
    )

    try:
        return r.status_code, r.json()
    except requests.exceptions.JSONDecodeError:
        return r.status_code, {"error": "No JSON returned", "body": r.text}

def zotero_upload_to_group(entry):
    headers = {'Zotero-API-Key': ZOTERO_API_KEY, 'Content-Type': 'application/json'}
    item_type = BIBTEX_TO_ZOTERO_TYPE.get(entry.get("ENTRYTYPE", "misc"), "document")
    creators = [{"creatorType": "author", "name": entry.get("author", "")}]

    metadata = [{
        "itemType": item_type,
        "title": entry.get("title", ""),
        "creators": creators,
        "date": entry.get("date", entry.get("year", "")),
        "url": entry.get("url", ""),
        "abstractNote": entry.get("abstract", ""),
        "extra": entry.get("note", ""),
        "tags": [{"tag": k.strip()} for k in entry.get("keywords", "").split(",") if k.strip()],
        "publicationTitle": entry.get("journal", ""),
        "volume": entry.get("volume", ""),
        "issue": entry.get("number", entry.get("issue", "")),
        "pages": entry.get("pages", ""),
        "publisher": entry.get("publisher", ""),
        "DOI": entry.get("doi", entry.get("DOI", "")),
        "reportType": entry.get("type", "") if item_type == "report" else "",
        "thesisType": "PhD Thesis" if entry.get("ENTRYTYPE") == "phdthesis" else (
            "Master's Thesis" if entry.get("ENTRYTYPE") == "mastersthesis" else ""
        ),
        "institution": entry.get("institution", "") if item_type == "report" else "",
        "university": entry.get("school", "") if item_type == "thesis" else "",
        "court": entry.get("court", "") if item_type == "case" else "",
        "reporter": entry.get("reporter", "") if item_type == "case" else "",
        "committee": entry.get("committee", "") if item_type == "hearing" else "",
        "billNumber": entry.get("billnumber", "") if item_type == "bill" else "",
        "session": entry.get("session", "") if item_type == "bill" else "",
        "legislativeBody": entry.get("legislativebody", "") if item_type == "bill" else ""
    }]

    r = requests.post(
        f"https://api.zotero.org/groups/{ZOTERO_GROUP_ID}/items",
        headers=headers,
        data=json.dumps(metadata)
    )

    try:
        return r.status_code, r.json()
    except requests.exceptions.JSONDecodeError:
        return r.status_code, {"error": "No JSON returned", "body": r.text}


def fetch_formatted_citation_from_group(group_id, item_key, style="chicago-author-date", retries=3, delay=1.5):
    import time
    headers = {"Accept": "text/html"}
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}?format=bib&style={style}"

    for attempt in range(retries):
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text.strip()
        elif r.status_code == 404:
            if attempt < retries - 1:
                print(f"⏳ Citation not yet available from group (attempt {attempt + 1}), retrying in {delay}s...")
                time.sleep(delay)
        else:
            print(f"⚠️ Group citation fetch failed with status: {r.status_code}")
            return None
    print("⚠️ Group citation not available after retries.")
    return None


def zotero_delete_group_item(group_id, item_key, version=None):
    headers = {'Zotero-API-Key': ZOTERO_API_KEY}
    if version:
            headers['If-Unmodified-Since-Version'] = str(version)
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}"
    r = requests.delete(url, headers=headers)
    if r.status_code == 204:
        print(f"🗑️ Deleted group item: {item_key}")
    else:
        print(f"⚠️ Failed to delete group item {item_key}: {r.status_code}")

def build_markdown(entry, citekey=None, zotero_key=None, citation_mode="minimal", zotero_group_key=None, formatted_citation=None):
    zotero_url = f"https://www.zotero.org/{ZOTERO_USERNAME}/items/{zotero_key}" if zotero_key else ""
    info = parse_responsible_party(entry)
    lastname_readable = f"{info['first_lastname']} et al" if info["multiple"] else info["first_lastname"]
    year = extract_year(entry)
    title_words = re.findall(r'\b\w+\b', entry.get("title", ""))
    slug = " ".join(re.sub(r"[^\w\s]", "", word).capitalize() for word in title_words[:4])
    aliases = f'"{lastname_readable} {year} {slug}","{lastname_readable} {year}", "{citekey}"'
    callnumber = f"{entry.get('callnumber', '')}"

    md = f"""---
citekey: "{citekey or entry.get('ID', 'UNKNOWN')}"
aliases: [{aliases}]
type: "{entry.get('ENTRYTYPE', 'article')}"
zotero_key: "{zotero_key or ''}"
zotero_url: "{zotero_url}"
zotero_library_id: {ZOTERO_USER_ID}
responsible: "{get_responsible_party(entry)}"
title: "{entry.get('title', '')}"
year: "{extract_year(entry)}"
callnumber: "{callnumber}"
autoupdate: true
---
# Supplied Content <span title="This section is supplied by Zotero and should not be edited here. It contains bibliographic information about the item and should be edited, if necessary, in Zotero as edits made here are not synced back to Zotero and will be overwritten durimg updates.">ⓘ</span>

## Chicago Author-Year Bibliography
{formatted_citation or generate_citation(entry, citation_mode, zotero_key, zotero_group_key)}

## Abstract <span title="This field stores a supplied abstract and should not be edited here. User-supplied notes and summaries should go in a separate section below the edit line.">ⓘ</span>
{entry.get('abstract', 'None supplied')}

## Keywords <span title="This field stores supplied keywords and should not be edited here. User-supplied keywords should go in a separate section below the edit line.">ⓘ</span>
{', '.join(f"[[{k.strip()}]]" for k in entry.get("keywords", "").split(','))}
## Bibliographic Note <span title="This field stores Zotero's 'extra' field and is intended for supplied bibliographic metadata. Do not edit unless syncing manually. User notes go below.">ⓘ</span>
{entry.get('note', 'None supllied.')}

## Related Files and URLs. <span title="This field stores supplied URLs and files and should not be edited here. User-supplied URLS or files should go in a separate section below the edit line.">ⓘ</span>
{zotero_url}

---

<!-- Do not edit above this line: all changes should be made in Zotero -->

# User-generated Content <span title="This section is for Obsidian-focussed notes. it is preserved during updates. The headers and sections are freeform and can be adapted or added as needed.">ⓘ</span>

## User Notes <span title="This field is for user-supplied content that belongs closely to the record as a whole but does not need to be added to the canonical record in Zotero. Notes on specific topics or content within the content(e.g. quotstions, observations and thoughts)  should be created as separate unique notes and linked here.">ⓘ</span>



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

def main(text, commit=False, citation_mode="minimal"):
    group_items_to_delete = []
    if "@bibtex" in text and "@end" in text:
        bibtex_raw = extract_blocks(text, "@bibtex", "@end")
    else:
        print("🔎 No @bibtex block markers found — assuming entire input is raw BibTeX.")
        bibtex_raw = text.strip()

    if not bibtex_raw.startswith("@"):
        print("❌ Input does not appear to be valid BibTeX.")
        return

    # Optional: warn if markdown block is still present (legacy input)
    if "@markdown" in text:
        print("⚠️ Detected @markdown block — ignored. Markdown is now built from Zotero.")

    # Find all BibTeX blocks in the input (supporting multiple)
    entries = load_bibtex_entries(bibtex_raw)

    if not entries:
        print("❌ No BibTeX entries found.")
        return

    for bib in entries:
        citekey = generate_citekey(bib)
        print(f"\n✅ Parsed citekey: {citekey}")
## Dry-run block
        if not commit:
            zotero_key = None
            group_key = None
            formatted_citation = None
            print("🟡 Dry-run mode. No Zotero upload or file write.")
            print(json.dumps(bib, indent=2))
            filename = generate_filename(bib)
            print(f"\n📄 Would write file: {filename}")
            print("📦 Markdown preview:\n")
            if citation_mode == "zotero":
                md = build_markdown(
                    bib,
                    citekey=citekey,
                    zotero_key=zotero_key,
                    citation_mode=citation_mode,
                    zotero_group_key=group_key,
                    formatted_citation=formatted_citation
                )
            else:
                md = build_markdown(
                    bib,
                    citekey=citekey,
                    zotero_key=zotero_key,
                    citation_mode=citation_mode
                )
            print(md)
## the commit block
        else:
            status, resp = zotero_upload(bib)
            if status in [200, 201] and 'successful' in resp and '0' in resp['successful']:
                zotero_item = resp['successful']['0']
                key = zotero_item['key']
                time.sleep(1.5)  # Wait before first attempt (helps with API propagation)

                # Upload to public group for citation
                group_status, group_resp = zotero_upload_to_group(bib)
                if group_status in [200, 201] and 'successful' in group_resp and '0' in group_resp['successful']:
                    group_item = group_resp['successful']['0']
                    group_key = group_item['key']
                    group_version = group_item['version']
                    group_items_to_delete.append((group_key, group_version))
                    print(f"🌐 Group upload successful (Key: {group_key})")

                    time.sleep(1.5)
                    formatted_citation = fetch_formatted_citation_from_group(ZOTERO_GROUP_ID, group_key)
                else:
                    print(f"⚠️ Group upload failed — using fallback citation.")
                    formatted_citation = generate_citation(bib, mode="minimal")

                md = build_markdown(
                    bib,
                    citekey=citekey,
                    zotero_key=key,
                    citation_mode=citation_mode,
                    zotero_group_key=group_key,
                    formatted_citation=formatted_citation
                )
                print(f"✅ Zotero upload successful (Key: {key})")
                year = extract_year(bib)

                citekey = generate_citekey(bib)

                filename = generate_filename(bib)
                save_file(md, filename, OBSIDIAN_PATH)
                print(f"✅ Markdown saved: {filename}")
                log_run({"bibtex": bib, "zotero_response": zotero_item}, citekey)
            else:
                print(f"❌ Zotero upload failed: {status}")
                print(json.dumps(resp, indent=2))

    if commit and group_items_to_delete:
        print(f"🧹 Cleaning up {len(group_items_to_delete)} group item(s)...")
        for gkey, version in group_items_to_delete:
            zotero_delete_group_item(ZOTERO_GROUP_ID, gkey, version)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true", help="Actually upload to Zotero and write files")
    parser.add_argument("--zotero", action="store_true", help="Use Zotero CSL citation formatting")
    parser.add_argument("--citeproc", action="store_true", help="Use local citeproc-py formatting (WIP)")
    parser.add_argument("--minimal", action="store_true", help="Use minimal fallback citation formatting")
    args = parser.parse_args()

    if args.zotero:
        citation_mode = "zotero"
    elif args.citeproc:
        citation_mode = "citeproc"
    elif args.minimal:
        citation_mode = "minimal"
    else:
        citation_mode = "minimal"
    print(f"🧾 Citation mode set to: {citation_mode}")


    import platform

    if platform.system() == "Linux" and not os.environ.get("PREFIX"):
        import pyperclip
        input_text = pyperclip.paste()
        print("📋 Clipboard input (Linux) detected and loaded.")
        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(input_text)
    elif os.environ.get("PREFIX"):  # Android Termux
        import subprocess
        try:
            clipboard = subprocess.check_output(["termux-clipboard-get"]).decode("utf-8")
            print("📋 Android clipboard detected via termux-clipboard-get.")
            with open("input.txt", "w", encoding="utf-8") as f:
                f.write(clipboard)
            print("📋 Clipboard input (Android/Termux) saved to input.txt.")
            input_text = clipboard
        except Exception as e:
            print(f"❌ Failed to read clipboard: {e}")
            exit(1)
    else:
        with open("input.txt", encoding="utf-8") as f:
            input_text = f.read()
        print("📄 Loaded input from file.")

    print(f"🚦 Running in {'COMMIT' if args.commit else 'DRY-RUN'} mode.")
    main(input_text, commit=args.commit)


