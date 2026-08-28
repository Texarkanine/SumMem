---
task_id: fold-pack-captions
date: 2026-08-28
complexity_level: 2
---

# Reflection: fold-pack-captions

## Summary

`fold_request` now quotes pack captions without grain or content-id. Wake, recall, zoom, and the `Run:` line still carry ids. QA passed.

## Requirements vs Outcome

All four brief requirements landed. Leaf-pair quotes stayed dated. Empty captions (missing `.summ`) quote blank text instead of reconstructing `xN <prefix>:`. Nothing added beyond the plan except pinning `WAKE_LINES` to 2 in the pack-pair wake assertion.

## Plan Accuracy

File list and TDD order held. The real surprise was not `format_wake_line` leaking into fold; it was `wake_text` expanding under-budget packs, so a default-budget `wake_text` assertion never saw `x2` lines.

## Build & QA Observations

Red-then-green was two tests; the wake assertion needed one fix. QA passed with no rework. A live `note` immediately printed caption-only pack quotes and `Run:` prefixes, which is the agent-facing proof.

## Insights

### Technical
- `wake_text` expands packs when the view is under `WAKE_LINES`. A test that wants packed wake lines must pin the budget at or over the view size.

### Process
- Nothing notable

### Million-Dollar Question

Wake listings orient; fold quotes are the writing task. If that split had been the original contract, `fold_request` would never have called `format_wake_line` for grain>1 packs. Two local selections are that design. A shared `_fold_quote_line` still waits for a second caller.
