# Current Task: wake-root-header

**Complexity:** Level 1

## Fix

Root `wake` printed `== Project-root Memories ==` only when the catalog and the document were both non-empty. A git-root-only store (the usual consumer case) dumped memories with no label.

The header now prints whenever the git-root document is non-empty. Empty documents still omit it. Pull wakes stay unlabeled.

## Files

- `summem` — root-wake stdout assembly
- `tests/test_scopes.py` — no-catalog case expects the header
- `tests/test_proof_ingest.py` — proof 1 expects the header above merged notes

## QA

**Result:** PASS

- Completeness: all four acceptance criteria hold. The header is gated on git-root store plus a non-empty document, not on catalog presence.
- Regression: catalog labeling, empty-root omission, and unlabeled pull wakes are unchanged.
- Documentation: `docs/architecture/index.md` and `memory-bank/systemPatterns.md` name the header as a non-empty root-document label.
- No KISS, DRY, YAGNI, or Integrity blockers.

