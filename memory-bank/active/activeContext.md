# Active Context

## Current Task: note-membership
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Retargeted `test_prompt_text_invariants` and `test_how_to_text_is_the_usage_section` to pin `work in this clone`; dropped bootstrap `clone` forbid and how-to `another machine` require
- Rewrote `prompt_text()` Register Memories body and `how_to_text()` note paragraph to the creative Option A sentences; copied `prompt_text()` onto the `AGENTS.md` prefix
- Persistent docs / OptMem left alone
- `tox -e py311 -- tests/test_init.py`: 11 passed; `tox run-parallel`: 369 passed, 1 skipped (py311, py314); py312/py313 skipped (no interpreters)
- QA verified the diff matches plan verbatim, sentence-count parity held, no stale phrasing left in shipped docs; PASS with the preflight shared-constant advisory carried forward (not re-raised)

## Next Step
- `/niko-reflect`
