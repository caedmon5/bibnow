# Bibnow v2.0.2

**Bibnow** is a command-line tool for adding (and linking) bibliographic entries in Zotero and Obsidian. To use it, you do the following:

1. Create **Citation Stylesheet Language (CSL)** bibliographic entries for the items you you wish to add to Zotero/Obsidian. This is best done using an AI chatbot such as ChatGPT.
2. Copy the code produced by the bot.
3. Run the script in a terminal (instructions below).

The script will take the input from your clipboard and format the item(s) for insertion into your Zotero library and your Obsidian vault, using the Zotero item ID and unique URL to ensure that the two entries are linked to each other (future iterations will work on automatic syncing as well).

Bibnow currently works on Linux and Android (using Termux), though since it is entirely written in Python, it should be easily adaptable to other environments.

Version 2 is a complete refactor. Most importantly for the user, it now requires input to be in **Citation Style Language (CSL)** rather than **BibTex** (as was required by version 1). CSL uses JSON and is far better at translating into Zotero's internal languages, greatly reducing the number of errors (and complexity of the code) and producing cleaner and better entries in both Zotero and Obsidian.

---

## What’s new in v2 (plain English)

- **Clipboard or file in — CSL-JSON only.**  
  - If your clipboard has valid JSON, v2 uses it; otherwise it looks for `v2/input.txt`.  
  - (BibTeX is **not** accepted in v2—convert it first or use the older path.)

- **Safer Zotero uploads.**  
  - Clear success/failure, correct item key + public web link.

- **Better field mapping.**  
  - `keywords` as a **string** or **list**  
  - legal cases (`caseName`, `court`, `dateDecided`)  
  - single-field creators (institutional authors: `"literal"` / `"name"`)

- **Obsidian notes** 
  - Notes are now built from a template that you can edit to suit your own needs. 

- **No secrets in code.**  
  - Private settings live in `.env` (loaded automatically).

## Changelog

### v2.0.1 (2025-08-24)
- Fixed CSL → Zotero keyword mapping (`keyword` vs `keywords`)
- Prevented duplication of keywords in `extra`
- Obsidian YAML now renders `keywords:` as wikilinked list entries (`- "[[Keyword]]"`)

### v2.0.2 (2025-08-25)
- fixed issue with double quotes inside YAML

---

## Requirements

- Python 3.9+
- A Zotero account and **API key**  
  (zotero.org → Settings → Feeds/API → Create new private key)
- Obsidian (optional but recommended). Bibnow doesn't interact with Obsidian directly. But the Markdown notes it produces are easily used within Obsidian.

---

## Quickstart (Linux or Android/Termux)

```bash
# 1) Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2) Configure your environment (.env auto-loads via python-dotenv)
cp .env.example .env
# Open .env and fill in:
#   ZOTERO_API_KEY=your_key_here
#   ZOTERO_LIBRARY=user            # or: group
#   ZOTERO_USER_ID=632779          # required if LIBRARY=user (numeric)
#   ZOTERO_USERNAME=daniel.odonnell # required if LIBRARY=user (for web links)
#   ZOTERO_GROUP_ID=6069337        # required if LIBRARY=group (numeric)
#   OBSIDIAN_VAULT_PATH=/path/to/your/Obsidian/vault

# 3) Run (clipboard JSON preferred; file fallback is v2/input.txt)
python3 v2/pipeline.py           # dry-run (prints what would happen)
python3 v2/pipeline.py --commit  # actually create the Zotero item and write the note
```

### Android/Termux specifics

```bash
pkg update
pkg install python git termux-api
termux-setup-storage   # grant storage permission once

# Recommended Obsidian path on Android:
#   OBSIDIAN_VAULT_PATH=/sdcard/Documents/Obsidian/LN Literature Notes

# Put JSON on clipboard and run:
termux-clipboard-set '{"id":"a1","type":"article-journal","title":"Termux Test","author":[{"family":"Lee","given":"Min"}],"issued":{"date-parts":[[2024]]}}'
cd v2 && source ../.venv/bin/activate && python3 pipeline.py --commit
```

---

## Inputting bibliography

Bibnow v2 expects **CSL-JSON**. You can supply **one item** or a **list of items**.

- **Clipboard method (easiest):** copy the JSON to your clipboard and run `python3 v2/pipeline.py`.  
- **File fallback:** put the JSON in `v2/input.txt` and run the same command.

**Single item example:**

