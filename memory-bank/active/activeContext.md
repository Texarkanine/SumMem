# Active Context

## Current Task: drop-equal-grain-pair
**Phase:** BUILD - COMPLETE

## What Was Done
- Moved the four-line selector into `tests/test_fold.py` as `_equal_grain_pair`.
- Deleted `equal_grain_pair` from `summem`. Did not wire `fold_request` to it.
- Fold tests 21 passed, then full `tox` 275 passed on py311–py314.

## Next Step
- Spawn `/niko-qa`.
