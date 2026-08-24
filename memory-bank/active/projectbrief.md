# Project Brief

## User Story

As a consumer of the copied `summem` script, I want unused production helpers removed so the driver stays lean.

## Use-Case(s)

### Use-Case 1

Delete `equal_grain_pair` from `summem`. `fold_request` keeps its own adjacent-same-grain walk.

### Use-Case 2

Fold tests keep the same pins and nap-cascade oracles, using a local copy of the four-line selector instead of a production symbol.

## Requirements

1. Delete `equal_grain_pair` from `summem`.
2. Keep the same four-line adjacent-same-grain walk in `tests/test_fold.py` (local helper or inline).
3. Existing pins and nap-cascade oracles stay; they stop importing a production symbol.
4. Do not wire `fold_request` to call the helper.

## Constraints

1. Work only on `feat/drop-equal-grain-pair` in this worktree.
2. Do not reformat `summem`.
3. TDD: move the helper into the test module before (or in the same change after) tests use the local copy.
4. Suite via `tox` / `uv`, not bare `python3`.

## Acceptance Criteria

1. `summem` has no `equal_grain_pair`.
2. `fold_request` still walks adjacent same-leaf-count nodes itself.
3. `tests/test_fold.py` still pins oldest pair, 16+1 none, 8+8 not 16+8, 1+1 not 2+1, duplicate ids, and the two cascade oracles.
4. Full `tox` suite passes.
