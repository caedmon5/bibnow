# obsidian_writer_config.py

import os
from config import OBSIDIAN_VAULT_PATH

OUTPUT_DIR = OBSIDIAN_VAULT_PATH  # write directly into Obsidian vault

FILENAME_PREFIX = "LN "           # required: matches your canonical style
USE_ET_AL = True                  # include 'et al.' if multiple authors
TITLE_WORD_LIMIT = 4              # for title_short
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "obsidian_note.md.tmpl")
