# Decision: Membership Wording

## Context

**What**: The exact membership sentences for `note`, and which surface (bootstrap `prompt_text()`, how-to `how_to_text()`, or both) carries each piece.

**Why it matters**: Every agent session loads both surfaces. Wrong words recreate the telemetry firehose. Extra words tax every context window. A probe that means “still true next quarter” was already tried (`must still be true after a fresh clone`) and rejected because it banned write-time gotchas.

**Constraints**:
- Lore (gotchas, norms, failed approaches, uncanonicalized invariants) plus in-flight work that changes how someone else should use the tree.
- Not PR/QA/archive telemetry.
- Personal, machine-local, preference facts still out.
- As few sentences as today, denser, no example dump, no When/What headings.
- Do not name OptMem or any sibling memory product. Prefer leaving OptMem’s global rule alone.
- Keep `(mandatory)` as “qualifying facts must be recorded,” not “emit a note every session.”
- Keep writer-only / untracked.
- Keep the wake-usage split: bootstrap stays a small always-unless prefix.

## Options Evaluated
- **A — Work-in-this-clone probe, split surfaces**: Bootstrap only swaps “would still need” for “needs in order to work in this clone.” How-to replaces “designs, decisions, invariants” and the clone-portability lecture with a genre list, a short denylist, and skip-if-nothing-qualifies. OptMem unchanged.
- **B — Full test on both surfaces**: Same two-to-four sentences in `AGENTS.md` and on every root wake. Stronger when an agent notes before waking; doubles the token cost because both are in context after wake.
- **C — How-to only; bootstrap untouched**: Lowest bootstrap churn. Leaves the dump heading and “would still need” in `AGENTS.md`, which is always loaded and is what agents copy.

## Analysis

| Criterion | A Split probe | B Duplicate full test | C How-to only |
|-----------|---------------|----------------------|---------------|
| Density after wake | One copy of the denylist | Two copies | One copy, but bootstrap still says the old test |
| Matches wake-usage split | Yes | No — bootstrap grows | Yes |
| Stops AGENTS.md-only dump | Probe in bootstrap is the load-bearing shift | Yes | No |
| Survives “eternal currency” failure | Write-time gotchas still legal; denylist is events, not truth-over-time | Same | Same, if how-to is read |
| OptMem unnamed | Yes | Yes | Yes |

Key insights:
- “Another contributor would still need” is true of the next agent on this PR. “Needs in order to **work in this clone**” is true of someone using the tree. That is the axis clone-portability did not name.
- “Decisions” in today’s how-to is how “opened PR #70” qualifies. The genre list must not include it.
- `(mandatory)` without “skip if nothing qualifies” will still emit a tweet to satisfy the heading. Fold that into the existing redundant-memories line rather than adding a fifth sentence.
- Putting `clone` in the bootstrap breaks `test_prompt_text_invariants` (`clone` forbidden). That pin kept the *portability lecture* out of the upgrade-stable prefix. “This clone” is the membership probe, not “even when cloned on another machine.” Retarget the pin; keep forbidding `another machine` and `must still be true after a fresh clone` on the bootstrap.
- How-to currently *requires* `another machine`. Dropping the lecture means retargeting that pin too. `clone` stays (in “this clone”).
- OptMem’s ingest is events for a single actor. SumMem’s test is tree-need. They do not have to name each other. Do not edit the OptMem rule.

## Decision

**Selected**: Option A — work-in-this-clone probe, split surfaces
**Rationale**: Density and the wake-usage split forbid duplicating the denylist into `AGENTS.md`. Leaving bootstrap on “would still need” (C) leaves the dump instruction in the file that is always present. The probe plus a how-to denylist encodes the fine line without eternal-currency; OptMem stays untouched.
**Tradeoff**: An agent that notes without ever waking sees only the probe, not the denylist. Wake is already mandatory at session start; that is an accepted miss, not a reason to lengthen the bootstrap.

## Implementation Notes
- Bootstrap `prompt_text()` Register Memories body becomes: `` `{AGENT_BIN} note "…"` records one short line another contributor needs in order to work in this clone. Personal, machine-local, and user preference facts stay out. `note` may sometimes print further instructions; always follow them. `` Heading stays `(mandatory)`. Writer-only paragraph unchanged.
- How-to note paragraph becomes: `` `{AGENT_BIN} note "…"` records one short line another contributor needs in order to work in this clone: gotchas, norms, failed approaches, unfinished work that occupies the tree. Not that a PR opened, checks passed, or a task archived. Personal, machine-local, and user preference facts stay out. Skip if nothing qualifies or it is already remembered. `` Nap / recall / catalog paragraphs unchanged.
- Copy `prompt_text()` into `AGENTS.md` prefix (lockstep).
- `tests/test_init.py`: drop `clone not in` on `prompt_text`; keep `another machine` and `must still be true after a fresh clone` out of bootstrap. Drop required `another machine` on `how_to_text`; keep `clone`. Add a load-bearing pin that both strings contain `work in this clone` (same class as today’s `contributor` pin, not a full-sentence change-detector). Do not pin the denylist examples.
- Do not edit OptMem. Do not rewrite store notes. Do not change `fold_request`.
- Do not add When/What headings.
