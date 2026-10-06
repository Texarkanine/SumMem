# Progress

Fix middle orphans: replace the neighbors-only equal-grain fold picker with oldest-pair-first skip fold, narrow `nap` to same-grain nearest pairs, sort wake's opened rows by date, leave legacy non-power-of-two packs alone, and update the docs. Red regression tests already exist on this branch.

**Complexity:** Level 3

## 2026-10-06 - RESEARCH (pre-Niko) - COMPLETE

* Work completed
    - Reproduced the stall on the real driver and named five ways a wall forms (unseen partner across a merge, late note, zipper reopen, surgery, non-power-of-two pack).
    - Committed red regression tests: `299c0fa`, `b9dc459` (`tests/test_middle_orphans.py`, `tests/test_nap_reject.py`).
    - Simulated six fold rules on the real driver with four writers and git-style merges. Harness, results, and the visual review are in `memory-bank/active/creative/fold-research/`.
    - Scanned the 22 local stores (11 repos): no non-power-of-two packs, no walls in the four stores that have folded.
    - Recorded findings in SumMem (`ded53bc`, `35fc79b`).
* Decisions made
    - Operator: never write a non-power-of-two pack.
    - Operator: skip fold; oldest pair first, chosen over the operator's pull-back rule on simulation evidence.
    - Operator: decision 2 = yes (`nap` takes same grain, nearest); decision 3 = yes (wake sorts opened rows by date); decision 4 = no (do not open legacy packs).
    - Operator: captions only through the normal fold cascade; opening legacy packs up front is dangerous.
* Insights
    - Today's rule only works while grains never rise from older to newer rows. Any merge can break that, and then the rows before the wall are dead lines.
    - Pure pull-back strands rows forever, for example a young `main` `[4, 1]` followed by a merged 8-pack. Misordering piles up while a wall stands.
    - Oldest-pair-first makes the same choice as today on a healthy listing, and keeps the one-writer shape after 87–97% of merges.

## 2026-10-06 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified as Level 3.
* Decisions made
    - Level 3, not Level 2. The change is in the core fold contract described in `docs/architecture/index.md`. It spans the fold picker, the `nap` pair rule, wake expansion, test fixtures, and five docs. It needed a design exploration (six algorithms) before planning. Comparable earlier changes (equal-grain #1, zipper-heal #3) were Level 3.
