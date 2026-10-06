# Algorithm Decision: Nap Pair Rule

## Problem

`write_nap` (`summem:851`) accepts two ids only when their rows are neighbors in the view (`_adjacent_nodes`, `summem:836–848`), whatever their grains. The new picker names pairs that are not neighbors, and the operator forbids non-power-of-two packs. What exactly should `nap` accept?

- **Input**: the healed view and two ids (unique prefixes already resolved).
- **Output**: the ordered pair (older first) or a refusal with an agent-safe message (no store paths, no git).
- **Invariants**:
  - Every pair the picker requests is accepted.
  - No pack whose grain is not a power of two is ever written — including two equal legacy odd packs.
  - Earlier refusals keep their order and words: range token (CLI), `unknown id. Copy an id from wake.`, `unknown id` for a pack missing its `.tree`, `unreadable pack`, `overlapping packs`.

## Options Evaluated

- **A. Same grain, nearest**: same grain, and no row of that grain sits between them. *(Operator: yes.)*
- **B. Same grain, any distance**: same grain only.
- **C. Neighbors only, plus same grain**: today's adjacency, plus a grain check.
- **D. Today**: neighbors only, any grain.

## Analysis

| Criterion | A | B | C | D |
|---|---|---|---|---|
| Accepts every picker request | ✓ | ✓ | ✗ skip pairs refused, stall returns | ✗ |
| Never writes non-2ᵏ packs | ✓ | ✓ | ✓ | ✗ |
| Blocks pointless misordering | ✓ | ✗ oldest 1 + newest 1 allowed | ✓ | — |
| Simplicity | one scan between the two rows | one comparison | one comparison | today |

Key insights:

- The "same grain" half is required by the no-odd-grain rule; it is not a preference.
- Under A, every legal nap is a nearest same-grain pair, which is the only kind the picker ever requests. B also allows pairing across a closer partner. That only adds misordering: a fresh note can land at the oldest position.
- Closure: notes are grain 1 and equal folds double, so with A every pack written is 2ᵏ and trees stay balanced (depth = log₂ grain; simulation depth 10 at about 1,500 notes).
- Error order matters. Four existing tests nap a note with a pack and expect `unknown id` / `unreadable pack` / `overlapping packs`: `test_nap.py::test_nap_missing_tree_unknown_id_has_no_wake_hint`, `::test_write_nap_malformed_tree_raises_unreadable_pack`, `::test_write_nap_note_inside_adjacent_nap_raises`, and `test_cli.py::test_cli_malformed_tree_returns_1_without_traceback`. A prototype that checked grain before loading children failed all four. The grain and nearest checks must run after `_as_child` and the overlap check.

## Decision

**Selected**: A. Same grain, nearest.
**Rationale**: It accepts every request the picker can make, rejects everything else that could add misordering, and is what keeps grains powers of two forever.
**Tradeoff**: Agents lose the ability to nap arbitrary neighbors of different grains. Usage already tells them to do the requested nap, and no product flow needs an unequal nap. A merge landing between a fold request and the agent's `nap` can put a row between the pair, so the nap is refused. That is the same class as today's `not adjacent`, and the next `note` asks again.

## Implementation Notes

- Rename `_adjacent_nodes` to `_pair_nodes`, which returns `(older, newer)`. Keep the loop over duplicate-id hits, since two same-text notes share an id until heal.
- In `write_nap`, the order is: resolve hits (`unknown id. Copy an id from wake.`) → `_as_child` for both rows → overlap check → grain check → nearest check. The grain and nearest checks can live in `_pair_nodes` if it runs after child loading, or as a second call; the order is the requirement.
- Refusal meanings (exact wording is the build's choice; keep it agent-safe and in today's style, problem first, then a next step only when known):
  - same row named twice → not two rows (today: `not adjacent`);
  - unequal grains → not the same grain;
  - equal grains that are not a power of two (two legacy 6-packs) → refused too: the result would be a non-power-of-two pack;
  - a same-grain row between them → a nearer row of that grain sits between them.
- Retarget pins: `test_nap.py:233–234` (`not adjacent`, `sit next to each other in wake`), `test_nap.py:357` (`match="not adjacent"`), `test_cli.py:405` (`not adjacent`).
- Fixtures that nap unequal grains today must stop: `tests/gitutil.py::fold_ids` (a left fold that makes 3-, 5-, 7-packs; 7 calls in 4 files) and `tests/test_zipper.py::_plant_abd_abe` plus `test_heal_abd_vs_abe_unique_cover` (a 2-pack napped with a note on purpose). A balanced `fold_ids` breaks only `test_wake_expand.py::test_zoom_expanded_child_id`, which assumes the left-spine tree (prototype, 393 passed).
- Commit type: a narrowing of a CLI command on a 0.x product. Use `fix:` for the stall, and state the `nap` change in the body.
