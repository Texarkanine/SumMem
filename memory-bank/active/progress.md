# Progress

Rework PR #95 so `note` and `nap` read and digest each nap children file (`.tree`) at most once per command, with heal, fold, and nap sharing that one result. Measure first; smallest change; net `summem` lines zero or negative; behavior unchanged.

**Complexity:** Level 2

## 2026-10-31 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Verified the operator's facts at dd16eac: `note` reads every `.tree` twice (heal's `leaf_digests` raw-JSON walk, then `_fold_grains` via `_as_child`); `nap` reads up to three times (heal, `write_nap`'s nearer-twin `_fold_grains`, then `fold_request` re-lists and scans again).
    - Benchmarked `origin/main` (060f078; `summem` identical to the branch base e8b77a7) and dd16eac on a 4094-leaf scratch store.
* Decisions made
    - Level 2: one component, no design fork that needs a creative phase.

## 2026-10-31 - PLAN - COMPLETE

* Work completed
    - Plan with measurements in `tasks.md`. A throwaway process-wide prototype halved `.tree` reads (`note` 22 → 11, `nap` 34 → 12) and broke 10 tests that edit files in place between direct calls, plus the raw-JSON pin.
* Decisions made
    - Scope the parse cache to `with_store_lock`, the window in which a nap path names fixed bytes. Cache unreadable results too, so "at most once" also holds for a broken file.
    - Heal reads through `_as_child` (one parse, no refusal drift); delete `_digests_of_dict` and the test that pinned it.
* Insights
    - Subprocess timing at this scale drifts by tens of ms between back-to-back blocks; interleave drivers and also report in-process time.
