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

## 2026-08-24 - BUILD - COMPLETE

* Work completed
    - Local `_equal_grain_pair` in `tests/test_fold.py`; production function removed from `summem`.
    - `fold_request` left with its own ViewNode walk.
    - `tox` 275 passed py311–py314.
* Decisions made
    - Same four-line walk in tests; no production symbol.
* Insights
    - Tests stayed green after the move, then stayed green after the deletion.
