# Progress

Cut the per-invocation import floor: drop dataclasses, lazy-import command-only modules, keep the 3.11 gate before tomllib.

**Complexity:** Level 2

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed worktree `feat/drop-dataclasses` at `ddc239e` (main), not stacked on #54/#55/#56
    - Woke OptMem and SumMem; issue #52 ingested as already-approved intent
    - Measured importtime/wall cost; hole is real
    - Classified Level 2
* Decisions made
    - Implement rather than close/defer: slots remove the dataclasses/inspect chain; lazy imports remove tomllib/subprocess from `version`/`init`/help
    - argparse is leftover (~33 ms) and optional only after (1) and (2)
* Insights
    - Issue text says six dataclasses; this `main` has five (`NoteChild`, `Tree`, `NapChild`, `ViewNode`, `ProjectedNode`)
    - `fcntl` itself is cheap; it is still in the acceptance "do not import" list
    - `test_zipper.py` patches `m.fcntl.flock`; `test_cli.py` uses `dataclasses.replace` on `ViewNode`

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Wrote TDD plan: fresh-interpreter isolation, slots + `_replace`, lazy imports, optional argparse leftover, techContext
* Decisions made
    - No new test file; extend `tests/test_cli.py` and retarget two existing patches
    - Unit 4 runs only if argparse is still the leftover after units 2–3; early-out exact argv, keep ArgumentParser for `-h` on real commands
    - Runtime `sys.modules` probe, not a source-scan change-detector, is the dataclasses/import contract
* Insights
    - Bare `-h` already returns `usage_text()` before the parser; moving `import argparse` below that early-out is enough if unit 4 runs

## 2026-08-25 - PREFLIGHT - COMPLETE

* Work completed
    - Validated implementation plan against codebase reality.
    - Verified TDD plan encoding, convention compliance, and dependency impact.
* Decisions made
    - Preflight passed (PASS).
* Insights
    - Plan is solid. Suggested implementing `replace` as a method on the classes rather than a standalone function.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - Replaced five dataclasses with `__slots__` + `_replace` + `_eq_by_slots`
    - Lazy-imported tomllib/fcntl/subprocess/random; early-out version/init/-h before argparse
    - Isolation tests in a fresh interpreter; 3.14 probe traces driver `__import__`
    - tox 287 passed on py311–py314; Python 3.10 still prints the floor message
* Decisions made
    - Kept `_replace` as a helper (preflight advisory was method-on-class)
    - Added `__eq__` only after codec round-trip tests failed
    - Unit 4 shipped: argparse was the leftover
* Insights
    - 3.14 pathlib imports fcntl; absence from `sys.modules` is not portable
    - Wall `version` dropped from ~110–135 ms to ~60–80 ms on this machine (pyenv shim still extra)

## 2026-08-25 - QA - COMPLETE

* Work completed
    - Reviewed the complete branch diff against the Level 2 plan and project brief
    - Checked KISS, DRY, YAGNI, completeness, regression, integrity, and documentation
    - Ran the full tox matrix and the Python 3.10 floor check
* Decisions made
    - QA passed; no implementation changes are required
* Insights
    - tox passed 287 tests on each of Python 3.11, 3.12, 3.13, and 3.14
    - The fresh-interpreter probe omits `random`, but the implementation localizes it to `note` and the acceptance criteria name only tomllib/fcntl/subprocess/dataclasses

## 2026-08-25 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-drop-dataclasses.md`
    - Reconciled persistent files
* Decisions made
    - productContext skip — no audience/use-case change; standing-contract probe clean
    - systemPatterns skip — argparse still builds command `-h`; usage_text still handwritten; slots are a tech convention already in techContext
    - techContext skip — lazy-import and slots sentences landed in BUILD
* Insights
    - 3.14 pathlib/fcntl is the standing test oracle, already noted in SumMem