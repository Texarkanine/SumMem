# Progress

Print leaf `wake` rows as `x1 (YYYY-MM-DD): text` from the note stamp. Leave nap lines undated. Update the shared printer, tests, and agent-facing copy so leaves are distinct rows and dates are not burned in prose.

**Complexity:** Level 2

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed: dates on leaves only, parenthetical day, `x1` row prefix, no date on naps, no after-colon fake body
    - Classified as Level 2
* Decisions made
    - Level 2: enhancement to one print contract (`format_wake_line` and its callers), not a bug and not a new subsystem
    - Task id: `dated-leaf-wake`
    - Grain-1 packs stay caption-only; only `kind == "note"` is dated
* Insights
    - OptMem already dates leaves only; dating packs with the leftmost stamp would misrepresent span
    - Dates were on every wake line after wake-listing and were dropped in tree-schema; this restores a leaf-only, parenthetical form rather than that old shape

## 2026-08-24 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan: dated leaf printer (TDD) then briefing/prompt lockstep
    - Mapped exact-line tests in `test_wake.py`, `test_wake_expand.py`, and `test_fold.py`
* Decisions made
    - One printer change; zoom and nested recall stay undated `{id}  {text}`
    - Fold CLI tests match `  x1 (` + `): text` so they do not depend on `date.today()`
    - `_day_from_stamp` slices the existing 16-char UTC stamp; no new clock
* Insights
    - `format_wake_line` already feeds wake, expand, recall’s view pass, and fold_request — dating notes there is the whole print surface
    - The 2026-08-19 dated-every-line format is the failure mode to avoid, not the template

## 2026-08-24 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the dated-leaf-wake plan against `summem`, the test tree, and briefing docs
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is acceptable as-is; no TDD step swap or change-detector strike
    - Unlisted `tests/test_proof_ingest.py` exact wake-line set is an advisory, not a blocking gap (`tox` is already the unit-done gate)
* Insights
    - `format_wake_line` already feeds wake, expand, fold, and recall's view pass; recall tests use stored-sentence substrings and stay green
    - `_day_from_stamp` is gone from the script; restoring it is not duplication
    - CLI proof notes use writer-now UTC; retarget that proof from the filename stamp, not `date.today()`

## 2026-08-24 - BUILD - COMPLETE

* Work completed
    - Restored `_day_from_stamp`; `format_wake_line` dates notes only
    - Retargeted wake/expand/fold/ingest exact lines; added grain-1, empty-caption, hyphenated-day, and nested-expand cases
    - Updated systemPatterns, architecture invariant, and prompt lockstep
    - `tox` 272 passed py311–py314
* Decisions made
    - Adopted preflight `dated_leaf` helper in `tests/conftest.py`; ingest proof reads filename stamps
    - Empty-caption and nested-expand got dedicated tests (listed behaviors, not a re-plan)
* Insights
    - Splitting `kind == "note"` from `leaves <= 1` is what keeps a grain-1 pack undated
    - `dated_leaf` and `_day_from_stamp` slice the same 16-char stamp; the unit test on the helper is the lock
