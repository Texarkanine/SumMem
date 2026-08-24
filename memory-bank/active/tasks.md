# Current Task: require-python

**Complexity:** Level 1

## Build

- What broke: `summem` imported `tomllib` at module load (`summem:72`). `require_python()` ran only from `main()` and from `surgery.py` after `load_summem()` already exec'd the module. Python 3.10 died with `ModuleNotFoundError: No module named 'tomllib'` before `SumMem needs Python 3.11 or newer`.
- Why: `tomllib` is stdlib since 3.11. The floor check was after import.
- What changed: immediately after `import sys`, refuse `sys.version_info < (3, 11)` with the same stderr line and `SystemExit(1)`, then `import tomllib`. `require_python()` is unchanged for in-process tests and `main()`.
- Files affected: `summem`; `tests/test_cli.py` (source-order contract + live 3.10 subprocess).

## QA

- Result: PASS
- Review baseline: projectbrief (issue #38 floor before `tomllib`); Level 1, no creative docs
- Implementation matches the plan: 3-line `sys.version_info < (3, 11)` gate immediately after `import sys` and before `import tomllib`; same stderr line and `SystemExit(1)` as `require_python()`; `require_python()` left in place; surgical edit only; docs-toolchain pins untouched
- Tests: source-order contract always runs; live 3.10 subprocess skips if no 3.10 interpreter; existing injected-tuple test unchanged
- Advisories (non-blocking):
  - Import-time gate duplicates `require_python()` body — required by the sibling-safe / leave-function-in-place plan
  - No dedicated `surgery.py` 3.10 subprocess test; same `exec_module` path as the driver

