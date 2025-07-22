# 📚 `bibnow`

> A lightweight pipeline for generating BibTeX, Obsidian markdown, and Zotero-compatible entries from scholarly sources — optimised for mobile and cross-platform workflows.

📎 See full setup and usage guide in [INSTRUCTIONS.md](INSTRUCTIONS.md)

---

## ✅ Current Stable Release: `v0.2.1`

This branch (`main`) reflects the **latest stable version** (`v0.2.1`), which is:

- ✅ Fully working on **Linux**
- ✅ Fully working on **Android (Termux / Python 3.12)**
- ✅ Includes:
  - Baseline fallback citation support
  - `responsible_party`, `record_title`, `record_year` in YAML
  - Markdown formatting compatible with Obsidian

> This version does **not** include citeproc-based formatting. For advanced citation output, use the experimental `v0.3.x` branch.

---

## 🚧 Want Better Citations? Try `v0.3.0-rc1` (Linux Only)

A **release candidate for `v0.3.0`** is available on the [`dev`](https://github.com/caedmon5/bibnow/tree/dev) branch and tagged as [`v0.3.0-rc1`](https://github.com/caedmon5/bibnow/releases/tag/v0.3.0-rc1).

It adds:

- 🧠 **Formatted citation blocks** using CSL (Chicago Author–Date)
- ✍️ Smart quotation fallback
- 📄 Fully compatible output with `v0.2.1`

> ⚠️ `v0.3.0-rc1` does **not** work on Android due to missing `lxml` support.

---

## 📦 Requirements

- Python 3.11+ (v0.2.1 works on 3.12; v0.3.0 requires `lxml`)
- Linux, Termux (Android), macOS (untested but likely compatible)

Install dependencies:
```bash
pip install -r requirements.txt
