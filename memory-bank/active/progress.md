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
