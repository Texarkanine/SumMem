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

## 2026-08-24 - BUILD - COMPLETE

* Work completed
    - Unit 1: `reaches` / `zoom_reaches` enqueue `_nap_child_ids` from `Tree.kids`; `tests/test_gitutil.py` monkeypatches `zoom_text` to wake grammar.
    - Unit 2: zoom children print `format_wake_line(_projected_child(...), named_ids)`; dropped `_zoom_note_line`; `_find_in_tree` returns `NoteChild | NapChild`.
    - Unit 3: recall matches `node.caption` / nested text and sum, prints the same grammar.
    - Unit 4: Register Memories clause is clone-portability membership; lockstep `prompt_text()` / `AGENTS.md` / `docs/agents-prompt.md`.
    - Unit 5: atlas § Zoom and recall and `systemPatterns.md` wake-dates-leaves paragraph updated.
    - `uvx --with tox tox`: py311–py314, 275 passed each.
* Decisions made
    - Took preflight advisories: one listing renderer (`_projected_child` + `format_wake_line` only); did not reopen the wake printer; both walkers changed in unit 1.
    - `zoom_reaches` loads the driver as `summem_gitutil` (register in `sys.modules` before `exec_module`) so it does not import `conftest`.
* Insights
    - Uncommitted product files in this workspace were restored to HEAD more than once during plan/preflight. Stage and commit as soon as a slice is green.

## 2026-08-24 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of all five plan units against `summem`, `tests/gitutil.py`, zoom/recall/init tests, prompt lockstep, and atlas/briefing updates.
    - Verified walkers enqueue `NapChild.id` from trees (not zoom stdout tokens); zoom/recall share `_projected_child` + `format_wake_line`; recall matches sentences; prompt clone-portability wording; docs aligned.
    - Re-ran `uvx --with tox tox`: 275 passed on py311–py314.
    - Wrote `memory-bank/active/.qa-validation-status` with first line `PASS`.
* Decisions made
    - PASS with advisories only; no Build rework required.
* Insights
    - Proof suites indirectly validate `zoom_reaches` after the walker retarget; a dedicated wake-grammar test exists for in-process `reaches` only.
    - `prompt_text()` still labels pack prefixes `<hash>` in Other commands while stdout uses `short_id`; harmless but could be tightened in a follow-up.

## 2026-08-24 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-agent-display-unify.md`.
    - Reconciled persistent files: systemPatterns already carried the listing contract from Build; productContext and techContext unchanged.
* Decisions made
    - Left QA advisories as follow-ups (dedicated `zoom_reaches` test, prompt `<hash>` wording, shared gitutil helpers in the monkeypatch test).
* Insights
    - Stdout-as-id in proof walkers was the real plan gap, not the printer.
    - Uncommitted product files do not survive overlapping plan/preflight in this workspace.

## 2026-08-24 - ARCHIVE - IN-PROGRESS

* Work completed
    - Operator invoked `/niko-archive` then `/handoff`.
* Decisions made
    - Category: enhancements (unify existing listing printers; not a new command).
* Insights
    - Working tree was already clean at REFLECT COMPLETE (`6de680b`).
