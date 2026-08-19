---
task_id: wake-listing
date: 2026-08-19
complexity_level: 2
---

# Reflection: wake-listing

## Summary

Wake is a recency budget of dated lines; `note`/`nap` print an OptMem-style `Run:` prompt with unique prefixes. SHA-256 stays on disk. It works, after one QA round on identical notes.

## Requirements vs Outcome

Delivered: `WAKE_LINES` cap, dated note/pack lines, fold prompt from writes only, prefix `nap`/`zoom`, proofs inverted. Added in re-run: a repeated content id is one prefix, not an ambiguous 64-hex pair. Nothing dropped.

## Plan Accuracy

Units 1–5 were the right sequence. The plan said two prefix matches are an error, meaning two *distinct* ids. Build applied that to a list that still had duplicate rows, so twins emitted full hashes and `resolve_id` rejected the command it had just printed.

## Build & QA Observations

Format, cap, and prompt landed clean. First QA failed on twins; the suite had `write_nap(id, id)` but no CLI prompt that had to round-trip the prefix. Second QA passed after `dict.fromkeys` in `short_id`/`resolve_id` plus three regressions.

## Insights

### Technical
- A content id names leaves. Uniqueness for prefixes is the set of ids, not the list of view rows.

### Process
- Tests that assert `short_id()`'s own output hide this class of bug. Assert length 8 (or "not 64 hex") on a duplicated id list.

### Million-Dollar Question

Treat the namable set as a set of ids from unit 1. That is what the re-run built. No other shape.
