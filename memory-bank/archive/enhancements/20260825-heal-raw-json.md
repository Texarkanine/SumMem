---
task_id: heal-raw-json
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: Heal raw-JSON overlap checks

## SUMMARY

Heal overlap checks hash leaves from `json.loads` dicts instead of building frozen `Tree` graphs. `note` and `nap` reuse one `list_view` result and the already-loaded knobs. Rematerialize and pack writes still use `Tree`. [SumMem#51](https://github.com/Texarkanine/SumMem/issues/51). tox 290 on py311–py314. QA PASS.

## REQUIREMENTS

- `leaf_digests` / overlap walk raw tree JSON. No `Tree` for digest-only work.
- Thread one `list_view` and one `knobs` through the `note` / `nap` body.
- Heal still zipper-drops subsets, rematerializes non-subset overlap, and refuses overlapping `write_nap`.
- Crash order, flock, and wait-free wake unchanged. No new store file.
- Out of scope: skip-heal marker (#53), dropping dataclasses (#52), catalog (#49), recall/zoom (#50).

## IMPLEMENTATION

Level 2. Two units.

- [`summem`](../../../summem): `_digests_of_dict` walks `{"c":[...]}` and touches the same keys as `_tree_from_dict` so malformed packs still yield `None`. `leaf_digests` `json.loads`s the `.tree` and calls it. `_digests_of_tree` remains for rematerialize / `_nap_stem`. `heal_view` returns the final view and re-lists only after a mutation. `write_nap(..., nodes=)` and `fold_request(..., nodes=, entry_chars=)` are optional. `note_locked` passes heal's view into fold. `nap_locked` passes that view into `write_nap`; fold after the write lists once. `list_view` closed; `os.scandir` out.
- Tests: `tests/test_zipper.py` (no-`Tree` digest walk, heal return, threaded `write_nap`, CLI note lists once, CLI nap hands nodes through). `tests/test_fold.py` (threaded fold does not list or parse knobs). Existing zipper and overlapping `write_nap` tests kept.

Preflight PASS WITH ADVISORY (`StoreContext`); declined. QA PASS (advisory: nap CLI test does not count the post-write list).

## TESTING

TDD in plan order. `uvx --with tox tox`: py311–py314, 290 passed each. `/niko-qa` PASS.

## LESSONS LEARNED

- A digest-only walker that is looser than `loads_tree` will return a set for a pack `_as_child` cannot load, then rematerialize raises. Same keys, or `None`.
- Monkeypatch `loads_tree` is the no-dataclass oracle. Do not add a wall-clock assertion.

## PROCESS IMPROVEMENTS

Nothing notable beyond the timing-test pre-mortem, which held.

## TECHNICAL IMPROVEMENTS

If heal had never used `Tree` for digests, the write path would already take optional `nodes` / `entry_chars`. That is what shipped. A `StoreContext` type would have been extra.

## NEXT STEPS

Open a non-draft PR on `feat/heal-raw-json` that Fixes #51. Do not stack on #54 or #55. Same-leafset nap captions from this worktree's catch-up fold may three-way-conflict with those siblings.
