# Project Brief

## User Story

As an agent working in a clone of this repository, I want the baked SumMem prompt to separate *when* to note from *what* belongs in a note, so that a session-end dump is less likely to record a machine-local fact.

## Use-Case(s)

### Agent records a portable fact

The agent learns a project decision that would still be true after a fresh clone on another machine. It runs `.summem/summem note` with that fact.

### Agent learns a machine-local fact

The agent observes something true only on this laptop (interpreter build, uv version, local PATH). It does not put that sentence in SumMem. OptMem or a PR/archive is the other channel; the baked prompt does not name OptMem.

## Requirements

1. Change `prompt_text()` so Register Memories has a workflow sentence and a separate membership test.
2. The membership test is clone-portability: would this still be true for a stranger who cloned tomorrow on another machine? Personal, machine-local, and preference facts stay out.
3. Keep `AGENTS.md` lockstep with `prompt_text()` (`test_agents_md_starts_with_prompt_text`).
4. Keep existing `test_prompt_text_invariants` (`.summem/summem`, `personal`, `contributor`, no “before any other tool call”).

## Constraints

1. No store or CLI change.
2. Do not name OptMem in the baked prompt.
3. Do not redact the existing leaked note.
4. Do not use that leak’s wording as the negative example.
5. Do not add a token denylist or a wake reminder.
6. Decision record: `memory-bank/active/creative/creative-note-membership.md`.

## Acceptance Criteria

1. `prompt_text()` (and this repo’s `AGENTS.md` prefix) splits workflow from membership; membership ends on a clone-portability test.
2. `tox` (or `uvx --with tox tox`) passes, including `tests/test_init.py`.
3. Product commands and on-disk store format are unchanged.
