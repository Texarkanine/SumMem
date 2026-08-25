---
task_id: slobac-audit-ratchet
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: slobac-audit-ratchet

## SUMMARY

Applied the 2026-08-25 SLOBAC audit of `tests/` as a ratchet, not a punch list. Nineteen oracles and one dead fixture were tightened. Finding 59 Phase A renamed `test_proof_*.py` to capability files and stripped `First proof N`. Findings 60–63 stayed: process-level tests next to in-process units. A later PR #48 review found the expand-child zoom oracle still green if `zoom_text` ignores `child.id`; that pin is now the two public wake lines for the `eight-b-4` nap. No product CLI change. [PR #48](https://github.com/Texarkanine/SumMem/pull/48).

## REQUIREMENTS

- Work from `.slobac/2026-08-25T12-27-19/audit.md` as a filter: fix obviously wrong and fixable holes; leave product-shaped findings.
- Do not Phase B regroup or delete the process-level tests.
- Do not add typed exceptions for ratchet `ValueError` messages.
- Do not swap subprocess proofs for in-process units, or the reverse.
- Pin `test_zoom_expanded_child_id` so a wrong-child or `wake_text` return fails.
- `tox` stays green.

## IMPLEMENTATION

Level 2, then two reworks (Phase A fossils; L1 zoom-oracle pin). Tests only, except memory-bank sentences that had globbed `test_proof_*`.

Accepted: 1, 2, 3, 5, 6, 7, 10, 13, 18, 19, 20, 21, 22, 32, 41, 42, 45, 46, 47, then finding 59 Phase A. Finding 14 rejected after preflight: the 3.10 subprocess proof skips in CI (no CPython 3.10), so the source-order pin is the floor guard that runs there.

Renames: `test_worktree_note_merge.py`, `test_caption_conflict.py`, `test_squash_clone_zoom.py`, `test_nap_reject.py`, `test_branch_pack_merge.py`, `test_path_walkup_and_catalog.py`.

`test_zoom_expanded_child_id` asserts `child.kind == "nap"` and `out.splitlines() == [x5 {short_id}: eight-b-3, dated_leaf(..., "b5")]` from `child.tree.kids`. No `_projected_child`. No substring-absent `b6`/`b7`.

The punch list under `.slobac/2026-08-25T12-27-19/` shipped with the work. Store notes and one fold landed as script writes.

## TESTING

Baseline and after each cluster: `uvx --with tox tox -e py311`. Full `tox` py311–py314: 284 passed after the ratchet, after Phase A, and after the zoom pin. `/niko-qa` PASS twice (original L2; L1 rework). Probe: the new expected lines are not `wake_text` and not `x2 00b0aaaa: eight-a-0`; they match real `zoom_text`.

## LESSONS LEARNED

- A note filename is already `{stamp}-{rand}`. `_seq_prefix` on that name is the name.
- `test_driver_refuses_python_310_before_tomllib` is not CI coverage. The source-order pin is.
- Expand walks the right 8-pack. The first non-file frontier child is the `eight-b-4` nap; its zoom is `x5 …: eight-b-3` plus dated `b5`. A pack-family substring oracle still passes `wake_text`.
- Vacuous `raises` and loose-text `match=` on the same ratchet cancel: keep `ValueError` plus the stable message.

## PROCESS IMPROVEMENTS

- An all-smells audit is a filter. Pair findings that cancel before treating the report as a punch list.
- Preflight correctly rejected deleting the 3.11 source-order pin. The first plan over-accepted finding 14.
- Leftover VISION numbering is the deliverable-fossils smell. Phase A (rename) is enough when the modules are the acceptance surface named in product context.

## TECHNICAL IMPROVEMENTS

A test-owned pack-line helper beside `dated_leaf()` in `conftest.py` would have made findings 3, 18, and 19 a one-line oracle. Not added; the ratchet did not need a new vocabulary.

## NEXT STEPS

- [PR #48](https://github.com/Texarkanine/SumMem/pull/48) on `initial-slobac`. Merge when reviews are satisfied.
- Findings 60–63 remain on purpose (harness layering). Phase B regroup is out.
- The 2026-08-25 assessor run used mixed models across shards; treat that report as the ratchet source that was applied, not as a recalibrated taxonomy.
