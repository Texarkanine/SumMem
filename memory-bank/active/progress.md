# Progress

Move the duplicated broken-children setup out of the fold and nap tests into one helper in `tests/gitutil.py`. The four existing cases stay. No product change.

**Complexity:** Level 2

## 2026-10-30 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Read issue #89 and the two call sites.
    - Classified the task as Level 2.
* Decisions made
    - The duplication is real, so the task proceeds.
    - Level 2 because the change is one test helper in a named home, with no product behavior and no approach to choose.
* Insights
    - Fold's helper treats every non-`missing` value as unreadable. The nap test does the same. The shared helper should keep that branch.
