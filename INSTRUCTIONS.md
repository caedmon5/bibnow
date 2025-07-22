# 📘 Instruction Manual: `bibnow`

## ℹ️ What Is This?

`bibnow` is a lightweight, cross-platform tool (Linux and Android) that allows users to create bibliographic records **simultaneously** in **Zotero** and **Obsidian** from a single BibTeX input.

It streamlines the process of capturing, formatting, and annotating scholarly references — optimised for clipboard input, markdown export, and mobile workflows.

### Why use this instead of Zotero or Obsidian alone?

`bibnow` enables instant creation of:
- ✅ A clean Zotero record (via the Zotero API)
- ✅ A structured markdown literature note in your Obsidian vault
- ✅ Canonical, synchronised records between citation and annotation systems

It is especially helpful when:
- Working on mobile or in a terminal
- Managing mixed media (e.g. web pages, blog posts, legal decisions)
- Automating workflows using `git`, `termux`, or scripts

### Advantages

- ✅ Parses BibTeX into Obsidian+Zotero simultaneously
- ✅ Auto-generates `LN` filenames and wiki-linked keywords
- ✅ Supports clipboard or `input.txt` entry
- ✅ Structured YAML frontmatter for `citekey`, `type`, `callnumber`, etc.
- ✅ Includes fallback citation if no CSL support

---

## 🔧 Requirements

- Python 3.11+
- Platform: Linux or Android (via Termux)
- Accounts: Zotero API key, Zotero user ID + username
- Obsidian vault path

---

## 🚀 Installation

```bash
git clone https://github.com/caedmon5/bibnow.git
cd bibnow
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit `config.py` with:

```python
ZOTERO_API_KEY = "your-zotero-api-key"
ZOTERO_USER_ID = "123456"
ZOTERO_USERNAME = "yourusername"
OBSIDIAN_VAULT_PATH = "/full/path/to/your/vault"
```

---

## 💡 Usage

```bash
bibnow              # preview from clipboard or input.txt
bibnow --commit     # upload to Zotero + save to Obsidian
```

---

## 🆕 Output Fields in YAML

Each markdown note includes:

- `responsible_party`: First-named author/editor/court/etc.
- `record_title`: Title of the cited item
- `record_year`: Four-digit year
- **Baseline citation** (fallback line):
  ```
  Responsible Party. Year. Title.
  ```

---

## 🧪 Testing

Paste BibTeX to clipboard or into `input.txt`, then:

```bash
bibnow --dryrun
```

Watch for:
- ✅ Parsed citekey and preview markdown
- ✅ No errors from Zotero or file write
- ✅ Fields like `responsible_party`, `record_title`, etc. appear in YAML

---

## 🧭 Version Info

This manual covers `v0.2.1` (or `v1.2.0` depending on SemVer choice), which adds baseline citation support and metadata fields.
