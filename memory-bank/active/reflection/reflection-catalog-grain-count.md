---
task_id: catalog-grain-count
date: 2026-09-15
complexity_level: 2
---

# Reflection: catalog-grain-count

## Summary

Root-wake catalog lines are `N: ./path`, with `N` from filename grain on the same `git ls-files` pass that discovers stores. How-to names the `./` token. QA passed.

## Requirements vs Outcome

Delivered as briefed: no padding, `0:` for empty children, fold keeps nap-stem grain, no `list_view`/`heal`, pulls unchanged, no `note --path` recipe. Root grain is not computed from `.summem/` index paths; catalog skips root, and `started_stores` still gates the git root on `is_store`.

## Plan Accuracy

Sequence and files were right. Two surprises: `assert "./pkg" in lines` is an exact line, not a suffix; parsing root-relative `.summem/` “to be complete” would list a phantom root after `rmtree` of `.summem`. Both were existing tests, not new design.

## Build & QA Observations

Build was one red-then-green cycle per unit. QA PASS with no findings. The uncommitted `note --path <catalog>` draft would have shipped if how-to tests had not forbidden it.

## Insights

### Technical
- Nested-store discovery keys on `/.summem/`. Root-relative `.summem/` is a different path shape on purpose: do not unify them when adding a parser.

### Process
- A plan that says “substring still matches” needs to say whether the assert is `in out` or `in lines`.

### Million-Dollar Question

This is the original `store_stats` count living inside the listing wake already paid for, with the #10 “not a command” catalog shape. If grain had stayed after #10, it would have been this helper rather than a second `iterdir`. Nothing larger to redesign.
