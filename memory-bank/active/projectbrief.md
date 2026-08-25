# Project Brief: Heal raw-JSON overlap checks

## Source

[SumMem#51](https://github.com/Texarkanine/SumMem/issues/51) — already-approved intent. Do not expand into catalog, recall/zoom prefix tables, skip-heal markers, or dropping dataclasses from the whole script.

## User Story

As a contributor running `note` and `nap` on a growing store, I want heal overlap checks to walk `json.loads` dicts and to reuse one `list_view` / one `knobs` result on the write path, so a no-overlap write no longer spends tens of milliseconds building unused `Tree` objects per pack.

## Requirements

- `leaf_digests` / the overlap check walk raw tree JSON. Do not build `Tree` for digest-only work.
- Thread one `list_view` result and one `knobs` result through the `note` / `nap` body instead of re-listing and re-parsing config.
- `os.scandir` in `list_view` is in scope only if that function is already open.
- Heal still zipper-drops subsets, rematerializes non-subset overlap, and refuses overlapping `write_nap`.
- Crash order, flock, and wait-free wake do not change.
- No new store file.
- Rematerialize and `write_nap` still use real `Tree` objects when they write a pack.

## Out of Scope

- Skip-heal marker (#53)
- Dropping dataclasses from the whole script (#52)
- Catalog (#49)
- Recall/zoom prefix tables (#50)
