# 📦 Release Notes – Version 0.2.1

## 🚀 New Features

- 🧾 **Baseline Citation Support**
  - Adds a new fallback citation line to markdown output: `Responsible Party. Year. Title.`
  - Works even when CSL output is not available
- 📄 **YAML Metadata Enhancements**
  - New YAML fields:
    - `responsible_party`
    - `record_title`
    - `record_year`

## 🛠 Improvements

- Markdown output is more robust
- Lays groundwork for future field sanitisation (e.g. skipping invalid BibTeX fields)

## 🔧 Internals

- Supports clean DRY-RUN previews
- Compatible with all v0.2.0-format notes and filenames

---

Released: 2025-07-22
Maintainer: Daniel Paul O'Donnell
