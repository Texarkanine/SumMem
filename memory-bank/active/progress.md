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
