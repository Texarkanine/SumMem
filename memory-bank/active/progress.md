# Progress

Delete unused `equal_grain_pair` from `summem` and keep the equal-grain selector in fold tests only.

**Complexity:** Level 1

## 2026-08-24 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Operator restated issue #39: production must stay lean; selector belongs in test code.
    - Classified Level 1 (single-component dead-code removal).
* Decisions made
    - Do not wire `fold_request` to the helper. Duplicate the four-line walk in `tests/test_fold.py`.
* Insights
    - `fold_request` needs adjacent ViewNodes; the test helper returns ids. The copies can differ for that reason.
