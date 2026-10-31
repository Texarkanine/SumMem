# Active Context

## Current Task: share-break-children
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Level 2 plan written for issue #89.
- One executable step: move the broken-children setup to `break_children` in `tests/gitutil.py` and point the fold and nap tests at it.
- No new product behavior. The four existing cases are the red/green lock. No new test file.
- Public name is `break_children`, matching `plant_pack` and `fold_ids`. The else branch stays "write `not a tree`".

## Next Step
- Preflight validation.
