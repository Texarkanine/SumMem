---
task_id: recall-zoom-prefix
date: 2026-08-25
complexity_level: 2
---

# Reflection: recall-zoom-prefix

## Summary

Recall and zoom now build one prefix table per command and parse each view `.tree` at most once. QA caught an id-keyed row map that collapsed same-text notes; the rework keeps preorder hits and tree-ordered children.

## Requirements vs Outcome

Delivered issue #50: unique prefixes once (sort plus neighbor LCP), one walk shared with `named_ids`, match surface and skip-a-pack unchanged, wake/fold `short_id` call sites left alone. Added coverage for duplicate dated notes and caption-before-leaf order that the first plan did not list.

## Plan Accuracy

The four executable units and the atlas update were the right sequence. The planned id-to-row `dict` could not represent two view rows that share a content id. That was a plan hole, not a product fork; the same walk gained an ordered hits list.

## Build & QA Observations

Prefix table and parse-once tests went red then green on the first pass. First QA FAIL was real: a two-note same-text probe printed two January 2 lines. Rework plus three tests; second QA PASS. `uvx --with tox tox` 295 on py311–py314.

## Insights

### Technical
- Prefix uniqueness is among distinct ids; printed rows are not. An id-keyed row map cannot be the only index when two notes share text and keep two dates.

### Process
- A QA "plan must rerun" can still be a fixable build gap when the walk is right and only the result shape is wrong.

### Million-Dollar Question

One view index that yields the id set, preorder hits, and per-nap child rows, then a separate linear prefix table over that id set. `named_ids` is a projection. That is what shipped after the QA rework.
