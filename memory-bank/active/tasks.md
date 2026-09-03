# Current Task: wake-omit-empty-catalog

**Complexity:** Level 1

## Fix

- **What broke:** Root `wake` always printed catalog how-to (`Listed catalog lines…`, `wake --path`, “ignore `--path` if there was no catalog”) even when `catalog_text()` was empty.
- **Why:** `how_to_text()` baked that paragraph into every Usage section.
- **What changed:** `how_to_text(*, catalog=False)` omits catalog how-to by default. Root `wake` passes `catalog=bool(cat)`. The leftover “ignore if no catalog” sentence is gone; it only made sense when the paragraph was unconditional. Operator `-h` / bare invocation are unchanged.
- **Files:** `summem`, `tests/test_init.py`, `tests/test_scopes.py`

## QA

✅ PASS. Requirements 1-3 and all three acceptance criteria met; no KISS/DRY/YAGNI/completeness/regression/integrity violations. `tox -e py311 -- tests/test_init.py tests/test_scopes.py -n0`: 43 passed.

Advisories (non-blocking):

1. `memory-bank/systemPatterns.md` line 5 still enumerates "catalog pull" as unconditional `how_to_text` content. Hand to the wrap-up `reconcile-persistent` step.
2. `test_prompt_and_how_to_are_disjoint` duplicates catalog negatives already pinned by two other tests in the same file.
