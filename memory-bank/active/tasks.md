# Task: multi-store-filing rework 3

* Complexity: Level 1

## Fix

- **What broke:** printed paths with spaces were ambiguous and not paste-safe (`There is a store in :/team docs.`). Only `Run:` shell-quoted; sentence lines printed paths bare, so the full stop ran into the path.
- **Why:** `_root_path` built the `:/` form, and quoting lived only in `_fold_store_flag`.
- **Change:** `_root_path` now shell-quotes (`shlex.quote`; ordinary paths unchanged), so every printed path is paste-safe. Paths in sentences (`start`, `not a directory`, the three resolver errors) are backticked. `shlex` moved to a module import.
- **Files:** `summem`, `tests/test_scopes.py`, `docs/user-guide/{commands,stores}.md`, `memory-bank/systemPatterns.md`.
- **Verify:** `tox run-parallel` py311–py314 OK (461 tests); `properdocs build --strict` clean.
