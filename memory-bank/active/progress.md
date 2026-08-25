# Progress

Rename nap caption files from `.sum` to `.summ` in the script, tests, docs, and this repo’s stores. Put a verified `find … -exec` migration recipe in the PR body for the squash-merge `BREAKING CHANGES:` footer.

**Complexity:** Level 2

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified as Level 2 (small self-contained enhancement)
    - Wrote ephemeral memory-bank files
* Decisions made
    - Migration recipe is PR-body only; operator will attach it to the squash-merge `BREAKING CHANGES:` footer
    - Store directory stays `.summem/`; only the caption suffix changes
* Insights
    - `.sum` collides with checksum files; `.summ` implies both summary and summem
