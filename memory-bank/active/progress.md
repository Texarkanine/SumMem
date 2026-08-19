# Progress

Clean-cut `.tree` JSON (`c` / `type: note|nap`, no `v`) and undated wake lines, as specified in `projectbrief.md`.

**Complexity:** Level 2

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator confirmed and added undated wake
    - Classified Level 2 (self-contained enhancement of codec + wake formatter)
* Decisions made
    - No dual-read of `kids`/`k`/`v`
    - Stay JSON; ignore unknown fields instead of a version field
    - `type` values are the product words `note` and `nap`
    - Wake drops `YYYY-MM-DD`; packs stay `xN <prefix>: caption`
* Insights
    - `k` next to `kids` was the original hole; full-word `type` removes that clash without compact-key theater
    - A `type` field is a discriminator, not a reason to switch to XML
