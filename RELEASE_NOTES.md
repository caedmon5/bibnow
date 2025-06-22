# 📦 Release Notes – Version 1.1.0

## 🚀 New Features

- 🎭 **Expanded Zotero Type Mapping**
  - Added support for BibTeX types: `@film`, `@hearing`, `@case`, `@poster`, `@presentation`, `@blog`
  - Improved fallback metadata (e.g., use `court`, `institution`, `director` when `author` is absent)

- 🧠 **Smarter Citekey and Filename Generation**
  - Citekeys follow `LastnameYYYYFirstSecondThird`
  - Markdown filenames follow `LN Lastname et al YYYY Title.md`

- 🪵 **Enhanced Markdown Output**
  - Correctly formats YAML frontmatter, Chicago-style bibliography, and wikilinked keywords
  - Gracefully fills missing values with "TBD" to prevent rendering issues

## 🛠 Fixes and Improvements

- 🛠 **Zotero Upload**
  - Removed deprecated `year` field (was causing `Invalid property 'year'` errors)
  - All dates now sent via `date` field only

- 🧱 **Parser Robustness**
  - More reliable BibTeX parsing from full or block-captured clipboard input
  - Multi-author detection now reliably triggers `et al` in filenames

- 📄 **Markdown Output**
  - Fixed broken or unaligned abstract/keyword sections in YAML or Markdown
  - Introduced fallback handling for citation logic when bibliographic fields are sparse

## ❗ Known Issues

- 🎬 Some exotic BibTeX types like `@manual`, `@software` not yet supported
- 🧑‍⚖️ `@case` and `@hearing` entries may require title-casing or manual verification
- 🖋 Output bibliography entries still assume English Chicago-style formatting

---

Released: 2025-06-22  
Maintainer: Daniel Paul O'Donnell
