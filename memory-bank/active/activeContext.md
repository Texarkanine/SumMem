# Active Context

## Current Task: nap-variant-stems
**Phase:** PLAN - COMPLETE

## What Was Done

- Preflight FAIL (fixable): two existing tests still asserted four-part same-path / caption-only conflict, scheduled too late.
- Plan revised: those inversions move into unit 2; `_nap_stem` is deleted in unit 3 in favor of `nap_stem` + `_write_pair`; `started_stores` is extracted for catalog and migrate.

## Next Step

- Re-run preflight. On PASS / PASS WITH ADVISORY, stop and wait for `/niko-build`.
