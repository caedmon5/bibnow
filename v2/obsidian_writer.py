import os
import re
from string import Template

from config import ZOTERO_USER_ID
from obsidian_writer_config import (
    OUTPUT_DIR,
    FILENAME_PREFIX,
    USE_ET_AL,
    TITLE_WORD_LIMIT,
    TEMPLATE_PATH
)

def generate_citekey(zotero_item: dict) -> str:
    creators = zotero_item.get("creators", [])
    if creators:
        first_creator = creators[0]
        lastname = first_creator.get("lastName") or first_creator.get("name", "unknown")
    else:
        lastname = "unknown"

    lastname = re.sub(r"[^\w\s]", "", lastname).capitalize()
    year = zotero_item.get("date", "")[:4] or "XXXX"
    title = zotero_item.get("title", "")
    title_words = re.findall(r"\b\w+\b", title)
    title_part = ''.join(word.capitalize() for word in title_words[:4])

    return f"{lastname}{year}{title_part}"

def generate_filename(zotero_item: dict) -> str:
    creators = zotero_item.get("creators", [])
    title = zotero_item.get("title", "")
    date = zotero_item.get("date", "")[:4] or "XXXX"

    if creators:
        first_creator = creators[0]
        lastname = first_creator.get("lastName") or first_creator.get("name", "Unknown")
    else:
        lastname = "Unknown"

    if USE_ET_AL and len(creators) > 1:
        lastname += " et al"

    title_words = re.findall(r"\b\w+\b", title)
    title_part = " ".join(word.capitalize() for word in title_words[:TITLE_WORD_LIMIT])

    return f"{FILENAME_PREFIX}{lastname} {date} {title_part}.md"

def build_markdown_from_zotero(zotero_item: dict, citekey: str, zotero_key: str = None) -> str:
    # Prepare values
    creators = zotero_item.get("creators", [])
    responsible = ", ".join(
        f"{c.get('firstName', '')} {c.get('lastName', c.get('name', ''))}".strip()
        for c in creators
    )
    year = zotero_item.get("date", "")[:4] or "XXXX"
    title = zotero_item.get("title", "Untitled")
    title_words = re.findall(r"\b\w+\b", title)
    title_part = " ".join(word.capitalize() for word in title_words[:TITLE_WORD_LIMIT])
    extra = zotero_item.get("extra", "None supplied.")
    abstract = zotero_item.get("abstractNote", "None supplied")
    tags = zotero_item.get("tags", [])
    tag_list = [t.get("tag") for t in tags if t.get("tag")]
    wikilinks = ", ".join(f"[[{t}]]" for t in tag_list)
    zotero_url = f"https://www.zotero.org/users/{ZOTERO_USERNAME}/items/{zotero_key}" if zotero_key else ""

    # Load template
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = Template(f.read())

    return template.safe_substitute({
        "citekey": citekey,
        "aliases": "",
        "type": zotero_item.get("itemType", "document"),
        "zotero_key": zotero_key or "",
        "zotero_url": zotero_url,
        "responsible_party": responsible,
        "record_title": title,
        "record_title_short": title_part,
        "record_year": year,
        "callnumber": zotero_item.get("callNumber", ""),
        "baseline_citation": f"{responsible}. {year}. {title}.",
        "abstract": abstract,
        "keywords_display": wikilinks,
        "extra": extra
    })

def write_obsidian_note(markdown: str, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return path
