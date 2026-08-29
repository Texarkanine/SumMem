---
task_id: note-membership
date: 2026-08-28
complexity_level: 3
---

# Reflection: note-membership

## Summary

Retargeted shipped `note` membership to “work on this repository”: a concise bootstrap probe, plus the existing root-wake genre list, telemetry denylist, and skip condition. QA passed; the phrase remains deliberately direct on both readable prompt surfaces.

## Requirements vs Outcome

Delivered as specified after PR feedback clarified that contributors use separate clones. Both surfaces carry the repository-work probe; how-to retains genre and PR/checks/archive denylist; writer-only and wake-usage split are untouched; no sibling product is named; the eternal-currency phrase is absent; sentence counts remain 3 bootstrap / 4 how-to. The phrase is intentionally repeated rather than factored into a constant.

## Plan Accuracy

The file list, TDD order, and scope were right. PR feedback exposed an imprecise subject noun, so creative and plan ran again before the revised tests. The red run failed on precisely the two changed output pins; lockstep correctly stayed green until `prompt_text()` changed. Named risks around denylist change-detectors, `(mandatory)`, and store rewriting did not materialize.

## Creative Phase Review

The first creative decision held on placement: split surfaces still keep the denylist off the always-loaded bootstrap. The second decision corrected the probe to repository work, which accurately matches committed cross-clone context. The accepted miss for agents that note before waking remains unchanged.

## Build & QA Observations

The revised output-pin tests first failed twice as expected, then all three targeted tests passed. `tests/test_init.py` passed 11/11, and `tox run-parallel` passed on py311 and py314 while py312/py313 were skipped for missing interpreters. Removing the later constant preserved those results.

## Cross-Phase Analysis

Preflight's body-versus-assertion check made the wording change straightforward. The repeated drift advisory prompted a constant, but the operator rejected that indirection: two direct, adjacent copies are easier to read and have negligible maintenance cost. Creative removed clone ambiguity before code changed, and the final direct form preserved verified behavior.

## Insights

### Technical

- The bootstrap and how-to deliberately repeat one short phrase; `AGENTS.md` lockstep still protects the separately generated bootstrap copy.

### Process

- For prompt-copy tasks, preflight that reads proposed bodies against surviving assertions is the load-bearing gate.
- A repeated advisory still requires a readability and ownership check; two short, adjacent prompt literals do not justify indirection.
