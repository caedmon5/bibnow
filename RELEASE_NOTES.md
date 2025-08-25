# v2.0.2 - escape double quotes in YAML

- fixed problem in YAML of Obsidian when items had internal double quotes. They are escaped now throughout.

# v2.0.1 – Keyword handling fix

- Accepts CSL keyword (singular) in addition to keywords
- Prevents keyword, id, and section from appearing in extra
- Obsidian YAML frontmatter now outputs proper wikilinked keywords: lists
- Fully backward-compatible bugfix (safe to upgrade from v2.0.0)

# Bibnow v2.0.0

**Highlights**
- CSL-JSON only ingestion (clipboard first, fallback to `v2/input.txt`)
- Safer Zotero uploads with clear success/error and correct public links
- Legal case mapping: `caseName`, `court`/`authority`, `dateDecided`
- Keywords as string *or* list
- Single-field creators (`"name"`/`"literal"`) for institutions
- Obsidian notes from template with tidy filenames
- Secrets via `.env` (auto-loaded), no keys in code
- Linux + Android/Termux support

**Breaking change**
- BibTeX is no longer accepted directly in v2 (convert to CSL-JSON first).

**Setup**
- `pip install -r requirements.txt`
- `cp .env.example .env` → fill in Zotero details + vault path
- `python3 v2/pipeline.py --commit`
