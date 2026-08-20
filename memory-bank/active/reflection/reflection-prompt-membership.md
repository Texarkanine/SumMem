---
task_id: prompt-membership
date: 2026-08-20
complexity_level: 2
---

# Reflection: prompt-membership

## Summary

Split the baked Register Memories paragraph so the dump imperative and the clone-portability membership test are separate sentences. `AGENTS.md` lockstep. No store or CLI change. QA passed after a `tasks.md` duplicate was removed.

## Requirements vs Outcome

Delivered the creative’s sentence split. Did not name OptMem, redact the leak, add a denylist, or add phrase tests. Did not take the first-preflight advisory (labeled When to note / What belongs headings).

## Plan Accuracy

The first plan invented executable tests on prompt wording. Those would have been green-before-change on the `personal` split, and they were change-detectors. Operator cut them; replan as prose/policy was the right unit type. File list (`prompt_text()`, `AGENTS.md`) was correct throughout.

## Build & QA Observations

Build was the two-file wording change; 215 tests × four Pythons stayed green. First QA failed because marking the prose unit complete pasted its three steps a second time. Rework deleted that block. Second QA passed.

## Insights

### Technical

- The old dump sentence already ended before `Personal, machine-local… stay out`. What was still jammed into the imperative was `acceptable in git forever`, not the stay-out clause.

### Process

- Asserting on `prompt_text()` sentences is a change-detector. `init` printing that string does not make the wording an executable unit. The lockstep test (`AGENTS.md` prefix equals `prompt_text()`) is the contract that belongs.
- Do not check off a plan unit by duplicating its body.

### Million-Dollar Question

Labeled child blocks under Register Memories (`When to note` / `What belongs`), the same cheap-agent move as the catalog headings. We shipped two unlabeled sentences instead. That is still option B; it is not the stronger structure the first preflight named.
