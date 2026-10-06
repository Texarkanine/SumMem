# Decision: Legacy Packs Whose Grain Is Not a Power of Two

## Problem

Before this change, `nap` accepted any two neighbors, so a store can already hold packs whose grain is not a power of two. They come from agents napping off-request, from left-fold-era stores (16+1+1+…), or from the zipper example's 4+2. Such a row never meets an equal row, so under any equal-grain picker it is never folded. Should the driver open them?

- **Constraints** (operator): captions are requested only through the normal fold cascade; nothing forces naps; opening packs up front is dangerous.

## Options Evaluated

- **Never open** *(operator: no)*: leave them; the picker skips them.
- **Open when the cascade reaches it**: when the picker would use one of its children, open it and nap that child in the same request.
- **Open eagerly in heal**: `heal_view` opens every non-2ᵏ pack.
- **One-time operator script**: a `migrate.py`-style rewrite the operator runs on purpose.

## Analysis

| Criterion | Never open | Open on reach | Open in heal | Script |
|---|---|---|---|---|
| Captions asked outside the cascade | none | none, but each open adds a row, so one extra caption later | indirectly: the row count jumps, then fold requests follow | only when run |
| Dead rows | one per legacy pack, never more | none | none | none after the run |
| Long legacy pack (16+1+1+…) | stays one line | opens one level per request: many extra captions over time | flattens into one loose note per leaf at once | operator-controlled |
| Code | none | picker + opener | heal branch | new script |

Key insights:

- The local scan of 22 stores across 11 repositories found **zero** non-power-of-two packs, listed or nested (`fold-research/oddscan.py`, 2026-10-06). Stores on other machines or in consumer repos are unknown.
- Once `nap` refuses unequal grains (`creative-nap-pair-rule.md`), the count of such packs can never grow.
- Zipper and surgery still reopen packs as they do today, so they could bring a nested odd pack back into the listing. There are none nested on this machine.
- No-stall bound becomes ⌊log₂ N⌋ + 1 + *k*, where *k* is the number of legacy odd rows: 0 everywhere scanned.

## Decision

**Selected**: Never open.
**Rationale**: It costs nothing on every store we can see, requests no caption outside the cascade, and can't flatten a long legacy pack.
**Tradeoff**: A store that holds such a pack keeps it as one extra wake line, forever. If a real store ever needs it, the remedy is an operator-run script, not an automatic path.

## Implementation Notes

- No production code. The V1 picker skips rows with no same-grain partner, and `heal_view` (`summem:706`) stays as it is. Drop the eager open used in an earlier scratch prototype.
- Rewrite `tests/test_middle_orphans.py::test_odd_grain_pack_is_not_stranded` to the decided behavior:
  - plant a legacy 6-pack with `_plant_pack` (moving to `tests/gitutil.py`);
  - record notes and obey fold requests;
  - assert the 6-pack is still listed and is never named in a fold request;
  - assert other rows keep folding, so the view returns to budget.
- Keep `_obey`'s check that every pack it writes has a power-of-two grain.
