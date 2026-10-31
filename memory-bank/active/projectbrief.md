# Project Brief

## User Story

As an agent folding a store, I want a fold request to name only a pair `nap` can write, so that a hand-edited children file cannot stall every later `note`.

## Use-Case(s)

### Use-Case 1

A nap's `.tree` parses, and the number of digests in it is not the grain in the filename. The view is over budget and another legal same-grain pair exists. `fold_request` names that other pair. `nap` accepts it.

### Use-Case 2

A nap whose children file is missing or unreadable stays ineligible: never requested, never a nearer twin. Wake still lists the filename grain.

## Requirements

1. Fold eligibility is whatever `nap` can actually fold.
2. `_fold_grains` builds that grain from `_as_child`. A `ValueError` from `_as_child` is ineligible (grain 0). Otherwise the grain is the digest count `_as_child` returns, not `node.leaves`.
3. A row `nap` would refuse is never requested and never counts as a nearer twin.
4. Filename grain stays what wake lists.
5. `_fold_grains` is the helper both `fold_request` and `write_nap`'s nearest-twin check already share. Point it at `_as_child` instead of a second `loads_tree`.

## Constraints

1. Issue #88 only. Do not move `_break_children` (that is issue #89).
2. The disagreement takes a hand-edited store. Do not invent a writer that emits it.
3. Executable behavior is test-first. SumMem notes commit with the code.
4. Stop at the Level 1 completion gate. Do not archive, open a pull request, merge, or push.

## Acceptance Criteria

1. A test whose `.tree` parses and whose digest count is not the stem's grain: the request names some other legal pair, and `nap` accepts that pair.
2. Existing missing and unreadable children-file tests still pass.
3. Wake listing for that nap still shows the filename grain.
