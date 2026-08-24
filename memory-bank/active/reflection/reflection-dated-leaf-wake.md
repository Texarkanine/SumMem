---
task_id: dated-leaf-wake
date: 2026-08-24
complexity_level: 2
---

# Reflection: dated-leaf-wake

## Summary

Leaf wake lines are now `x1 (YYYY-MM-DD): text` from the filename stamp. Packs stay undated. The change is print-only; store files and zoom/recall `{id}  {text}` did not move.

## Requirements vs Outcome

All seven brief requirements landed. Nothing was dropped. Additions were implementer notes from preflight: `dated_leaf` in `tests/conftest.py`, retarget of `tests/test_proof_ingest.py`, and dedicated tests for empty caption and nested expand.

## Plan Accuracy

The printer-then-prose sequence was right. The Challenges grep list was too narrow: it named wake/expand/fold exact strings and missed the ingest proof’s `{"alpha", "beta"}` set. Preflight caught that; build did not discover it the hard way. The 2026-08-19 “date every line” shape did not sneak back in.

## Build & QA Observations

Build was one TDD cycle on `format_wake_line` plus lockstep copy. QA passed on the first Grok pass. The first QA spawn (GPT) died at launch on Other Models quota and never wrote a status file.

## Insights

### Technical

- Dating a pack with the leftmost child’s day is a lie once grain can span months. `kind == "note"` vs `leaves <= 1` is the load-bearing split: grain-1 packs and missing/conflict `.sum` lines stay undated because they are not notes.

### Process

- A wake-format change has to grep the whole `tests/` tree for exact line *sets*, not only the files named in the plan. `test_proof_ingest.py` was the leftover that the named-file grep would have missed.
- Other Models quota is still exhausted on 2026-08-24. Spawn Niko judge children on Grok first, or the phase dies before it starts.

### Million-Dollar Question

What we built is the OptMem-shaped answer: date only the thing that has one day. The false start was dating every wake line in wake-listing, then stripping dates in tree-schema. If leaf-only dates had been the assumption, `_day_from_stamp` would have stayed on the printer and tree-schema would have dropped pack dates only.
