# === Core conditional mappings ===

def map_container_title(csl, zotero, item_type):
    """Maps CSL 'container-title' to appropriate Zotero container field."""
    container = csl.get("container-title")
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
        zotero[target] = container

def map_publisher_field(csl, zotero, item_type):
    """Maps CSL 'publisher' to Zotero field (university, institution, or publisher)."""
    val = csl.get("publisher")
    if not val:
        return
    if item_type == "thesis":
        zotero["university"] = val
    elif item_type == "report":
        zotero["institution"] = val
    else:
        zotero["publisher"] = val

def map_genre(csl, zotero, item_type):
    """Maps CSL 'genre' to Zotero-specific type fields."""
    genre = csl.get("genre")
    if not genre:
        return
    if item_type == "report":
        zotero["reportType"] = genre
    elif item_type == "thesis":
        zotero["thesisType"] = genre
    else:
        zotero["extra"] = zotero.get("extra", "") + f"\ngenre: {genre}"

def map_event(csl, zotero, item_type):
    """Maps CSL 'event' to Zotero 'conferenceName' (only for conferencePaper)."""
    event = csl.get("event")
    if event and item_type == "conferencePaper":
        zotero["conferenceName"] = event

def map_title_short(csl, zotero, item_type):
    """Maps CSL 'title-short' to Zotero 'shortTitle'."""
    short = csl.get("title-short")
    if short:
        zotero["shortTitle"] = short

def map_note(csl, zotero, item_type):
    """Maps CSL 'note' to Zotero 'extra'."""
    note = csl.get("note")
    if note:
        zotero["extra"] = zotero.get("extra", "") + f"\n{note}"

def map_issued_date(csl, zotero, item_type):
    """Maps CSL 'issued' field to Zotero 'date' (prefers raw, falls back to year)."""
    issued = csl.get("issued")
    if not issued:
        return
    if "raw" in issued:
        zotero["date"] = issued["raw"]
    elif "date-parts" in issued:
        dp = issued["date-parts"][0]
        zotero["date"] = "-".join(str(d) for d in dp if d is not None)

# === Legal/Governmental ===

def map_case_fields(csl, zotero, item_type):
    """Maps fields for legal cases."""
    if item_type != "case":
        return
    zotero["caseName"] = csl.get("title", "")
    if "authority" in csl:
        zotero["court"] = csl["authority"]
    if "issued" in csl:
        zotero["dateDecided"] = csl["issued"].get("raw", "")

def map_bill_fields(csl, zotero, item_type):
    """Maps fields for bills."""
    if item_type != "bill":
        return
    for k in ["billNumber", "session", "legislativeBody"]:
        if k in csl:
            zotero[k] = csl[k]

def map_statute_fields(csl, zotero, item_type):
    """Maps fields for statutes."""
    if item_type != "statute":
        return
    for k in ["nameOfAct", "section", "code"]:
        if k in csl:
            zotero[k] = csl[k]

def map_hearing_fields(csl, zotero, item_type):
    """Maps fields for legislative hearings."""
    if item_type != "hearing":
        return
    for k in ["committee", "legislativeBody"]:
        if k in csl:
            zotero[k] = csl[k]

# === Media, interviews, presentations ===

def map_presentation_fields(csl, zotero, item_type):
    if item_type != "presentation":
        return
    if "event" in csl:
        zotero["meetingName"] = csl["event"]

def map_interview_fields(csl, zotero, item_type):
    if item_type != "interview":
        return
    if "medium" in csl:
        zotero["interviewMedium"] = csl["medium"]

def map_audio_fields(csl, zotero, item_type):
    if item_type != "audioRecording":
        return
    if "medium" in csl:
        zotero["audioRecordingFormat"] = csl["medium"]

def map_video_fields(csl, zotero, item_type):
    if item_type != "videoRecording":
        return
    if "medium" in csl:
        zotero["videoRecordingFormat"] = csl["medium"]

# === Common fields ===

def map_doi(csl, zotero, item_type):
    if "DOI" in csl:
        zotero["DOI"] = csl["DOI"]

def map_url(csl, zotero, item_type):
    if "URL" in csl:
        zotero["url"] = csl["URL"]

def map_pages(csl, zotero, item_type):
    if "page" in csl:
        zotero["pages"] = csl["page"]

def map_language(csl, zotero, item_type):
    if "language" in csl:
        zotero["language"] = csl["language"]

def map_abstract(csl, zotero, item_type):
    if "abstract" in csl:
        zotero["abstractNote"] = csl["abstract"]

# === Generic metadata extensions ===

def map_access_date(csl, zotero, item_type):
    if "accessed" in csl:
        if "raw" in csl["accessed"]:
            zotero["accessDate"] = csl["accessed"]["raw"]

def map_tags(csl, zotero, item_type):
    if "keywords" in csl:
        tags = [t.strip() for t in csl["keywords"].split(",")]
        zotero["tags"] = [{"tag": t} for t in tags if t]

def map_extra_fields(csl, zotero, item_type):
    """Catch-all for nonstandard CSL fields."""
    standard_keys = {
        "title", "type", "author", "editor", "issued", "DOI", "URL", "container-title",
        "publisher", "page", "note", "language", "accessed", "abstract",
        "title-short", "genre", "event", "keywords"
    }
    for k, v in csl.items():
        if k not in standard_keys:
            zotero["extra"] = zotero.get("extra", "") + f"\n{k}: {v}"
