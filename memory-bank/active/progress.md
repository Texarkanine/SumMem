# Progress

Rework PR #95 so `note` and `nap` read and digest each nap children file (`.tree`) at most once per command, with heal, fold, and nap sharing that one result. Measure first; smallest change; net `summem` lines zero or negative; behavior unchanged.

**Complexity:** Level 2

## 2026-10-31 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Verified the operator's facts at dd16eac: `note` reads every `.tree` twice (heal's `leaf_digests` raw-JSON walk, then `_fold_grains` via `_as_child`); `nap` reads up to three times (heal, `write_nap`'s nearer-twin `_fold_grains`, then `fold_request` re-lists and scans again).
    - Benchmarked `origin/main` (060f078; `summem` identical to the branch base e8b77a7) and dd16eac on a 4094-leaf scratch store.
* Decisions made
    - Level 2: one component, no design fork that needs a creative phase.
