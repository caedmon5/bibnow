# Fallback Lockpoint: citeproc-patch integration

**Tag:** v1.3.0-citeproc-patch  
**Branch:** fallback-citeproc-patch  
**Date:** 2025-07-02  
**Commit Summary:**
- Restores full bib_to_csl() functionality with extended BibTeX field support
- Patches citeproc-py to handle missing quote terms
- Adds CSL patching for punctuation-in-quote option
- Safe end-to-end bibnow --commit pipeline

This version is stable and suitable as a rollback base.
