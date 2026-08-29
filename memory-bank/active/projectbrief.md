# Project Brief

## User Story

As an agent in a repository with SumMem, I want a short, meaning-dense membership test for `note` so the decaying view holds what another contributor working on this repository still needs — lore, and in-flight work that changes how they should use the tree — instead of a firehose of process telemetry.

## Use-Case(s)

### Use-Case 1

An agent finishes a normal-sized change, opens a PR, and watches CI. It does not `note` that the PR was opened, that it still needs merge, that QA passed, or that a Niko task was archived.

### Use-Case 2

An agent is twenty hours into a forty-hour refactor that occupies a real area of the tree. It does `note` that the work is in flight and roughly how far along it is, because another contributor starting work on the repository would step on it or duplicate it.

### Use-Case 3

An agent learns a gotcha, a team norm, a failed approach, or an invariant that has not found a canonical home (CI hates hard-wrapped markdown; do not retry that NP-complete refactor). It does `note` that sentence.

## Requirements

1. Retarget the baked membership language in `prompt_text()` (committed `AGENTS.md` bootstrap) and `how_to_text()` (root-wake Usage) so a `note` is something another contributor working on this repository would still need.
2. That set includes lore (gotchas, team norms, failed approaches, invariants not yet in docs) and in-flight work that actually changes how someone else should use the tree.
3. Routine process telemetry stays out: opened a PR, still needs merge, QA PASS, archived to X.
4. Personal, machine-local, and user-preference facts still stay out.
5. Wording is every-context-window: as few sentences and words as will carry the meaning. No lecture, no example dump.
6. SumMem states its own test. Do not name or special-case OptMem or any other memory product.

## Constraints

1. Do not change the store, CLI verbs, or nap/zoom/recall mechanics.
2. Keep the writer-only rule and “files it writes are part of your work; do not leave them untracked.”
3. Keep the wake-usage split: bootstrap stays a small always-unless prefix; versioned how-to stays on root wake.
4. Do not name OptMem, Niko, or `memory-bank/` in shipped agent text.
5. Prefer not to edit OptMem’s global rule. Adjust it only if SumMem cannot carry the membership test alone, and even then without either product naming the other.
6. Do not restore the forbidden phrase `must still be true after a fresh clone` unless this task deliberately retargets that invariant. Write-time-true gotchas (a README that still shows the old shape) must still be legal notes.
7. Do not rewrite existing store notes. Ingest guidance going forward is the fix; compression is not asked to wash the current tail.

## Acceptance Criteria

1. An agent following only the shipped bootstrap plus root-wake how-to can tell a tree-affecting in-flight note from routine PR/QA/archive telemetry, and can tell lore from both.
2. `AGENTS.md` stays lockstep with `prompt_text()`.
3. Shipped agent text does not name OptMem or any sibling memory product.
4. Existing `test_init.py` bootstrap/how-to invariants still hold except those this task deliberately retargets.
5. The membership language is shorter or equal in sentence count to today’s, and denser — not a longer Register Memories section.
