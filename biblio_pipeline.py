import requests, json, os, re, time
from config import ZOTERO_API_KEY, ZOTERO_USER_ID, ZOTERO_USERNAME

def generate_citekey(author, date_str, title):
    # Extract last name from author field
    lastname = re.sub(r'[^A-Za-z]', '', author.split()[-1])

    # Get year (YYYY) from date
    year_match = re.search(r'\d{4}', date_str)
    year = year_match.group(0) if year_match else "XXXX"

    # First three words of title
    title_words = re.findall(r'\b\w+\b', title)
    slug = ''.join(word.capitalize() for word in title_words[:3])

    return f"{lastname}{year}{slug}"

def generate_filename(author, date_str, title):
    # Split author into capitalized parts
    name_parts = [w.capitalize() for w in author.replace('-', ' ').split()]
    lastname_parts = name_parts[-2:] if len(name_parts) >= 2 else name_parts[-1:]

    # Extract year
    year_match = re.search(r'\d{4}', date_str)
    year = year_match.group(0) if year_match else "XXXX"

    # Title-cased first 3 words
    title_words = re.findall(r'\b\w+\b', title)
    title_part = ' '.join(w.capitalize() for w in title_words[:3])

    return f"LN {' '.join(lastname_parts)} {year} {title_part}.md"


# Dynamic base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
import platform

if "ANDROID_STORAGE" in os.environ or platform.system() == "Linux" and "com.termux" in os.environ.get("HOME", ""):
    # Android (e.g. Termux or Pydroid)
    OBSIDIAN_PATH = "/sdcard/Documents/Obsidian/LN Literature Notes"
else:
    # Default to Linux desktop
    OBSIDIAN_PATH = "/home/dan/wealtheow/LN Literature Notes"

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
    metadata = [{
        "itemType": "journalArticle",
        "title": entry.get("title", ""),
        "creators": [{"creatorType": "author", "name": entry.get("author", "Unknown")}],
        "publicationTitle": entry.get("journal", ""),
        "date": entry.get("date", ""),
        "url": entry.get("url", ""),
        "abstractNote": entry.get("abstract", ""),
        "extra": entry.get("note", ""),
        "tags": [{"tag": k.strip()} for k in entry.get("keywords", "").split(',')]
}]

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
{entry.get('note', 'TBD')}

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
entries = re.findall(r'@\w+\{[^@]+\}', bibtex_raw, re.DOTALL)

if not entries:
    print("❌ No BibTeX entries found.")
    return

for bibtext in entries:
    bib = parse_bibtex(bibtext)
    citekey = generate_citekey(
        author=bib.get("author", "Unknown"),
        date_str=bib.get("date", ""),
        title=bib.get("title", "")
    )
    print(f"\n✅ Parsed citekey: {citekey}")
    if not commit:
        print("🟡 Dry-run mode. No Zotero upload or file write.")
        print(json.dumps(bib, indent=2))
    else:
        status, resp = zotero_upload(bib)
        if status in [200, 201]:
            zotero_item = resp['successful']['0']
            key = zotero_item['key']
            print(f"✅ Zotero upload successful (Key: {key})")
            md = build_markdown(bib, key)
            filename = generate_filename(
                author=bib.get("author", "Unknown"),
                date_str=bib.get("date", ""),
                title=bib.get("title", "")
            )
            save_file(md, filename, OBSIDIAN_PATH)
            print(f"✅ Markdown saved: {filename}")
            log_run({"bibtex": bib, "zotero_response": zotero_item}, citekey)
        else:
            print(f"❌ Zotero upload failed: {status}")
            print(json.dumps(resp, indent=2))

    citekey = generate_citekey(
        author=bib.get("author", "Unknown"),
        date_str=bib.get("date", ""),
        title=bib.get("title", "")
    )

    print(f"✅ Parsed citekey: {citekey}")
    if not commit:
        print("🟡 Dry-run mode. No Zotero upload or file write.")
        print(json.dumps(bib, indent=2))
    else:
        status, resp = zotero_upload(bib)
        if status in [200, 201]:
            zotero_item = resp['successful']['0']
            key = zotero_item['key']
            print(f"✅ Zotero upload successful (Key: {key})")
            md = build_markdown(bib, key)
            filename = generate_filename(
                author=bib.get("author", "Unknown"),
                date_str=bib.get("date", ""),
                title=bib.get("title", "")
            )
            save_file(md, filename, OBSIDIAN_PATH)
            print(f"✅ Markdown saved: {filename}")
            log_run({"bibtex": bib, "zotero_response": zotero_item}, citekey)
        else:
            print(f"❌ Zotero upload failed: {status}")
            print(json.dumps(resp, indent=2))


if __name__ == "__main__":
    import platform

    if platform.system() == "Linux" and not os.environ.get("PREFIX"):
        import pyperclip
        input_text = pyperclip.paste()
        print("📋 Clipboard input (Linux) loaded.")
        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(input_text)
    elif os.environ.get("PREFIX"):  # Android Termux
        import subprocess
        try:
            clipboard = subprocess.check_output(["termux-clipboard-get"]).decode("utf-8")
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

    main(input_text, commit=True)


