# Progress

`fold_request` quotes leaf pairs as dated wake lines. Issue #80 wants every fold quote to be caption / note text only; ids stay on `Run:`; wake / recall / zoom stay listing grammar.

**Complexity:** Level 1

## 2026-08-29 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated [issue #80](https://github.com/Texarkanine/SumMem/issues/80); operator approved.
    - Classified Level 1: bug leftover from #72 in one function plus its test and contract docs.
* Decisions made
    - L1: skip plan, creative, and preflight; go to Build.
* Insights
    - #72 left leaf-pair quotes on `format_wake_line` on purpose. That split is now the defect.

## 2026-08-29 - BUILD - COMPLETE

* Work completed
    - `fold_request` quotes `node.caption` for both sides of every pair.
    - Tests: leaf-pair text-only quotes; dated pins in remaining/nap/note stdout retargeted; pack-pair and empty-caption tests still pass.
    - Atlas, `systemPatterns.md`, README example: fold quotes, period.
    - `tox -e py311`: 372 passed, 1 skipped.
* Decisions made
    - One code path for notes and packs. Empty caption stays a blank quote because caption is empty, not because of a special case.
* Insights
    - `format_wake_line` remains the listing grammar. Fold is not a listing.
