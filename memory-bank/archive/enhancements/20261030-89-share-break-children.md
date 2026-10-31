---
task_id: 89-share-break-children
complexity_level: 2
date: 2026-10-30
status: completed
---

# TASK ARCHIVE: share-break-children

## SUMMARY

`break_children` in `tests/gitutil.py` is the only setup that unlinks a nap's children file or writes `not a tree`. The fold and nap tests call it. The four existing cases still pass, and the product is unchanged.

## REQUIREMENTS

- One helper, used by both tests, living in `tests/gitutil.py` beside `plant_pack` and `fold_ids`.
- `missing` unlinks the children file. Any other `how`, including `unreadable`, writes `not a tree`.
- The four cases stay: missing and unreadable, for `fold_request` and for `nap`.
- No product change, no new test file, and no change-detector that only checks the helper exists.
- Stay inside issue #89. The diff stays on the import lines and one call per test so it does not collide with issue #88.

## IMPLEMENTATION

Level 2 test-fixture move. `break_children(node, how)` unlinks `node.tree_path` when `how` is `missing` and otherwise writes `b"not a tree\n"`. `tests/test_fold.py` dropped `_break_children`. `tests/test_nap.py` dropped the inline unlink and write. Both call `break_children`. Imports stay alphabetical. The shared `how` list was left at the call sites so the parametrize lines stay untouched.

The import and the empty stub landed in one edit, because the suite cannot collect a name that does not exist yet. The red run still came before the function body.

- [`tests/gitutil.py`](../../../tests/gitutil.py) — `break_children`
- [`tests/test_fold.py`](../../../tests/test_fold.py) — fold call site
- [`tests/test_nap.py`](../../../tests/test_nap.py) — nap call site

Persistent files were left as they are. This task did not change who the product is for, a system-wide contract, or how to run the suite.

## TESTING

No new assertions. The existing four cases are the checks. Against a `pass` stub they failed as preflight predicted: fold named the grain-2 pair, and nap refused the outer pair. After the real body, those two tests passed (4 passed). `tox -e py311` was 420 passed. `/niko-qa` was PASS. `tox run-parallel` passed on py311, py312, py313, and py314. This repo has no lint or build target.

Preflight was PASS WITH ADVISORY. Advisories: treat the import and the stub as one edit, keep imports alphabetical, and do not export a shared `how` list in this task.

## LESSONS LEARNED

- When a test already exists, the red run is those assertions against an empty stub. The stub has to be importable before the suite collects, so adding the import and adding the empty function are one edit.
- The else branch was already the unreadable path in both copies. The shared helper kept it. Raising on an unknown `how` would have been new behavior.
- Sharing the `how` list would put one more fact in one place and would also edit decorator lines a parallel fold change is likely to touch. Leaving that list at the call sites is the smaller contract.

## PROCESS IMPROVEMENTS

Nothing beyond the import-and-stub sequence above. Preflight already named that advisory, and the build followed it.

## TECHNICAL IMPROVEMENTS

None. A catalog of one test helper does not belong in the architecture docs or the persistent briefings.

## NEXT STEPS

Open the pull request that closes issue #89.
