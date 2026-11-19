# Active Context

## Current Task: multi-store-filing
**Phase:** PREFLIGHT - COMPLETE (FAIL (fixable))

## What Was Done
- Revised Level 2 rework plan in `memory-bank/active/tasks.md` addressing the Preflight `FAIL (fixable)` defect in Finding 17 (`assert "compression" not in out` plus `nodes=nodes[1:]`) and incorporating all six actionable Preflight advisories (help-loop deduplication to 11 tests, `wake_lines=0` on healed identical notes, deduplicating shared helpers in `test_surgery.py`/`test_nap.py` via `gitutil.py`, removing `if m._try_fcntl() is None:` in `held()`, housing `COMMAND_ONLY`/`fresh_imported` in `gitutil.py`, and moving `_note_id`/`_nap_names` with the `nap` CLI tests; expected collected test count `459 → 445`).

## Next Step
- Re-run Level 2 Preflight validation via subagent (`/niko-preflight`).
