# Current Task: wake-omit-empty-catalog

**Complexity:** Level 1

## Fix

- **What broke:** Root `wake` always printed catalog how-to (`Listed catalog lines…`, `wake --path`, “ignore `--path` if there was no catalog”) even when `catalog_text()` was empty.
- **Why:** `how_to_text()` baked that paragraph into every Usage section.
- **What changed:** `how_to_text(*, catalog=False)` omits catalog how-to by default. Root `wake` passes `catalog=bool(cat)`. The leftover “ignore if no catalog” sentence is gone; it only made sense when the paragraph was unconditional. Operator `-h` / bare invocation are unchanged.
- **Files:** `summem`, `tests/test_init.py`, `tests/test_scopes.py`
