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

## 2026-08-20 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the plan against the CLI, tests, onboarding docs, architecture, TDD rules, and project conventions
    - Wrote `.preflight-status` with `FAIL (fixable)`
* Decisions made
    - Build remains gated until the plan schedules removal of stale “paste” wording from the affected code and retained test docstrings
    - Kept stdout/stderr separation for exact redirect output as an advisory rather than changing the plan
* Insights
    - The proposed shipped-file equality test is a valid cross-file lockstep contract, not a prose change-detector
    - The implementation structure otherwise preserves the standalone-driver, no-write, and public CLI contracts

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Replanned after preflight FAIL (fixable)
    - Scheduled docstring rewrites: `prompt_text()` ("pasted"), `init_text()` ("paste recipe"), `test_agents_md_starts_with_prompt_text` ("the paste does not drift")
* Decisions made
    - Those lines are instructional comments, not new executable behavior; no change-detector on docstring text
    - Did not take the advisory to split `init` recipe onto stderr
* Insights
    - Contributor-facing comments can re-teach a rejected onboarding path even when CLI output is fixed

## 2026-08-20 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-ran preflight checks on the updated plan
    - Wrote `.preflight-status` with `PASS WITH ADVISORY`
* Decisions made
    - Plan is now acceptable for build phase
* Insights
    - Added an advisory to consider adding a `--raw` flag to `init` (or making it the default when stdout is not a tty) to make redirection a perfect onboarding path

## 2026-08-20 - BUILD - COMPLETE

* Work completed
    - Added `PROMPT_DOC` and `docs/agents-prompt.md` lockstep with `prompt_text()`
    - Restored `AGENTS.md` prefix spaces
    - Rewrote `init_text()` / `usage_text()` and leftover "paste" docstrings
    - Updated README, architecture, and briefing
    - tox: 224 passed on py311–py314
* Decisions made
    - Did not take the `--raw` / non-tty advisory
* Insights
    - The wrap-paste defect was already in this repo's `AGENTS.md`; lockstep restore was the repair
