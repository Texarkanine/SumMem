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
