# Active Context

## Current Task: named-ids-tree-errors
**Phase:** COMPLEXITY-ANALYSIS - COMPLETE

## What Was Done
- Verified issue #40 on this worktree: `_TREE_PARSE_ERRORS` includes `AttributeError`; `named_ids` excepts `(OSError, UnicodeDecodeError, ValueError, TypeError, KeyError)` and skips it
- `_tree_from_dict` does `child.get("type")`; a non-mapping child (`{"c":[1]}`) raises `AttributeError`
- Existing skip tests use `{not json` (`JSONDecodeError` ⊂ `ValueError`), so they do not catch this gap
- Classified Level 1: bug fix, single function

## Next Step
- Load Level 1 workflow and enter BUILD
