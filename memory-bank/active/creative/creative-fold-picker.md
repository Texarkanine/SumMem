# Algorithm Decision: Fold Picker

## Problem

`fold_request` (`summem:1225`) chooses which two view rows the agent should `nap` when the view has more rows than `WAKE_LINES`. Today it takes the oldest two **neighbors** with the same grain (`summem:1240–1245`).

- **Input**: the healed view, rows sorted by filename (each row's position is its oldest leaf's `{stamp}-{rand}`), each with a grain (`leaves`); the budget.
- **Output**: one pair of view rows, or no request.
- **Invariants**:
  - Every pack written has a grain that is a power of two (operator).
  - Captions are requested only through this cascade: one pair per request, and the next request comes after the nap.
  - Deterministic: the same view gives the same pair on every clone, so concurrent writers fold the same leaf set and the zipper max-register settles captions.
  - With one writer, the choice must equal today's at every step.
  - Wake stays wait-free; positions and stems don't change.

**Defect.** Today's rule works only while grains never rise from an older row to a newer one, which a single writer guarantees. A merge, a late note, a zipper reopen, or surgery can put an older row before a bigger newer row: a **wall**. The row before a wall can never meet an equal neighbor again, since new notes land at the end and the row after the wall only grows. So that row, and everything older, are dead wake lines. Each event can kill about log₂ lines, and the events pile up.

## Options Evaluated

- **Today, equal neighbors**: oldest pair of adjacent equal-grain rows.
- **Unequal fold (R2)**: oldest neighbors where the older grain is less than twice the newer.
- **Skip fold, smallest grain first (V2)**: the two oldest rows of the smallest grain that appears twice, any distance apart.
- **Skip fold, oldest pair first (V1)**: the oldest row that has a same-grain row anywhere below it, paired with the nearest such row.
- **Pull-back only (operator's proposal)**: only pairs whose rows between are all smaller (a block jumps back only over smaller rows), ranked by fewest walls, then shortest jump, then oldest.
- **Fewest walls, any jump**: any same-grain pair with no same grain between, ranked by fewest walls, then shortest jump, then oldest.

## Analysis

Simulation on the real driver: 4 writers, 1,500 notes, merges at 8% per note, two seeds, budget 32. Harness and raw output: `fold-research/`. Visual: `fold-research/fold-review.html`.

| Criterion | Today | R2 | V2 | V1 | Pull-back | Fewest walls |
|---|---|---|---|---|---|---|
| Correctness: never stalls over budget | ✗ 76/113 · 101/119 merges | ✓ | ✓ | ✓ 0 · 0 | ✓ at b32, ✗ 71/113 at b8 | ✓ |
| Grains stay powers of two | ✓ | ✗ (3, 35, 1,371) | ✓ | ✓ | ✓ | ✓ |
| One writer unchanged | ✓ | ✓ | ✗ 0 verbatim vs 26 | ✓ | ✓ | ✓ |
| Strands rows forever | yes | no | no | no | yes (`[4, 1]` + 8-pack) | no |
| Notes listed above an older note | 807 · 802 | — | — | **179 · 103** | 965 · 1,251 | 209 · 191 |
| Worst misplacement ÷ own pack | 4.2 · 4.6 | — | — | **0.2 · 0.1** | 0.2 · 1.2 | 0.2 · **18.2** |
| Recent notes verbatim | 1 · 1 | — | 0 (1 writer) | **28 · 28** | 21 · 14 | 28 · 20 |
| Simplicity | one loop | one loop | grouping | one loop | ranking + gap test | ranking |
| Time per request | O(n) | O(n) | O(n) | O(n²), n ≈ 33 | O(n³) | O(n³) |

Key insights:

- On a listing whose grains never rise, equal grains sit together, so V1's "oldest row with a twin below" is exactly "oldest equal neighbors". V1 is a conservative extension of today's rule.
- Bound: with only power-of-two grains, a view where no two rows share a grain is a binary number, so it has at most ⌊log₂ N⌋ + 1 rows. Over a 32-line budget a pair always exists until about 8.6 billion notes.
- Misordering accumulates while a wall stands, because every later block that folds past a stranded row jumps over it again. Taking one larger jump early beats many small jumps later; that is why pull-back loses on its own metric.
- Smallest-grain-first folds the newest notes first, which destroys the recency gradient.
- One writer under today's rule guarantees that grains never rise, each grain ≥ 2 appears at most twice, and at most one grain is doubled at a time (`single.py`, 5,000 notes). A pack of 64 with nothing near its size below it is normal. V1 keeps that one-writer shape after 87–97% of merges, and in 85–97% has exactly the grains a single writer would have with that many notes (`sim4.py`). It never showed more than 2 copies of a grain. Today's rule kept it after 2–11% of merges, with up to 28 copies of one grain.
- Your example `[16, 8, 4, 2, 1, 4, 2, 1, 2, 1]`: V1, pull-back, and fewest-walls all end at `[32, 4, 4, 1×7]`. Pull-back reproduces your hand-worked steps exactly. V1 folds 8+8 and 16+16 before the second wall (`results/walks.json`).

## Decision

**Selected**: Skip fold, oldest pair first (V1) — "nap the oldest row that has a row of the same grain anywhere below it, with the nearest such row."
**Rationale**: It is the only option that never stalled, kept recent notes verbatim, and listed the fewest notes above older ones in both seeds. It is identical to today for one writer, keeps every grain a power of two, and heals existing stores with no script. It is a one-loop change.
**Tradeoff**: A nap's leaves are no longer guaranteed to be contiguous in time. A newer note can sit inside an older-positioned pack: 7–12% of notes are listed above an older note at budget 32, by at most 0.2× the size of their own pack. The operator accepted this: with concurrent writers, strict chronological contiguity was never achievable, because a merged branch's pack already spans `main`'s notes. "No row strands forever" is argued and simulated, not proven, so the plan adds a seeded property test as a ratchet.

## Implementation Notes

- Replace only the pair loop in `fold_request`. For each `i`, take the first `j > i` with `nodes[j].leaves == nodes[i].leaves`, and stop at the first `i` that has one. Keep the remaining-count text, the `Run:` line, and the empty return.
- Skip any row whose grain is not a power of two, both as the older row and as a partner. One legacy odd row has no twin, so it is skipped anyway. Two legacy rows of the same odd grain (say two 6-packs) would otherwise be requested and folded into a 12-pack (see `creative-legacy-odd-packs.md`).
- `nap` must accept exactly the pairs this picker names (see `creative-nap-pair-rule.md`).
- `surgery.py:246` prints `fold_request` after excision, so surgery's stranded rows get requested with no surgery change.
- Pre-existing, out of scope: if the picked pack's `.tree` is missing, `nap` fails with `unknown id` and the same request repeats. Today's rule has the same behavior.
