# Active Context

## Current Task: wake-never-cut
**Phase:** BUILD - COMPLETE (QA rework)

## What Was Done
- First QA FAIL: stale wake-budget definition at atlas settings paragraph; untracked leftover store files.
- Rewrote the settings-paragraph definition (fold trigger + expand-when-short; over-budget still prints every node).
- Did not commit the leftover `55a93401` pair: those sentences already live in the committed 32-pack. Parked leftovers in `stash@{0}`.

## Next Step
- Re-run Level 1 QA via a spawned `/niko-qa` subagent.
