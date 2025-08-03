# bibnow: Modular Bibliographic Processing Pipeline (v2)

**bibnow** is a modular Python pipeline for processing bibliographic entries from ChatGPT into both Zotero and Obsidian. It supports automated ingestion from the system clipboard (via `input.txt`), rich metadata extraction, and structured export to both citation management and note-taking systems.

---

## 📁 Directory Structure

- `legacy_bibtex/` – Original BibTeX-based pipeline (v1); kept for reference.
- `v2/` – New modular CSL-based pipeline under active development.
- `vendor/` – External dependencies (e.g., `citeproc`).
- `input.txt` – Clipboard-captured input for new entries.
- `config.py` – User-specific configuration for Zotero credentials and file paths.
- `README.md` – Project overview (this file).

---

## 🚀 Current Workflow (v2)

This version assumes bibliographic entries are copied from a ChatGPT code block into `input.txt` and follow CSL JSON or valid extended formats.

**Steps:**

1. **Read Input**  
   - `input_handler.py`: Loads `input.txt` (clipboard content) and parses into CSL-compatible JSON entries.

2. **Upload to Zotero**  
   - `zotero_writer.py`: Pushes the record to Zotero using the API and retrieves the item key and permanent URL.

3. **Fetch Zotero Citation Info**  
   - `zotero_query.py`: Queries the Zotero API to fetch full metadata after ingestion.

4. **Write Obsidian Note**  
   - `obsidian_writer.py`: Creates a literature note in Obsidian format (YAML frontmatter, citation block, keywords, etc.).

---

## 🔧 Configuration

Edit `config.py` to define:

- Your **Zotero API key**
- Zotero **user/group ID**
- Output path to your **Obsidian vault**
- Obsidian attachment and filename conventions

---

## 🧪 Development Notes

- Uses `v2-main` Git branch.
- A future step will add `step 0`: LLM-based metadata enrichment.
- Primary input source is `input.txt` (clipboard dump).
- Designed for modular testing and component replacement.

---

## 🏛 Legacy Pipeline (v1)

The older BibTeX-based pipeline is retained in `legacy_bibtex/`. It is frozen and no longer under development but remains functional.

---

## 🗓 Versioning

- `v1`: BibTeX-based, monolithic (`legacy_bibtex/`)
- `v2`: CSL-based, modular, Zotero-first (`v2/`)

---

## 📌 Status

**Active development** on v2.  
Target: full Zotero–Obsidian pipeline replacement with simplified parsing and better error handling.
