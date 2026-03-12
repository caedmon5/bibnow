
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
        "encyclopediaArticle": "encyclopediaTitle",
        "tvBroadcast": "programTitle",
        "radioBroadcast": "programTitle",
        "podcast": "seriesTitle",
        "blogPost": "blogTitle",
        "forumPost": "forumTitle",
        "webpage": "websiteTitle"
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
    """Maps CSL 'publisher' to Zotero field (university, institution, network, or publisher)."""
    val = csl_item.get("publisher")
    if not val:
        return
    if item_type == "thesis":
        zotero_item["university"] = val
    elif item_type == "report":
        zotero_item["institution"] = val
    elif item_type in ("tvBroadcast", "radioBroadcast"):
        zotero_item["network"] = val
    elif item_type == "film":
        zotero_item["distributor"] = val
    elif item_type == "computerProgram":
        zotero_item["company"] = val
    elif item_type == "videoRecording":
        zotero_item["studio"] = val
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
    elif item_type == "presentation":
        zotero_item["presentationType"] = genre
    elif item_type == "film":
        zotero_item["genre"] = genre
    elif item_type == "webpage":
        zotero_item["websiteType"] = genre
    elif item_type == "letter":
        zotero_item["letterType"] = genre
    elif item_type == "manuscript":
        zotero_item["manuscriptType"] = genre
    elif item_type == "map":
        zotero_item["mapType"] = genre
    elif item_type == "forumPost":
        zotero_item["postType"] = genre
    else:
        zotero_item["extra"] = zotero_item.get("extra", "") + f"\ngenre: {genre}"

def map_event(csl_item, zotero_item, item_type):
    """Maps CSL 'event' or 'event-title' to Zotero conference/meeting field."""
    event = csl_item.get("event") or csl_item.get("event-title")
    if not event:
        return
    if item_type == "conferencePaper":
        zotero_item["conferenceName"] = event
    elif item_type == "presentation":
        zotero_item["meetingName"] = event

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

    # Case name: prefer explicit CSL 'caseName', else fall back to 'title'
    if csl_item.get("caseName"):
        zotero_item["caseName"] = csl_item["caseName"]
    elif csl_item.get("title"):
        zotero_item["caseName"] = csl_item["title"]
    # Ensure plain 'title' does not linger and get echoed into 'extra'
    zotero_item.pop("title", None)

    # Optionally map other legal-specific fields if needed
    if "URL" in csl_item:
        zotero_item["url"] = csl_item["URL"]
    # Court: prefer explicit 'court' if present, else fall back to 'authority'
    court_val = csl_item.get("court") or csl_item.get("authority")
    if court_val:
        zotero_item["court"] = court_val
    if "issued" in csl_item:
        date_parts = csl_item.get("issued", {}).get("date-parts")
        if date_parts and isinstance(date_parts, list):
            try:
                parts = date_parts[0]
                if len(parts) == 3:
                    zotero_item["dateDecided"] = f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
                elif len(parts) == 2:
                    zotero_item["dateDecided"] = f"{parts[0]:04d}-{parts[1]:02d}"
                elif len(parts) == 1:
                    zotero_item["dateDecided"] = f"{parts[0]:04d}"
            except Exception:
                zotero_item["dateDecided"] = csl_item["issued"].get("raw", "")
        else:
            zotero_item["dateDecided"] = csl_item["issued"].get("raw", "")
        
    # Handle CSL 'page' or 'pages' → Zotero 'firstPage'
    if "page" in csl_item or "pages" in csl_item:
        page_val = csl_item.get("page") or csl_item.get("pages")
        if isinstance(page_val, str):
            # If it's a range like '112–120', extract the first page
            zotero_item["firstPage"] = page_val.split("-")[0].strip()
        else:
            zotero_item["firstPage"] = str(page_val)


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
    """Presentation event mapping now handled by map_event. Kept for API compat."""
    pass

def map_interview_fields(csl_item, zotero_item, item_type):
    """Medium mapping now handled by map_medium. Kept for API compat."""
    pass

def map_audio_fields(csl_item, zotero_item, item_type):
    """Medium mapping now handled by map_medium. Kept for API compat."""
    pass

def map_video_fields(csl_item, zotero_item, item_type):
    """Medium mapping now handled by map_medium. Kept for API compat."""
    pass

# === Common fields ===

def map_doi(csl_item, zotero_item, item_type):
    if "DOI" in csl_item:
        zotero_item["DOI"] = csl_item["DOI"]

def map_url(csl_item, zotero_item, item_type):
    if "URL" in csl_item:
        zotero_item["url"] = csl_item["URL"]

def map_pages(csl_item, zotero_item, item_type):
    if item_type == "case":
        return  # 'pages' is not valid for Zotero case
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
        elif "date-parts" in csl_item["accessed"]:
            dp = csl_item["accessed"]["date-parts"][0]
            zotero_item["accessDate"] = "-".join(str(d) for d in dp if d is not None)

