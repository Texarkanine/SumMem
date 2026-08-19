---
task_id: tree-schema
date: 2026-08-19
complexity_level: 2
---

# Reflection: tree-schema

## Summary

Clean-cut `.tree` JSON (`c` + `type: note|nap`, no `v`) and undated wake lines. Requirements met. 177 tests pass. One QA round-trip for a leftover date in `systemPatterns.md`.

## Requirements vs Outcome

Delivered as specified: no dual-read of `kids`/`k`/`v`; unknown fields ignored; missing or unsupported `type` is `ValueError`; notes print caption only; packs print `xN <prefix>: caption`. Added the type-reject tests and extra wake/proof assertion rewrites that preflight demanded. Did not regenerate the repo's own `.summem/naps` (advisory; operator-owned store).

## Plan Accuracy

Codec and `format_wake_line` were the right centers. The plan listed unit-test files; proof tests still asserted `" xN "` (space left by the old date) and ingest still split `YYYY-MM-DD: text`. Same class of stale assertion as `endswith(": solo")`, one directory over.

## Build & QA Observations

Build was substitution in two functions plus docs. First QA failed because wait-free prose in `systemPatterns.md` still named a date after the undated-wake heading was updated. Second QA passed. Four advisories remain: old on-disk trees, `zoom` traceback on parse failure, empty grain-1 caption line, loose `(KeyError, ValueError)` in the kids-without-c test.

## Insights

### Technical

- Pack lines used to start with a date, so tests looked for `" xN "` with a leading space. After the date dropped, that substring is gone even though grain is still there. Search for `" xN "` not `xN`.

### Process

- When a contract is restated twice in one briefing file, updating the heading is not enough. The wait-free paragraph repeated the date.

### Million-Dollar Question

This shape is the one you'd pick from a blank page: one array key, a word discriminator, payload names as they already were, no version field. `type` in JSON is a tag, not a reason to leave stdlib `json`.
