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
