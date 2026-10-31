# Progress

One bad fold row must drop out of the pair scan. A note that disappears after listing stays one digest and is not opened during the scan. A children file that parses with a non-string note text is grain 0. Neither aborts the other rows.

**Complexity:** Level 1

## 2026-10-31 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Read both review threads on pull request 95
    - Traced `_fold_grains` through `_as_child`, `_note_child`, and `_digests_of_tree`
* Decisions made
    - Level 1: both failures live in the fold scan of `summem`
    - A vanished note stays at `node.leaves` (one digest); the scan does not open it
    - Non-string note text raises `ValueError` from the digest path so the existing catch applies
* Insights
    - Catching `OSError` in the scan would also let the other rows fold, and would hide the missing note from the pair. The review asks for the note to stay at `node.leaves`.
    - `loads_tree` accepts a non-string `text`. `note_file_bytes` then raises `AttributeError` outside the `ValueError` catch.

## 2026-10-31 - BUILD - COMPLETE

* Work completed
    - Failing tests for a note unlinked after listing, and for a parsed children file whose note text is not a string
    - `_fold_grains` keeps notes at `node.leaves`
    - `_digests_of_tree` raises `ValueError("unreadable pack")` for non-string note text
    - py311: 425 passed
* Decisions made
    - The scan does not catch `OSError`. A missing note still counts as one digest until something naps that row.
    - The new error is `ValueError`, not a wider catch
* Insights
    - Grain 0 from catching `OSError` would drop the missing note out of the pair. Keeping `node.leaves` leaves `OSError` on the nap of that row.

## 2026-10-31 - QA - COMPLETE

* Work completed
    - Reviewed the `summem` and `tests/test_fold.py` diff against the brief
    - py311: 425 passed
* Decisions made
    - PASS, no blocking findings
* Insights
    - The raise sits in `_digests_of_tree`, so `nap` of a pack with non-string note text now says `unreadable pack` instead of crashing.
