# Active Context

## Current Task: heal-same-text
**Phase:** BUILD - IN-PROGRESS (unit 3)

## What Was Done
- Unit 2: `write_nap` rejects any intersecting digest sets. Direct `write_nap` of two identical-text notes raises `overlapping packs`; both notes remain. After heal, napping one id twice is `not adjacent`. Kept the existing overlap error string (one family).

## Next Step
- Unit 3: retarget fold listings so after heal there is one node and no `(id, id)` pair.
