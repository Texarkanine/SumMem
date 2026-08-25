---
task_id: catalog-ls-files
date: 2026-08-25
complexity_level: 2
---

# Reflection: catalog-ls-files

## Summary

Root-wake catalog now enumerates other started stores with one `git ls-files -z --cached --others --exclude-standard` filtered on `.summem/config.toml`. Output, pull omission, and ignore semantics stayed. QA PASS. 287 tests on py311–py314.

## Requirements vs Outcome

Delivered as specified in #49. Atlas/README left unchanged: Scopes still describes a walk that honors git ignore, not a committed index. The only added behavior is the `config.toml` sentinel (a `.summem` dir without that file is no longer listed).

## Plan Accuracy

The plan was right. `--others` was the load-bearing flag: existing start-then-wake tests never `git add` the child store. The gitignore test was already green on the old walk; the reds that proved the change were no-`os.walk` and the sentinel.

## Build & QA Observations

Build was linear: stub, red on two of three new tests, replace the walk, green. Full tox 287 on four Pythons. QA PASS with no advisories.

## Insights

### Technical
- `--cached` alone would silently drop every uncommitted `start`. `--others --exclude-standard` is what matches the old `check-ignore` contract for untracked stores.

### Process
- A new ignore-source test can pass before the rewrite. The walk-ban and sentinel tests were the ones that could only go green after the hole closed.

## Million-Dollar Question

If catalog had always been "ask git for the tree," `_ignored_store` would never have existed. That is what we built.
