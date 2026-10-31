# Active Context

## Current Task: share-break-children
**Phase:** REFLECT COMPLETE

## What Was Done
- `break_children` in `tests/gitutil.py` is the shared broken-children setup. `missing` unlinks `tree_path`. Any other `how` writes `not a tree`.
- `tests/test_fold.py` and `tests/test_nap.py` call it. No product file changed.
- QA PASS. `tox -e py311` was 420 passed. `tox run-parallel` passed on py311, py312, py313, and py314.
- Reflection is `memory-bank/active/reflection/reflection-89-share-break-children.md`.
- Persistent files were left as they are. This task did not change who the product is for, a system-wide contract, or how to run the suite. A catalog of one test helper does not belong in those files.

## Next Step
- Standing consent stops at reflect. Do not archive.
