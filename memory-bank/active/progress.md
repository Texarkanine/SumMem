# Progress

Make `recall` and `zoom` unique-prefix in linear time and parse each view `.tree` at most once per command, as specified in issue #50.

**Complexity:** Level 2

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed worktree `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem` on `feat/recall-zoom-prefix`
    - Read issue #50 and the current `short_id` / `named_ids` / recall / zoom helpers
    - Classified Level 2 (simple enhancement)
* Decisions made
    - Implement; the hole is real and useful (measured 19s common-word recall on a 5k-leaf store)
    - Standing consent through archive and a non-draft PR; L3 halt-at-preflight does not apply because this is L2
* Insights
    - Wake listing is already cheap; leave wake/fold `short_id` call sites alone unless a shared table is free
    - `test_zoom.py` monkeypatches `named_ids` for the ambiguous-prefix case; parse-once must not silently drop that seam without updating the test

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `memory-bank/active/tasks.md`
    - Mapped TDD onto existing recall/zoom/wake tests; no new test files
* Decisions made
    - `unique_prefixes` via sort plus neighbor LCP; `short_id` becomes a lookup so wake/fold output stays equivalent
    - `format_wake_line` accepts a prefix `dict` for O(1) lines; list path stays for wake/fold
    - `_view_packs` records parse status only; commands decide warn vs raise
    - No process-global parse cache; no 5k-leaf pytest fixture
* Insights
    - `test_ambiguous_prefix_is_error` must move off a `named_ids` patch if zoom no longer calls it
