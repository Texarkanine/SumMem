---
task_id: equal-grain
date: 2026-08-19
complexity_level: 3
---

# Reflection: equal-grain

## Summary

Equal-grain fold requests, carry-stable nap names, and in-memory right-edge wake expand landed on `.summem/summem`. `WAKE_LINES` is a printed-line budget; `nap` still unlinks. Proofs 2–6 hold with 64/32/4 packs. 101 tests. First QA failed on wait-free nested trees, one-load caching, and a leftover aligned-cover sentence; rework then passed.

## Requirements vs Outcome

The brief is met: equal-grain file pairs never 16+1; catch-up after `nap`; `{stamp}-{rand}` inherited from the left child; `WAKE_LINES` expands the newest nap in memory when the directory is short and does not write children back; `write_nap` still requires view-file ids; proof 4 is 64/32/4. Out of milestone as planned: `cover(T)` after merge, scopes, `write_nap` of virtual ids, redaction, parsing `config.toml`. No requirement was dropped. The first creative pass (notes stay) was operator-amended before plan; the build followed the amendment.

## Plan Accuracy

The L3 plan's four units were the right sequence: stems first (same-second `[1, 2, 1]` is a filename problem), then the picker, then expand plus every `wake_text` consumer, then contract wording. File lists held. Two gaps showed up in QA, not in the unit-3 test list: a valid JSON tree with an empty nested nap still raises from `min()`, and a failed `.tree` load was retried on every expand iteration. The plan said "load at most once" and "malformed does not split" but the tests planted decode failures, not semantic emptiness, and did not count loads.

## Creative Phase Review

The first-pass choice (notes stay, wake covers) did not hold: the operator locked unlink plus in-memory expand. That amendment is what got built. Friction: the creative document kept first-pass implementation notes after the lock, and `VISION.md` still opened temporal bias with "Wake uses OptMem's cover." Both survived unit 4's surgical edits until QA. The expand algorithm itself translated cleanly: rightmost expandable nap, in-memory kids, `ProjectedNode` off the writer.

## Build & QA Observations

Carry-stable stems went green on the same-second case that had failed preflight. Picker and catch-up were small. Expand was the cost: every test that harvested ids from `wake_text` had to move to `list_view` or pin `WAKE_LINES` before `wake_text` changed, or the suite would go red for the wrong reason. Proof 4's 100 commits remain the slow test. First QA ([equal-grain L3 QA](6059351b-3f8b-46a8-8838-e2cb10a0ede1), gpt-5.6-sol-medium) reproduced a wait-free crash and the double parse; those were real. Second QA ([equal-grain re-QA](c4ed0112-229c-49f1-a359-a6c329bd746f), gemini-3.1-pro) passed the rework.

## Cross-Phase Analysis

Preflight's same-second stall is why unit 1 existed; without it, equal-grain plus `minStamp` would have shipped `[1, 2, 1]`. Creative's operator amendment is why expand exists at all; the revoked notes-stay plan would have made proof 4's "three files after squash" a lie. Unit 4 rewrote fold policy and year-later file count but left "Wake uses OptMem's cover" in the same section, so QA had a contract finding that planning had already decided. Decode-only malformed tests in unit 3 are why wait-free looked done until QA walked a valid nested empty nap.

## Insights

### Technical

- Wait-free fallback is not `except JSONDecodeError`. A tree that parses and has two kids can still be unsplittable (a nested nap with no notes). Project both children before replacing the file row.
- `wake_text` is the printed cut, not the file oracle. Tests that need ids for `nap` should use `list_view`. Tests that need a caption line should pin `WAKE_LINES` to the file count.
- Same-second order is the left child's `{stamp}-{rand}`, not `minStamp` alone. Equal-grain without that prefix reorders the interval.

### Process

- When an operator amendment supersedes a creative choice, tombstone the old implementation notes in the same unit that edits `VISION.md`. Stale "notes stay" paragraphs next to a locked unlink sentence will fail QA.
- Malformed means more than bytes that do not parse. If wait-free is an invariant, plant a semantically empty nested child, not only `{not json`.
