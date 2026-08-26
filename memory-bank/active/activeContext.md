# Active Context

## Current Task: 16-hex-leafset
**Phase:** BUILD - IN-PROGRESS

## What Was Done
- Preflight PASS WITH ADVISORY. No creative-phase decisions apply (leftover creative docs are from prior work).
- Unit 1 green: `leafset_id` returns SHA-256 `[:16]`; `_parse_nap_stem` requires a 16-hex leaf-set field. 355 tests pass excluding `tests/test_migrate.py` (expected-red until unit 2).

## Next Step
- Unit 2: rewrite migrate tests to plant 64-hex fixtures with hashlib, then dual-source `_old_stem` + recursive `_shorten_tree` + `_write_pair` then unlink.
