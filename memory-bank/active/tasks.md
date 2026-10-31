# Task: share-break-children

* Task ID: 89-share-break-children
* Complexity: Level 2
* Type: simple enhancement

Move the duplicated broken-children setup into one helper in `tests/gitutil.py`. `tests/test_fold.py` defines `_break_children`: `missing` unlinks `node.tree_path`, and any other value writes `b"not a tree\n"`. `tests/test_nap.py` repeats those four lines inside `test_nap_pairs_across_a_same_grain_pack_whose_children_file_is_broken`. Both tests parametrize `how` as `missing` and `unreadable`. No product change. The four cases stay.


## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior. These existing outcomes must still hold after both call sites use the shared helper:

- Fold, missing: grains 2, 1, 2, 1, 1, oldest pack's children file unlinked, budget 4 → `fold_request` names the two oldest grain-1 ids, and `nap` of that Run line exits 0 and prints `Saved.`
- Fold, unreadable: same store, oldest pack's children file replaced with `not a tree` → the same pair and the same `Saved.`
- Nap, missing: three grain-2 packs, middle children file unlinked → `write_nap` of the outer two leaves grains 4, 2, and the broken row's name is still the second node.
- Nap, unreadable: same store, middle children file replaced with `not a tree` → the same grains and the same remaining name.

Edge: do not add a third `how`, a raised error for an unknown `how`, or a test that only checks the helper exists. The else branch stays "write `not a tree`".

### Test Infrastructure

- Framework: pytest, run with `tox -e py311` (one test or file under that env while iterating)
- Test location: `tests/`
- Conventions: shared store fixtures live in `tests/gitutil.py` (`plant_pack`, `fold_ids`, `init_repo`). Callers import them by name. Cases use `pytest.mark.parametrize`. Docstrings state the store shape and the outcome.
- New test files: none

## Implementation Plan

### 1. Shared `break_children` — executable

- Files: `tests/gitutil.py`, `tests/test_fold.py`, `tests/test_nap.py`

1. Stub tests: no new test functions. In `test_fold.py`, drop `_break_children` and import `break_children` from `gitutil` next to `fold_ids` and `init_repo`. Call `break_children(view[0], how)` in `test_fold_request_skips_a_pack_whose_children_file_is_broken`. In `test_nap.py`, import `break_children` next to `init_repo` and `plant_pack`, and replace the inline `if how == "missing"` block in `test_nap_pairs_across_a_same_grain_pack_whose_children_file_is_broken` with `break_children(broken, how)`. Leave every assertion as it is.
2. Stub interface: add `def break_children(node, how: str) -> None` to `tests/gitutil.py` beside `plant_pack`, with a docstring that states `missing` unlinks the children file and any other `how` writes `not a tree`. Body is `pass`.
3. Write tests and run red: the assertions already exist. Run the two tests under `tox -e py311`. They must fail because the children file is still intact: fold names a different pair, and nap refuses the outer pair.
4. Write code and run green: replace `pass` with the existing branches (`unlink` on `missing`, otherwise `tree_path.write_bytes(b"not a tree\n")`). Re-run the same two tests. They must pass. Do not edit `summem` or any other test.

No documentation step. README, architecture docs, and `memory-bank/techContext.md` do not describe this fixture.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `tox -e py311` and pytest
- View nodes already expose `tree_path` (both call sites use it today)
- Issue #88 is parallel and must not be edited

## Challenges & Mitigations

- Issue #88 will also edit fold and nap tests. Mitigation: change only the import lines and the broken-children call. Do not reflow the surrounding tests.
- A public helper in `gitutil.py` is unprefixed (`plant_pack`, `fold_ids`). A leading underscore would mark it private to that module. Mitigation: name it `break_children`.
- An unknown `how` currently takes the unreadable branch. Raising would be new behavior. Mitigation: keep the else branch.
- Two `tox -e py311` processes on this worktree would stomp `.tox/py311`. Mitigation: one tox at a time.
- A test that asserts `break_children` is defined would be a change-detector. Mitigation: the four existing cases are the only checks.

## Pre-Mortem

- The plan treats a test move as a product change and edits `summem` or adds a mode. Response: step 4 forbids product edits, and the test plan forbids a third `how`.
- The shared function drifts from one call site (different path attribute, different bytes). Response: both sites use `node.tree_path` and `b"not a tree\n"` today; the helper is those two lines and nothing else.
- A wide diff in `test_fold.py` or `test_nap.py` collides with #88. Response: already covered by the first challenge; the edit stays on the import and the call.
- Preflight or build invents a new test file. Response: test plan says no new test files.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
