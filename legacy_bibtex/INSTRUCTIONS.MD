# 📘 Instruction Manual: `biblio_mobile_pipeline_v1`

## ℹ️ What Is This?

`biblio_mobile_pipeline_v1` is a lightweight, cross-platform tool (currently Linux and Android) that allows users to create bibliographic records **simultaneously** in **Zotero** (a bibliographic management application) and **Obsidian** (a markdown-based knowledge management tool).

The script is designed for researchers and students who want to capture, organise, and annotate bibliographic references seamlessly across desktop and mobile devices.

`biblio_mobile_pipeline_v1` accepts a bibliographic entry in **BibTeX** format — a widely supported citation format exported by most academic databases, journals, and citation managers — and outputs:

- ✅ A properly formatted entry in your Zotero library (via the Zotero API)
- ✅ A well-structured markdown literature note (with a public Zotero link) in your Obsidian vault

This enables researchers to maintain a clean, canonical bibliographic record for citation (via **Zotero**) while linking it to a personal reading and annotation space (via **Obsidian**).

### Why use this instead of Zotero or Obsidian alone?

`biblio_mobile_pipeline_v1` allows you to add records **simultaneously** to both Zotero and Obsidian, ensuring synchronisation between the two systems. It is significantly faster than either tool’s graphical user interface (GUI) for entering structured bibliographic information — especially when working from mobile devices.

When used with AI-generated BibTeX (see below), the results are often richer and more accurate than those imported via browser plugins — particularly for blogs, videos, and other nonstandard media.

Additional advantages:

- ✅ Automatically generates **clean, reusable YAML** headers
- ✅ Embeds **public Zotero links** directly in the Obsidian note
- ✅ Keeps Obsidian and Zotero records **in sync and canonical**
- ✅ Accepts input from clipboard or file, with **no GUI required**
- ✅ Compatible with automation pipelines, Git-based vaults, and mobile workflows

---

## 🔧 Required Software and Setup

Before beginning, ensure you have the following accounts and services set up. These are essential for syncing across devices and enabling Zotero/Obsidian integration.

### Accounts and Services

