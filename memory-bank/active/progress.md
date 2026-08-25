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

## 2026-08-25 - PREFLIGHT - COMPLETE

* Work completed
    - Validated implementation plan via `/niko-preflight` skill
* Decisions made
    - The first line of `.preflight-status` is PASS
* Insights
    - The implementation plan is structurally sound and strictly follows TDD requirements.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - Prefix table, shared view-tree walk, recall one pass, zoom one pass, atlas update
    - `uvx --with tox tox` 292 passed on py311–py314
* Decisions made
    - `short_id` delegates to `unique_prefixes([*ids, cid], floor)`
    - Wake expand still uses `_projected_child`; recall/zoom use indexed rows
* Insights
    - Eight new tests (292 total, was 284). Proof walkers still enqueue from `Tree.kids`.

## 2026-08-25 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the implementation against issue #50, the Level 2 plan, and established duplicate-id behavior
    - Ran `uvx --with tox tox`: 292 tests passed on each of Python 3.11, 3.12, 3.13, and 3.14
    - Probed duplicate-note indexing and nested row order directly
* Findings
    - The id-keyed projected-row dictionary collapses valid repeated note or nap occurrences; zoom can print the wrong date for a duplicate note and recall can omit distinct rows
    - Nap rows are inserted after descendants, changing nested recall from preorder to postorder
* Decision
    - FAIL; Plan must rerun because the planned id-to-row dictionary cannot preserve row multiplicity and order

## 2026-08-25 - BUILD - REWORK AFTER QA FAIL

* Work completed
    - `_index_tree` now returns preorder `hits`, first-id lookup, and per-nap child rows
    - Added three tests for duplicate dated notes and nested caption-before-leaf order
    - `uvx --with tox tox` 295 passed on py311–py314
* Decisions made
    - Treated QA "plan must rerun" as a fixable build gap: same walk, row-preserving structure
    - First matching id still wins for zoom find, matching old `_find_in_tree`
* Insights
    - Prefix uniqueness is among distinct ids; printed rows are not. An id-keyed row map cannot be the only index.

## 2026-08-25 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the reworked implementation against the previous QA FAIL findings
    - Verified `_index_tree` returns preorder `hits` and per-nap child rows
    - Verified `_zoom_kids` formats child rows in tree order
    - Verified new tests for duplicate note dates and nested caption-before-leaf order
* Findings
    - The id-keyed row dict was successfully replaced with an ordered `hits` list and a `first` lookup dict, preserving duplicate notes.
    - Nap rows are appended before descendants, restoring preorder traversal.
    - The implementation is acceptable as-is.
* Decision
    - PASS

## 2026-08-25 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-recall-zoom-prefix.md`
    - Reconciled persistent files
* Decisions made
    - Persistent briefing files needed no update; the atlas already carries parse-once and the prefix table
* Insights
    - Prefix uniqueness is among distinct ids; printed rows are not
