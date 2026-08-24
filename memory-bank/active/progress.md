# Progress

Unify agent-facing recall/zoom lines with wake’s grammar, make recall match sentences not formatted lines, and reword Register Memories so clone-portability cannot be read as eternal currency.

**Complexity:** Level 2

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated and approved; operator added that wake short hashes are the convention and zoom’s long hashes need a reason.
    - Classified Level 2 (Q1 fix → multiple components → L2). Not L3: no new addressing scheme; `short_id` already lengthens only until unique.
* Decisions made
    - Agent stdout never prefers 64-hex. Nested packs keep `xN <prefix>:` as the zoom handle. Nested leaves are dated with no hash.
    - Do not surgery the parenthesized note; fix the prompt that caused the misreading.
* Insights
    - Wake-listing already moved agent ids to unique prefixes; zoom/nested recall were left on the old `{64hex}  text` printer.
    - LlamaPReview’s “note must remain true after clone” reading is a prompt defect, not a store defect.

## 2026-08-24 - PLAN - COMPLETE

* Work completed
    - Wrote TDD plan: zoom children + recall match/print + prompt invariant + atlas/briefing.
    - Mapped tests onto `tests/test_zoom.py`, `tests/test_recall.py`, `tests/test_init.py`; no new test files.
* Decisions made
    - Printed pack prefixes always `short_id` against `named_ids` so a recall/zoom line is a zoom handle.
    - Match haystack is caption/text; printer stays `format_wake_line`.
* Insights
    - Dogfood `zoom 01b18901` dumping 64-hex is the pre-wake-listing printer (`_zoom_note_line`); wake-listing never updated it.

## 2026-08-24 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the plan against `summem` zoom/recall printers, existing tests, and `tests/gitutil.py`.
    - Wrote `memory-bank/active/.preflight-status` with first line `FAIL (fixable)`.
* Decisions made
    - Did not edit the implementation plan (no TDD order swap; no change-detector strike).
* Insights
    - `reaches` / `zoom_reaches` treat the first whitespace token of a zoom line as a content id. After `format_wake_line` that token is grain (`x1` / `xN`), so proof/zipper/surgery walks break unless the helpers are retargeted.

## 2026-08-24 - PLAN - COMPLETE (re-plan)

* Work completed
    - Retargeted leftover `{id}  text` zoom/nap/recall success tests into unit 1.
    - Scheduled `tests/gitutil.py` walkers to enqueue `NapChild` ids from the children tree, not `line.split()[0]`.
    - Kept prompt membership and atlas/briefing units; lockstep still `prompt_text()` first.
* Decisions made
    - Take the preflight advisory as the walker fix (test infra only). Do not parse a second stdout grammar.
    - Walker tests and zoom tests are written together in unit 1 step 3; walker and printer ship together in step 4.
* Insights
    - Uncommitted product edits appeared during this re-plan (zoom/nap/gitutil/summem). They were restored to HEAD so the plan stays a plan.

## 2026-08-24 - PLAN - COMPLETE (rework)

* Work completed
    - Added unit 1: proof walkers enqueue from trees; `tests/test_gitutil.py` monkeypatches `zoom_text` to wake grammar so the old `split()[0]` path goes red first.
    - Unit 2 now retargets `test_zoom_two_note_nap_prints_both_texts`, `test_zoom_loose_note_id_prints_the_note`, `test_zoom_nap_of_naps_prints_two_children_not_leaves`, and the zoom parse in `test_nap_of_two_naps_nests_napchild_and_unions_digests`.
* Decisions made
    - Do not parse the new `xN prefix:` line for ids. Walk `Tree.kids`. Keep `sentence in` zoom output so squash proofs still exercise zoom.
    - No parallel dated_* test names; change the existing functions.
* Insights
    - `conftest` imports `gitutil`, so `zoom_reaches` cannot call `load_summem`; it must `SourceFileLoader` `SCRIPT`.

## 2026-08-24 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-validated the reworked plan against `summem` zoom/recall printers, leftover `{id}  text` / `split("  ")` tests, and `tests/gitutil.py` walkers.
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`.
* Decisions made
    - Did not edit the implementation plan (no TDD order swap; no change-detector strike).
    - Prior FAIL (walkers parse zoom stdout; leftover exact-format tests) is now scheduled; not a new fail.
* Insights
    - `conftest.py` does not currently import `gitutil`; SourceFileLoader on `SCRIPT` is still the right load for `zoom_reaches`.
    - Wake still unique-prefixes against view ids; the plan's recall/zoom `named_ids` can print a longer prefix for the same view pack.
