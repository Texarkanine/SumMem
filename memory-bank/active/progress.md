# Progress

Fold grain for pairing comes from the children `nap` can read, not from the filename. A hand-edited `.tree` that parses with a different digest count must not be requested and must not block a legal pair.

**Complexity:** Level 1

## 2026-10-30 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified issue #88 as a Level 1 bug fix in `_fold_grains`.
    - Confirmed a parsing `.tree` still contributes `node.leaves`, so `fold_request` can name a pair `write_nap` refuses with `not a power of two`.
* Decisions made
    - Level 1: one helper, no plan, creative, or preflight. QA is the completion gate. No archive.
    - Grain is `len(digests)` from `_as_child`, or 0 when that call raises `ValueError`. Filename grain stays on the wake listing.
* Insights
    - `_as_child` already turns a missing or unreadable children file into `ValueError`. Catching that covers the #87 grain-0 cases without a second `loads_tree`.
