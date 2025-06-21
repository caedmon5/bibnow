# biblio_mobile_pipeline_v1

This repository contains a lightweight, cross-platform bibliography processing pipeline designed for researchers using **Zotero**, **Obsidian**, and **mobile devices** (especially Android).

It enables rapid creation of well-structured markdown literature notes and automatic uploads to Zotero from BibTeX-formatted entries, using a single clipboard copy-paste or input file.

---

## 🚀 Features

- ✅ Automatic extraction and parsing of BibTeX from clipboard (Linux) or `input.txt` (Android)
- ✅ Uploads metadata to your personal Zotero library via API
- ✅ Generates fully structured Obsidian `.md` literature notes:
  - YAML frontmatter (with `autoupdate: true`)
  - Chicago Author–Date citation block
  - Abstract
  - Keywords (as `[[wikilinks]]`)
  - Note (from `note` field in BibTeX)
  - Related Zotero links
- ✅ Dynamic platform detection (Linux vs Android)
- ✅ Logs Zotero API response and metadata to timestamped JSON files
- 📄 File naming follows:  
  `LN Lastname [et al] YYYY First Second Third Word.md`

---

## 📂 Directory Structure

```
biblio_mobile_pipeline_v1/
├── biblio_pipeline.py         # Main processing script
├── config.py                  # Personal Zotero credentials (NOT SHARED)
├── input.txt                  # Used on Android (Termux/Pydroid3) to load BibTeX
├── output/
│   └── biblio-log/            # JSON logs of Zotero uploads
└── README.md
```

---

## 🧠 Requirements

Install with pip (Linux) or Pydroid repository (Android):

```bash
pip install requests
```

If running on Linux with clipboard support:

```bash
pip install pyperclip
sudo apt install xclip  # or xsel
```

---

## 💻 Linux Desktop Usage

1. Copy BibTeX entry (surrounded by `@bibtex` and `@end`)
2. Run the script:
   ```bash
   python3 biblio_pipeline.py
   ```

> 📋 Input is pulled automatically from the clipboard.

---

## 📱 Android Usage (Termux or Pydroid)

1. Paste BibTeX (with `@bibtex` and `@end`) into `input.txt`
2. Run:
   ```bash
   python3 biblio_pipeline.py
   ```

> 📄 Input is read from `input.txt` if clipboard access is not available.

---

## ✍️ Format for BibTeX Input

Surround your BibTeX entry like so:

```
@bibtex
@article{Lastname2025ShortTitle,
  author = {Jane Lastname and Sam Coauthor},
  title = {Example Title for Reference},
  journal = {Some Journal},
  date = {2025-06-21},
  year = {2025},
  url = {https://example.com},
  abstract = {This study explores...},
  keywords = {example, research, mobile tools},
  note = {User is interested in this because...}
}
@end
```

---

## 📥 Output

- Markdown file saved to:
  - `/home/dan/wealtheow/LN Literature Notes` on Linux
  - `/sdcard/Documents/Obsidian/LN Literature Notes` on Android
- Zotero item created via API
- JSON log written to `output/biblio-log/`

---

## 🔐 Notes

- You must create a `config.py` file with your Zotero credentials:
  ```python
  ZOTERO_API_KEY = "your-api-key"
  ZOTERO_USER_ID = "your-numeric-id"
  ZOTERO_USERNAME = "your-username"
  ```
- Keep this file out of version control.

---

## 🧭 Roadmap

- [ ] Sync existing Obsidian notes with Zotero updates (`autoupdate: true`)
- [ ] Daily note linking
- [ ] Context menu or button shortcut on Android

---

## 🗂️ License

MIT (except user-specific config files).
