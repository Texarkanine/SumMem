# Task: equal-grain

* Task ID: equal-grain
* Complexity: Level 2
* Type: simple enhancement

Replace oldest-two left-fold requests with equal-grain pair selection and a sequential catch-up print after `nap`, so `HEAD` is a short power-of-two tree. Binary `nap`, leaf-set identity, and wait-free wake stay. Proof 4 keeps squash+zoom; helper pack sizes become 64/32/4.

Pins (issue #1 allows either catch-up emission; this plan picks one):

1. `equal_grain_pair(nodes)` returns the first adjacent pair in view order whose `leaves` match. No pair → `None`.
2. One pair per request. After a successful `nap`, print `fold_request` (same as `note`). Do not pre-print a disjoint list from a snapshot: the new parent may itself pair with a neighbor.
3. `write_nap` still folds any two adjacent view nodes. The picker is what refuses 16+1. Post-merge lazy cover remains an agent `nap`.
4. Delete `oldest_adjacent`. Do not leave a second fold policy.
5. Proof 4 helper packs: 100 notes folded with `fold_ids` as 64/32/4. That helper may stay a left spine. Production shape is asserted in `tests/test_fold.py`.

## Test Plan (TDD)

### Behaviors to Verify

- All-ones picker: three loose notes → `equal_grain_pair` returns the two oldest ids.
- 16+1 picker: a 16-leaf nap adjacent to one loose note → `None`.
- Two 8s beside a 16: view `16, 8, 8` → the two 8s, not 16+8.
- 2+1+1 picker: view `2, 1, 1` → the two 1s, not 2+1.
- Duplicate-id ones: two adjacent notes with the same text → `(id, id)`.
- Over-budget `note` with no equal-grain pair: `WAKE_LINES=1` and view `16, 1` → stdout empty, no nap written.
- Over-budget `note` of ones: `WAKE_LINES=3` and a fourth note → still prints the two oldest ids and writes no nap (existing behavior, grains are 1).
- Catch-up: `WAKE_LINES=2`, four ones, `nap` the first requested pair → stdout is the remaining two 1s, not the 2-leaf parent plus a 1.
- Catch-up quiet: `nap` when the view is at or under `WAKE_LINES` → stdout empty.
- Long stream: `WAKE_LINES=8`, 24 `note`s, agent loop of requested `nap`s until quiet → every `leaves` is a power of two, `len(view) <= 8`, at least one nap has `leaves >= 4`, no node has `leaves == 17`.
- Depth: 16 ones folded by repeating `equal_grain_pair` + `write_nap` until one node → zoom hops to an original sentence `<= 4`.
- Proof 4: 100 notes, helper folds 64/32/4, squash onto `main`, clone zooms `n000` / `n064` / `n096`; wake grains `(64 notes,` / `(32 notes,` / `(4 notes,`.

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`
- Test location: `tests/`
- Conventions: `test_*.py`; `load_summem()` via `SourceFileLoader`; `gitutil.init_repo` / `fold_ids` / `zoom_reaches`; monkeypatch `WAKE_LINES`; CLI through `m.main([...])` and `capsys`
- New test files: none

## Implementation Plan

### 1. Equal-grain picker and production shape — executable

- Files: `tests/test_fold.py`, `.summem/summem`

1. Stub tests: in `tests/test_fold.py`, add empty `test_equal_grain_pair_returns_two_oldest_ids_when_all_ones`, `test_equal_grain_pair_returns_none_for_16_plus_1`, `test_equal_grain_pair_returns_two_8s_not_16_plus_8`, `test_equal_grain_pair_returns_two_1s_not_2_plus_1`, `test_equal_grain_pair_duplicate_ids_when_same_text`, `test_over_budget_note_prints_nothing_when_16_plus_1`, `test_long_stream_grains_are_powers_of_two`, `test_sixteen_leaf_pack_zoom_depth_is_log`. Leave `test_oldest_adjacent_returns_two_oldest_ids` in place until the write-tests step deletes it.
2. Stub interface: add `equal_grain_pair(nodes: list[ViewNode]) -> tuple[str, str] | None` on `.summem/summem` with an empty body (`return None`) and a docstring that it returns the oldest adjacent same-leaf-count ids. Do not rewire `fold_request` yet.
3. Write tests and run red: `uv run --python 3.11 --with pytest pytest tests/test_fold.py`. Assertions: all-ones returns `nodes[0].id, nodes[1].id`; build a 16-leaf pack with `fold_ids` plus one note → `None`; two 8-leaf packs plus one 16-leaf pack sorted by stamp so the 16 is oldest → the two 8s; `write_nap` two of four ones then pair the remaining view → two 1s; two `write_note` of `"same"` → `(id, id)`; `WAKE_LINES=1`, 16-pack plus one note, `main(["note", ...])` already over budget → out empty; 24 CLI notes at `WAKE_LINES=8`, while `fold_request` is two ids `write_nap` them, then every `node.leaves` is in `{1,2,4,8,16,32,...}`, `len(list_view) <= 8`, some `leaves >= 4`, none `== 17`; 16 notes, loop `equal_grain_pair` + `write_nap` until one node, `zoom_reaches` with hop count `<= 4`. Delete `test_oldest_adjacent_returns_two_oldest_ids` in this step (replaced by the all-ones case). Keep `test_over_budget_note_requests_oldest_pair_and_writes_no_nap` as the all-ones CLI case. Expected red: `equal_grain_pair` is `None`; `fold_request` still names 16+1; the long stream still left-spines.
4. Write code and run green: implement `equal_grain_pair` as a left-to-right scan for `nodes[i].leaves == nodes[i+1].leaves`; point `fold_request` at it; delete `oldest_adjacent`. Re-run `tests/test_fold.py`.

### 2. Catch-up print after nap — executable

- Files: `tests/test_fold.py`, `.summem/summem`

1. Stub tests: add empty `test_nap_prints_remaining_ones_not_parent_plus_one`, `test_nap_prints_nothing_when_at_or_under_budget`.
2. Stub interface: no new function. `fold_request` already exists. The nap branch of `main` will print it.
3. Write tests and run red: `WAKE_LINES=2`, four ones via `write_note`, `main(["nap", id_a, id_b, "x"])` for the first `fold_request` pair → stdout is the two remaining 1 ids and does not contain the 2-leaf parent's id; `WAKE_LINES=32`, `nap` two of three ones → stdout empty. Expected red: nap prints nothing.
4. Write code and run green: after `write_nap` succeeds in `main`, `sys.stdout.write(fold_request(parent, WAKE_LINES))`. Re-run `tests/test_fold.py`.

### 3. Proof 4 helper packs — executable

- Files: `tests/test_proof_squash.py`

1. Stub tests: none new. Modify `test_three_packs_squash_clone_zooms_originals`.
2. Stub interface: none. `fold_ids` stays the in-pack helper.
3. Write tests and run red: this step is not expected to go red. Change slices to `ids[0:64]`, `ids[64:96]`, `ids[96:100]`; grain asserts to `(64 notes,` / `(32 notes,` / `(4 notes,`; zoom sentences `n000`, `n064`, `n096`. Run `uv run --python 3.11 --with pytest pytest tests/test_proof_squash.py` — stays green on the helper. Then run the full suite so nothing else still asserts 40/30/30.
4. Write code and run green: no production change in this unit.

### 4. Contract wording — prose/policy

- Files: `VISION.md`, `ROADMAP.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. In `VISION.md` Temporal bias, replace the "simpler equivalent" oldest-two / oldest *k* sentence with equal-grain: only adjacent same-leaf-count nodes; never 16+1; the year-later diagram is the fold rule, not a picture of a different product.
2. In `VISION.md` Squash, change the 40/30/30 listing to 64/32/4 so the example matches the proof 4 helper packs.
3. In `VISION.md` Long-lived branches, keep lazy adjacent folds after merge; do not say the production request is oldest-two regardless of grain. Do not add an aligned `[0, 8192)` rebuild.
4. In `ROADMAP.md` Phase 2, replace the left-fold / oldest-adjacent bullet with equal-grain requests. In Later, distinguish equal-grain / short tree (this issue) from full aligned cover as a wake pretty-printer (still Later).
5. In `memory-bank/systemPatterns.md`, add one briefing sentence: fold *requests* name adjacent equal-grain nodes; `nap` still accepts any adjacent pair the agent named.

## Technology Validation

No new technology - validation not required

## Dependencies

- `ViewNode.leaves` already on the view (filename grain)
- `list_view`, `fold_request`, `write_nap`, `_adjacent_nodes` multiplicity
- `tests/gitutil.py` `fold_ids` as a test helper only
- Existing proofs 2, 3, 5, 6 must stay green (`fold_ids` of four notes and an agent `nap` of two 4-leaf packs remain valid)

## Challenges & Mitigations

- Proof 4 unit stays green: it is adapting a helper's pack sizes so 40/30/30 is not the documented shape. The red tests for equal-grain live in unit 1. Do not treat a green proof 4 as evidence the picker works.
- `write_nap` of 16+1 still succeeds: required so VISION's post-merge lazy cover stays an agent `nap`. Production tests refuse that pair on the printer, not the writer.
- Catch-up vs snapshot list: a snapshot of disjoint 8+8 and 8+8 misses the new 16+16. Sequential print after `nap` is the mitigation (pin 2).
- Long-stream test on a `None` stub is all 1s (vacuous powers of two): mitigation is asserting `len(view) <= WAKE_LINES` and some `leaves >= 4`.
- Depth test must not call `fold_ids`: that helper is a left spine and would fail hops `<= 4` even after the picker is correct.

## Pre-Mortem

- Plan failed because we refused 16+1 inside `write_nap` and broke post-merge unequal packs: already covered by Challenge 2 and pin 3.
- Plan failed because we implemented `cover(T, budget)` as a wake pretty-printer: out of brief; unit 4 must not add a cover pass. Cut that if it appears in review.
- Plan failed because proof 4 still encodes 40/30/30 and QA reads that as the product: unit 3 plus VISION squash listing.
- Plan failed because `nap` stayed silent and catch-up was still one request per later `note`: unit 2.

## Preflight Report

**Result:** FAIL — rearchitecture required

### Blocking Findings

1. **Same-second folds do not preserve adjacency.** Notes explicitly tie-break equal timestamps by the random suffix, but a nap replaces that suffix with its leaf-set hash. Folding two adjacent same-second notes can therefore move the parent elsewhere in the sorted view. A four-note reproduction produced grains `[1, 2, 1]`; a 24-note equal-grain simulation at `WAKE_LINES=8` stopped over budget with 12 grains: `[2, 4, 2, 4, 2, 1, 2, 1, 2, 1, 2, 1]`. No adjacent equal-grain pair remained. The planned picker and catch-up chain therefore do not guarantee the Project Brief's short-tree or bounded-view outcome under an already-supported input.
2. **The planned 16+1 CLI test constructs 16+1+1.** Unit 1 says to build a 16-pack plus one note and then run `main(["note", ...])`. The command writes another note before requesting a pair, so a correct picker returns the adjacent 1+1 pair instead of empty output. The red test would reject the required implementation.
3. **The depth assertion has no valid implementation path.** `zoom_reaches` bounds total breadth-first nodes visited, not zoom hops or maximum tree depth. Calling it with a bound of four cannot establish `O(log leaves)` and can reject a balanced tree depending on the target. The revised plan must assert the maximum nested nap-to-note depth directly, while retaining a separate CLI zoom reachability check.

### Passed Checks

- Units 1 and 2 encode tests before production code; unit 3 is a test-only proof fixture update; unit 4 correctly omits tests for prose and policy.
- Proposed files and the one-file product layout match `systemPatterns.md` and `techContext.md`.
- `write_nap` remains the general adjacent-pair primitive, preserving explicit unequal-grain post-merge naps and existing leaf-set identity.
- Proof 4's 64/32/4 slices are compatible with its intentionally left-spined helper, and the full-suite checkpoint accounts for proofs 2, 3, 5, and 6.
- No overlapping production fold policy or new dependency is proposed.

### Required Replanning

- Define a carry-stable sequence key for naps so replacing adjacent children leaves the parent at the left child's position even when timestamps tie; update the filename/parser contract, view ordering, and same-second regression tests together.
- Correct the 16+1 test setup by starting from a lone 16-pack before the CLI `note`, or test `fold_request` directly on a prebuilt 16+1 view.
- Replace the proposed `zoom_reaches` hop bound with a direct maximum-tree-depth assertion and a separate `zoom_reaches` reachability assertion.
- Update the stale `tests/test_fold.py` module wording and retained test name so they describe equal-grain requests rather than the removed left-fold policy.

### Radical Innovation Advisory

Carry the lexicographically earliest original note order key in every nap filename, independently of leaf-set identity. A concrete shape is `<stamp>-<leftmost-note-rand>-<leafset>-<leaves>`: notes already provide `<stamp>-<rand>`, and a parent inherits the minimum descendant key. Sorting by that explicit key keeps a new parent in the replaced interval without opening `.tree`, preserves wait-free wake, and remains deterministic for the same leaf set. This changes the on-disk naming/parser contract and raises the design surface beyond the current Level 2 plan, so preflight did not apply it.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (FAIL — rearchitecture required)
- [ ] Build
- [ ] QA
