# Bibnow Bibliographic Pipeline

A flexible, extensible bibliography-processing pipeline designed to transform raw BibTeX input into rich, citation-ready formats for use in Obsidian, Zotero, and Markdown workflows.

---

## 📦 Features

- ✅ Converts BibTeX entries into:
  - Valid CSL JSON objects
  - Chicago Author–Date bibliographic strings
  - Obsidian-compatible Markdown with YAML frontmatter
- ✅ Supports full CSL formatting via `citeproc-py`
- ✅ Injects fallback smart quotes if CSL locale is missing quote terms
- ✅ Automatically patches CSL styles to enforce US punctuation (`punctuation-in-quote`)
- ✅ Uploads entries to Zotero via `pyzotero`
- ✅ Supports extended BibTeX fields (`callnumber`, `keywords`, `abstract`, etc.)
- ✅ Handles legal and edge citation cases (planned)

---

## 🚀 Quick Start

```bash
# Run interactively
bibnow

# Process clipboard content and commit to Zotero + Markdown
bibnow --commit
```

---

## 🗂 Directory Structure

```
bib_formatter.py         # Converts BibTeX to CSL + formats bibliography
biblio_pipeline.py       # Main pipeline: parses, formats, uploads
author_utils.py          # Utilities for parsing names, roles
config.py                # Style paths, Zotero keys, directory locations
/csl/                    # CSL style files (e.g. chicago-author-date.csl)
/locales/                # Locale XML files (fallback if citeproc is missing data)
```

---

## 🔧 Configuration

Edit `config.py` to set paths for:

- Default CSL style (`BIBLIO_STYLE`)
- Markdown output location
- Zotero API credentials

---

## 🧪 Testing

You can test edge-case entries using:

- `@article`, `@book`, `@inproceedings`
- `@thesis` (PhD/Master)
- Planned: `@case`, `@bill`, `@video`, `@unpublished`, etc.

---

## 📌 Version

Current stable version: **v1.3.0-citeproc-patch**  
Tag: [`v1.3.0-citeproc-patch`](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v1.3.0-citeproc-patch)

---

## 📍 Roadmap

- [ ] Extend support for media and legal BibTeX types
- [ ] Refactor field access using helper functions
- [ ] Externalise platform detection into shared tools repo
- [ ] Improve visual placement of user-defined interest statements
- [ ] Obsidian wiki-link support for flagged interest terms

---

## 🔒 Fallback Branch

Use `fallback-citeproc-patch` if rollback to a known working version is needed.

---

## 👤 Author

Created and maintained by [@caedmon5](https://github.com/caedmon5) for academic research and personal productivity workflows.

