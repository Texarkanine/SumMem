# Active Context

## Current Task: middle-orphans
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

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

- Preflight run 2: PASS WITH ADVISORY. It built Units 1–4 in scratch: 5 failed, 397 passed, and all 5 failures are retargets the plan names. Seven advisories are in `.preflight-status`; the plan was not edited after the PASS.

## Next Step
- Operator runs `/niko-build`.
- At build start, decide which advisories to fold in.
- Recommended now (corrections, no design change):
  1. Stranding-test count: five red stranding/stall tests plus the red odd-grain test, not six plus one.
  2. `_pair_nodes` returns positions (`lo`, `hi`).
  3. `write_nap` compares stem grains and also checks that the children's leaf counts are equal and sum to a power of two.
  4. Keep the node form of `_equal_grain_pair` and add a grain-list form.
  5. Unit 1 gate is 395 passed / 7 failed.
  6. Requirement 5 says "never opened on disk".
- Operator's call: advisory 7, an exhaustive two-writer model check up to 8 notes. It would turn "no row strands forever" from two sampled seeds into a check of every case at small sizes, but it needs a copy of the zipper in test code.
