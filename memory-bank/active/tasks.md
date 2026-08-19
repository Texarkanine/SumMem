# Current Task: cli-help

**Complexity:** Level 1

## Rework fix

- **What broke:** `find_store_parent` returned cwd when no `.git` existed, so `wake`/`start` created a store that cannot merge.
- **Why:** VISION allowed “stop at `$PWD` if not in git.” That is not a real mode.
- **What changed:** `find_store_parent` raises `ValueError("not in a repository")`. Store commands print that and exit 1. `start` probes before mkdir. Help still works. VISION parenthetical struck.
- **Files:** `.summem/summem`, `tests/test_cli.py`, `VISION.md`
