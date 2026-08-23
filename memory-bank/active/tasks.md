# Current Task: fold-request-path

**Complexity:** Level 1

## Fix

- **What broke:** `fold_request()` `Run:` line was always `nap <id-a> <id-b>`, even when the invoking command used `--path` against a child store. Pasting from repo root walked up to the root store and failed with `unknown id`.
- **Why:** `fold_request()` received only the resolved store `parent`. It never compared that store to walk-up from `$PWD`. `surgery.py` reprints the same helper after excision, so it had the same gap.
- **What changed:** `_fold_path_flag(parent)` inserts ` --path REL` when `resolve_parent($PWD)` is not that store. `REL` is the relative path from cwd to `parent`. `surgery.py` needed no call-site change.
- **Files:** `summem`; tests in `tests/test_fold.py`, `tests/test_scopes.py`, `tests/test_surgery.py`.
