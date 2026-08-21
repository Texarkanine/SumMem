---
task_id: note-ack
date: 2026-08-21
complexity_level: 2
---

# Reflection: note-ack

## Summary

`summem note` now prints `Saved.` after a successful write, then maybe a fold request. The baked prompt says the note is already stored; do not retry. QA passed.

## Requirements vs Outcome

Delivered as specified. ACK is `Saved.` on the `note` path only. Write still happens inside `note_locked` before ACK. Prompt lockstep and README match. No `surgery.py`. Did not move ACK inside `note_locked` (preflight advisory); took the cheap over-budget-nap `Saved.` assertion.

## Plan Accuracy

The named silent-stdout retargets were the right list. Red was five empty-stdout failures. No extra files, no helper. Resume from BUILD after the prior session died at `resource_exhausted` did not need a re-plan.

## Build & QA Observations

TDD was clean: stubs, red, two `stdout.write` calls, green. Full `tox` 238 on py311–py314. QA PASS with two non-blocking advisories (post-lock ACK; atlas silent on `Saved.`). Other Models quota blocked `gemini-3.1-pro`; inherit QA worked.

## Insights

### Technical
- `fold_request` is shared with `nap`. Putting `Saved.` in that helper is the lie this bug was about. Prefix on `main`'s `note` branch is the whole design.

### Process
- A BUILD-READY baton is enough to resume after `resource_exhausted`. Re-running plan/preflight would have been waste.

### Million-Dollar Question
If ACK had been assumed from the start, `note` would never have been silent, so tests would never have encoded `out == ""`. The helper would still return fold text or empty; only `note` would prefix `Saved.`. Printing ACK immediately after `write_note` (before heal) is closer to OptMem; the committed post-lock print still matches the wire contract when heal succeeds.
