# Task: drop-dataclasses

* Task ID: drop-dataclasses
* Complexity: Level 2
* Type: simple enhancement

Replace the five frozen dataclasses with `__slots__` types, drop `import dataclasses`, and import `tomllib` / `fcntl` / `subprocess` / `random` only on the commands that need them. Optional leftover: keep argparse out of the `version` / `init` / bare-help path. Stay in class definitions, module imports, and `main` dispatch.

## Test Plan (TDD)

### Behaviors to Verify

- `version` in a fresh interpreter → `tomllib`, `fcntl`, and `subprocess` are absent from `sys.modules` after `main` returns 0
- `init` in a fresh interpreter → same three modules absent after `main` returns 0
- `-h` in a fresh interpreter → same three modules absent after `main` returns 0
- `version` / `init` / `-h` in a fresh interpreter → `dataclasses` is absent from `sys.modules`
- `_prepare_nap` / `ProjectedNode` copy → a changed field is applied and other public fields stay; no `dataclasses.replace`
- `ViewNode` public fields → `id` can be copied with other fields intact (existing `test_ambiguous_prefix_is_error` after it stops using `dataclasses.replace`)
- Existing: `sys.version_info` is read immediately after `import sys` and before any `import tomllib`
- Existing: Python 3.10 prints `SumMem needs Python 3.11 or newer` and does not mention `tomllib`
- Existing: store commands, SourceFileLoader load of repo-root `summem`, command `-h` / `--path` contracts

### Test Infrastructure

- Framework: pytest via tox (`py311`–`py314`)
- Test location: `tests/`
- Conventions: load repo-root `summem` with `load_summem()` / `SourceFileLoader`; CLI cases live in `tests/test_cli.py`; 3.10 floor already in `tests/test_cli.py`; flock monkeypatch in `tests/test_zipper.py`
- New test files: none

## Implementation Plan

### 1. Fresh-interpreter import isolation — executable

- Files: `tests/test_cli.py`

1. Stub tests: `test_version_skips_command_only_imports`, `test_init_skips_command_only_imports`, `test_help_skips_command_only_imports` (empty bodies)
2. Stub interface: none — `main` already exists
3. Write tests and run red: spawn `sys.executable` with a `SourceFileLoader` probe of repo-root `summem`, run `main(["version"])` / `main(["init"])` / `main(["-h"])`, print whether `tomllib`, `fcntl`, `subprocess`, and `dataclasses` are in `sys.modules`; assert absent and exit 0. Must fail while those modules are imported at the top of `summem`
4. Write code and run green: deferred to units 2–3 (isolation stays red until both land)

### 2. Slots types and `_replace` — executable

- Files: `summem`, `tests/test_cli.py`

1. Stub tests: none new beyond unit 1's `dataclasses` assertion; modify `test_ambiguous_prefix_is_error` to call the replacement helper instead of `dataclasses.replace`
2. Stub interface: keep `NoteChild`, `Tree`, `NapChild`, `ViewNode`, `ProjectedNode` names and field names; add `_replace(obj, **changes)` (or a method) with the same keyword contract as `dataclasses.replace`
3. Write tests and run red: unit 1's `dataclasses` assertion still red; `test_ambiguous_prefix_is_error` red if it already uses `_replace` before the helper exists
4. Write code and run green: delete `from dataclasses import dataclass, replace`; implement the five types as `__slots__` classes with the current public fields and defaults (`ViewNode.sum_path` / `tree_path`; `ProjectedNode.tree` / `tree_path` / `tree_attempted`); implement `_replace`; switch `_prepare_nap` to `_replace`. Do not rewrite `catalog_text`, `named_ids` / `short_id` / `recall_text` / `zoom_text`, or `heal_view` / `leaf_digests` except constructors

### 3. Lazy command-only imports — executable

- Files: `summem`, `tests/test_zipper.py`

1. Stub tests: none new (unit 1 covers the user-visible contract)
2. Stub interface: no new public functions
3. Write tests and run red: unit 1 still red while `import tomllib` / `fcntl` / `subprocess` / `random` stay at module top
4. Write code and run green: keep `import sys` then the `sys.version_info` 3.11 gate; move `import tomllib` into `knobs`; `import subprocess` into `_ignored_store`; `import fcntl` into `with_store_lock`; `import random` into the `note` path in `main`. Change `test_cli_wake_on_overlapping_head_writes_nothing` to patch stdlib `fcntl.flock` (same module object the lazy import binds). Leave `test_version_info_is_checked_before_import_tomllib` as the source-order pin

### 4. Argparse leftover — executable

- Files: `summem`

1. Stub tests: none unless measurement after units 2–3 still shows argparse as the leftover import on `version`
2. Stub interface: none
3. Write tests and run red: only if this unit runs — then extend the unit 1 probe to assert `argparse` is absent after `main(["version"])`, `main(["init"])`, and `main(["-h"])`
4. Write code and run green: only if this unit runs — early-return exact `["version"]` / `["init"]` / `_HELP_FLAGS` (already handwritten `usage_text`) before `import argparse`; construct the existing `ArgumentParser` only for other argv. Do not rewrite subcommand `-h` text. Skip the unit if argparse is no longer the leftover

### 5. Tech context — prose/policy

- Files: `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. Record that `tomllib` / `fcntl` / `subprocess` / `random` load inside the functions that need them
2. Keep the sentence that `sys.version_info` is checked immediately after `import sys` and before any `tomllib` import

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest / tox / uv
- Existing `tests/test_cli.py` 3.10 helpers (`_cpython_310`)
- Sibling PRs #54 / #55 / #56 edit other regions of `summem`; this lane is class defs + imports + `main` dispatch

## Challenges & Mitigations

- Isolation probe already has `subprocess` / `fcntl` in `sys.modules` because the parent pytest process imported them: run the probe in a fresh `sys.executable` child; do not inspect the pytest process
- `test_zipper.py` patches `m.fcntl.flock`: after the lazy import, `m.fcntl` is missing — patch `fcntl.flock` on the stdlib module
- `test_cli.py` uses `dataclasses.replace` on `ViewNode`: switch that one call to `_replace`; keep field names
- Moving `import tomllib` past the 3.11 gate must not move the gate: keep the `sys.version_info` check as the next statement after `import sys`
- Slots types without field `__eq__` could break a hidden compare: add `__eq__` only if an existing test fails; do not invent hashing
- Hand-rolled argparse would drift `note -h` / `invalid choice`: unit 4 only early-outs exact argv and keeps the existing parser for everything else
- Merge with #54/#55/#56: do not rewrite catalog / recall / heal bodies

## Pre-Mortem

- Slots land but `version` still imports dataclasses because a leftover `replace` import remains: unit 1's runtime `dataclasses` assertion is the gate; unit 2 deletes both `dataclass` and `replace`
- Lazy `tomllib` reorders the 3.11 gate and 3.10 dies with `ModuleNotFoundError`: already covered by Challenge (gate stays after `import sys`) plus existing `test_driver_refuses_python_310_before_tomllib`
- Isolation tests go green in-process because pytest already imported the modules and the assertion is inverted: already covered by Challenge (fresh child)
- Unit 4 rewrites dispatch and command `-h` drifts: already covered by Challenge (early-out only; keep ArgumentParser)
- The change is not useful because compile of the no-suffix file still dominates: measured dataclasses+tomllib+subprocess are tens of milliseconds on this machine; still implement (1) and (2); skip a marshal cache

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
