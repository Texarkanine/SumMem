# Active Context

## Current Task: start, help, and nap replies
**Phase:** COMPLEXITY-ANALYSIS - COMPLETE

## What Was Done

- Complexity is Level 2. The work is three CLI behaviors in `summem` plus the docs that describe them. No new subsystem.
- Operator decisions: `start` refuses a missing directory and uses one success sentence. Help stays a small stdlib rewrite; bare `summem` stays stderr and exit 2. An already-folded `nap` succeeds. Other nap misses stay short refusals and do not say to copy an id from `wake`.

## Next Step

- Load the Level 2 workflow and run the plan phase.
