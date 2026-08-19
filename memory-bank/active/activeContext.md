# Active Context

## Current Task: wake-listing
**Phase:** BUILD - COMPLETE (PASS)

## What Was Done
- Unique prefix (`short_id` / `resolve_id`), dated wake lines, `WAKE_LINES` cap, OptMem-style `fold_request`
- `nap`/`zoom` resolve unique prefixes (zoom among `named_ids`)
- Inverted proofs, nap/scopes/zipper wake-string asserts; VISION + `systemPatterns.md`

## Files
- `/home/mobaxterm/git/SumMem/.summem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_wake.py`
- `/home/mobaxterm/git/SumMem/tests/test_wake_expand.py`
- `/home/mobaxterm/git/SumMem/tests/test_fold.py`
- `/home/mobaxterm/git/SumMem/tests/test_cli.py`
- `/home/mobaxterm/git/SumMem/tests/test_zoom.py`
- `/home/mobaxterm/git/SumMem/tests/test_nap.py`
- `/home/mobaxterm/git/SumMem/tests/test_scopes.py`
- `/home/mobaxterm/git/SumMem/tests/test_zipper.py`
- `/home/mobaxterm/git/SumMem/tests/test_proof_conflict.py`
- `/home/mobaxterm/git/SumMem/tests/test_proof_branches.py`
- `/home/mobaxterm/git/SumMem/tests/test_proof_ingest.py`
- `/home/mobaxterm/git/SumMem/tests/test_proof_squash.py`
- `/home/mobaxterm/git/SumMem/VISION.md`
- `/home/mobaxterm/git/SumMem/memory-bank/systemPatterns.md`

## Decisions
- Over-budget wake: newest `WAKE_LINES` files, no `.tree` expand
- Unknown/ambiguous prefix: exit 1; overlapping nap after heal is unknown → exit 1 (no concat)
- Stored id stays 64 hex; print/accept unique prefix (floor 8)

## Next Step
- QA subagent
