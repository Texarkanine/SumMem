---
task_id: prompt-commit-notes
date: 2026-08-19
complexity_level: 2
---

# Reflection: prompt-commit-notes

## Summary

Shipped [SumMem#14](https://github.com/Texarkanine/SumMem/issues/14): the baked prompt now tells agents to `git add` and commit the files the script wrote, and the briefing no longer says this repo ignores store data. 208 pytest. QA PASS after one assertion rework.

## Requirements vs Outcome

Delivered as specified. Added a briefing narrow (CLI stays git-silent; activation block teaches publish) so `productContext` and the atlas would not contradict the prompt. Did not make the script commit, add hooks, or change note identity.

## Plan Accuracy

File list and TDD sequence were right. The real surprise was QA, not the plan: a bare `"commit"` substring is too weak even when the cited witness (`committed AGENTS.md`) is not in `prompt_text()`.

## Build & QA Observations

Build was one red-then-green test plus three prose edits. QA FAIL was a real hole in the test, not in the prompt. Tightening to `commit them` and `own commit` closed it.

## Insights

### Technical
- A prompt-content assert has to name the instruction (`commit them`), not a word that other sentences can grow (`commit` / `committed`).

### Process
- Nothing notable

### Million-Dollar Question

The script stays the only writer. Git publish is an agent duty the prompt already owed, not a new store role. What we built is the foundational shape.
