# Active Context

## Current Task: equal-grain
**Phase:** QA - COMPLETE (FAIL)

## What Was Done
- Carry-stable nap stems, equal-grain picker plus catch-up, in-memory wake expand, contract wording
- Files: `.summem/summem`, `tests/test_fold.py`, `tests/test_wake_expand.py`, `tests/test_wake.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_view.py`, `tests/test_zoom.py`, `tests/test_recall.py`, `tests/test_proof_conflict.py`, `tests/test_proof_squash.py`, `tests/test_proof_branches.py`, `VISION.md`, `ROADMAP.md`, `memory-bank/systemPatterns.md`
- `ProjectedNode` is the printed row; `ViewNode` stays the storage row. `fold_request` uses file count. Expand writes nothing.
- Proof 4 is 64/32/4. Caption proofs pin `WAKE_LINES` to file count.
- Full suite: 99 passed

## Deviations from Plan
- `ProjectedNode` also holds `tree_path` so file-backed naps can load `.tree` without mixing into `write_nap`
- Added `test_unreadable_tree_does_not_split` (preflight wait-free requirement)
- Proof 2 post-nap wake is in-process with a pinned budget instead of subprocess `wake`

## Next Step
- Build rework: wait-free nested-tree fallback, one-load cache, VISION cover vs later
