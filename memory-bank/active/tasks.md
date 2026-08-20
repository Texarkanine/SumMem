# Current Task: wake-root-header

**Complexity:** Level 1

## Fix

Root `wake` printed `== Project-root Memories ==` only when the catalog and the document were both non-empty. A git-root-only store (the usual consumer case) dumped memories with no label.

The header now prints whenever the git-root document is non-empty. Empty documents still omit it. Pull wakes stay unlabeled.

## Files

- `summem` — root-wake stdout assembly
- `tests/test_scopes.py` — no-catalog case expects the header
- `tests/test_proof_ingest.py` — proof 1 expects the header above merged notes
