# config.py
import os
from dotenv import load_dotenv

# Auto-load .env file if present in project root
load_dotenv()

ZOTERO_API_KEY    = os.getenv("ZOTERO_API_KEY")
LIBRARY_TYPE      = os.getenv("ZOTERO_LIBRARY", "user").lower()  # "user" | "group"
ZOTERO_USER_ID    = os.getenv("ZOTERO_USER_ID")
ZOTERO_USERNAME   = os.getenv("ZOTERO_USERNAME")
ZOTERO_GROUP_ID   = os.getenv("ZOTERO_GROUP_ID")
OBSIDIAN_VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/home/youruser/wealtheow/LN Literature Notes")

# Optional per-user overrides without editing repo files.
try:
    from config_local import *  # noqa: F401,F403
except Exception:
    pass

# Minimal validation with clear messages
def _die(msg: str):
    raise RuntimeError(f"[config] {msg}")

if not ZOTERO_API_KEY:
    _die("ZOTERO_API_KEY is not set. Copy .env.example to .env and fill it in.")

if LIBRARY_TYPE not in {"user", "group"}:
    _die("ZOTERO_LIBRARY must be 'user' or 'group'.")

if LIBRARY_TYPE == "user":
    if not ZOTERO_USER_ID or not ZOTERO_USERNAME:
        _die("For ZOTERO_LIBRARY=user, set both ZOTERO_USER_ID (numeric) and ZOTERO_USERNAME (string).")
else:
    if not ZOTERO_GROUP_ID:
        _die("For ZOTERO_LIBRARY=group, set ZOTERO_GROUP_ID (numeric).")