- ✅ **Zotero** ([https://www.zotero.org](https://www.zotero.org))

  - Free account required to store and sync your library
  - Go to **Settings → Feeds/API** to generate a **Zotero API key** (save this to a file as you will need it later)
  - You will also need:
    - Your **numeric Zotero user ID** (found in API settings)
    - Your **Zotero username** (for constructing public URLs)

- ✅ **Obsidian** ([https://obsidian.md](https://obsidian.md))

  - Install the app locally on each system
  - Create or identify a synced vault for storing output
  - You can sync across devices using:
    - Obsidian Sync (paid)
    - Git, Dropbox, or Syncthing (free alternatives)

- ✅ **GitHub** (optional, recommended)

  - Used to download the script and optionally suggest improvements

- ✅ **AI Chatbot** (e.g., ChatGPT, Gemini)

  - Not required by the script, but useful for generating or cleaning BibTeX input

This manual assumes minimal command-line experience and provides full instructions.

### Software

You will also need the following software:

- ✅ **This script**: [`biblio_mobile_pipeline_v1`](https://github.com/caedmon5/biblio_mobile_pipeline_v1)

  - There are two version series:
    - **v0.2.x** — Android-compatible, plain citation formatting
    - **v0.3.x** — Linux-compatible, supports citation styling and fallback quotes
  - The output is cross-compatible: notes generated on Android with `v0.2.0` can be used alongside those from `v0.3.0` on Linux.
  - You will choose the version you need in the installation step.

- ✅ **Terminal or command-line interface**

  - **Linux**: Use *Terminal*, *Konsole*, or *xterm*
  - **Android**: Install [Termux](https://f-droid.org/packages/com.termux/)

- ✅ **Python 3.11+**

  - Linux:
    ```bash
    sudo apt install python3.11 python3-pip
    ```
  - Android/Termux:
    ```bash
    pkg install python
    ```

- ✅ **Git**

  - Linux:
    ```bash
    sudo apt install git
    ```
  - Android/Termux:
    ```bash
    pkg install git
    ```

---

## 🚀 Installation Procedure

### 1. Clone the Repository

You will need to choose which version branch to use:

- 📱 Use `v0.2-stable` if you are on **Android (Termux)** and require compatibility with Python 3.12
- 🖥️ Use `v0.3-stable` if you are on **Linux** and want fully formatted citations (CSL + quote support)

You can clone the repo with:

```bash
# For Android (v0.2.x)
git clone --branch v0.2-stable https://github.com/caedmon5/biblio_mobile_pipeline_v1.git

# For Linux (v0.3.x)
git clone --branch v0.3-stable https://github.com/caedmon5/biblio_mobile_pipeline_v1.git

cd biblio_mobile_pipeline_v1
```

If you want to browse or switch branches after cloning, use:

```bash
git branch -a              # show available branches
git checkout v0.2-stable   # or v0.3-stable
```

When you open a terminal (Linux) or Termux (Android), you'll normally start in your home directory (`~/`). Unless you manage projects in a custom structure, cloning the repo there is fine.

```bash
git clone https://github.com/caedmon5/biblio_mobile_pipeline_v1.git
cd biblio_mobile_pipeline_v1
```

### 2. Configure `config.py`

Before running the script, you must configure the file `config.py`. This file stores your personal Zotero credentials and the path to your Obsidian vault.

1. Open the `config.py` file in your editor:

   ```bash
   nano config.py
   ```

2. Replace the placeholder values with your actual information:

   ```python
   ZOTERO_API_KEY = "your-zotero-api-key"
   ZOTERO_USER_ID = "your-zotero-user-id"         # numeric ID
   ZOTERO_USERNAME = "your-zotero-username"       # lowercase username

   OBSIDIAN_VAULT_PATH = "/full/path/to/your/vault"

   BIBLIO_STYLE = "/full/path/to/csl/chicago-author-date.csl"  # only for v0.3+
   ```

   If you are using version `v0.2.x`, the `BIBLIO_STYLE` line is not used and can be left blank or removed.

---

### 3. Install Python Dependencies

Before running the script, you must configure the file `config.py`. This file stores your personal Zotero credentials and the path to your Obsidian vault.

1. Open the `config.py` file in your editor:

   ```bash
   nano config.py
   ```

2. Replace the placeholder values with your actual information:

   ```python
   ZOTERO_API_KEY = "your-zotero-api-key"
   ZOTERO_USER_ID = "your-zotero-user-id"         # numeric ID
   ZOTERO_USERNAME = "your-zotero-username"       # lowercase username

   OBSIDIAN_VAULT_PATH = "/full/path/to/your/vault"

   BIBLIO_STYLE = "/full/path/to/csl/chicago-author-date.csl"  # only for v0.3+
   ```

   If you are using version `v0.2.x`, the `BIBLIO_STYLE` line is not used and can be left blank or removed.

Once the config is set:

```bash
pip install -r requirements.txt
```

If using `v0.3.0+` on Linux, make sure `lxml` is installed:

```bash
pip install lxml
```

```bash
pip install -r requirements.txt
```

If using `v0.3.0+` on Linux, make sure `lxml` is installed:

```bash
pip install lxml
```

---

## 🔁 Create a `bibnow` Command Alias (Optional)

You can run the script directly using:

```bash
python biblio_pipeline.py        # preview
python biblio_pipeline.py --commit  # upload and write
```

To simplify usage, we recommend creating a `bibnow` alias or script:

### A. Android (Termux) — easiest

Edit your shell config:

```bash
nano ~/.bashrc    # or ~/.zshrc
```

Add this line:

```bash
alias bibnow='python ~/git/biblio_mobile_pipeline_v1/biblio_pipeline.py'
```

Apply the changes:

```bash
source ~/.bashrc
```

Then run:

```bash
bibnow          # preview mode
bibnow --commit # writes to Zotero and Obsidian
```

### B. Linux (with virtualenv or conda)

```bash
echo '#!/bin/bash
source /path/to/venv/bin/activate
python /path/to/biblio_pipeline.py "$@"' > ~/bin/bibnow
chmod +x ~/bin/bibnow
```

Ensure `~/bin` is in your PATH.

### C. Linux (no virtualenv)

```bash
echo '#!/bin/bash
python3 /full/path/to/biblio_pipeline.py "$@"' > ~/bin/bibnow
chmod +x ~/bin/bibnow
```

This works if your system Python has all required packages installed globally.

---

## 🧪 Test the Installation

Once your environment is set up, test that everything is working correctly.

### 1. Create a test BibTeX entry

Paste the following BibTeX entry into your clipboard, or save it to a file called `input.txt` in your repo directory:

```bibtex
@article{Test2025Quotes,
  author = {Doe, Jane},
  title = {Testing “Smart Quotes” in CSL Output},
  journal = {Journal of Testing},
  volume = {12},
  number = {3},
  pages = {45--67},
  date = {2025-04},
}
```

### 2. Run the script in preview mode

```bash
bibnow --dryrun
```

You should see terminal output similar to this:

```text
📋 Clipboard input (Linux) detected and loaded.
🚦 Running in DRYRUN mode.
✅ Parsed citekey: Doe2025TestingSmart
📄 Preview output:
---
citekey: "Doe2025TestingSmart"
type: "article"
---
# Chicago Author-Year  Bibliography
Doe, Jane. 2025. “Testing “Smart Quotes” in CSL Output.” *Journal of Testing* 12(3): 45–67.
...
```

Confirm:

- ✅ You get a parsed citekey
- ✅ A Markdown preview is shown
- ✅ No errors appear (especially no `lxml`, `locales.json`, or CSL errors)

### 3. (Optional) Test a second format

```bibtex
@incollection{Doe2025EdBook,
  author    = {Doe, Jane},
  title     = {Smart Quotes and Citation Logic},
  booktitle = {Styles and Formats in the Digital Age},
  editor    = {Green, Sam and Taylor, Robin},
  publisher = {Routledge},
  year      = {2025},
  pages     = {55--70},
  address   = {New York}
}
```

Run:

```bash
bibnow --dryrun
```

You should see output like this:

```text
✅ Parsed citekey: Doe2025EdBook
📄 Preview output:
---
citekey: "Doe2025EdBook"
type: "incollection"
---
# Chicago Author-Year  Bibliography
Doe, Jane. 2025. “Smart Quotes and Citation Logic.” In *Styles and Formats in the Digital Age*, edited by Sam Green and Robin Taylor, 55–70. New York: Routledge.
...
```

This confirms proper formatting of book chapters and edited volumes.

If both tests pass, you're ready to begin full use with `--commit`.

---

## ✅ Final Checklist Before Use

- If something goes wrong, asking a chatbot to help is always a good move: AI-based chatbots are excellent at helping you understand error messages. Below are some common issues, however.

---

## ❌ What to Do If It Fails

Here are some common problems and how to fix them:

- ``

  - You're on Linux and haven't installed `lxml` yet:
    ```bash
    pip install lxml
    ```
  - On Android, `lxml` is not supported for Python 3.12+ — use branch `v0.2-stable` instead.

- `` or ``

  - Check that your `config.py` exists and is filled out with real values.

- ``

  - Your API key may be wrong or not have write access. Regenerate and paste it into `config.py`.

- **No file created, or preview ends early**

  - Check for missing fields in your BibTeX. All entries must have `author`, `title`, and `date`.

If you’re stuck, try running:

```bash
bibnow --dryrun > debug.txt
```

and send that file to a helper or save for troubleshooting.

