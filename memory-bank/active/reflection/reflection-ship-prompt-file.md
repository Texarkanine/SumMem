---
task_id: ship-prompt-file
date: 2026-08-20
complexity_level: 2
---

# Reflection: ship-prompt-file

## Summary

Shipped `docs/agents-prompt.md` as the copyable baked prompt (lockstep with `prompt_text()`), stopped teaching screen-paste from `init`, and restored this repo's wrap-damaged `AGENTS.md` prefix. QA passed.

## Requirements vs Outcome

Delivered as specified in #19 and the brief. `init` still prints (redirect is wrap-safe) and still writes nothing. Did not add `--raw` or split recipe onto stderr.

## Plan Accuracy

The file list and TDD order held. First preflight failed because contributor docstrings still said "paste"; that gap was real, not a surprise about the store or CLI. No build reorder.

## Build & QA Observations

Build was linear. The existing `AGENTS.md` already had the wrap-paste defect (`cloneon`, `napbefore`); restoring lockstep was the repair, not extra scope. QA passed on the first pass; the redirect-is-not-prompt-only note stayed advisory.

## Insights

### Technical

- `init` already emitted correct bytes. The defect is selecting a wrapping terminal, not a wrong print. A committed file is the install artifact; stdout is a reprint.
- This repository's `AGENTS.md` is not that artifact: it carries a Niko suffix. Lockstep `startswith` still matters, and it was already red against `prompt_text()`.

### Process

- Retiring a word from the operator path means scanning docstrings and test names, not only CLI output. First preflight caught the leftover "paste" comments.

### Million-Dollar Question

If onboarding had assumed a file from the start, `docs/agents-prompt.md` would have been the artifact and `init` a reprint. That is what we built. Recipe-on-stderr / `--raw` would make redirect prettier; it is not the foundation.
