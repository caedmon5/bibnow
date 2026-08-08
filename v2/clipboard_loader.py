# clipboard_loader.py

import platform
import os
import subprocess
from pathlib import Path

# Anchor the input file to the repo root rather than the working directory.
# The bare relative path "input.txt" meant that running the documented
# `python3 v2/pipeline.py` from the repo root read ./input.txt, while running
# it from v2/ read a different file — so a stale scratch file could be
# processed silently in place of the intended entries.
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_PATH = REPO_ROOT / "input.txt"

def detect_platform():
    """
    Returns one of: 'windows', 'macos', 'ios', 'ipad', 'android-termux', 'android', 'linux', 'unknown'
    """
    sysname = platform.system()
    machine = platform.machine()
    env_home = os.environ.get("HOME", "")

    if sysname == "Windows":
        return "windows"
    elif sysname == "Darwin":
        plat = platform.platform()
        if "iPhone" in plat:
            return "ios"
        if "iPad" in plat:
            return "ipad"
        return "macos"
    elif sysname == "Linux":
        if "com.termux" in env_home:
            return "android-termux"
        if "ANDROID_STORAGE" in os.environ:
            return "android"
        return "linux"
    else:
        return "unknown"

def _looks_like_json(s: str) -> bool:
    s = s.strip()
    return s.startswith("{") or s.startswith("[")

def load_clipboard_or_file(filepath=None):
    """
    Attempts to read JSON/BibTeX from clipboard (Linux or Termux), or falls back to input.txt.

    `filepath` defaults to <repo root>/input.txt, independent of the working
    directory. Pass an explicit path to override.
    """
    filepath = Path(filepath) if filepath else DEFAULT_INPUT_PATH
    platform_type = detect_platform()

    if platform_type == "linux":
        try:
            import pyperclip
            content = (pyperclip.paste() or "").strip()
            if _looks_like_json(content):
                print("📋 Clipboard input (Linux) loaded.")
                # mirror to file for auditability
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return content
            elif "@article" in content or "@book" in content or "@inproceedings" in content:
                # save BibTeX for reference but do not return it (v2 is JSON-only)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print("⚠️ Detected BibTeX in clipboard; v2 expects CSL JSON. Falling back to input.txt.")
                # fall through to file load below
        except Exception as e:
            print(f"⚠️ pyperclip failed: {e}")

    elif platform_type == "android-termux":
        try:
            content = subprocess.check_output(["termux-clipboard-get"]).decode("utf-8").strip()
            # always mirror clipboard to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            if _looks_like_json(content):
                print("📋 Clipboard input (Android/Termux) loaded.")
                return content
            elif "@article" in content or "@book" in content or "@inproceedings" in content:
                print("⚠️ Detected BibTeX in clipboard; v2 expects CSL JSON. Falling back to input.txt.")
                # fall through to file load below
            # else: non-JSON, non-BibTeX → fall through
        except Exception as e:
            print(f"❌ Failed to read clipboard: {e}")

    # Fallback to file
    with open(filepath, encoding="utf-8") as f:
        print(f"📄 Loaded input from file: {filepath}")
        return f.read()
