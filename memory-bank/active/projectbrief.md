# Project Brief

## User Story

As a contributor working on fold and nap tests, I want one helper that breaks a nap's children file so that the missing and unreadable cases are not copied in two modules.

## Use-Case(s)

### Use-Case 1

A fold test damages the oldest same-grain pack's `.tree` (unlink, or write `not a tree`) and still asks for the two oldest grain-1 rows.

### Use-Case 2

A nap test damages the middle pack's `.tree` the same two ways and still pairs the outer two packs.

## Requirements

1. One helper, used by both tests.
2. Home is `tests/gitutil.py`, beside `plant_pack` and `fold_ids`.
3. `missing` unlinks the children file. `unreadable` writes `not a tree`.
4. The four cases stay: missing and unreadable, for `fold_request` and for `nap`.
5. No product change.

## Constraints

1. Stay inside issue #89. Issue #88 edits fold and nap tests in a sibling worktree; do not touch that tree.
2. Do not invent a change if the duplication is not real. It is real.
3. Executable product behavior is unchanged, so do not add a change-detector test for the helper's existence.
4. SumMem notes that record a repo fact are committed with the code.
5. Leave `memory-bank/active/` in place. Do not archive, open a pull request, merge, or push.

## Acceptance Criteria

1. `tests/test_fold.py` no longer defines `_break_children`.
2. `tests/test_nap.py` no longer inlines the unlink and `not a tree` writes.
3. Both call the helper in `tests/gitutil.py`.
4. `test_fold_request_skips_a_pack_whose_children_file_is_broken` and `test_nap_pairs_across_a_same_grain_pack_whose_children_file_is_broken` still pass for `missing` and `unreadable`.
