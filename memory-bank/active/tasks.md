# Task: equal-grain

* Task ID: equal-grain
* Complexity: Level 2
* Type: simple enhancement

Replan after preflight FAIL. Equal-grain requests plus sequential catch-up, with nap names that inherit the left child's `{stamp}-{rand}` so same-second folds stay in interval order. Leaf-set id stays identity. Proof 4 helper packs become 64/32/4.

Pins:

1. Stem `{stamp}-{rand}-{leafset}-{leaves}`. `{stamp}-{rand}` is copied from the **left** child's filename (`name.split("-")[0:2]`). Do not min-scan descendants. Do not open `.tree` to sort.
2. `_parse_nap_stem` returns `(stamp, rand, leafset, leaves)`. No migration: tests build via `write_nap`; this repo does not commit store data.
3. `equal_grain_pair(nodes)` is the first adjacent same-`leaves` pair in view order. Delete `oldest_adjacent`.
4. One pair per request. After a successful `nap`, print `fold_request`. No snapshot list.
5. `write_nap` still folds any two adjacent view nodes. The picker refuses 16+1.
6. Proof 4 helper packs: `fold_ids` on slices 64/32/4. Production shape lives in `tests/test_fold.py`.
7. Stay Level 2. No creative phase.

## Test Plan (TDD)

### Behaviors to Verify

