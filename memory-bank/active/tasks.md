# Current Task: require-python

**Complexity:** Level 1

## Build

- What broke: `summem` imported `tomllib` at module load (`summem:72`). `require_python()` ran only from `main()` and from `surgery.py` after `load_summem()` already exec'd the module. Python 3.10 died with `ModuleNotFoundError: No module named 'tomllib'` before `SumMem needs Python 3.11 or newer`.
- Why: `tomllib` is stdlib since 3.11. The floor check was after import.
- What changed: immediately after `import sys`, refuse `sys.version_info < (3, 11)` with the same stderr line and `SystemExit(1)`, then `import tomllib`. `require_python()` is unchanged for in-process tests and `main()`.
- Files affected: `summem`; `tests/test_cli.py` (source-order contract + live 3.10 subprocess).

## QA

- (pending)
