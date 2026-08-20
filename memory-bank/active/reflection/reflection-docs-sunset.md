---
task_id: docs-sunset
date: 2026-08-19
complexity_level: 2
---

# Reflection: docs-sunset

## Summary

Retired `VISION.md` and `ROADMAP.md`. The living surface is a sibling-genre README, a mkdocs-shaped `docs/` (architecture atlas, leftovers notes, landing), and a memory-bank that no longer treats VISION as the contract. QA failed once on inherited VISION sentences, then passed.

## Requirements vs Outcome

All six brief items landed. Leftovers were real (sqlite, hooks, `cover(T)`, pack-size, hot margin). The architecture page was written, not skipped. One addition: an `AGENTS.md` When-to-load pointer after the baked prompt. Preflight’s test-docstring invariant anchoring was left undone (no operator direction).

## Plan Accuracy

The six-step sequence was right. The triage list was not closed enough on the strongest claims: “file count,” “same leaves, same `.tree` bytes,” and “vanished id is success” sounded true because VISION said them. The surprise was QA, not missing files.

## Build & QA Observations

Build was prose-only and the suite stayed at 207. First QA caught three atlas lies that copy-forwarded retired contract language. Rework narrowed each claim to `summem` and aligned the briefing.

## Insights

### Technical
- Nested captions live inside `.tree`. Leaf-set identity never implied identical payload bytes except for the same `Tree` (same grouping, same nested wording).

### Process
- When sunsetting a design doc, the sentences most worth keeping are the ones to verify against the code. “Still sounds right” is how a retired contract becomes VISION 2.0.

### Million-Dollar Question

This is the shape we would have started with: README for operators, `docs/architecture` for changers, `docs/notes` for not-yet, memory-bank as an incomplete briefing. Nothing more elegant emerged.
