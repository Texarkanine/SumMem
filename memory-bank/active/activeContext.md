# Active Context

## Current Task: pytest-xdist
**Phase:** BUILD - COMPLETE

## What Was Done
- `tox.ini`: `pytest-xdist` dep; `[testenv] commands = pytest -n auto --maxprocesses=4 {posargs}`. Coverage commands unchanged (serial).
- Three contracts in `tests/test_tox_runner.py`. Docs: `README.md`, `memory-bank/techContext.md`, `.cursor/rules/SumMem-testing.mdc`.
- Serial-marker count **0**, justified on [issue #64](https://github.com/Texarkanine/SumMem/issues/64#issuecomment-5419816806).
- `tox -e py311`: 358 passed, 4 workers, 19.96s. `tox run-parallel`: 28.77s vs `-n0` 38.78s. `tox -e coverage`: 358 passed serial, lcov written, no xdist workers.

## Files modified
- `/home/mobaxterm/git/SumMem/tox.ini`
- `/home/mobaxterm/git/SumMem/tests/test_tox_runner.py`
- `/home/mobaxterm/git/SumMem/README.md`
- `/home/mobaxterm/git/SumMem/memory-bank/techContext.md`
- `/home/mobaxterm/git/SumMem/.cursor/rules/SumMem-testing.mdc`
- `/home/mobaxterm/git/SumMem/memory-bank/active/tasks.md`
- `/home/mobaxterm/git/SumMem/memory-bank/active/progress.md`
- `/home/mobaxterm/git/SumMem/memory-bank/active/activeContext.md`

## Key decisions
- Cap at 4, not unbounded `auto`. Coverage stays serial.
- `test_coverage_env_runs_serial` was already green (lock on absence of `-n`); not a TDD miss of a new behavior.

## Next Step
- QA review (subagent).
