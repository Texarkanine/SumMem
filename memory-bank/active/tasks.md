# Current Task: drop-equal-grain-pair

**Complexity:** Level 1

## Build

- [x] What broke: `equal_grain_pair` lived in the copied `summem` driver and was never called by production.
- [x] Why: fold tests used it as an oracle; that is not a reason to keep it in a script consumers copy.
- [x] What changed: deleted the function from `summem`. Added `_equal_grain_pair` in `tests/test_fold.py` (same four-line adjacent-same-grain walk). Pins and nap-cascade oracles now call the local helper. `fold_request` still walks adjacent ViewNodes itself.
- [x] Files: `summem`, `tests/test_fold.py`
- [x] `uvx --with tox tox` 275 passed on py311–py314
