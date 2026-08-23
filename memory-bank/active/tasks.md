# Current Task: fold-request-path

**Complexity:** Level 1

## Fix

- **What broke:** `fold_request()` `Run:` line was always `nap <id-a> <id-b>`, even when the invoking command used `--path` against a child store. Pasting from repo root walked up to the root store and failed with `unknown id`.
- **Why:** `fold_request()` received only the resolved store `parent`. It never compared that store to walk-up from `$PWD`. `surgery.py` reprints the same helper after excision, so it had the same gap.
- **What changed:** `_fold_path_flag(parent)` inserts ` --path REL` when `resolve_parent($PWD)` is not that store. `REL` is the relative path from cwd to `parent`. `surgery.py` needed no call-site change.
- **Files:** `summem`; tests in `tests/test_fold.py`, `tests/test_scopes.py`, `tests/test_surgery.py`.

## QA Results

**Verdict:** PASS

- **KISS / DRY / YAGNI:** `_fold_path_flag` compares walk-up from `$PWD` to the folded store and inserts `--path REL`. Surgery stays a consumer. No argv threading, no extra surface.
- **Completeness:** Nested include, in-store omit, `note --path` paste-and-run, and surgery `--path` paste-and-run are all asserted. Existing in-store `Run:` tests now `chdir` so they still lock the no-hint line.
- **Regression / integrity:** Nap id resolution, walk-up, `AGENT_BIN` / `CLI_NAME` split, and ACK placement are unchanged. No stubs, TODOs, or debug leftovers.
- **Documentation:** `systemPatterns.md` records the `Run:` `--path REL` contract. `docs/agents-prompt.md` and `docs/surgery.md` stay accurate (paste the printed line; surgery ellipsis is the same helper).
- **Advisory (non-blocking):** `REL` is unquoted. A store path with spaces would break the `Run:` line. Not in the brief; typical package paths do not have spaces.
