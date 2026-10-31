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

## 2026-10-31 - PREFLIGHT - COMPLETE (run 2)

* Result: `PASS WITH ADVISORY` (first line of `.preflight-status`)
* Findings
    - Run 1's fixable finding is resolved: the cache holds `(Tree, digests)` keyed on `tree_path`, captions come from the current node, and `_replace_bytes` evicts what the driver writes.
    - Advisory: the planned `with_store_lock` docstring reason ("a nap path names fixed bytes") is the claim run 1 disproved. Base it on "only this process writes under the lock, and `_replace_bytes` evicts what it writes".
    - Advisory: the note test needs at least two loose notes after heal for a `Run:` line. The nap test should take its pair from a `Run:` line, not from hard-coded indexes.
    - Radical (advisory): a write-through cache. Seed `(tree, digests)` after `_write_pair` in `rematerialize_child` and `write_nap`, so a post-merge zipper heal never reparses the kids it just wrote. About 2 to 3 lines; re-measure a merge-heal case first.

## 2026-10-31 - BUILD - COMPLETE

* Work completed
    - TDD: two read-count tests were red at dd16eac, with each existing `.tree` read 3 times in both `note` and `nap`. Built to the amended plan; py311 gave 426 passed.
    - Commit 4a0b9e9 `fix: read each children file once per command` holds the code, tests, the architecture sentence, and the SumMem notes and naps.
    - Net `summem` delta from dd16eac is −8 lines (+36 −44; the lock body was re-indented).
* Measurements after build, same 4094-leaf store, median of 15, two passes. Pass 1 was a noisier machine.
    - `.tree` reads: `note` 22 → 11 and `nap` 34 → 12 (dd16eac → built). Digests: `note` 8236 → 4142 and `nap` 12353 → 4165.
    - In-process, pass 1 then pass 2:
        - `note`: main 85.0 / 64.7, dd16eac 110.4 / 67.5, built 69.1 / 51.1 ms.
        - `nap`: main 121.3 / 90.0, dd16eac 141.6 / 123.6, built 56.8 / 55.6 ms.
    - Subprocess median, interleaved, pass 1 then pass 2:
        - `note`: main 175 / 140, dd16eac 197 / 154, built 162 / 137 ms.
        - `nap`: main 188 / 174, dd16eac 207 / 181, built 170 / 128 ms.
        - `version` (startup only): 59–82 ms.
* Decisions made
    - Declined preflight run 2's write-through cache. The benchmark has no heal split to justify the lines.

## 2026-10-31 - QA - COMPLETE (run 1)

* Result: `FAIL` (first line of `.qa-validation-status`). Build must rerun. The plan stands.
* Findings
    - Blocking (Documentation): SumMem memory still says heal walks raw JSON (#51). Root wake's first line reads "heal raw JSON". No new note supersedes it, so a later agent could restore the second parse that #88 rules out. Fix: record one superseding note, nap if asked, and commit. No code change.
    - Advisory: the read-count tests pin the exact number of `.tree` files read (`len(counts) == 3` / `4`). The contract is "at most once", so a correct change that reads fewer files would turn them red.
    - Advisory: `_digests_of_tree` now runs inside `_as_child`'s `try`, so non-`ValueError` digest errors give "unreadable pack". This matches heal's old refusal set (#88). `_CHILDREN` is set before the lock is taken, and nesting would fall back to a fresh parse. Neither needs action.
    - Clean: KISS, DRY, YAGNI, completeness, integrity, regression (the eviction keys match the `list_view` paths), and the architecture sentence. `tox -e py311`: 426 passed.

## 2026-10-31 - BUILD - COMPLETE (QA run 1 rework)

* Work completed
    - Recorded the superseding SumMem note: heal no longer walks raw JSON (#51 reversed). It shares `_as_child`'s parse and refusal set (#88). Did the nap the driver asked for.
    - Took the QA advisory: the read-count tests now assert only `max(counts.values(), default=0) <= 1`, which is still red at dd16eac (3 reads). Dropped the unused return value of `_over_budget_naps`.
    - `tox -e py311`: 426 passed. Commit d482447.
