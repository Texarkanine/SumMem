---
task_id: cli-help
date: 2026-08-19
complexity_level: 2
---

# Reflection: cli-help

## Summary

PR #5 review punch list is in: tests load repo-root `summem`, recall searches the store, zoom/recall degrade on bad trees, the fold prompt uses `ENTRY_CHARS`, `note` is an explicit arm, VISION matches. 197 pytest. QA passed.

## Requirements vs Outcome

Delivered the accepted judge items. Kept the operator wake footer (`You are up to speed.`). Did not add stderr warnings for skipped sibling trees.

## Plan Accuracy

Sequence was right once preflight forced a catalog-prefix red and `unreadable pack` (JSONDecodeError is already a ValueError). Three FAIL (fixable) preflights before PASS WITH ADVISORY.

## Build & QA Observations

TDD reds were real on SCRIPT equality, catalog prefix, loose-note recall, and `unreadable pack`. QA found one leftover “explicit config command” in `systemPatterns.md` — fixed in reflect.

## Insights

### Technical
- `JSONDecodeError` subclasses `ValueError`. A zoom test that only asserts `ValueError` stays green while the CLI still leaks the parser message.

### Process
- Printed invocation strings are a dependency of moving the driver. `"summem wake" in catalog` is already true of `.summem/summem wake`.

### Million-Dollar Question

If the committed driver had always been repo-root `summem`, `CLI_NAME` would have been the only printed name from the first catalog, and tests would have loaded that path. The store-local `.summem/summem` copy would still exist for `ensure_store`. That is what we have now.
