# Project Brief

## User Story

As an operator whose repository is written by several agents at once, I want the fold request to keep compressing the listing no matter how merges interleave the rows, so that no wake line is stranded forever and recent notes stay verbatim, the way they do with a single writer.

## Use-Case(s)

### Use-Case 1: Branches fold notes the other side never saw

`main` holds `[8, 4, 2, 1]` (the 1 is `foo`). Two branches that never saw `foo` record later notes and fold them. After merge the listing is `[8, 4, 2, 1, 2, 2]`. Today the next folds give `[8, 4, 2, 1, 4]`: over budget, no request, and `foo` plus everything older never folds again. The fold request must keep finding pairs and fold the older rows away.

### Use-Case 2: Other ways a row gets stranded

A late note stamped before a pack `main` already folded, a zipper reopen, `surgery.py` excising one note from a pack, or a legacy pack whose grain is not a power of two can each leave an older row next to a bigger newer one (a **wall**). The same rule must heal the first four. A legacy non-power-of-two pack is left alone and must not block other folds.

### Use-Case 3: One writer, unchanged

A single writer must see exactly today's behavior: the same pair requested at every step, the same listings, the same number of recent notes verbatim.

## Requirements

1. **Fold picker.** When the view is over budget, `fold_request` names the oldest row that has a row of the same grain anywhere below it, paired with the nearest such row. It returns no request only when no two power-of-two rows share a grain. Rows whose grain is not a power of two are never named.
2. **`nap` pair rule.** `nap` accepts two view rows of the same grain with no row of that grain between them, even when they are not neighbors. It refuses unequal grains. It refuses a same-grain pair with a nearer same-grain row between them. It keeps today's earlier refusals and their order: range token, unknown id, unreadable pack, overlapping packs.
3. **No new non-power-of-two packs.** No code path writes a pack whose grain is not a power of two.
4. **Wake order.** When wake opens packs in memory (view shorter than budget), the printed rows are sorted by each row's oldest note, so an opened pack's newer child lands at its own date.
5. **Legacy packs.** A pack already on disk whose grain is not a power of two is never opened automatically, never requested, and does not stop other rows from folding.
6. **Self-heal.** Stores that already have walls heal through the normal fold requests. No migration script.
7. **Docs.** Help text, README, architecture, theory, and `memory-bank/systemPatterns.md` describe the new rule instead of "adjacent".

## Constraints

1. No on-disk format change: nap stems, positions (leftmost child's `{stamp}-{rand}`), the `.tree` format, and identity stay as they are.
2. Captions are requested only through the normal fold cascade. Nothing opens packs up front or forces naps.
3. Wake stays wait-free: no new file reads or writes in wake.
4. The script stays the only writer. No new commands. CLI output stays silent on git and store paths.
5. Python 3.11 floor, standard library only, one shebang file.
6. Today's single-writer behavior is preserved exactly.
7. Operator decisions (2026-10-06): never write a non-power-of-two pack; skip fold with oldest pair first; `nap` takes same grain and nearest (decision 2 = yes); wake sorts opened rows by date (decision 3 = yes); legacy non-power-of-two packs are not opened (decision 4 = no).

## Acceptance Criteria

1. The six middle-orphan tests in `tests/test_middle_orphans.py` that pin stranding pass. `test_odd_grain_pack_is_not_stranded` is rewritten to decision 4 and passes.
2. `tests/test_nap_reject.py::test_nap_of_unequal_grains_rejected_without_writing` passes.
3. `test_oldest_same_grain_pair_folds_before_newer_notes` still passes (oldest pair first on a healthy listing).
4. New tests cover the `nap` pair rule, wake's expanded row order, and a seeded multi-writer property test (no stall with a pair available, every written pack a power of two, no note lost, one-writer shape restored after merges stop).
5. Every pre-existing test passes, with retargets limited to the ones named in the plan.
6. `tox run-parallel` is green on py311–py314.
7. The docs listed in Requirement 7 no longer say folds need neighbors.
