# Progress

Root-wake catalog lines show leaf grain as `N: ./path` from the existing `git ls-files` pass, with no per-store walk.

**Complexity:** Level 2

## 2026-09-15 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified catalog grain counts as Level 2 (simple enhancement of `catalog_text`).
    - Wrote the project brief from the approved intent plus the fast-count constraint.
* Decisions made
    - Not a bug fix; self-contained listing change; counting design already chosen (filename grain, one ls-files pass).
    - Digit padding, Usage-on-pull, pack `xN`, and topic-filing `note --path` stay out.
* Insights
    - `started_stores` already scans every git-visible `/.summem/` path and discards the filename; grain is in those names.
    - Original `store_stats` (file-backend) walked each store’s `notes/` and `naps/`; PR #10 inverted `test_catalog_count_preserves_folded_note_grain` when counts were stripped.

## 2026-09-15 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 TDD plan: `_listed_store_grains` one pass, catalog `N: ./path`, how-to `./` token, surgical briefing.
* Decisions made
    - `catalog_text` must not also call `started_stores` (that would `ls-files` twice).
    - Filename-only grain is an accepted overcount for leftover variants/index; tests pin the healed fold path.
    - Out-of-scope `note --path <catalog>` draft is dropped, not shipped.
* Insights
    - Root `.summem/…` paths do not contain `/.summem/`; root still enters `started_stores` via `is_store`.
