# zotero_query.py

"""
Read-side queries against the Zotero web API.

One job: decide whether a work is already in the library, so the pipeline does
not create a second item for something already filed. The deduplication
protocol in the bibnow skill is a discipline followed while entries are being
written; this is the check that does not depend on anyone remembering.

Why a local index rather than the search endpoint
-------------------------------------------------
Zotero's `q` parameter searches titles, creators, years, and attachment
full text. It does **not** index the DOI or ISBN fields: searching for a DOI
that is demonstrably present on an item returns nothing. Identifier matching —
the only kind strong enough to catch a work whose title has been recorded
differently — therefore has to happen client side.

The library is large enough (~15k items) that fetching it per run is not
viable, so it is cached locally and refreshed incrementally: Zotero returns a
library version with every response, and `?since=<version>` returns only what
has changed since. First build costs a few minutes; steady state costs one
request.

Matching runs strongest-evidence-first:

  1. DOI  — an exact match is treated as the same work.
  2. ISBN — same, for books.
  3. Title + first author surname + year — the fallback for anything with no
            identifier. Strict about the title, lenient about the year, since
            grey literature and preprints are dated inconsistently across
            sources.

Every match is returned for the caller to report. Nothing is deleted, merged,
or overwritten here.
"""

import json
import re
import unicodedata
from pathlib import Path

import requests

from config import ZOTERO_API_KEY
from zotero_writer import API_BASE

HEADERS = {"Zotero-API-Key": ZOTERO_API_KEY}
PAGE_SIZE = 100
CACHE_PATH = Path(__file__).resolve().parent.parent / ".zotero-index.json"


class ZoteroQueryError(RuntimeError):
    """Raised when the library could not be consulted at all."""


# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------

def _normalise_text(value: str) -> str:
    """Casefold, strip accents and punctuation, collapse whitespace."""
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^\w\s]", " ", value.casefold())
    return re.sub(r"\s+", " ", value).strip()


def _normalise_doi(value: str) -> str:
    """Strip resolver prefixes and case, so a bare DOI and a doi.org URL match."""
    if not value:
        return ""
    value = str(value).strip().casefold()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value.rstrip("/")


def _normalise_isbns(value: str) -> set:
    """Zotero stores several ISBNs in one field; return them all, digits only."""
    if not value:
        return set()
    return {
        re.sub(r"[^0-9xX]", "", token).casefold()
        for token in re.split(r"[\s,;]+", str(value))
        if re.sub(r"[^0-9xX]", "", token)
    }


def _year_of(value: str) -> str:
    match = re.search(r"\b(1\d{3}|2\d{3})\b", str(value or ""))
    return match.group(1) if match else ""


def _first_author_surname(item: dict) -> str:
    creators = item.get("creators") or []
    for creator in creators:
        if creator.get("creatorType") == "author":
            return creator.get("lastName") or creator.get("name") or ""
    for creator in creators:
        return creator.get("lastName") or creator.get("name") or ""
    return ""


def _digest(data: dict) -> dict:
    """The fields the index needs, from a full Zotero item."""
    return {
        "key": data.get("key", ""),
        "itemType": data.get("itemType", ""),
        "title": data.get("title", ""),
        "date": data.get("date", ""),
        "doi": _normalise_doi(data.get("DOI")),
        "isbns": sorted(_normalise_isbns(data.get("ISBN"))),
        "ntitle": _normalise_text(data.get("title")),
        "surname": _normalise_text(_first_author_surname(data)),
        "year": _year_of(data.get("date")),
    }


# --------------------------------------------------------------------------
# index
# --------------------------------------------------------------------------

def _load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {"version": 0, "items": {}}
    try:
        with open(CACHE_PATH, encoding="utf-8") as handle:
            cache = json.load(handle)
        if isinstance(cache.get("items"), dict):
            return cache
    except (OSError, ValueError):
        pass
    return {"version": 0, "items": {}}


def _save_cache(cache: dict) -> None:
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as handle:
            json.dump(cache, handle)
    except OSError as exc:
        print(f"⚠️ Could not write the Zotero index cache: {exc}")


