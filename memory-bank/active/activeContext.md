# Active Context

## Current Task: heal-same-text
**Phase:** BUILD - COMPLETE (PASS)

## What Was Done
- Unit 1: removed the note/note skip. Heal keeps the later filename of two identical loose notes. Packed-text duplicates still drop. `assert_unique_cover` checks note/note pairs.
- Unit 2: `write_nap` rejects any intersecting digest sets. Kept the existing `overlapping packs` error string.
- Unit 3: fold tests after heal see one node and no `(id, id)` pair. `fold_request` unchanged.
- Unit 4: Identity, Zipper, `systemPatterns.md`, and `docs/theory.md` describe trigger 1 as the shoebox. Leak section replaced with Duplicate receipts.
- Recoverable extra: `test_zoom_keeps_duplicate_note_dates` and `test_recall_keeps_duplicate_note_dates` now plant a children file instead of calling `write_nap`.
- py311: 371 passed, 1 skipped. `tox run-parallel`: py311 and py314 OK; py312 and py313 skipped (no interpreter).

## Next Step
- QA review.
