# Current Task: cli-help

**Complexity:** Level 1

## Rework fix

- **What broke:** `find_store_parent` returned cwd when no `.git` existed, so `wake`/`start` created a store that cannot merge.
- **Why:** VISION allowed “stop at `$PWD` if not in git.” That is not a real mode.
- **What changed:** `find_store_parent` raises `ValueError("not in a repository")`. Store commands print that and exit 1. `start` probes before mkdir. Help still works. VISION parenthetical struck.
- **Files:** `.summem/summem`, `tests/test_cli.py`, `VISION.md`

## QA (rework)

**Result:** PASS

- KISS/DRY/YAGNI: raise in `find_store_parent`; `start` probes then mkdir; no extra mode. Does not block.
- Completeness: store commands error; help still prints; VISION fallback struck. Does not block.
- Regression/integrity: catalog and in-repo auto-create unchanged; error names repository, not git or store files. Does not block.
- Advisory: `systemPatterns.md` still omits the no-repo failure sentence that VISION now has. Does not block.
- Advisory: `note`/`nap`/`zoom`/`recall` without a repo share wake’s `resolve_parent` path; command `-h` never reaches the check. Distinctive cases are tested. Does not block.
