# Progress

Stop wake from dropping oldest view nodes when the listing is over `WAKE_LINES`. Over-budget prints stay complete; `note`/`nap` fold the count back to spec.

**Complexity:** Level 1

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator approved
    - Classified Level 1 (single-component bug in `expand_frontier`)
    - Wrote ephemeral brief, context, tasks stub, and this file
* Decisions made
    - Level 1: remove the newest-N slice; do not redesign fold or expand-under-budget
    - Work on a feature branch off `origin/main`
* Insights
    - The atlas already says an at-or-over-budget wake lists view nodes and does not zipper. The cut is `nodes[-budget:]` in `expand_frontier`, pinned by `test_wake_prints_at_most_wake_lines_newest`.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - Removed both newest-N slices in `expand_frontier`
    - Inverted the newest-four wake oracle; added oldest-pack keep; retargeted recall and 8-2-1 zipper tests
    - Surgical atlas / product / patterns updates
* Decisions made
    - `WAKE_LINES` stays a fold budget and an expand-when-short target, not a print cap
    - Expand overshoot (if a nap ever splits by more than +1) stays visible rather than re-slicing
* Insights
    - A second `frontier[-budget:]` after expand would have kept cutting even after the first slice was gone
    - The 8-2-1 zipper case already documented “lists three files at budget 2”; the test had drifted to a cap
