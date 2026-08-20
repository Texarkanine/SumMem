# Project Brief

## User Story

As an operator, I want the baked SumMem prompt to tell agents to `git add` and commit the note and nap files the script just wrote, so those facts leave the machine and other clones can see them.

## Use-Case(s)

### Use-Case 1

An agent runs `.summem/summem note "…"` (or a nap the script requested), then `git add`s the files the script wrote and commits them with the rest of the work or as their own commit.

### Use-Case 2

An agent still never invents filenames, rewrites note bytes, or deletes store files by hand. The script remains the only writer.

## Requirements

1. Tweak `prompt_text()` so agents `git add` the note and nap files the script just wrote, and commit them with the rest of the work or as their own commit.
2. Keep the "script is the only writer" rule: never invent filenames, rewrite note bytes, or delete store files by hand.
3. The committed `AGENTS.md` block stays lockstep with `prompt_text()`.
4. Fix `memory-bank/techContext.md` so it does not say this repo ignores generated store data.

## Constraints

1. As specified in [SumMem#14](https://github.com/Texarkanine/SumMem/issues/14).
2. The script does not call `git commit` itself.
3. No harness hooks.
4. Note and nap identity do not change.

## Acceptance Criteria

1. `prompt_text()` (and therefore this repo's `AGENTS.md` block) tells agents to `git add` and commit the files the script wrote.
2. The prompt still forbids inventing filenames, rewriting note bytes, or deleting store files by hand.
3. `memory-bank/techContext.md` no longer claims this repository ignores generated store data.
4. Existing `AGENTS.md` lockstep and prompt invariant tests still hold; new tests cover the publish instruction.