- Nap stem: two notes → file is `{left.stamp}-{left.rand}-{leafset}-2`, not `{stamp}-{leafset}-2`.
- Same-second slot: four notes, same UTC second, `write_nap` of the two oldest → `list_view` grains `[2, 1, 1]` in that order.
- All-ones picker: three loose notes → `equal_grain_pair` returns the two oldest ids.
- 16+1 picker: 16-leaf nap plus one later note → `equal_grain_pair` is `None`; `fold_request` is empty.
- Over-budget CLI 16+1: lone 16-pack, `WAKE_LINES=1`, `main(["note", "x"])` → stdout empty (view is 16+1, not 16+1+1).
- Two 8s beside a 16: view `16, 8, 8` → the two 8s.
- 2+1+1 picker: view `2, 1, 1` → the two 1s.
- Duplicate-id ones: two adjacent notes with the same text → `(id, id)`.
- Over-budget ones: `WAKE_LINES=3`, fourth note → two oldest ids, no nap written.
- Catch-up: `WAKE_LINES=2`, four ones, `nap` the first pair → stdout is the remaining two 1s, not parent+1.
- Catch-up quiet: `nap` at or under budget → stdout empty.
- Same-second long stream: 24 notes, **same** datetime, `WAKE_LINES=8`, loop `fold_request` + `write_nap` until quiet → every `leaves` is a power of two, `len(view) <= 8`, some `leaves >= 4`, none `== 17`.
- Depth: 16 ones folded by `equal_grain_pair` + `write_nap` until one node → max nap-to-note depth in `.tree` `<= 4`; `zoom_reaches` still finds an original sentence (bound 200).
- Proof 4: 100 notes, helper 64/32/4, squash, clone zooms `n000` / `n064` / `n096`.

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`
- Test location: `tests/`
- Conventions: `test_*.py`; `load_summem()`; `gitutil.init_repo` / `fold_ids` / `zoom_reaches`; monkeypatch `WAKE_LINES`; CLI via `m.main` + `capsys`
- New test files: none
- Existing tests that treat `name.split("-")[1]` as leafset (`tests/test_nap.py`, `tests/test_view.py`, `tests/test_wake.py`) must use `split("-")[-2]` (or `_parse_nap_stem`) in unit 1

## Implementation Plan

### 1. Carry-stable nap names — executable

- Files: `tests/test_nap.py`, `tests/test_view.py`, `tests/test_wake.py`, `tests/test_fold.py`, `.summem/summem`

1. Stub tests: add empty `test_nap_stem_inherits_left_child_seq_prefix` and `test_same_second_nap_stays_in_left_slot` in `tests/test_fold.py`.
2. Stub interface: add `_seq_prefix(name: str) -> str` returning `""` for now. Do not change `write_nap` yet.
3. Write tests and run red: `uv run --python 3.11 --with pytest pytest tests/test_nap.py tests/test_view.py tests/test_wake.py tests/test_fold.py`. Assert stem `f"{_seq_prefix(left.name)}-{leafset}-2"`; four same-second notes (one `datetime`, `Random(1..4)`), nap oldest two, `[n.leaves for n in list_view] == [2, 1, 1]`. Change existing stem/split assertions: `tests/test_nap.py` `stem = f"{min_stamp}-{leafset}-2"` and `split("-")[1]` on a `.tree` name; `tests/test_view.py` and `tests/test_wake.py` `split("-")[1]` as leafset → `split("-")[-2]`. Expected red: `write_nap` still names `{stamp}-{leafset}-{leaves}`; same-second grains are not `[2, 1, 1]`.
4. Write code and run green: `_seq_prefix` is `"-".join(name.split("-")[:2])`; `write_nap` stem `f"{_seq_prefix(left.name)}-{leafset}-{leaves}"`; `_parse_nap_stem` accepts `{stamp}-{rand}-{leafset}-{leaves}` (`stamp` 16 chars, `rand` 16 hex, `leafset` 64 hex, `leaves` digits) and returns `(stamp, rand, leafset, leaves)`; `list_view` still sorts by `node.name` and still uses parsed `leafset` as `id`. Re-run those four files.

### 2. Equal-grain picker and production shape — executable

- Files: `tests/test_fold.py`, `.summem/summem`

1. Stub tests: empty `test_equal_grain_pair_returns_two_oldest_ids_when_all_ones`, `test_equal_grain_pair_returns_none_for_16_plus_1`, `test_equal_grain_pair_returns_two_8s_not_16_plus_8`, `test_equal_grain_pair_returns_two_1s_not_2_plus_1`, `test_equal_grain_pair_duplicate_ids_when_same_text`, `test_over_budget_note_prints_nothing_when_16_plus_1`, `test_long_stream_same_second_grains_are_powers_of_two`, `test_sixteen_leaf_pack_tree_depth_is_log`. Rewrite the module docstring. Rename `test_oldest_adjacent_returns_two_oldest_ids` out in step 3.
2. Stub interface: `equal_grain_pair(nodes: list[ViewNode]) -> tuple[str, str] | None` returning `None`. Do not rewire `fold_request` yet.
3. Write tests and run red: all-ones → two oldest ids; 16-pack (`fold_ids` of 16 notes) plus one later-second note → `None`; `WAKE_LINES=1`, **lone** 16-pack, `main(["note", "x"])` → stdout empty; two 8-packs plus an older 16-pack → the two 8s; four ones, nap two, remaining pair is two 1s; two `"same"` notes → `(id, id)`; 24 `write_note`s at one datetime, `WAKE_LINES=8`, while `fold_request` has two ids `write_nap` them → pow2 grains, `len(view) <= 8`, some `leaves >= 4`, none `== 17`; 16 ones, loop `equal_grain_pair` + `write_nap` until one node → max NoteChild depth in the `.tree` `<= 4`, then `zoom_reaches` that sentence. Delete `test_oldest_adjacent_returns_two_oldest_ids`. Keep `test_over_budget_note_requests_oldest_pair_and_writes_no_nap` as the all-ones CLI case (rename to `test_over_budget_note_requests_equal_grain_ones`). Expected red: stub `None`; `fold_request` still oldest-two (16+1).
4. Write code and run green: scan `nodes[i].leaves == nodes[i+1].leaves`; point `fold_request` at `equal_grain_pair`; delete `oldest_adjacent`. Depth helper lives in `tests/test_fold.py` (recurse `NapChild.tree`); do not add a production `tree_depth`. Re-run `tests/test_fold.py`.

### 3. Catch-up print after nap — executable

- Files: `tests/test_fold.py`, `.summem/summem`

1. Stub tests: empty `test_nap_prints_remaining_ones_not_parent_plus_one`, `test_nap_prints_nothing_when_at_or_under_budget`.
2. Stub interface: none. Reuse `fold_request`.
3. Write tests and run red: `WAKE_LINES=2`, four ones, `main(["nap", ...])` first pair → stdout is the remaining two 1 ids, not the 2-leaf id; `WAKE_LINES=32`, nap two of three → stdout empty. Expected red: nap prints nothing.
4. Write code and run green: after `write_nap` succeeds in `main`, `sys.stdout.write(fold_request(parent, WAKE_LINES))`. Re-run `tests/test_fold.py`.

### 4. Proof 4 helper packs — executable

- Files: `tests/test_proof_squash.py`

1. Stub tests: none new. Modify `test_three_packs_squash_clone_zooms_originals`.
2. Stub interface: none. `fold_ids` stays the in-pack helper.
3. Write tests and run red: not expected to go red. Slices `ids[0:64]`, `ids[64:96]`, `ids[96:100]`; grains `(64 notes,` / `(32 notes,` / `(4 notes,`; zoom `n000`, `n064`, `n096`. Run `tests/test_proof_squash.py` (green on helper), then the full suite so nothing else still asserts 40/30/30.
4. Write code and run green: no production change in this unit.

### 5. Contract wording — prose/policy

- Files: `VISION.md`, `ROADMAP.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Sequence / store table: nap files are `{minStamp}-{rand}-{leafset}-{leaves}`. `minStamp`+`rand` is the leftmost child's order key; `leafset` is identity; `leaves` is grain. Do not say `minStamp` alone is the sort key.
2. Temporal bias: replace oldest-two / oldest *k* with equal-grain; never 16+1; year-later diagram is the fold rule.
3. Squash listing: 40/30/30 → 64/32/4.
4. Long-lived branches: lazy adjacent folds after merge; no aligned `[0, 8192)` rebuild; do not say the request is oldest-two regardless of grain.
5. `ROADMAP.md` Phase 2: equal-grain requests, not oldest-adjacent left-fold. Later: equal-grain / short tree (this issue) vs full aligned cover as a wake pretty-printer (still Later).
6. `systemPatterns.md`: one briefing sentence — fold *requests* are equal-grain; nap names carry leftmost `{stamp}-{rand}`; `nap` still accepts any adjacent pair.

## Technology Validation

No new technology - validation not required

## Dependencies

- `ViewNode.name` / `list_view` filename sort already exist
- `write_nap`, `_adjacent_nodes` multiplicity, `fold_request`
- `tests/gitutil.py` `fold_ids` (helper only)
- Proofs 2, 3, 5, 6 stay green; nap-of-naps inherits the left nap's prefix

## Challenges & Mitigations

- Same-second long stream is the regression preflight reproduced; a mixed-time stream can pass without the new prefix. Unit 2 uses one datetime.
- `split("-")[1]` in three test files becomes the rand; switching to `[-2]` is required in unit 1 or those tests go red for the wrong reason after `write_nap` changes.
- 16+1 CLI starts from a **lone** 16-pack so `note` creates 16+1, not 16+1+1.
- Depth is max NoteChild depth in `.tree`, not `zoom_reaches(..., bound=4)`.
- `write_nap` of 16+1 still succeeds (post-merge lazy cover).
- Do not re-level: one extra filename field on an already-edited stem, not a new subsystem.

## Pre-Mortem

- Plan failed because leafset stayed the second field: unit 1 same-second `[2, 1, 1]` plus the 24-note same-second stream.
- Plan failed because we opened `.tree` to sort: pin 1; `_seq_prefix` is filename-only.
- Plan failed because we min-scanned all descendant rands: inherit **left** child; view order already picked left.
- Plan failed because 16+1 CLI still built 16+1+1: unit 2 lone pack.
- Plan failed because we shipped `cover(T)`: unit 5 must not add a cover pass.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (FAIL — 2026-08-18; same-second order)
- [x] Replan after FAIL
- [ ] Preflight
- [ ] Build
- [ ] QA
