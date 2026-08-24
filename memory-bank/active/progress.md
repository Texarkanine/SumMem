# Progress

`named_ids` omits `AttributeError` from `_TREE_PARSE_ERRORS`, so a children file whose child is not a mapping can abort `summem zoom` with a traceback. Align that except with the other tree readers.

**Complexity:** Level 1

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed the mismatch on `feat/named-ids-tree-errors` at `c003779`
    - Classified Level 1 (single-function bug fix)
* Decisions made
    - Parent-approved restatement: `except _TREE_PARSE_ERRORS:` in `named_ids`
    - Close-without-PR only if the bug is not real; it is real
* Insights
    - Existing unreadable-tree tests use invalid JSON, which `named_ids` already swallows

## 2026-08-24 - BUILD - COMPLETE

* Work completed
    - Failing tests for `{"c":[1]}` then one-line `except _TREE_PARSE_ERRORS:` in `named_ids`
    - Full `tox` 278 passed (py311–py314)
* Decisions made
    - Tests live in `test_zoom.py` next to the existing unreadable-sibling cases
    - No CLI-only test: `zoom_text` is the CLI path and already covers the abort
* Insights
    - `JSONDecodeError` ⊂ `ValueError`, so `{not json` never exercised `AttributeError`
