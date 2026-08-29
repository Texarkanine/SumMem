# Decision: Membership Subject Wording

## Context

**What**: Choose the shared membership probe that replaces “another contributor needs in order to work in this clone” on the bootstrap and root-wake how-to.

**Why it matters**: SumMem's facts move through committed repository history, including between contributors' separate clones. The existing phrase usefully rejects process telemetry but can imply that contributors share one physical checkout.

**Constraints**:
- Keep the distinction between lore or tree-affecting in-flight work and PR/QA/archive telemetry.
- Preserve the short split surface: a probe on the bootstrap, genre and denylist on root wake.
- Keep personal, machine-local, and user-preference facts out.
- Do not change store, CLI, or nap/zoom/recall behavior.
- Do not name another memory product.
- Update both shipped surfaces and their targeted invariant pins together.

## Options Evaluated

- **A — Repository work**: Say “another contributor needs to work on this repository.”
- **B — Checkout work**: Say “another contributor needs to work in this checkout.”
- **C — Generic need-to-know**: Say “another contributor needs to know.”

## Analysis

| Criterion | A — Repository work | B — Checkout work | C — Generic need-to-know |
|-----------|---------------------|-------------------|--------------------------|
| Matches cross-clone sharing | Yes | No — points at one local copy | Partly — no shared object named |
| Preserves the membership boundary | Yes — work is the discriminator | Yes, but only locally | No — process telemetry can be “known” |
| Agent-facing clarity | Idiomatic and precise | Correct only for the current actor | Broad and regresses the prior wording |
| Sentence cost | No increase | No increase | No increase |

Key insights:
- A SumMem note is committed repository context; it cannot coordinate uncommitted state in a different contributor's checkout.
- “Work on this repository” names the shared object while preserving the practical test that excludes status updates.
- The old “would still need” wording failed because it did not say what the fact was needed *for*; option C repeats that failure.

## Decision

**Selected**: A — Repository work
**Rationale**: “Another contributor needs to work on this repository” is concise, idiomatic, and accurate across independent clones. It retains the work-oriented membership test without claiming that contributors share a checkout.
**Tradeoff**: “Repository” is slightly broader than “clone,” but the how-to's examples and denylist retain the required boundary.

## Implementation Notes

- In `summem`, replace “needs in order to work in this clone” with “needs to work on this repository” in `prompt_text()` and `how_to_text()`.
- Copy the revised `prompt_text()` output into the committed `AGENTS.md` prefix to preserve lockstep.
- Retarget `tests/test_init.py` from the `work in this clone` probe to `work on this repository`; remove the now-obsolete how-to requirement that `clone` appear.
- Re-run the targeted init tests, then the prescribed full suite after implementation.
