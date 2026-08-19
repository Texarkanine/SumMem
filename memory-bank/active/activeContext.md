# Active Context

## Current Task: equal-grain
**Phase:** PLAN - COMPLETE (L3 — wake expand)

## What Was Done
- Locked operator design: `nap` unlinks; wake expands the newest nap in memory when file count `< WAKE_LINES`
- Equal-grain requests and carry-stable stems stay; `fold_request` still keys off files
- Re-leveled to L3; brief and plan rewritten

## Next Step
- `/niko-preflight` (L3 auto-spawn after plan)
