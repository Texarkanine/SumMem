# Active Context

## Current Task: middle-orphans (rework: broken naps stall fold)
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Rework from PR #87 review, Level 1. `_fold_grains` gives a nap with a missing or unreadable children file grain 0, so `fold_request` never names it and `write_nap`'s nearest-twin check never counts it. Four new tests; `tox run-parallel` green.

## Next Step
- Level 1 QA in a subagent. After PASS: push `middle-orphans`, then `/niko-archive` for the Level 3 task when the operator is ready.
