# Project Brief

## User Story

As an operator onboarding a repository, I want to put the SumMem agent prompt into `AGENTS.md` without selecting wrapped terminal output, so spaces and wording survive insertion.

## Use-Case(s)

### Use-Case 1

An operator copies the driver from this repository into another tree and needs the baked prompt. They obtain it as a file (or by redirecting `init`) and insert it at the top of that tree's `AGENTS.md` with whatever editor or copy tool they already use.

### Use-Case 2

Someone runs `summem init` in a wrapping terminal. The printed recipe must not tell them to select the wrapped screen as the install path.

## Requirements

1. As described in [summem init: copy/pasting is hard.](https://github.com/Texarkanine/SumMem/issues/19): do not treat selecting `init` stdout from a wrapping terminal as the onboarding path.
2. Ship the baked prompt in this repository as a file ready for manual copy or insertion.
3. Do not hard-wrap that file to guess the destination `AGENTS.md` wrap style.
4. `prompt_text()` remains the single prompt source; shipped copies stay lockstep with it.

## Constraints

1. `init` does not write `AGENTS.md` or create a store.
2. This repository's `AGENTS.md` may keep extra sections after the baked prefix.
3. CLI output stays silent on git. The prompt still must not name store files or a `git add` procedure.
4. No new language, package, or test runner.

## Acceptance Criteria

1. A committed file in this repository is exactly `prompt_text()` and can be copied or inserted without selecting a wrapping terminal.
2. README onboarding tells the operator to use that file (not "run init and paste the screen").
3. `init` still prints the prompt (pipe/redirect is wrap-safe) and still writes nothing.
4. This repository's `AGENTS.md` still starts with `prompt_text()`.
