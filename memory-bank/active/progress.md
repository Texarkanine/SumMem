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