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

## Rework

- [x] Test: filename grains differ, digest counts are equal and a power of two. The request names that pair, and `nap` accepts it. Wake still lists the filename grain.
- [x] `write_nap` drops `left.leaves != right.leaves`. `len(digs_l) != len(digs_r)` is the same-grain refusal.
- [x] The digest-count-3 test still requests and accepts the other legal pair.
- [x] `tox -e py311`: 422 passed.

## QA round 1

**Result:** FAIL. Addressed in Rework. Review HEAD.

Also delete the qa status file as part of entering QA. I'll git rm it in the same commit.

- **Completeness / requirement 3:** `fold_request` can still name a pair `nap` refuses. Two nap rows with equal digest counts and different filename grains (e.g. filename 2 and 4, both 4 digests) get grains `[4, 4]` from `_fold_grains`, so they are requested. `write_nap` then raises `not the same grain` on `left.leaves != right.leaves` (`nap` exits 1) and the next note asks for the same pair. Reproduced with a scratch test, since removed. Build progress notes name this shape and leave it. The brief says fold eligibility is whatever `nap` can fold and a row `nap` would refuse is never requested.
- **Fix direction for Build:** write the failing test for this shape first. Then make the two sides agree. Either `write_nap` compares the digest counts it already has and drops the filename-based `leaves` check (keep a refusal for a loose note against a pack, as `tests/test_nap.py` expects), or `_fold_grains` also marks a row whose digest count differs from its filename grain as ineligible. Pick one and keep AC 3 (wake lists the filename grain).
- **Advisory:** `_fold_grains` now calls `_note_child`, which reads each loose note file. A note removed between listing and the request raises `OSError`, uncaught. It was not read before.
- **Advisory:** the new test uses a digest count of 3, which `_fold_pair` already skips. It does not show that the digest count, rather than the filename, decides the pair. Pin a pow2 digest count that differs from the stem too.
- **No issue:** KISS, DRY (reuses `_as_child`; second `loads_tree` removed), YAGNI, integrity. Docs in `docs/architecture/index.md` and `memory-bank/systemPatterns.md` updated and accurate. `_TREE_PARSE_ERRORS` is still used elsewhere. `tox -e py311`: 421 passed.