def map_volume(csl_item, zotero_item, item_type):
    """Maps CSL 'volume' to Zotero 'volume'."""
    val = csl_item.get("volume")
    if val:
        zotero_item["volume"] = str(val)

def map_issue(csl_item, zotero_item, item_type):
    """Maps CSL 'issue' to Zotero 'issue'."""
    val = csl_item.get("issue")
    if val:
        zotero_item["issue"] = str(val)

def map_edition(csl_item, zotero_item, item_type):
    """Maps CSL 'edition' to Zotero 'edition'."""
    val = csl_item.get("edition")
    if val:
        zotero_item["edition"] = str(val)

def map_isbn(csl_item, zotero_item, item_type):
    """Maps CSL 'ISBN' to Zotero 'ISBN'."""
    val = csl_item.get("ISBN")
    if val:
        zotero_item["ISBN"] = val

def map_issn(csl_item, zotero_item, item_type):
    """Maps CSL 'ISSN' to Zotero 'ISSN'."""
    val = csl_item.get("ISSN")
    if val:
        zotero_item["ISSN"] = val

def map_number(csl_item, zotero_item, item_type):
    """Maps CSL 'number' to appropriate Zotero field."""
    val = csl_item.get("number")
    if not val:
        return
    number_map = {
        "report": "reportNumber",
        "tvBroadcast": "episodeNumber",
        "radioBroadcast": "episodeNumber",
        "podcast": "episodeNumber",
        "patent": "patentNumber",
        "bill": "billNumber"
    }
    target = number_map.get(item_type)
    if target:
        zotero_item[target] = str(val)
    else:
        zotero_item["extra"] = zotero_item.get("extra", "") + f"\nnumber: {val}"

def map_medium(csl_item, zotero_item, item_type):
    """Maps CSL 'medium' to type-appropriate Zotero field."""
    val = csl_item.get("medium")
    if not val:
        return
    medium_map = {
        "interview": "interviewMedium",
        "audioRecording": "audioRecordingFormat",
        "videoRecording": "videoRecordingFormat",
        "tvBroadcast": "videoRecordingFormat",
        "radioBroadcast": "audioRecordingFormat",
        "artwork": "artworkMedium"
    }
    target = medium_map.get(item_type)
    if target:
        zotero_item[target] = val
    else:
        zotero_item["extra"] = zotero_item.get("extra", "") + f"\nmedium: {val}"

def map_place(csl_item, zotero_item, item_type):
    """Maps CSL 'event-place' or 'publisher-place' to Zotero 'place'."""
    val = csl_item.get("event-place") or csl_item.get("publisher-place")
    if val:
        zotero_item["place"] = val

def map_number_of_pages(csl_item, zotero_item, item_type):
    """Maps CSL 'number-of-pages' to Zotero 'numPages'."""
    val = csl_item.get("number-of-pages")
    if val:
        zotero_item["numPages"] = str(val)

def map_series(csl_item, zotero_item, item_type):
    """Maps CSL 'collection-title' / 'collection-number' to Zotero series fields."""
    title = csl_item.get("collection-title")
    number = csl_item.get("collection-number")
    if title:
        if item_type in ("book", "bookSection", "conferencePaper"):
            zotero_item["series"] = title
        else:
            zotero_item["seriesTitle"] = title
    if number:
        zotero_item["seriesNumber"] = str(number)

def map_tags(csl_item, zotero_item, item_type):
    """
    Map CSL keywords to Zotero tags.
    Accept both singular 'keyword' (array/string) and plural 'keywords'.
    """
    kw = csl_item.get("keyword") or csl_item.get("keywords")
    if not kw:
        return
    if isinstance(kw, list):
        tags = [str(t).strip() for t in kw]
    else:
        tags = [t.strip() for t in str(kw).split(",")]
    zotero_item["tags"] = [{"tag": t} for t in tags if t]

def map_extra_fields(csl_item, zotero_item, item_type):
    """Catch-all for nonstandard CSL fields."""
    standard_keys = {
        "title", "type", "author", "editor", "issued", "DOI", "URL", "container-title",
        "publisher", "page", "note", "language", "accessed", "abstract",
        "title-short", "genre", "event", "event-title", "event-place", "keywords",
        "keyword", "id", "section", "category", "topic",
        "caseName", "court", "authority",
        "volume", "issue", "edition", "ISBN", "ISSN", "number", "medium",
        "publisher-place", "number-of-pages", "collection-title", "collection-number"
    }
    for k, v in csl_item.items():
        if k not in standard_keys:
            zotero_item["extra"] = zotero_item.get("extra", "") + f"\n{k}: {v}"
