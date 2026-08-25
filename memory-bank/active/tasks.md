# Current Task: wake-never-cut

**Complexity:** Level 1

## What broke

`expand_frontier` sliced `nodes[-budget:]` (and again `frontier[-budget:]` after expand). An over-budget wake dropped the oldest view nodes, so packed history vanished from the document.

## Why

`WAKE_LINES` is a fold budget and an under-budget expand target, not a shrink-to-fit print cap. The atlas already said an at-or-over-budget wake lists view nodes.

## What changed

- Removed both newest-N slices in `expand_frontier`. Over-budget wake lists every view node. Under-budget expand is unchanged.
- Replaced `test_wake_prints_at_most_wake_lines_newest` with full-view and oldest-pack oracles. Updated the recall and 8-2-1 zipper tests that pinned the old cap.
- Atlas, `systemPatterns.md`, and `productContext.md` now say wake does not drop nodes to fit the budget.

## Files affected

- `summem`
- `tests/test_wake.py`
- `tests/test_recall.py`
- `tests/test_zipper.py`
- `docs/architecture/index.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/productContext.md`
