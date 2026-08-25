---
task_id: drop-dataclasses
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: drop-dataclasses

## SUMMARY

Cut the per-invocation import floor. Five frozen dataclasses became `__slots__` types; `tomllib` / `fcntl` / `subprocess` / `random` / `argparse` load only on the paths that need them. Exact `version` / `init` / `-h` skip those imports. [Issue #52](https://github.com/Texarkanine/SumMem/issues/52). tox 287 passed on py311–py314. Python 3.10 still prints `SumMem needs Python 3.11 or newer`.

## REQUIREMENTS

- Replace `NoteChild`, `Tree`, `NapChild`, `ViewNode`, `ProjectedNode` with slots (or equivalent). Keep public field names. Provide `_replace` instead of `dataclasses.replace`.
- Import `subprocess`, `fcntl`, `random`, and `tomllib` only on commands that need them.
- `import dataclasses` gone from the driver.
- `version` / `init` / help do not import `tomllib`, `fcntl`, or `subprocess`.
- Python 3.10 still dies with the floor message before `tomllib`. `sys.version_info` stays immediately after `import sys`.
- Stay in class definitions, module imports, and `main` dispatch. No marshal / `.pyc` cache. Sibling PRs #54/#55/#56 also edit `summem`.
- Argparse drop optional only if it remained the leftover.

## IMPLEMENTATION

Level 2. Lane kept.

- [`summem`](../../../summem): slots classes; `_replace` and `_eq_by_slots`; `import tomllib` in `knobs`, `subprocess` in `_ignored_store`, `fcntl` in `with_store_lock`, `random` in the `note` path, `argparse` after exact `version` / `init` / handwritten help return. 3.11 gate unchanged.
- [`tests/test_cli.py`](../../../tests/test_cli.py): fresh-interpreter probe records imports whose globals are the driver. `test_ambiguous_prefix_is_error` uses `_replace`.
- [`tests/test_zipper.py`](../../../tests/test_zipper.py): flock monkeypatch targets stdlib `fcntl`.
- [`memory-bank/techContext.md`](../../techContext.md): lazy-import and slots sentences.

Unit 4 shipped: argparse was the leftover (~12 ms). `__eq__` added after codec round-trip compared `Tree` objects.

## TESTING

TDD in plan order. Preflight PASS (advisory: method vs helper; kept helper). Isolation tests red, then green. First tox: py311–py313 287, py314 failed because pathlib imports fcntl — probe switched from `sys.modules` to driver `__import__`. Second tox: 287 on py311–py314. `/usr/bin/python3.10 ./summem version` exits 1 with the floor message. `/niko-qa` PASS (advisory: probe omits `random`).

## LESSONS LEARNED

- 3.14 pathlib imports fcntl. "Module absent from sys.modules" is not a portable isolation oracle.
- Frozen-dataclass `__eq__` is load-bearing for `loads_tree` round-trip tests. Slots need an explicit compare.

## PROCESS IMPROVEMENTS

- Isolation tests that name stdlib modules should trace the driver's importer, not `sys.modules`, when a transitive stdlib import can appear on one CPython minor.

## TECHNICAL IMPROVEMENTS

Command `-h` still pays argparse. A full hand-roll would drop that on `note -h` as well; this ticket kept argparse to avoid `-h` drift.

## NEXT STEPS

None for this shard. Three-way merge with #54/#55/#56 is expected (class defs + imports + `main` only).
