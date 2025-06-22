# 📚 biblio_pipeline_v1

A command-line Python tool for uploading BibTeX bibliography entries to Zotero and generating Obsidian-compatible Markdown notes for scholarly use. Supports full clipboard integration and automated metadata extraction for a wide range of reference types.

## ✨ Features

- ✅ Full BibTeX-to-Zotero type mapping, including:
  - `@article`, `@book`, `@inproceedings`, `@thesis`, `@report`
  - `@online`, `@blog`, `@presentation`, `@poster`
  - `@case`, `@hearing`, `@film`
- 📋 Clipboard support for Linux and Android (Termux)
- 🧠 Smart citekey and filename generation using `LastName et al` and first 3 title words
- 🪵 Markdown output for Obsidian with embedded metadata, abstract, keywords, and notes
- 🔍 Fallback handling for missing authors (e.g., cases, hearings, films)
- 📅 Graceful handling of Zotero's `year` limitations by using `date`

## 🛠 Setup

### Python Requirements
```bash
pip install -r requirements.txt
```
Dependencies:
- `requests`
- `bibtexparser`
- `pyperclip` (Linux only)
- `termux-clipboard-get` (Android only)

### Configuration
Edit `config.py` with your Zotero API credentials:
```python
ZOTERO_API_KEY = "your-api-key"
ZOTERO_USER_ID = "your-user-id"
ZOTERO_USERNAME = "your-username"
```

## ▶ Usage

### Commit to Zotero and write to Obsidian
```bash
python3 biblio_pipeline.py --commit
```

### Dry-run to test parsing only
```bash
python3 biblio_pipeline.py
```

Supports input via:
- Clipboard (Linux/Android)
- `input.txt` fallback

## 🔁 Filename and Citekey Format

- Citekey: `LastnameYYYYFirstSecondThirdWord`
- Markdown filename
