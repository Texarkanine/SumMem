# Active Context

## Current Task: heal-same-text
**Phase:** BUILD - IN-PROGRESS (unit 2)

## What Was Done
- Unit 1: removed the note/note skip in `_first_overlap`. Heal keeps the later filename of two identical loose notes. Packed-text duplicate notes still drop (trigger 1). `assert_unique_cover` now checks note/note pairs.

## Next Step
- Unit 2: `write_nap` rejects any digest overlap.
