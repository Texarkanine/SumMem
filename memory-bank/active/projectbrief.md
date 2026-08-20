# Project Brief

## User Story

As an operator of a repository, I want a baked SumMem agent prompt that `summem init` prints and that this repo puts at the top of `AGENTS.md`, so every harness that reads that file wakes root memory once and records only durable public facts.

## Use-Case(s)

### Operator opts a repo in

They run `summem init`, paste the printed block at the top of committed `AGENTS.md`, and keep `CLAUDE.md` as `@AGENTS.md` if Claude-only tools should see the same block.

### Agent starts a session in an opted-in repo

They find repo-root `summem`, run a root wake once, skip if a root wake is already in the conversation, then `note` only stranger-clone facts.

### This repo dogfoods the prompt

We write the same block at the top of our `AGENTS.md` and check that cheap Composer 2.5 (not fast) subagents follow it.

## Requirements

1. Bake one prompt into the driver. `summem init` prints it (status + paste recipe), the way `memo init` does. `init` does not write `AGENTS.md`.
2. Recommend the top of committed `AGENTS.md` so every harness that reads that file gets it. `CLAUDE.md` stays a thin `@AGENTS.md` pointer — not “AGENTS.md or CLAUDE.md.”
3. Put that block at the top of this repo’s `AGENTS.md`. Keep the existing memory-bank section under it. Keep `CLAUDE.md` as `@AGENTS.md`.
4. Wake once at session start; skip if a root wake is already in the conversation. Never say “before any other tool call.”
5. Notes are stranger-clone public facts only. Personal, machine, and preference facts stay out.
6. Tell agents how to find repo-root `summem` (CWD / `--path`, not `.summem/summem`). Habitat may mention git to find the root; the agent interface still must not treat git as the store.
7. After writing, instrument this repo and see whether cheap Composer 2.5 (not fast) subagents follow the prompt.

## Constraints

1. As specified in [issue #2](https://github.com/Texarkanine/SumMem/issues/2) and its comments.
2. Do not copy `VISION.md` Activation as-is. Do not copy OptMem’s wake-first or “AGENTS.md or CLAUDE.md” wording.
3. Out of scope: file backend, harness hooks as the load mechanism, operator-local memory tools.
4. Presence of the driver alone is not activation; the `AGENTS.md` block is.

## Acceptance Criteria

1. `summem init` prints a baked prompt plus a paste-at-top-of-`AGENTS.md` instruction.
2. This repo’s `AGENTS.md` starts with that prompt. `CLAUDE.md` remains `@AGENTS.md`.
3. The prompt matches issue #2’s wake and note rules and the find-the-driver comments.
4. Catalog `usage_text` names `init` the same way other commands are named.
5. Composer 2.5 (not fast) subagents given the prompt can follow it (wake once, skip duplicate root wake, note policy, find the driver).
