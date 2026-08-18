# Active Context

## Current Task: ingest
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Replanned ingest as one shebang script at `.summem/summem`.
- Dropped hatchling, `src/`, and PATH console entry.
- Kept identity freezes (no-delimiter hex join, canonical JSON `.tree`, 64-hex wake ids, UTC clock).
- Validated loading a no-suffix shebang file via `SourceFileLoader` under pytest.
- Preflighted the plan: proved proof 1's merge shape, added missing tests for the UTF-8 reconfigure and the error-text rule, pinned the dot-prefixed temp file, made the version guard injectable and unpreemptable, and routed the identity byte rules into `VISION.md`.

## Decisions
- This repo becomes a store only when a working driver is bound to an agentic hook. Ingest ships `.summem/summem`. Do not commit `.summem/config.toml` or notes from this tree.

## Next Step
- `/niko-build` is unblocked. Strict argparse (`note "-foo"` needs `--`) still stands unless you say otherwise.