def _get(path: str, params: dict):
    try:
        response = requests.get(
            f"{API_BASE}{path}", headers=HEADERS, params=params, timeout=30
        )
    except requests.exceptions.RequestException as exc:
        raise ZoteroQueryError(f"Zotero request failed: {exc}") from exc
    if response.status_code != 200:
        raise ZoteroQueryError(
            f"Zotero returned {response.status_code}: {response.text[:200]}"
        )
    return response


def refresh_index(verbose: bool = True) -> dict:
    """
    Bring the local index up to date and return it.

    Fetches only items changed since the cached library version, plus the list
    of items deleted since then. Raises ZoteroQueryError if the library cannot
    be reached.
    """
    cache = _load_cache()
    since = cache.get("version", 0)
    first_build = not cache["items"]

    if verbose and first_build:
        print("🔎 Building the Zotero index for the first time (one-off, a few minutes)…")

    start = 0
    fetched = 0
    latest_version = since
    while True:
        response = _get(
            "/items",
            {"since": since, "limit": PAGE_SIZE, "start": start,
             "format": "json", "itemType": "-attachment || note"},
        )
        latest_version = int(response.headers.get("Last-Modified-Version", latest_version))
        batch = response.json()
        if not batch:
            break
        for entry in batch:
            data = entry.get("data", {})
            key = data.get("key")
            if key:
                cache["items"][key] = _digest(data)
        fetched += len(batch)
        if verbose and first_build and fetched % 1000 == 0:
            print(f"   …{fetched} items")
        if len(batch) < PAGE_SIZE:
            break
        start += PAGE_SIZE

    # Drop anything deleted upstream, so stale entries cannot raise false alarms.
    if since:
        deleted = _get("/deleted", {"since": since}).json().get("items", [])
        for key in deleted:
            cache["items"].pop(key, None)

    cache["version"] = latest_version
    _save_cache(cache)

    if verbose and fetched:
        print(f"🔎 Zotero index updated: {fetched} item(s) changed, {len(cache['items'])} total.")
    return cache


# --------------------------------------------------------------------------
# matching
# --------------------------------------------------------------------------

def find_existing_items(zotero_item: dict, index: dict = None) -> list:
    """
    Look for items in the library that appear to be the same work.

    Takes a Zotero-shaped item (post-mapping, pre-upload) and returns a list of
    summary dicts for any matches, strongest evidence first. An empty list means
    no match was found. Raises ZoteroQueryError if the library could not be
    reached and no usable cache exists.
    """
    if index is None:
        index = refresh_index()

    matches = {}

    def remember(entry, reason):
        if entry["key"] not in matches:
            matches[entry["key"]] = {**entry, "matched_on": reason}

    doi = _normalise_doi(zotero_item.get("DOI"))
    isbns = _normalise_isbns(zotero_item.get("ISBN"))
    ntitle = _normalise_text(zotero_item.get("title"))
    surname = _normalise_text(_first_author_surname(zotero_item))
    year = _year_of(zotero_item.get("date"))

    for entry in index["items"].values():
        if doi and entry.get("doi") == doi:
            remember(entry, "DOI")
            continue
        if isbns and isbns.intersection(entry.get("isbns") or []):
            remember(entry, "ISBN")
            continue
        if ntitle and entry.get("ntitle") == ntitle:
            if surname and entry.get("surname") and surname != entry["surname"]:
                continue
            # Absent years on either side are not evidence of difference.
            if year and entry.get("year") and year != entry["year"]:
                continue
            remember(entry, "title + creator + year")

    order = {"DOI": 0, "ISBN": 1, "title + creator + year": 2}
    return sorted(matches.values(), key=lambda m: order.get(m["matched_on"], 9))


def describe_matches(matches: list, username: str = "") -> str:
    """One line per match, for printing to the operator."""
    lines = []
    for match in matches:
        label = f"{match['key']} [{match['itemType']}] {match['title'][:70]}"
        if match.get("date"):
            label += f" ({match['date'][:10]})"
        lines.append(f"   ↳ matched on {match['matched_on']}: {label}")
        if username:
            lines.append(f"     https://www.zotero.org/{username}/items/{match['key']}")
    return "\n".join(lines)
