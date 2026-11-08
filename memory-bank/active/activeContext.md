# Active Context

## Current Task: start, help, and nap replies
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done

- Planned three executable slices: `start`, `help`, then nap replies, then a prose pass on the user guide, the architecture pages, and the ratchet sentence in `systemPatterns.md`.
- Locked the strings: `There is a store in ./path.`, `not a directory: ./path`, `unknown id`, `not a fold row`. An already-folded nap reuses `Saved.` and the existing fold or idle line.
- Preflight 1 returned `FAIL (fixable)` on three items. The plan was revised to include `tests/test_path_walkup_and_catalog.py`, use the 16-hex `leafset_id([note_digest(...)])` for note children, and treat any pair of known ids that is not a direct nap pair as `not a fold row`.
- Preflight 2 re-evaluated all checks against codebase reality and confirmed all prior issues are resolved. Preflight passed with an advisory on `_nap_miss` implementation.

## Next Step

- Proceed to Build (`/niko-build`).

