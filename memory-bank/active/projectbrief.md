# Project Brief: read-once

Approved rework of [PR #95](https://github.com/Texarkanine/SumMem/pull/95) on `feat/fold-grain-as-child` (head dd16eac). Stop doing repeated `.tree` work per command.

## User Story

As an operator whose `summem` driver is pasted into every consumer repository and runs inside the round trip of agent turns, I want `note` and `nap` to read and digest each nap children file (`.tree`) at most once per command, so the driver does no more work than the outcome needs.

## Operator Constraints

1. The driver is pasted into every consumer repo, so people read it: as few lines of Python as possible.
2. It runs inside many agent turns: do nothing beyond what the outcome needs.
3. When the two conflict, measure, and say which was chosen and why.

## Requirements

- Measure first: a large scratch store outside the repo (about 4096 leaves in naps, plus loose notes over `WAKE_LINES`). Time `note` and `nap` at `origin/main` and dd16eac; count `.tree` reads per command. Record the numbers in the plan.
- If the gain is real: the smallest change that reads and digests each `.tree` at most once per command, with heal, fold, and nap sharing that one result. Prefer zero or negative net `summem` line delta. No new dependencies, no new eager imports.
- If there is no meaningful gain, or the gain costs lines out of proportion: stop with DEFERRED and the numbers; change no code.
- Issue #88 stands: fold grain comes from what nap can actually fold. Do not reintroduce a second parse whose refusals can drift from nap's.
- Behavior unchanged; all existing tests pass. Repo TDD rule. No change-detector tests; a read-count test only if it guards a nameable contract.
- Record a SumMem note in this worktree and commit it with the work: the driver is pasted into every consumer repo and runs in agent turns, so use fewest lines and do no more work than the outcome needs.
- Standing consent through reflect (or QA PASS at L1). No archive, no push, no PR.
