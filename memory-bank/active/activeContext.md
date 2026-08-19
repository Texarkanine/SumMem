# Active Context

## Current Task: wake-listing
**Phase:** BUILD - COMPLETE (PASS)

## What Was Done
- Prefix uniqueness is among distinct content ids, not view-row count
- Identical adjacent notes print/accept the same 8-hex prefix; `nap` still folds both rows

## Files
- `/home/mobaxterm/git/SumMem/.summem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_wake.py`
- `/home/mobaxterm/git/SumMem/tests/test_fold.py`
- `/home/mobaxterm/git/SumMem/tests/test_cli.py`

## Decisions
- `list(dict.fromkeys(ids))` inside `short_id` and `resolve_id`; view still keeps both rows

## Next Step
- QA subagent
