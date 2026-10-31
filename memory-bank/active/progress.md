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

## 2026-10-30 - BUILD - COMPLETE

* Work completed
    - `_fold_grains` now uses `_as_child`. `ValueError` is grain 0. A parsed tree contributes its digest count.
    - Added `test_fold_request_skips_a_pack_whose_digest_count_is_not_the_stem_grain`. It failed on the filename pair, then passed.
    - `tox -e py311`: 421 passed.
    - Recorded the rule in SumMem and napped the pair that note requested.
* Decisions made
    - Did not change `write_nap`'s filename equality check. The issue points `_fold_grains` at `_as_child` and leaves that check in place.
* Insights
    - A row whose digest count matches another row, while its filename grain does not, can still be requested and then refused with `not the same grain`. The filed stall is the opposite shape, and that shape is what the test pins.

## 2026-10-30 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the diff against the brief. `tox -e py311`: 421 passed.
    - Reproduced a fold request that `nap` refuses: filename grains `[2, 4]`, digest counts `[4, 4]`.
* Decisions made
    - FAIL: requirement 3 is not met for that shape. Build reruns, test first.
* Insights
    - `write_nap` still checks `left.leaves != right.leaves` while `_fold_grains` now pairs on digest counts, so the two disagree whenever a stem and its tree differ.

## 2026-10-30 - BUILD - BLOCKED

* Work completed
    - Stopped after the QA fail. Did not change `write_nap` or `_fold_grains` further.
* Decisions made
    - The two fixes QA named are different products. The issue text does not choose between them. Left for the operator.
* Insights
    - Digest-count grain without a filename check lets a lying stem fold with a truthful row of that count. Zeroing every stem/digest mismatch also skips two rows `nap` would accept today when they lie the same way.

## 2026-10-30 - BUILD - IN-PROGRESS

* Work completed
    - Recorded the operator's choice and returned to build.
* Decisions made
    - `write_nap` drops the filename `leaves` check. Unequal digest counts are `not the same grain`. A power-of-two digest count stays eligible even when the filename disagrees, and it may fold with a truthful row of that count.
    - Do not mark a row ineligible only because the filename and the digest count disagree. Wake still lists `node.leaves`. Leave the OSError advisory alone.

## 2026-10-30 - BUILD - COMPLETE

* Work completed
    - Removed `left.leaves != right.leaves`. `len(digs_l) != len(digs_r)` raises `not the same grain`. A non-power-of-two total still raises `not a power of two`.
    - Added `test_fold_request_folds_a_lying_filename_with_a_truthful_row`. It failed on `not the same grain`, then passed. The digest-count-3 test still passes.
    - `tox -e py311`: 422 passed.
* Decisions made
    - Followed the operator: a lying stem stays eligible and may fold with a truthful row of the same digest count.
* Insights
    - A note and a 2-pack still fail `not the same grain`, because their digest counts are 1 and 2. Two legacy 6-packs still fail `not a power of two`.
