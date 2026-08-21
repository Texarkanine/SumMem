# Active Context

## Current Task: surgery
**Phase:** BUILD - COMPLETE

## What Was Done
- Repo-root `surgery.py`: `locate_note`, `plan_break_out`, `excise_note`, CLI (`--contains`, `--dry-run`, `--path`, optional NAME).
- Loads sibling `summem` via `SourceFileLoader`. Calls `rematerialize_child`, `_unlink_node`, `heal_view`, `with_store_lock`. Never `write_nap`. No `heal_view` during break-out.
- Tests: `tests/test_surgery.py` (16). tox 252 passed on py311–py314.
- Operator docs: `docs/surgery.md` linked from README and `docs/index.md`.
- Did not edit `summem`, `prompt_text()`, `docs/agents-prompt.md`, or `AGENTS.md`.

## Next Step
- QA review via `/niko-qa` subagent.
