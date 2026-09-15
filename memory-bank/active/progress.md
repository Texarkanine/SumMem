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

## 2026-09-15 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the Level 2 plan against the current catalog implementation, test suites, dependency use by `migrate.py`, and catalog documentation.
* Decisions made
    - Preflight result: PASS WITH ADVISORY.
    - Preserve the explicit removal of the uncommitted out-of-scope `note --path <catalog>` Usage draft during the planned wording change.
* Insights
    - The plan's single-scan helper keeps `started_stores()` compatible with migrate while preventing root `catalog_text()` from invoking `git ls-files` twice.

## 2026-09-15 - BUILD - COMPLETE

* Work completed
    - Catalog lines are `N: ./path` from filename grain on the existing ls-files pass.
    - How-to teaches the `./` token; `note --path` draft removed.
    - Briefing updated; full matrix 393 passed py311–py314.
* Decisions made
    - Root membership stays `is_store` only, not indexed `.summem/` paths.
    - Exact-line catalog tests pin `N: ./rel`, not a bare `./rel` line.
* Insights
    - `in lines` is not a suffix check; `./pkg` as a whole line disappeared once the prefix landed.

## 2026-09-15 - QA - COMPLETE

* Work completed
    - Semantic review of build diff (`summem`, tests, docs, systemPatterns) against plan and project brief.
    - Spot-reran `tests/test_scopes.py` and `tests/test_init.py` under py311: 52 passed.
* Decisions made
    - QA result: PASS. No KISS/DRY/YAGNI/completeness/regression/integrity/documentation findings block acceptance.
* Insights
    - `started_stores()` delegating to `_listed_store_grains` removed the prior duplicated scan without changing its `list[Path]` contract, satisfying both the DRY and migrate-compatibility constraints in one move.

## 2026-09-15 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-catalog-grain-count.md`.
    - Reconciled persistent files (systemPatterns already updated in build).
* Decisions made
    - No further persistent-file edits.
* Insights
    - Nested discovery is `/.summem/`; root-relative `.summem/` is a different shape.

