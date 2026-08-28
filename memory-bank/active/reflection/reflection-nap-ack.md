---
task_id: nap-ack
date: 2026-08-28
complexity_level: 2
---

# Reflection: nap-ack

## Summary

Successful `nap` now prints `Saved.` then either the next fold prompt or `Nothing left to compress.` QA passed. The over-long ratchet still does not ACK.

## Requirements vs Outcome

All five brief requirements shipped. One addition: `docs/surgery.md` Aftercare, from a preflight advisory, so the surgeon recipe does not still wait for silent nap stdout. `how_to_text` / `prompt_text` were left alone on purpose.

## Plan Accuracy

Sequence and file list held. The identified challenge (idle inside `fold_request` would ACK a note) did not materialize because the nap arm was the only printer. Preflight's blank-line advisory was the only test-plan tightening.

## Build & QA Observations

Red was three nap-stdout tests; the new rejected-nap test was already green. QA found no gaps. The `note`/`nap` ACK duplication is the known deferred helper.

## Insights

### Technical
- Idle means “no next fold request,” including an over-budget view with no equal-grain pair. That is the same honesty as `note` on a 16-pack plus one.

### Process
- Nothing notable

### Million-Dollar Question

One `emit_result` used by `note`, `nap`, and surgery's post-excision print — ACK and idle as flags, `fold_request` still a prompt builder. That is what you would have if silence had never been the nap contract. We kept the four-line nap arm; the helper waits for a third writer.
