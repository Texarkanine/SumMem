---
task_id: ship-prompt-file
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: ship-prompt-file

## SUMMARY

[SumMem#19](https://github.com/Texarkanine/SumMem/issues/19): onboarding copies [`docs/agents-prompt.md`](../../../docs/agents-prompt.md) (exact `prompt_text()`) instead of selecting wrapped `init` output. `init` still prints the same text and writes nothing; recipe and catalog no longer say paste. This repo’s `AGENTS.md` wrap-damaged spaces (`cloneon`, `napbefore`) were restored. Draft [PR #21](https://github.com/Texarkanine/SumMem/pull/21). 224 pytest. QA passed.

## REQUIREMENTS

- Do not treat selecting `init` stdout from a wrapping terminal as the install path.
- Ship the baked prompt as a file ready for copy or insertion. Do not hard-wrap it.
- `prompt_text()` stays the single source; shipped copies stay lockstep.
- `init` does not write `AGENTS.md`. This repo’s `AGENTS.md` may keep extra sections after the prefix.

## IMPLEMENTATION

`PROMPT_DOC = "docs/agents-prompt.md"`. Lockstep test: that file equals `prompt_text()`. `init_text()` tells the operator to insert `PROMPT_DOC` from the SumMem repository; `usage_text()` catalog line is `print the agent prompt`. README Quick Start step 2 copies the file. Architecture and briefing name the same path. Did not add `--raw` or put the recipe on stderr.

## TESTING

TDD in `tests/test_init.py`: shipped-file equality, `init` recipe names `PROMPT_DOC` and does not say paste, catalog line does not say paste. Existing write-nothing and `AGENTS.md` prefix tests stayed. `uvx --with tox tox`: 224 passed on py311–py314. `/niko-qa` PASS (redirect-is-not-prompt-only advisory only).

## LESSONS LEARNED

- `init` already emitted correct bytes. The defect is selecting a wrapping terminal. A committed file is the install artifact; stdout is a reprint.
- This repository’s `AGENTS.md` is not that artifact (Niko suffix). Prefix lockstep still matters, and it was already red.
- Retiring a word from the operator path includes docstrings and test names, not only CLI output.

## PROCESS IMPROVEMENTS

First preflight FAIL (fixable) was leftover “paste” in `prompt_text()` / `init_text()` docstrings and the `AGENTS.md` lockstep test docstring. Scan contributor comments when retiring a recipe word.

## TECHNICAL IMPROVEMENTS

Recipe-on-stderr or `--raw` would make `init > file` prompt-only. Not the foundation; left as advisory.

## NEXT STEPS

- Draft [PR #21](https://github.com/Texarkanine/SumMem/pull/21) on `onboarding-prompt`. This archive commit should land on that branch so the PR drops `memory-bank/active/`.
