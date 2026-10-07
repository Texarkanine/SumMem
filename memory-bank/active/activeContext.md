# Active Context

## Current Task: middle-orphans
**Phase:** BUILD - COMPLETE

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
- Preflight run 2: PASS WITH ADVISORY.
- Build: Units 1–5 implemented. `fold_request` names the oldest power-of-two row that has a same-grain row below it, with its nearest twin. `write_nap` accepts that pair and refuses unequal grain, a non-power-of-two total, and a nearer same-grain row. Wake sorts opened rows by the oldest note's `{stamp}-{rand}`. Docs and help no longer teach neighbors-only fold.

## Files
- `summem` — picker, nap checks, wake sort, usage line
- `tests/gitutil.py`, `tests/test_middle_orphans.py`, `tests/test_zipper.py`, `tests/test_branch_pack_merge.py`, `tests/test_wake_expand.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_fold.py`, `tests/test_fold_many_writers.py`
- `README.md`, `docs/architecture/index.md`, `docs/theory.md`, `docs/notes.md`, `memory-bank/systemPatterns.md`

## Decisions during build
- Advisories 1–6 applied. Advisory 7 (exhaustive two-writer model) was not built; the operator asked for the planned fix.
- Closest duplicate-id pair is tested on `_pair_nodes`. A successful `write_nap` of the same text twice hits "overlapping packs", because those rows share a digest.
- B18 reachability is one zoom walk of the view, the same assertion as walking each note. Seed 7 was 3.17 s.
- The lone legacy 6-pack test was already green before the picker. The two-6 case is the one that goes red without the skip.

## Integration
- `tox run-parallel` (py311–py314): all four OK. py311: 417 passed in 19.27 s.
- No linter or packaging target in `tox.ini`.

## Next Step
- QA.
