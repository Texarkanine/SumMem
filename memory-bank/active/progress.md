# Progress

Print leaf `wake` rows as `x1 (YYYY-MM-DD): text` from the note stamp. Leave nap lines undated. Update the shared printer, tests, and agent-facing copy so leaves are distinct rows and dates are not burned in prose.

**Complexity:** Level 2

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed: dates on leaves only, parenthetical day, `x1` row prefix, no date on naps, no after-colon fake body
    - Classified as Level 2
* Decisions made
    - Level 2: enhancement to one print contract (`format_wake_line` and its callers), not a bug and not a new subsystem
    - Task id: `dated-leaf-wake`
    - Grain-1 packs stay caption-only; only `kind == "note"` is dated
* Insights
    - OptMem already dates leaves only; dating packs with the leftmost stamp would misrepresent span
    - Dates were on every wake line after wake-listing and were dropped in tree-schema; this restores a leaf-only, parenthetical form rather than that old shape
