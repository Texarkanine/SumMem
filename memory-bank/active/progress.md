# Progress

Ship the baked agent prompt as a repository file so onboarding does not depend on selecting wrapped `init` output, as described in [SumMem#19](https://github.com/Texarkanine/SumMem/issues/19).

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed against issue #19
    - Classified as Level 2
    - Wrote ephemeral memory-bank files
* Decisions made
    - Level 2: single onboarding subsystem; not a store/architecture change; not a one-line wrap tweak (the issue rejects hard-wrapping `init` as the fix)
* Insights
    - `init` already emits correct bytes; the failure is selecting a wrapping terminal
    - This repo's `AGENTS.md` already shows the wrap-paste damage (`cloneon`, `napbefore`) versus `prompt_text()`

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `tasks.md`
* Decisions made
    - Copyable artifact is `docs/agents-prompt.md` (exact `prompt_text()`), not this repo's `AGENTS.md`
    - `init` stays a print; recipe and catalog drop "paste"
    - Do not hard-wrap the shipped file; do not have `init` write `AGENTS.md`
* Insights
    - Redirecting `init` is wrap-safe; selecting the screen is the defect
