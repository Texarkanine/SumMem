# Task: Heal raw-JSON overlap checks

* Task ID: heal-raw-json
* Complexity: Level 2
* Type: simple enhancement

`leaf_digests` and heal overlap checks walk `json.loads` dicts instead of building frozen `Tree` graphs. The `note` / `nap` bodies thread one `list_view` result and one `knobs` result. Rematerialize and pack writes still use `Tree`. No new store file. Stay off catalog, recall/zoom, skip-heal, and dataclass-class changes.

## Test Plan (TDD)

### Behaviors to Verify

- Nap `leaf_digests`: a readable `.tree` → the same digest set as today's `_digests_of_tree(loads_tree(...))`, without calling `loads_tree` or `_tree_from_dict`.
- Note `leaf_digests`: a loose note → `{note_digest(file bytes)}` (existing).
- Unreadable pack: missing `.tree`, non-JSON, or `{"v":1}` → `None` (existing).
- Heal subset: `{A,B}` next to `{A,B,C,D}` → drop the 2-pack, keep the 4-pack (existing).
- Heal non-subset overlap: rematerialize children, unique-leaf cover, no new caption text (existing).
- Overlapping `write_nap`: adjacent overlapping packs → `ValueError("overlapping packs")` and no new `.summ` (existing).
- `heal_view` return: after heal → returned nodes match a fresh `list_view` (same ids and kinds, in filename order).
- Threaded `write_nap`: `write_nap(..., nodes=listed)` → does not call `list_view`; still writes or refuses overlap.
- Threaded `fold_request`: `fold_request(..., nodes=listed, wake_lines=..., entry_chars=...)` → does not call `list_view` or `knobs`; same prompt text as today's call.
- CLI `note` on a no-overlap store under budget: `list_view` runs once (heal's terminal pass), not again inside `fold_request`; `knobs` is not called from `fold_request`.
- CLI `nap` on a no-overlap store: `write_nap` does not call `list_view` (uses heal's returned view); `fold_request` after the write may list once because the view changed.
- Wake / flock / crash order: wake still wait-free and unflocked; invalid nap caption still does not heal (existing).

### Test Infrastructure

- Framework: pytest via `tox` (`py311`–`py314`)
- Test location: `tests/`
- Conventions: `test_*.py`, `load_summem()` from `conftest`, `init_repo` / `assert_unique_cover` from `gitutil`. Zipper behavior lives in `tests/test_zipper.py`. Overlapping `write_nap` lives in `tests/test_nap.py`. Fold prompt text lives in `tests/test_fold.py`.
- New test files: none

## Implementation Plan

### 1. Raw-JSON digest walker — executable

- Files: `tests/test_zipper.py`, `summem`

1. Stub tests: add empty `test_leaf_digests_nap_does_not_build_tree` and `test_heal_view_returns_final_view` in `tests/test_zipper.py`.
2. Stub interface: add `_digests_of_dict(obj: dict) -> list[str]` in `summem` with an empty body; keep `_digests_of_tree` for rematerialize / `_nap_stem` / existing Tree callers.
3. Write tests and run red: nap `leaf_digests` equals the known note-digest set while `loads_tree` and `_tree_from_dict` are monkeypatched to raise; `heal_view` return ids match a subsequent `list_view`. Existing `test_leaf_digests_*` stay.
4. Write code and run green: `_digests_of_dict` walks `obj["c"]` the same way `_tree_from_dict` does (note `name`+`text`, nap `id`+`sum`+`tree`, unknown type → `ValueError`) but only hashes `note_file_bytes(text)`. `leaf_digests` `json.loads`s the `.tree` and calls `_digests_of_dict`. `heal_view` returns the last `list_view` it used (the no-overlap pass).

### 2. Thread one view and one knobs through note/nap — executable

- Files: `tests/test_zipper.py`, `tests/test_fold.py`, `summem`

1. Stub tests: add empty `test_write_nap_reuses_nodes`, `test_fold_request_reuses_nodes_and_entry_chars`, `test_cli_note_lists_once_when_disjoint` in `tests/test_zipper.py` (or `test_fold.py` for the fold-only case if that file already owns `fold_request` kwargs).
2. Stub interface: `write_nap(..., nodes=None)`, `fold_request(..., nodes=None, entry_chars=None)`, `heal_view(parent, nodes=None)`.
3. Write tests and run red: `write_nap` with `nodes=` does not call `list_view`; `fold_request` with `nodes=` and `entry_chars=` does not call `list_view` or `knobs` and matches the unthreaded prompt; CLI `note` on a 2-note store under `WAKE_LINES` calls `list_view` once.
4. Write code and run green: `heal_view` uses the passed list on the first pass and re-lists only after a mutation. `note_locked` passes heal's return into `fold_request` with `k["WAKE_LINES"]` and `k["ENTRY_CHARS"]`. `nap_locked` passes heal's return into `write_nap` and `entry_chars` into `fold_request` (fold re-lists after the write). Do not change `list_view` to `os.scandir`. Do not change `surgery.py`.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing zipper tests in `tests/test_zipper.py` and overlapping `write_nap` tests in `tests/test_nap.py` remain the behavior lock.
- `surgery.py` calls `heal_view(parent)` and `fold_request(parent, wake_lines)` — signatures stay backward compatible.
- Sibling PRs #54 (catalog) and #55 (recall/zoom) must three-way merge; this branch does not touch those functions.

## Challenges & Mitigations

- Parse-equivalence: a looser dict walk could return a digest set for a pack `loads_tree` would reject, then `_as_child` would raise on rematerialize. Mitigation: `_digests_of_dict` touches the same keys `_tree_from_dict` requires so `_TREE_PARSE_ERRORS` still yields `None`.
- Stale view after `write_nap`: synthesizing a post-write view to avoid the fold `list_view` can hand `fold_request` wrong adjacency. Mitigation: fold after `nap` lists once; only the pre-write list is reused.
- Scope creep into #52/#53: Mitigation: do not change dataclass class definitions, do not add a marker file, do not touch `catalog_text` / `named_ids` / `short_id`.

## Pre-Mortem

- The plan "proves" the hole with a timing test that flakes on a loaded machine: do not add a wall-clock assertion; monkeypatch `loads_tree` is the no-dataclass oracle.
- The plan threads a view through `fold_request` after `write_nap` and the fold line names vanished ids: already covered by the stale-view Challenge — fold re-lists after nap.
- The plan opens `list_view` for `os.scandir` and collides with #49's catalog work or a sibling merge: leave `list_view` closed.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