```json
{
  "id": "ex-1",
  "type": "article-journal",
  "title": "Minimal Example",
  "author": [{ "family": "Smith", "given": "Jane" }],
  "issued": { "date-parts": [[2023]] },
  "container-title": "Journal of Minimal Examples",
  "volume": "1",
  "page": "1-2",
  "keywords": "Testing, Pipelines"
}
```

**Batch example (with edge cases):**

```json
[
  {
    "id": "a1",
    "type": "article-journal",
    "title": "Batch: Article",
    "author": [{ "family": "Nguyen", "given": "Kim" }],
    "issued": { "date-parts": [[2022]] },
    "container-title": "Batching Quarterly",
    "volume": "12",
    "page": "10-22",
    "keywords": "Batching, Pipelines, Testing"
  },
  {
    "id": "b1",
    "type": "book",
    "title": "Batch: Book Keywords List",
    "author": [{ "family": "OMalley", "given": "Pat" }],
    "issued": { "date-parts": [[2021]] },
    "publisher": "Edge Case Press",
    "keywords": ["ListOne", "ListTwo", "ListThree"]
  },
  {
    "id": "c1",
    "type": "legal_case",
    "caseName": "Example v. Sample",
    "court": "Example Court",
    "issued": { "date-parts": [[1999]] }
  },
  {
    "id": "r1",
    "type": "report",
    "title": "Report With Single-Field Creator",
    "author": [{ "name": "Institute for Test Studies" }],
    "issued": { "date-parts": [[2018]] },
    "URL": "https://example.org/report",
    "abstract": "A minimal report to exercise name-only creators.",
    "keywords": "Reports, Single-Name Creator"
  }
]
```

> Tip: If you accidentally copy **BibTeX** (e.g., starts with `@article{…}`), v2 will warn you and ignore it. Convert to CSL-JSON first.

---

## What you’ll see

- **Console output:**  
  `✅ Upload successful. Zotero Key: 6ZAGUFM9`  
  `🔗 https://www.zotero.org/<username>/items/6ZAGUFM9`

- **Obsidian note:** a Markdown file in your vault, e.g.  
  `LN Smith 2023 Minimal Example.md`  
  with front-matter (citekey, item type, Zotero URL), a baseline citation, abstract (if any), keywords, and original metadata.

---

## FAQ

**Where do I put my Zotero API key?**  
In `.env` at the repo root. This file is **git-ignored** so secrets aren’t committed. You create this by copying the example file included in the repository v2/.env.example to v2/.env and filling in the fields with your own information.

**User vs Group library?**  
Set `ZOTERO_LIBRARY=user` (with `ZOTERO_USER_ID` + `ZOTERO_USERNAME`) or `ZOTERO_LIBRARY=group` (with `ZOTERO_GROUP_ID`). The tool will use the right API base and public web link format. For most researchers most of the time, you will use your user (i.e. personal) library.

**"How do I produce bibliographic items in CSL JSON?**
While you can code this by hand or use specialized tools, the best way is to use an AI-powered chatbot (the bot can also provide a summary and create keywords). A typical way of doing this is to use a prompt similar to the following, followed by an identifier (e.g. DOI, URL, ISBN) and, optionally, but recommended, the full text of the item to be added (so that the bot can make more accurate keywords and summaries):

> Please provide me with a Citation Style Language entry for the following bibliographic item(s). Generate an abstract/summary if none is present and provide rich keywords based on the supplied content.

**“Input is not JSON.”**  
Your clipboard or `input.txt` didn’t contain valid JSON. Check for trailing commas, missing braces, or that you didn’t paste BibTeX by mistake.

**Can I process several items at once?**  
Yes—pass a **JSON array** (see batch example). Each is uploaded and gets its own Obsidian note.

**Does it work offline?**  
Zotero upload needs internet; parsing and note generation are local.

---

## Troubleshooting

- `ModuleNotFoundError: dotenv` → `pip install -r requirements.txt` inside your venv.  
- Android: `termux-clipboard-* not found` → install **Termux:API** app, then `pkg install termux-api`.  
- Permission denied writing to vault (Android) → run `termux-setup-storage`; set `OBSIDIAN_VAULT_PATH` under `/sdcard/...`.  
- Wrong Zotero link → check `.env` values (user vs group, username vs numeric IDs).  
- Note title shows “XXXX” or “Untitled” → usually missing or mismapped fields; legal cases rely on `caseName` + `dateDecided` (both supported).

---

## Contributing / Safety

- `.env` and `v2/config_local.py` are **git-ignored** (see `.gitignore`).  
- Keep examples in `v2/tests/` and use `v2/run_tests.sh` to exercise the pipeline end-to-end.

---

## License

MIT
