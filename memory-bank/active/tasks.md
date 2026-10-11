# Tasks: middle-orphans rework — broken naps stall fold

## Fix

- **What broke:** A nap whose children file (`.tree`) is missing or will not parse still counted by its filename grain. `fold_request` named it, `write_nap` failed (`unknown id` / `unreadable pack`), and every later `note` asked for the same pair. `write_nap`'s nearest-twin check also counted it, so it blocked a valid pair of good rows around it.
- **Why:** `_fold_pair` and `_nearest_twin` saw only `node.leaves`, which comes from the filename. Oldest-pair-first makes a broken nap the request almost every time it has a later twin.
- **What changed:** New `_fold_grains(nodes)` returns each row's grain, 0 for a nap whose children file is missing or unreadable. `fold_request` and `write_nap` use it. 0 is not a power of two, so the picker skips the row and the twin check never counts it. The row stays listed; recovery is the operator's, through git.
- **Files:** `summem`, `tests/test_fold.py`, `tests/test_nap.py`, `docs/architecture/index.md`.

## Tests

- [x] `test_fold.py::test_fold_request_skips_a_pack_whose_children_file_is_broken[missing|unreadable]` — grains 2, 1, 2, 1, 1 with the oldest 2 broken: request names the two oldest 1s and `nap` accepts the Run: line.
- [x] `test_nap.py::test_nap_pairs_across_a_same_grain_pack_whose_children_file_is_broken[missing|unreadable]` — grains 2, 2, 2 with the middle broken: the outer two fold; the broken row stays listed.
- [x] `tox run-parallel` green on py311–py314.

## QA

PASS (2026-10-11). `tox -e py311`: 421 passed. Advisories are in `.qa-validation-status`: `_fold_grains` duplicates `_as_child`'s load, a parse-valid tree with a wrong digest count could still stall, the test helper is inlined in `test_nap.py`, and there is a bounded extra `.tree` read per over-budget mutation.
