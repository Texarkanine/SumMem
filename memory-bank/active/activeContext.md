# Active Context

## Current Task: fold-request-path
**Phase:** BUILD - COMPLETE

## What Was Done
- Confirmed issue #34: `fold_request()` omitted `--path` for nested stores; copy-paste from repo root failed with `unknown id`.
- `fold_request()` now adds `--path REL` when walk-up from `$PWD` would select a different store. `surgery.py` inherits the fix.
- Tests: unit (include/omit), CLI copy-paste after `note --path`, surgery `--path` copy-paste. `tox` 266 passed py311–py314.

## Next Step
- QA via `/niko-qa` subagent
