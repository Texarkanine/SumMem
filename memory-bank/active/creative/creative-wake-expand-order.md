# Algorithm Decision: Wake Expand Order

## Problem

When the view has fewer rows than `WAKE_LINES`, `expand_frontier` (`summem:1047–1074`) opens the newest expandable pack in memory and splices its two children where the pack was, repeating until the listing is long enough. With skip folds, and already with merged branch packs, a pack's newer child then prints above rows that are older than it. For example, a pack of `foo` (Jan 1) and `c1` (Jan 4), with a pack of Jan 2 notes after it, opens as Jan 1, Jan 4, Jan 2. A reader scanning the recent lines misreads the timeline.

- **Input**: the view rows plus children opened in memory.
- **Output**: the printed row order.
- **Invariants**:
  - Wake stays wait-free: no new file reads or writes.
  - Unexpanded listings print exactly as today.
  - The expand choice ("newest expandable pack") keeps working.
  - Ids and unique prefixes are unchanged.

## Options Evaluated

- **A. Sort by oldest note after each split** *(operator: yes)*: every row, opened or not, sorts by its oldest note's `{stamp}-{rand}`.
- **B. Splice in place**: today.
- **C. Position packs by newest note**: change where packs sit in the listing.

## Analysis

| Criterion | A | B | C |
|---|---|---|---|
| Opened children land at their date | ✓ | ✗ | partial |
| Unexpanded listing unchanged | ✓ (rows are already in filename order = oldest-note order) | ✓ | ✗ every skip pack moves |
| Wait-free | ✓ in memory | ✓ | ✓ |
| Disk/stem change | none | none | none, but the display stops matching the filename order |
| Existing tests changed (prototype) | **0** (394 passed) | — | not tried |

Key insights:

- At or over budget, wake opens nothing, so A changes nothing there. Every store on this machine is at budget or has nothing to open, so there is zero visible change today.
- A pack that stays closed still sits at its oldest note, and its newer notes show only through its caption. A cannot fix that. The picker's small jumps (≤ 0.2× own pack at budget 32) keep it small.
- `ProjectedNode` (`summem:185`) carries a seconds-only `stamp`. Sorting on that alone leaves rows from the same second in arbitrary relative order, so carry the full sequence key.

## Decision

**Selected**: A. Sort by oldest note after each split.
**Rationale**: It is display-only, has no disk or test fallout, and makes the opened view chronological for both skip packs and interleaved branch packs.
**Tradeoff**: An opened pack's two children are no longer printed next to each other. Nothing depends on that: `nap` takes view ids, not expanded ids, and `zoom` prints a pack's own children.

## Implementation Notes

- Add a `seq` slot to `ProjectedNode` (default `""`, so the keyword constructions in `tests/test_wake.py` keep working).
  - View rows: `_seq_prefix(node.name)` in `expand_frontier`.
  - `_projected_child`: a note child gets its `name`; a pack child gets `min(note.name for note in _note_children(child.tree))`.
- After each splice in `expand_frontier`, call `frontier.sort(key=lambda row: row.seq)`. The sort is stable, so equal keys keep the current order. The "newest expandable" scan (from the end) is unchanged.
- `_index_tree` (`summem:963`, `:983`) also builds `ProjectedNode`s, for recall and zoom; they can keep the default `seq`.
- Docs: `docs/architecture/index.md:165` ("replace the newest expandable nap with its two children") gains "then sort by date".
