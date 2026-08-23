# Progress

Investigate [issue #34](https://github.com/Texarkanine/SumMem/issues/34) and, if the report holds, make the fold request `Run:` line copy-paste safe when the resolved store is not the walk-up from `$PWD`. Same consideration for `surgery.py`.

**Complexity:** Level 1

## 2026-08-23 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed: investigate #34, fix if real, include surgery if the same gap exists
    - Classified as Level 1
* Decisions made
    - Level 1: bug, single component (`fold_request` output), no architecture
    - Task id: `fold-request-path`
* Insights
    - Existing tests cover scoped `nap --path` and root fold-request shape, not nested-store fold-request text

## 2026-08-23 - BUILD - COMPLETE

* Work completed
    - Reproduced #34: `note --path pkg` over budget printed `nap <ids>` with no `--path`; pasting from root was `unknown id`
    - `_fold_path_flag` compares `resolve_parent($PWD)` to the folded store and inserts `--path REL` when they differ
    - Tests in `test_fold.py`, `test_scopes.py`, `test_surgery.py`; `tox` 266 passed py311–py314
* Decisions made
    - Compute the hint from cwd vs `parent` inside `fold_request`, do not thread the original `--path` argv
    - Omit `--path` when walk-up already selects the store (cwd inside the store is fine)
    - `surgery.py` stays a consumer; no signature change
* Insights
    - Existing `fold_request` unit tests that did not `chdir` to the store would have gained a `--path` to the tmp repo; they now `chdir` so they still assert the in-store `Run:` line
