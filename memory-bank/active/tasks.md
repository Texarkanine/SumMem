# Current Task: fold-grain-as-child

**Complexity:** Level 1

## Build

- [x] `_fold_grains` reads `_as_child`. `ValueError` is grain 0. Otherwise the grain is the digest count, not the filename.
- [x] A hand-edited parsing `.tree` whose digest count is not the stem grain: the request names the other legal pair, and `nap` accepts it. Wake still lists the filename grain.
- [x] `tox -e py311`: 421 passed.

### What broke

A children file that parsed still counted as the filename grain. `fold_request` named that row, `nap` refused with `not a power of two`, and the next note asked for the same pair.

### Why

`_fold_grains` treated a successful `loads_tree` as eligible at `node.leaves`.

### What changed

`_fold_grains` now uses the digest count from `_as_child`, or 0 when that call raises `ValueError`. `fold_request` and `write_nap`'s nearest-twin check both already call it. Wake still lists the filename grain.

### Files

- `summem`
- `tests/test_fold.py`
- `docs/architecture/index.md`
- `memory-bank/systemPatterns.md`
- `.summem/` note, and the nap that note required
