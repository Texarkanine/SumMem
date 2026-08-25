# Active Context

## Current Task: drop-dataclasses
**Phase:** BUILD - COMPLETE

## What Was Done
- Five view types are `__slots__` classes with `_replace` and `_eq_by_slots`.
- `tomllib` / `fcntl` / `subprocess` / `random` / `argparse` import only where needed. Exact `version` / `init` / `-h` return before argparse.
- Isolation tests spawn a fresh interpreter and record imports whose globals are the driver. 3.14 pathlib pulls `fcntl`; `sys.modules` is the wrong oracle.
- tox py311–py314: 287 passed. `/usr/bin/python3.10 ./summem version` prints the 3.11 floor.

## Files modified
- `/home/mobaxterm/.cursor/worktrees/summem-issue-52/SumMem/summem`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-52/SumMem/tests/test_cli.py`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-52/SumMem/tests/test_zipper.py`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-52/SumMem/memory-bank/techContext.md`

## Key decisions
- Module-level `_replace`, not a method (plan primary; preflight advisory declined).
- `__eq__` added after `test_loads_tree_round_trip` compared `Tree` objects.
- Unit 4 ran: argparse was the leftover (~12 ms).

## Next Step
- QA review.
