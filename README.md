# 📚 `biblio_mobile_pipeline_v1`

> A lightweight pipeline for generating BibTeX, Obsidian markdown, and Zotero-compatible entries from scholarly sources — optimized for mobile and cross-platform workflows.

---

## ✅ Current Stable Release: `v0.2.0`

This branch (`main`) reflects the **current stable version** (`v0.2.0`), which is:

- ✅ Fully working on **Linux**
- ✅ Fully working on **Android (Termux / Python 3.12)**

> This version does **not** include formatted citation blocks or `citeproc`-based output.

---

## 🚧 Want Better Citations? Try `v0.3.0-rc1` (Linux Only)

A **release candidate for `v0.3.0`** is available on the [`dev`](https://github.com/caedmon5/biblio_mobile_pipeline_v1/tree/dev) branch and tagged as [`v0.3.0-rc1`](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v0.3.0-rc1).

It adds:

- 🧠 **Formatted citation blocks** using CSL (Chicago Author–Date)
- ✍️ Smart quotation fallback
- 📄 Fully compatible output with this version (`v0.2.0`)

> ⚠️ `v0.3.0-rc1` does **not** work on Android due to missing `lxml` support in Python 3.12 (ARM64).

---

## 📦 Requirements

- Python 3.11+ (v0.2.0 works on 3.12; v0.3.0 requires `lxml` which is not yet packaged for Android)
- Linux, Termux (Android), macOS (untested but likely compatible)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
bibnow --dryrun     # Preview formatted output
bibnow --commit     # Save to Zotero + Obsidian vault
```

---

## 📂 File Structure

- `input.txt`: BibTeX input (clipboard or file)
- `bib_formatter.py`: output generator for BibTeX + YAML + Markdown
- `biblio_pipeline.py`: main CLI entrypoint
- `vendor/citeproc/`: included only in v0.3.x+

---

## 🗂️ Versioning Strategy

| Version     | Linux | Android (Py 3.12) |
|-------------|--------|------------------|
| v0.2.0      | ✅     | ✅               |
| v0.3.0-rc1  | ✅     | ❌ (no `lxml`)    |

---

## 🧭 Quick Links

- [Latest stable release (`v0.2.0`)](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v0.2.0)
- [Development branch (`v0.3.0-rc1`)](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v0.3.0-rc1)
- [Dev source code](https://github.com/caedmon5/biblio_mobile_pipeline_v1/tree/dev)

---

## 📌 License

MIT
