# Current Task: named-ids-tree-errors

**Complexity:** Level 1

## Fix

- **What broke:** `named_ids` used a narrower except than `_TREE_PARSE_ERRORS` and omitted `AttributeError`.
- **Why:** `_tree_from_dict` calls `child.get("type")`. A valid-JSON tree whose child is not a mapping (`{"c":[1]}`) raises `AttributeError`. `zoom_text` calls `named_ids` first, so `summem zoom` aborted with a traceback. Invalid-JSON tests (`{not json`) already hit `ValueError` and hid the gap.
- **What changed:** `except _TREE_PARSE_ERRORS:` in `named_ids`, same as the other tree readers.
- **Files:** `summem` (one line), `tests/test_zoom.py` (three tests).
- **Verify:** three new tests red then green; `tox` 278 passed on py311–py314.
