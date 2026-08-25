# Active Context

## Current Task: wake-never-cut
**Phase:** BUILD - COMPLETE (QA rework 2)

## What Was Done
- Second QA FAIL: `WAKE_LINES = 0` made `expand_frontier` return `[]`.
- Removed that early return. Zero/negative budget lists every view node and does not expand.
- Regression: `test_wake_zero_budget_prints_every_view_node`.

## Next Step
- Re-run Level 1 QA via a spawned `/niko-qa` subagent.
