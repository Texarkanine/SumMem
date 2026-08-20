# Project Brief

## User Story

As a coding agent, I want over-long `note` and `nap` rejections (and other CLI errors that only complain) to state the problem and the next step I already know, so I can compress or correct and retry without guessing.

## Use-Case(s)

### Use-Case 1

An agent runs `.summem/summem note` with a line over the store limit. Stderr reports actual UTF-8 bytes, the limit, that accented characters cost 2 bytes, and to compress further. The store is unchanged.

### Use-Case 2

An agent runs `.summem/summem nap` with a caption over the same limit. The same ratchet footer appears. The store is unchanged.

### Use-Case 3

An agent hits another CLI error that today only names the failure. If the next step is not obvious and we know at least that step, stderr states the problem and that step. If we do not know the next step, stderr states the problem only.

## Requirements

1. As described in [SumMem#16](https://github.com/Texarkanine/SumMem/issues/16): replace `note is too long` with an OptMem-style ratchet for both `summem note` and `summem nap`.
2. Footer shape: actual byte count, the configured limit, the accented-character hint, and a compress-further instruction.
3. Walk other CLI error messages. If one only complains, state the problem. If the next step is not obvious and we know at least that next step, say it. Do not invent a next step.
4. Note and nap length ratchets are the must-ship work.

## Constraints

1. Write the footers in the spirit of [ISO 24495](https://www.iplfederation.org/iso-standard/) and [ASD-STE100](https://www.asd-ste100.org/): short, one meaning per word.
2. Do not mention store files, hashes as paths, or git in the agent-facing interface.
3. Length is still UTF-8 bytes against the store's `ENTRY_CHARS` (default 280). Do not change the limit or the store format.
4. Empty and multi-line entry checks stay rejections. Improve their text only if they fail the ratchet rule above.
5. Internal errors (clock UTC, unknown tree child type) are not agent-facing CLI ratchets unless they already print as such.

## Acceptance Criteria

1. Over-long `note` and `nap` print a ratchet footer with actual bytes, the store limit, the accented-character hint, and a compress-further instruction; exit nonzero; write nothing.
2. Exact-limit entries still accept.
3. Other CLI errors that only complained now state the problem, and a known next step when that step is not obvious.
4. Existing proofs and agent-interface rules still hold (no store paths, no git in agent-facing errors).
