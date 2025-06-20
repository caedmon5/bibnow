# 📚 biblio_mobile_pipeline_v1

This repository contains a mobile-friendly, clipboard-based bibliography pipeline that allows you to:

- Copy BibTeX data into your clipboard
- Run `bibnow` to:
  - Upload to **Zotero** via their API
  - Create a Markdown literature note in your **Obsidian** vault
  - Log all activity for tracking

It’s designed for use on both **Linux** (e.g., a laptop) and **Android** (via **Termux**), with platform-specific support for clipboard handling and file paths.

---

## 🔧 Features

- 🧠 **Smart citekey generation**: From author name, date, and title
- 🗃️ **Zotero sync**: Uploads via user API key and writes metadata, keywords, and abstract
- 📝 **Obsidian note creation**: Proper YAML frontmatter and markdown body
- 🗂️ **Logs**: Each entry is logged to a timestamped JSON file
- 📋 **Clipboard-aware**: On Linux, uses `pyperclip`; on Android, reads/writes to `input.txt`

---

## 📱 Android Setup (Termux)

1. Clone the repo to:

    ```bash
    /sdcard/Documents/git/biblio_mobile_pipeline_v1
    ```

2. Ensure required packages are installed:

    ```bash
    pkg install python git
    pip install requests
    ```

3. Create `config.py` in the root directory:

    ```python
    ZOTERO_API_KEY = "your_api_key"
    ZOTERO_USER_ID = "your_numeric_id"
    ZOTERO_USERNAME = "your_zotero_username"
    ```

4. To run:

    - Copy a BibTeX block to clipboard (with `@bibtex ... @end` markers)
    - In Termux, run:

    ```bash
    cd /sdcard/Documents/git/biblio_mobile_pipeline_v1
    python biblio_pipeline.py
    ```

---

## 💻 Linux Setup

1. Clone the repo to any subdirectory under:

    ```bash
    ~/git/
    ```

2. Install requirements:

    ```bash
    pip install requests pyperclip
    ```

3. Create `config.py` (see Android example)

4. On Linux, the clipboard will be read directly using `pyperclip`.

---

## 📄 File Locations

| Platform | Obsidian Notes Path                                   | Input Source             |
|----------|--------------------------------------------------------|--------------------------|
| Linux    | `/home/dan/wealtheow/LN Literature Notes`             | Clipboard (via pyperclip)|
| Android  | `/sdcard/Documents/Obsidian/LN Literature Notes`      | `input.txt`              |

---

## 🗂️ File Formats

Markdown entries are created using the following structure:

```markdown
---
citekey: "Lastname2025ShortTitle"
type: "article"
zotero_key: "ABC123"
zotero_url: "https://www.zotero.org/..."
zotero_library_id: 123456
autoupdate: true
---
# Chicago Author-Year  Bibliography
Lastname, Firstname. 2025. "Title of the Article." *Journal Name*. URL.

# Abstract  
...

# Keywords  
[[keyword one]], [[keyword two]], ...

# Notes  
...

# Related Files and URLs  
https://www.zotero.org/...
```

---

## 🧪 Testing

You can run in dry-run mode by replacing `commit=True` with `commit=False` at the bottom of `biblio_pipeline.py`.

---

## 🔐 Privacy

No private credentials are stored in this repository. Your Zotero API key, user ID, and username must be stored in a local `config.py` file that is `.gitignored`.

---

## 📦 Future Improvements

- Termux widget to launch `bibnow`
- Automatic Obsidian backlinking
- Daily note integration
- DOI metadata enrichment

---

**Author**: Daniel Paul O'Donnell  
**License**: MIT

