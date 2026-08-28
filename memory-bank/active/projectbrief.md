# Project Brief

## User Story

As a coding agent, I want a successful `nap` to print `Saved.` and, when the cascade is finished, `Nothing left to compress.` so that a long fold sequence does not end in silence I could read as failure or leftover work.

## Use-Case(s)

### Use-Case 1

A note that needs a nap prints `Saved.` plus the fold prompt. The agent naps. Each successful nap prints `Saved.` then either the next fold prompt (including “N compressions remain after this one” when that applies) or `Nothing left to compress.` when the view is at budget.

### Use-Case 2

An over-long `note` or `nap` hits the `ENTRY_CHARS` ratchet (`Too long: … Compress it further.`). The write does not land. Stdout has no `Saved.`

## Requirements

1. Successful `nap` prints `Saved.` then, if a fold is still owed, the existing fold prompt.
2. Successful `nap` with no further fold prints `Saved.` then `Nothing left to compress.`
3. A `note` that needs a nap still prints `Saved.` plus the fold prompt (unchanged).
4. The over-long ratchet on `note` and `nap` exits 1, stderr only, no `Saved.`
5. Retarget existing nap-stdout tests to this contract; do not delete them.

## Constraints

1. `Saved.` and `Nothing left to compress.` are printed by the command after a write that landed, not by assembling them inside `fold_request` (that helper still returns empty when there is nothing to fold).
2. Do not change OptMem.
3. Do not put `Nothing left to compress.` on a successful `note` that needs no nap.

## Acceptance Criteria

1. Mid-cascade `nap` stdout starts with `Saved.` and still contains the next pair plus any remaining-count line.
2. Last `nap` of a cascade stdout is `Saved.` then `Nothing left to compress.`
3. Over-long `note` and `nap` do not print `Saved.`
4. Tests that previously asserted empty nap stdout or `"Saved." not in` nap output assert the new bytes instead of being removed.
