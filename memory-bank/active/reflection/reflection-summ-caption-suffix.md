---
task_id: summ-caption-suffix
date: 2026-08-25
complexity_level: 2
---

# Reflection: summ-caption-suffix

## Summary

Nap captions now use `.summ`. The script, tests, this repo’s stores, and the user-facing docs match. The consumer `find … -exec` recipe was verified in a temp tree and is reserved for the PR body.

## Requirements vs Outcome

All four brief requirements landed. No dual-read of `.sum`. `NapChild.sum` was left alone. The find recipe was not shipped in-repo.

## Plan Accuracy

The three `summem` sites and eight test files were the right list. The leftover-`.sum` view case was the one new behavior. No step reordering.

## Build & QA Observations

TDD went red on 15 suffix pins, then green. QA passed with advisories only (hardcoded `.summ` tokens, leftover `.sum` orphans on unlink, recipe still owed to the PR).

## Insights

### Technical
- `Path.with_suffix(".sum")` on a `.summ` file replaces the last suffix and yields `.sum`. That is the safe way to plant a leftover caption in tests.

### Process
- A `find … -exec` that can destroy a store has to be proven in a temp tree with planted checksums, a driver, a nested store, a space in the name, a non-direct child, and an already-present dest. The command is the upgrade path; it is not product TDD.

### Million-Dollar Question

The suffix would have been `.summ` from the first nap writer, with one token both write sites and tests share. We did not add that token this change (preflight: do not apply). The on-disk pair is still caption + children; only the caption’s last letters changed.
