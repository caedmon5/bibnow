# 📚 `biblio_mobile_pipeline_v1`

> A lightweight pipeline for generating BibTeX, Obsidian markdown, and Zotero-compatible entries from scholarly sources — optimized for mobile and cross-platform workflows.

📎 See full setup and usage guide in [INSTRUCTIONS.md](INSTRUCTIONS.md)


---

## ⚠️ This is a Pre-release Development Branch

**Status:** `v0.3.0-rc1` (release candidate)  
**Platform Support:**  
- ✅ Fully working on **Linux**
- ❌ **Not yet functional on Android** (Termux + Python 3.12 lacks `lxml` support)

> Use [`v0.2.0`](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v0.2.0) if you are on Android.  
> Both versions produce compatible outputs and can be used side-by-side.

---

## 🆕 What's New in `v0.3.0`

- 🧠 **Full CSL support via vendored `citeproc`**
  - Includes fallback quotation logic for Chicago-style output
- ✍️ **Properly formatted citation blocks** in Obsidian (e.g., Chicago Author–Date)
- 💾 **Cross-compatible** output with `v0.2.0`:
  - YAML headers
  - BibTeX
  - Markdown for Obsidian and Zotero

---

## 📦 Requirements

- **Python 3.11+** (3.12 supported on Linux, *not yet on Android*)
- On Linux:
  ```bash
  pip install -r requirements.txt
  ```

- On Android (Termux): Use [`v0.2.0`](https://github.com/caedmon5/biblio_mobile_pipeline_v1/releases/tag/v0.2.0) until precompiled `lxml` becomes available for Python 3.12 / ARM64.

---

## 🚀 Usage

### On Linux:

```bash
bibnow --dryrun         # Preview output
bibnow --commit         # Save to Zotero + Obsidian vault
```

### On Android:

```bash
# Use latest v0.2.0 release — see GitHub releases
```

---

## 🧪 Test Status

| Version     | Linux | Android (Py 3.12) |
|-------------|--------|------------------|
| v0.2.0      | ✅     | ✅               |
| v0.3.0-rc1  | ✅     | ❌ (no `lxml`)    |

---

## 📍 Notes

- This version uses a vendored version of `citeproc` patched to support fallback quotation rendering for locales missing quote definitions.
- `input.txt` is ignored by Git and used for piped/clipboard BibTeX.
- Output is designed for use with:
  - Zotero (via API)
  - Obsidian (markdown files with YAML and citation block)
  - BibTeX-compatible LaTeX documents

---

## 🗂️ Versioning Strategy

- `main`: Tracks last **stable, cross-platform** release (currently `v0.2.0`)
- `dev`: Tracks **in-progress features** (e.g., citeproc, fallback quoting)
- `v0.3.0-rc1`: Pre-release candidate for Linux users

---

## 📌 License

MIT
