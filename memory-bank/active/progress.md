# Progress

Change fold requests from oldest-two left-fold to equal-grain pairs, emit a catch-up nap after each write while over budget, and rewrite proof 4's pack sizes so production fold matches the year-later short tree.

**Complexity:** Level 2

## 2026-08-18 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Advanced L4 `file-backend`: marked single-store complete, deleted single-store `tasks.md` / `activeContext.md` / `progress.md` / `.qa-validation-status` / `.preflight-status`
    - Classified issue #1 (equal-grain fold) as Level 2
    - Wrote a new `projectbrief.md` scoped to the picker, catch-up chain, and proof 4 pack math
* Decisions made
    - Level 2, not Level 3: one policy in the existing nap-request path; the CLI does not grow; identity, wake, zoom, and `write_nap` stay; architecture is already in issue #1 and `VISION.md`'s year-later diagram
    - Level 2, not Level 1: production fold shape and proof 4 packing change; not a single-component bug
* Insights
    - `write_nap` may still fold any two adjacent nodes so a post-merge lazy cover remains an agent nap; only the request printer becomes equal-grain
    - Proof 4's 40/30/30 is a left-spine helper, unreachable under equal-grain; squash+zoom stays, pack sizes become powers of two

## 2026-08-18 - PLAN - COMPLETE

* Work completed
    - Wrote the L2 equal-grain plan in `tasks.md`: picker, catch-up print after `nap`, proof 4 helper packs 64/32/4, contract wording
    - Mapped red tests to `tests/test_fold.py`; proof 4 stays a green helper adaptation
* Decisions made
    - Sequential emit after each `nap`, not a pre-printed disjoint list
    - `write_nap` still accepts any adjacent pair; only the request printer is equal-grain
    - Delete `oldest_adjacent` so a second fold policy cannot linger
    - No creative phase: issue #1 and the year-later diagram are the design
* Insights
    - A long-stream test that only asserts powers of two is vacuous on a `None` stub (all 1s); it must also bound view length and require a real fold
    - Depth must fold via `equal_grain_pair`, not `fold_ids`, or a correct picker still sees a left spine

## 2026-08-18 - PREFLIGHT - COMPLETE (FAIL)

* Work completed
    - Validated the plan's TDD ordering, conventions, dependency impacts, existing implementations, requirements, and proof touchpoints
    - Reproduced same-second parent reordering: four notes can become grains `[1, 2, 1]` after one adjacent fold
    - Reproduced an over-budget equal-grain stall: 24 same-second notes at budget 8 stopped at 12 view nodes with no adjacent equal pair
    - Recorded the failed gate and required replanning in `tasks.md` and `.preflight-status`
* Decisions made
    - Block build because the planned policy does not guarantee a short bounded view for supported same-second notes
    - Require `/niko-plan` to design a carry-stable nap sequence key before implementation
    - Require the 16+1 CLI setup and depth assertion to be corrected during replanning
* Insights
    - Minimum child time is not enough to preserve a folded interval when note timestamps tie; the leaf-set hash can move the parent between surviving notes
    - `zoom_reaches` bounds breadth-first work, not hop depth, so it cannot prove the logarithmic-depth acceptance criterion

## 2026-08-18 - PLAN - COMPLETE (replan after preflight FAIL)

* Work completed
    - Rewrote the L2 plan: carry-stable nap names first, then equal-grain picker, catch-up, proof 4 packs, contract wording
    - Added same-second `[2, 1, 1]` and 24-note same-second stream as the regression that failed preflight
    - Updated `projectbrief.md` with the filename order-key requirement
* Decisions made
    - Stem is `{stamp}-{rand}-{leafset}-{leaves}`; `{stamp}-{rand}` copied from the left child's filename
    - Stay Level 2; no creative phase
    - Depth is max NoteChild depth in `.tree`; `zoom_reaches` stays a reachability check
* Insights
    - Tests that used `split("-")[1]` as leafset must move to `[-2]` in the same unit as the stem change
    - A mixed-time long stream would not catch the stall; the hard case is one UTC second

