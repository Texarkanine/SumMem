# Current Task: named-ids-tree-errors

**Complexity:** Level 1

## Fix

- **What broke:** `named_ids` used a narrower except than `_TREE_PARSE_ERRORS` and omitted `AttributeError`.
- **Why:** `_tree_from_dict` calls `child.get("type")`. A valid-JSON tree whose child is not a mapping (`{"c":[1]}`) raises `AttributeError`. `zoom_text` calls `named_ids` first, so `summem zoom` aborted with a traceback. Invalid-JSON tests (`{not json`) already hit `ValueError` and hid the gap.
- **What changed:** `except _TREE_PARSE_ERRORS:` in `named_ids`, same as the other tree readers.
- **Files:** `summem` (one line), `tests/test_zoom.py` (three tests).
- **Verify:** three new tests red then green; `tox` 278 passed on py311–py314.

## QA Results

**Result:** PASS

- `named_ids` now uses `except _TREE_PARSE_ERRORS:` (includes `AttributeError`), matching the other tree readers and issue #40. Surgical one-line change; no reformat.
- Tests cover the reproducing payload `{"c":[1]}`: `named_ids` does not raise; zoom of that pack is `unreadable pack`; zoom of a sibling nested id still works and warns `skipped a pack`. Existing `{not json` cases remain.
- Advisory (does not block): no dedicated `recall_text` test for a non-mapping child. `recall_text` calls `named_ids` first, and that gate is tested. `recall_text`'s own tree walk already used `_TREE_PARSE_ERRORS`.
- No KISS/DRY/YAGNI/integrity/docs blockers. VISION.md, ROADMAP.md, and `milestones.md` were not created.
