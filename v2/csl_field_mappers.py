
# === Core conditional mappings ===

def map_container_title(csl_item, zotero_item, item_type):
    """Maps CSL 'container-title' to appropriate Zotero container field."""
    container = csl_item.get("container-title")
    if not container:
        return
    field_map = {
        "journalArticle": "publicationTitle",
        "magazineArticle": "publicationTitle",
        "newspaperArticle": "publicationTitle",
        "bookSection": "bookTitle",
        "conferencePaper": "proceedingsTitle",
        "dictionaryEntry": "dictionaryTitle",
        "encyclopediaArticle": "encyclopediaTitle"
    }
    target = field_map.get(item_type)
    if target:
        zotero_item[target] = container

def extract_year_from_issued(issued):
    """
    Extract a formatted string from CSL 'issued' object for Zotero's 'dateDecided'.
    Supports year, year-month, or full date.
    """
    try:
        parts = issued.get("date-parts", [])[0]
        return "-".join(str(p) for p in parts)
    except Exception:
        return ""


def map_publisher_field(csl_item, zotero_item, item_type):
    """Maps CSL 'publisher' to Zotero field (university, institution, or publisher)."""
    val = csl_item.get("publisher")
    if not val:
        return
    if item_type == "thesis":
        zotero_item["university"] = val
    elif item_type == "report":
        zotero_item["institution"] = val
    else:
        zotero_item["publisher"] = val

def map_genre(csl_item, zotero_item, item_type):
    """Maps CSL 'genre' to Zotero-specific type fields."""
    genre = csl_item.get("genre")
    if not genre:
        return
    if item_type == "report":
        zotero_item["reportType"] = genre
    elif item_type == "thesis":
        zotero_item["thesisType"] = genre
    else:
        zotero_item["extra"] = zotero_item.get("extra", "") + f"\ngenre: {genre}"

def map_event(csl_item, zotero_item, item_type):
    """Maps CSL 'event' to Zotero 'conferenceName' (only for conferencePaper)."""
    event = csl_item.get("event")
    if event and item_type == "conferencePaper":
        zotero_item["conferenceName"] = event

def map_title_short(csl_item, zotero_item, item_type):
    """Maps CSL 'title-short' to Zotero 'shortTitle'."""
    short = csl_item.get("title-short")
    if short:
        zotero_item["shortTitle"] = short

def map_note(csl_item, zotero_item, item_type):
    """Maps CSL 'note' to Zotero 'extra'."""
    note = csl_item.get("note")
    if note:
        zotero_item["extra"] = zotero_item.get("extra", "") + f"\n{note}"

def map_issued_date(csl_item, zotero_item, item_type):
    """Maps CSL 'issued' field to Zotero 'date' (prefers raw, falls back to year)."""
    issued = csl_item.get("issued")
    if not issued:
        return
    if "raw" in issued:
        zotero_item["date"] = issued["raw"]
    elif "date-parts" in issued:
        dp = issued["date-parts"][0]
        zotero_item["date"] = "-".join(str(d) for d in dp if d is not None)

# === Legal/Governmental ===

def map_case_fields(csl_item, zotero_item, item_type):
    """
    Special handling for legal cases in Zotero.
    - 'title' becomes 'caseName'
    - 'date' is removed (Zotero doesn't accept it)
    - 'issued' becomes 'dateDecided'
    """
    if item_type != "case":
    return

    # Remove unsupported Zotero field for 'case' items
    zotero_item.pop("date", None)



    if "title" in csl_item:
            zotero_item["caseName"] = csl_item["title"]
            # Important: remove 'title' if it was auto-mapped
            if "title" in zotero_item:
                del zotero_item["title"]

    # Optionally map other legal-specific fields if needed
    if "URL" in csl_item:
        zotero_item["url"] = csl_item["URL"]
    if "page" in csl_item:
        zotero_item["pages"] = csl_item["page"]
    if "authority" in csl_item:
        zotero_item["court"] = csl_item["authority"]
    if "issued" in csl_item:
        zotero_item["dateDecided"] = csl_item["issued"].get("raw", "")

def map_bill_fields(csl_item, zotero_item, item_type):
    """Maps fields for bills."""
    if item_type != "bill":
        return
    for k in ["billNumber", "session", "legislativeBody"]:
        if k in csl_item:
            zotero_item[k] = csl_item[k]

def map_statute_fields(csl_item, zotero_item, item_type):
    """Maps fields for statutes."""
    if item_type != "statute":
        return
    for k in ["nameOfAct", "section", "code"]:
        if k in csl_item:
            zotero_item[k] = csl_item[k]

def map_hearing_fields(csl_item, zotero_item, item_type):
    """Maps fields for legislative hearings."""
    if item_type != "hearing":
        return
    for k in ["committee", "legislativeBody"]:
        if k in csl_item:
            zotero_item[k] = csl_item[k]

# === Media, interviews, presentations ===

def map_presentation_fields(csl_item, zotero_item, item_type):
    if item_type != "presentation":
        return
    if "event" in csl_item:
        zotero_item["meetingName"] = csl_item["event"]

def map_interview_fields(csl_item, zotero_item, item_type):
    if item_type != "interview":
        return
    if "medium" in csl_item:
        zotero_item["interviewMedium"] = csl_item["medium"]

def map_audio_fields(csl_item, zotero_item, item_type):
    if item_type != "audioRecording":
        return
    if "medium" in csl_item:
        zotero_item["audioRecordingFormat"] = csl_item["medium"]

def map_video_fields(csl_item, zotero_item, item_type):
    if item_type != "videoRecording":
        return
    if "medium" in csl_item:
        zotero_item["videoRecordingFormat"] = csl_item["medium"]

# === Common fields ===

def map_doi(csl_item, zotero_item, item_type):
    if "DOI" in csl_item:
        zotero_item["DOI"] = csl_item["DOI"]

def map_url(csl_item, zotero_item, item_type):
    if "URL" in csl_item:
        zotero_item["url"] = csl_item["URL"]

def map_pages(csl_item, zotero_item, item_type):
    if "page" in csl_item:
        zotero_item["pages"] = csl_item["page"]

def map_language(csl_item, zotero_item, item_type):
    if "language" in csl_item:
        zotero_item["language"] = csl_item["language"]

def map_abstract(csl_item, zotero_item, item_type):
    if "abstract" in csl_item:
        zotero_item["abstractNote"] = csl_item["abstract"]

# === Generic metadata extensions ===

def map_access_date(csl_item, zotero_item, item_type):
    if "accessed" in csl_item:
        if "raw" in csl_item["accessed"]:
            zotero_item["accessDate"] = csl_item["accessed"]["raw"]

def map_tags(csl_item, zotero_item, item_type):
    if "keywords" in csl_item:
        tags = [t.strip() for t in csl_item["keywords"].split(",")]
        zotero_item["tags"] = [{"tag": t} for t in tags if t]

def map_extra_fields(csl_item, zotero_item, item_type):
    """Catch-all for nonstandard CSL fields."""
    standard_keys = {
        "title", "type", "author", "editor", "issued", "DOI", "URL", "container-title",
        "publisher", "page", "note", "language", "accessed", "abstract",
        "title-short", "genre", "event", "keywords"
    }
    for k, v in csl_item.items():
        if k not in standard_keys:
            zotero_item["extra"] = zotero_item.get("extra", "") + f"\n{k}: {v}"
