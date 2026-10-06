# Active Context

## Current Task: middle-orphans
**Phase:** PLAN - COMPLETE (rework after Preflight FAIL (fixable))

## What Was Done
- Level 3 plan written to `tasks.md`: five units (fixtures → `nap` pair rule → fold picker → wake expand order → docs), 20 behaviors, pinned check-order diagram.
- Four creative decisions recorded in `creative/` (fold picker, nap pair rule, wake expand order, legacy odd packs); research harness and visual review in `creative/fold-research/`.
- Operator decisions (2026-10-06):
  - never write a non-power-of-two pack;
  - skip fold with oldest pair first;
  - `nap` takes same grain and nearest (decision 2 = yes);
  - wake sorts opened rows by date (decision 3 = yes);
  - legacy non-power-of-two packs are not opened (decision 4 = no);
  - captions only through the fold cascade.
- Found during planning: two equal legacy odd packs (two 6-packs) would pair into a 12-pack. The picker skips non-power-of-two rows and `nap` refuses them.

- Preflight run 1: FAIL (fixable). It found one unlisted fixture (`test_branch_pack_merge.py`), plus advisories; all are folded into the plan.

## Next Step
- Preflight (sub-agent) validates the plan. On PASS / PASS WITH ADVISORY the operator runs `/niko-build`.
