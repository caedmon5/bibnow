# v2.1.0 - duplicate detection, preprints, and accumulated mapping fixes

Everything committed since v2.0.2. Backward-compatible: no input that worked before needs changing, though preprints should now be typed as such (see below).

**New**

- **Duplicate detection before upload.** The pipeline now checks whether a work is already in the library and skips it if so, reporting the existing item, its Zotero link, and the evidence the match was made on. Previously nothing prevented a second copy of an already-filed work. Matching is strongest-evidence-first: exact DOI, then ISBN, then title + first-author surname + year (strict on the title, lenient on the year, since preprints and grey literature are dated inconsistently across sources). `--allow-duplicates` files anyway.
  - This runs against a local index, not the search endpoint, because Zotero's `q` parameter does not index the DOI or ISBN fields — searching for a DOI that is demonstrably present on an item returns nothing. The index is cached in `.zotero-index.json` and refreshed incrementally via `?since=<version>`, with `/deleted` applied so removed items cannot raise false alarms. First build takes several minutes on a large library; steady state is a single request.
  - If the library cannot be reached, the run warns and proceeds. A network failure must never read as "no duplicates found".
- **Preprint support.** CSL `preprint` (a local extension — CSL 1.0.2 has no such type) and Crossref's `posted-content` both map to Zotero's preprint item, with `publisher` → Repository, `number` → Archive ID, and `genre` → Type. Preprints were previously filed as `journalArticle` with the server left as loose text in `extra`.
- **User-provided full text** is stored as a Zotero child note on the created item.

**Fixed**

- `input.txt` was opened as a bare relative path, so which file was read depended on the working directory: `python3 v2/pipeline.py` from the repo root read `./input.txt`, while the same command from `v2/` read `v2/input.txt`. A stale scratch file could be processed in place of the intended entries with no indication anything was wrong. Both loaders now resolve against the repo root, and the load message prints the path.
- Citekeys no longer contain spaces when the creator is a literal name such as "Wikipedia contributors".
- "et al" in Obsidian filenames now counts authors rather than all creators, so a single-author book with two editors is no longer filed as "Author et al".
- CSL `date-parts` are zero-padded to ISO 8601 across `map_issued_date`, `extract_year_from_issued`, and `map_access_date`; the last also accepts `date-parts` rather than raw dates only.
- Field mapping for web-based source types: `container-title` extended to broadcast, blog, forum, and webpage; `genre` mapped to `presentationType`/`postType`/`letterType` and the rest; new mappers for volume, issue, edition, ISBN, ISSN, number, medium, place, numPages, series; `publisher` mapped to `network`/`distributor`/`studio`/`company` for media types; missing comma in the `standard_keys` set.
- Zotero's `dateAdded` is recorded as `date_added` in the Obsidian frontmatter.

**Note on call numbers.** `call-number` continues to land in Zotero's `extra` rather than the `callNumber` field. This is deliberate: a populated `callNumber` marks a physical copy held, so auto-filling it for every cited book would destroy that distinction.

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
