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
