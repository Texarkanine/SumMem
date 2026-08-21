# Active Context

## Current Task: note-ack
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Unit 1: `note` prints `Saved.` after a successful lock, then a blank line and `fold_request` when over budget. Write still happens inside `note_locked` before ACK. `fold_request` / `nap` unchanged.
- Unit 2: reworded `prompt_text()` nap sentence (already stored; extra work; do not retry); lockstep `docs/agents-prompt.md` and `AGENTS.md`; README day-to-day sentence.
- TDD: stubs then red (5 failures) then green. Full `tox` 238 passed on py311–py314.

## Files modified
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/summem`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/tests/test_fold.py`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/tests/test_cli.py`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/tests/test_scopes.py`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/docs/agents-prompt.md`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/AGENTS.md`
- `/home/mobaxterm/.cursor/worktrees/summem-note-ack-723efac6/SumMem-4f7b2f511995/README.md`

## Key decisions
- ACK is after `with_store_lock` returns on the `note` branch (committed plan), not inside `note_locked` after `write_note` (preflight advisory). Wire order is still write-then-ACK-then-fold.
- Strengthened `assert "Saved." not in out` on over-budget nap (`test_nap_prints_remaining_ones_not_parent_plus_one`).

## Deviations from Plan
- Took the optional over-budget-nap `Saved.` assertion. Did not move ACK inside `note_locked`.

## Next Step
- Level 2 Reflect.
