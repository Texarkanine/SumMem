# Active Context

## Current Task: tree-schema
**Phase:** PLAN - COMPLETE (replan after preflight FAIL (fixable))

## What Was Done

- Preflight FAIL (fixable): missed `endswith(": …")` wake assertions; no negative tests for child `type`.
- Replanned: codec rejects missing/unknown `type`; wake unit lists `test_wake.py`, `test_wake_expand.py`, `test_nap.py`, `test_fold.py`.

## Next Step

Re-run preflight.
