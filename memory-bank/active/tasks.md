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
- QA rework: settings-paragraph wake budget is fold trigger + expand-when-short, not a print cap. Leftover `55a93401` / Parallel-naps store files parked in `stash@{0}` — they are not this task, and the AGPL sentences already live in the committed 32-pack.

## Files affected

- `summem`
- `tests/test_wake.py`
- `tests/test_recall.py`
- `tests/test_zipper.py`
- `docs/architecture/index.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/productContext.md`

## QA Result: FAIL

Suite green (313 on py311). Live `./summem wake` prints 34 lines at
`WAKE_LINES=32` including the oldest `x32` pack, so the fix itself is verified.
Two things must change before acceptance.

- [x] **Documentation.** Settings paragraph now defines the wake budget as the fold threshold and the under-budget expand target. Wake still prints every view node when over budget.
- [x] **Integrity.** Rejected as stated. HEAD's 32-pack already nests `55a93401` with both original AGPL note texts. The untracked pair is a leftover subset nap from local `main`; committing it would overlap. The Parallel-naps note is an earlier wording of HEAD `65041798`. Both parked in `stash@{0}`.

Advisories, no action required: `expand_frontier` still returns `[]` for
`budget <= 0`, which the new docstring does not cover (pre-existing, degenerate
config); `test_wake_over_budget_keeps_oldest_pack` rebuilds the same id list
from three `list_view` calls.
