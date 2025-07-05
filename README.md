# 📚 biblio_pipeline_v1

A command-line Python tool for uploading BibTeX bibliography entries to Zotero and generating Obsidian-compatible Markdown notes. Designed for cross-platform scholarly workflows, with full clipboard integration for both Android (Termux) and Linux.

---

## ✨ Features

- ✅ Converts BibTeX entries to Zotero-compatible JSON
- 📋 Automatically captures input from clipboard (Termux/Linux) or falls back to `input.txt`
- 🧠 Generates Obsidian-compatible Markdown notes with:
  - YAML frontmatter
  - Chicago-style citation block
  - Abstract, keywords, notes, and URLs
- 🪪 Automatic citekey and filename generation: `LastNameYYYYFirstSecondThirdWord`
- 🧱 Platform-aware setup: auto-detects Android (Termux) vs. Linux
- 📦 Outputs both `.bib` and `.md` files
- 🔐 Uploads entries directly to your Zotero library

---

## 🛠 Setup

📎 See full setup and usage guide in [INSTRUCTIONS.md](INSTRUCTIONS.md)


### 1. Install Dependencies

Install with:

```bash
pip install -r requirements.txt
```

Dependencies include:

- `requests`
- `bibtexparser`
- `pyperclip` (Linux only)
- `termux-clipboard-get` (Android only)

---

### 2. Configure `config.py`

Set your Zotero credentials and Obsidian vault path:

```python
ZOTERO_API_KEY = "your-zotero-api-key"
ZOTERO_USER_ID = "your-user-id"
ZOTERO_USERNAME = "your-zotero-username"

OBSIDIAN_VAULT_PATH = "/absolute/path/to/your/LN Literature Notes"
```

📌 You **do not** need to specify a platform — the script auto-detects whether you're on Android (Termux) or Linux and adapts accordingly.

---

## ▶ Usage

### Dry Run (no upload, prints preview)

```bash
python3 biblio_pipeline.py
```

- Reads from clipboard (`termux-clipboard-get` or `pyperclip`)
- Falls back to `input.txt` if clipboard fails
- Outputs a preview of the generated citekey, Markdown, and file name

---

### Commit Mode (upload to Zotero, save files)

```bash
python3 biblio_pipeline.py --commit
```

- Uploads to Zotero using your credentials
- Generates `.bib` and `.md` files in the appropriate location
- Logs the output in `output/biblio-log/`

---

## 📄 Filename and Citekey Format

- **Citekey**: `LastNameYYYYFirstSecondThirdWord`
- **Markdown filename**: `LN LastName YYYY First Second Third.md`
  - If multiple authors/editors: `LastName et al`

Example:
```text
Citekey: Smith2025OnTheNature
Filename: LN Smith 2025 On The Nature.md
```

---

## 🧪 Input Handling

Input must be valid BibTeX — either:
- Entire raw BibTeX
- Or a block wrapped in `@bibtex` ... `@end`

Example input:
```
@bibtex
@article{Smith2025OnTheNature,
  author = {Smith, John},
  title = {On the Nature of BibTeX},
  journal = {Journal of Citation},
  date = {2025}
}
@end
```

---

## 📁 Output Structure

- `.md` Markdown file: saved to the Obsidian vault path
- `.bib` BibTeX and `.json` log: saved in `output/`
- Files include:
  - Abstract, keywords, extra notes
  - Links back to the Zotero item
  - Warning headers indicating synced content

---

## 🚧 Known Issues (v0.2.0)

- `input.txt` must be manually cleared between runs if clipboard not used
- YAML escape handling is basic — certain complex abstracts or titles may require adjustment
- Markdown structure assumes specific Obsidian usage

---

## 🗂 Version Summary

| Version | Description                                |
|---------|--------------------------------------------|
| v0.1.0  | First shared version (pre-config.py)       |
| v0.1.1  | Android base (`android-base`)              |
| v0.1.2  | Layout fix (tested after 4c3465a)          |
| v0.2.0  | Config.py and platform detection (this)    |
| v0.3.0  | Citeproc integration (in development)      |

---

## 🤝 Contributions

Contributions, patches, and suggestions are welcome. Please open an issue or submit a PR.
