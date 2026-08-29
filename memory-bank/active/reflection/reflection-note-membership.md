---
task_id: note-membership
date: 2026-08-28
complexity_level: 3
---

# Reflection: note-membership

## Summary

Retargeted shipped `note` membership to “work on this repository”: a concise bootstrap probe, plus the existing root-wake genre list, telemetry denylist, and skip condition. QA passed after the repository wording and shared probe constant closed the prior drift advisory.

## Requirements vs Outcome

Delivered as specified after PR feedback clarified that contributors use separate clones. Both surfaces carry the repository-work probe; how-to retains genre and PR/checks/archive denylist; writer-only and wake-usage split are untouched; no sibling product is named; the eternal-currency phrase is absent; sentence counts remain 3 bootstrap / 4 how-to. `MEMBERSHIP_PROBE` was added during the revised build as the preflight advisory recommended, without changing the user-facing contract.

## Plan Accuracy

The file list, TDD order, and scope were right. PR feedback exposed an imprecise subject noun, so creative and plan ran again before the revised tests. The red run failed on precisely the two changed output pins; lockstep correctly stayed green until `prompt_text()` changed. Named risks around denylist change-detectors, `(mandatory)`, and store rewriting did not materialize.

## Creative Phase Review

The first creative decision held on placement: split surfaces still keep the denylist off the always-loaded bootstrap. The second decision corrected the probe to repository work, which accurately matches committed cross-clone context. The accepted miss for agents that note before waking remains unchanged.

## Build & QA Observations

The revised output-pin tests first failed twice as expected, then all three targeted tests passed. `tests/test_init.py` passed 11/11, and `tox run-parallel` passed on py311 and py314 while py312/py313 were skipped for missing interpreters. QA found no blockers or new advisories and confirmed that `MEMBERSHIP_PROBE` is the appropriate amount of sharing.

## Cross-Phase Analysis

Preflight's body-versus-assertion check made the wording change straightforward. Its repeated drift advisory became decisive once the PR-driven second wording revision demonstrated the same risk; build added one constant while retaining literal output assertions. Creative removed clone ambiguity before code changed, and QA confirmed the result without further rework.

## Insights

### Technical

- `MEMBERSHIP_PROBE` centralizes the phrase shared by `prompt_text()` and `how_to_text()`; the existing `AGENTS.md` lockstep assertion completes the three-surface consistency chain.

### Process

- For prompt-copy tasks, preflight that reads proposed bodies against surviving assertions is the load-bearing gate.
- A repeated advisory backed by a second real change is evidence to incorporate a small structural fix, not carry forward again.
