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

## 2026-10-31 - PREFLIGHT - COMPLETE

* Result: `FAIL (fixable)` (first line of `.preflight-status`)
* Findings
    - Fixable: caching `(NapChild, digests)` freezes `NapChild.sum`, but under the lock heal's `rematerialize_child` can write a missing `.summ` for a listed nap (`list_view` lists a `.tree`-only stem with caption `""`). `write_nap` would then bake an empty nested caption into a new payload. Cache `(Tree, digests)` keyed by `tree_path` and build `NapChild` from the current node per call; fix the Challenges claim.
    - Advisory: a cached `None` can stay stale after rematerialize repairs a broken `.tree` (refuse-not-corrupt; next command reads fresh). `surgery.py` also runs under the lock and gets the cache. `_CHILDREN` is the driver's first mutable module state.
    - Radical (advisory): evict `dest` from `_CHILDREN` in `_replace_bytes` (~2 lines) so the cache is coherent with every driver write by construction.

## 2026-10-31 - PLAN - COMPLETE (amended after preflight run 1)

* Decisions made
    - Took the required fix: the cache holds `(Tree, digests)` keyed by `tree_path`; `NapChild` is built from the current node each call, so captions are never cached.
    - Took the advisory: `_replace_bytes` drops `dest` from the cache in one line, so nothing the driver writes is served stale. One line of cost, and two plan caveats are gone.
