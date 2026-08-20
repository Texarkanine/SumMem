---
task_id: agents-prompt
date: 2026-08-19
complexity_level: 2
---

# Reflection: agents-prompt

## Summary

`summem init` prints a baked agent prompt; this repo’s `AGENTS.md` starts with the same block. Cheap Composer 2.5 agents woke once and skipped a second root wake.

## Requirements vs Outcome

Delivered as planned: help-shaped `init`, lockstep `AGENTS.md`, VISION/ROADMAP/persistent-file updates, Composer probes. Added a tighter pull sentence after Probe A followed the catalog as a command list. Did not rewrite catalog text (outside issue #2).

## Plan Accuracy

Sequence and files were right. The surprise was catalog wording, not `init` dispatch.

## Build & QA Observations

Build was TDD-clean (204 passed). QA passed with an advisory: `summem` on PATH vs `./summem`; Probe A already inferred `./summem`.

## Insights

### Technical
- A catalog line that is only `summem wake --path dogfood` is treated as “run this now” by a cheap agent. The prompt can say “when you work under that path”; the catalog still prints the bare command.
- Naming `.summem/summem` even to forbid it fails a substring invariant. Teach the positive: repo-root `summem`.

### Process
- Composer 2.5 probes caught the catalog over-pull; pytest would not have.

### Million-Dollar Question

Bake the prompt in the driver and lockstep it to `AGENTS.md` — that is the right shape. The catalog instruction should eventually match VISION (“when you work under that path”), not a bare command. That is a later change, not this one.
