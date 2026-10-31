---
task_id: 89-share-break-children
date: 2026-10-30
complexity_level: 2
---

# Reflection: share-break-children

## Summary

`break_children` in `tests/gitutil.py` is now the only setup that unlinks a nap's children file or writes `not a tree`. The fold and nap tests call it. The four cases still pass, and the product is unchanged.

## Requirements vs Outcome

Every requirement held. One helper, home in `tests/gitutil.py`, `missing` unlinks, any other `how` writes `not a tree`, and both tests use it. No product change. Nothing was added beyond the move and the SumMem note the script asked to nap.

## Plan Accuracy

The file list and the red/green lock were right. The empty stub failed the way preflight said it would: fold named the grain-2 pair, and nap refused the outer pair. The only sequence catch was that the import cannot be collected until the function exists, so the stub and the call-site edit landed together, and the red run still came before the body. The shared `how` list stayed out so the diff would not touch the parametrize lines issue #88 may edit.

## Build & QA Observations

The red run and the green run were each one `tox -e py311` invocation of the two tests (4 failed, then 4 passed). The full py311 suite was 420 passed. QA passed with no rework. `tox run-parallel` then passed on py311, py312, py313, and py314. This repo has no lint or build target.

## Insights

### Technical

Nothing notable. The else branch was already the unreadable path in both copies, and the shared helper kept it.

### Process

When a test already exists, the red run is those assertions against an empty stub. The stub has to be importable before the suite collects, so "add the import" and "add the empty function" are one edit.

### Million-Dollar Question

The helper beside `plant_pack` and `fold_ids` is the shape this would have had from the start. Sharing the `how` list as well would put one more fact in one place, and it would also edit the decorator lines a parallel fold change is likely to touch. Leaving that list at the call sites is the smaller contract.
