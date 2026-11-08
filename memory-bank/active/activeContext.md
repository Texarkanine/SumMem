# Active Context

## Current Task: start, help, and nap replies
**Phase:** BUILD - COMPLETE

## What Was Done

- `start` prints `There is a store in ./path.` and refuses anything that is not an existing directory.
- `help` rewrites to the existing `-h` path, including `help <command>`. Bare `summem` stays stderr and exit 2.
- `_nap_miss` treats an already-folded pair as success (`Saved.` and the real next fold or the idle line). Other misses are `not a fold row` or `unknown id`. `resolve_id` is unchanged, so zoom still names wake.
- Docs and the ratchet sentence match those words.
- py311: 441 passed.

## Files

- `/home/mobaxterm/worktrees/Texarkanine/SumMem/SumMem-nap-error-ratchet/summem`
- `tests/test_scopes.py`, `tests/test_cli.py`, `tests/test_surgery.py`, `tests/test_path_walkup_and_catalog.py`, `tests/test_nap.py`, `tests/test_nap_reject.py`
- `docs/user-guide/commands.md`, `docs/user-guide/stores.md`, `docs/user-guide/troubleshooting.md`
- `docs/architecture/wake.md`, `docs/architecture/merges-and-healing.md`
- `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`

## Deviations

- Five `start` call sites needed a directory because the previous line already mentioned `repo`. The first insert skipped them.
- `help` was added to the command lists in `systemPatterns.md` and `techContext.md`.
- No new `_child_id` helper. `_nap_miss` uses `_projected_child` and `_index_tree`.

## Next Step

- QA.

