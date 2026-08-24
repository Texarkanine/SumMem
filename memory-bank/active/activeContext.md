# Active Context

## Current Task: require-python
**Phase:** QA - COMPLETE (PASS)

## What Was Done

- TDD: two new tests in `tests/test_cli.py` went red (`version_info` after `import tomllib`; 3.10 subprocess `ModuleNotFoundError`), then green after the import-time floor
- `summem` now checks `sys.version_info < (3, 11)` immediately after `import sys` and before `import tomllib`
- `/usr/bin/python3.10 summem version` and `surgery.py version` both print `SumMem needs Python 3.11 or newer` and exit 1
- Full `tox`: 277 passed on py311, py312, py313, py314

## Next Step

- L1 wrap-up: reconcile-persistent done; delete `memory-bank/active/` and open the PR
