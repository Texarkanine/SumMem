---
task_id: recall-zoom-prefix
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: recall-zoom-prefix

## SUMMARY

Recall and zoom build one unique-prefix table per command (sort plus neighbor LCP) and parse each view `.tree` at most once. `named_ids` is that walk's id list. Wake and fold may still call `short_id` per line. Fixes [#50](https://github.com/Texarkanine/SumMem/issues/50). `uvx --with tox tox` 295 passed on py311–py314. QA FAIL then PASS after a row-preserving rework.

## REQUIREMENTS

- Unique prefixes once per command; each printed line is O(1).
- Parse each view children file at most once; share that walk with `named_ids`.
- Prefix uniqueness among distinct ids; a repeated id is still that one prefix.
- Recall still matches note text and nap captions, not grain, day, or id prefix.
- Zoom still walks `Tree.kids`, not stdout tokens.
- Unreadable siblings still print `skipped a pack` and do not fail if another pack answered.
- Wake/fold output must not regress. Stay out of catalog, heal, dataclasses, and skip-heal.

## IMPLEMENTATION

- [`summem`](../../../summem): `unique_prefixes`; `short_id` is a lookup; `format_wake_line` accepts a prefix `dict`. `_index_tree` / `_view_packs` walk each view `.tree` once and yield ids, preorder `hits`, first-id lookup, and per-nap child rows. `recall_text` and `zoom_text` consume that index. Dropped `_collect_ids`, `_recall_nested`, `_find_in_tree`. Left `_projected_child` for wake expand.
- [`tests/test_wake.py`](../../../tests/test_wake.py), [`tests/test_recall.py`](../../../tests/test_recall.py), [`tests/test_zoom.py`](../../../tests/test_zoom.py): prefix-table equivalence, parse-once counters, duplicate dated notes, caption-before-leaf order.
- [`docs/architecture/index.md`](../../../docs/architecture/index.md): Zoom and recall section plus a change-surface row.

First QA FAIL: an id-keyed row `dict` collapsed two same-text notes onto one stamp and printed nested captions after their leaves. Rework kept every dated row in preorder `hits` and formatted zoom children from tree-ordered lists.

## TESTING

`uvx --with tox tox`: 292 after the first build, 295 after the QA rework, each of py311–py314. `/niko-preflight` PASS. `/niko-qa` FAIL then PASS. Proof walkers still enqueue nap ids from `Tree.kids`.

## LESSONS LEARNED

- Prefix uniqueness is among distinct ids; printed rows are not. An id-keyed row map cannot be the only index when two notes share text and keep two dates.
- A QA "plan must rerun" can still be a fixable build gap when the walk is right and only the result shape is wrong.

## PROCESS IMPROVEMENTS

- When a plan stores projected rows by content id, add a duplicate-text fixture in the first test unit. The existing short_id uniqueness tests do not cover dated-row multiplicity.

## TECHNICAL IMPROVEMENTS

None beyond what shipped. Catalog (#49) and heal (#51) stay separate shards.

## NEXT STEPS

None for this shard. Sibling #49 (catalog) and #51 (heal) must not land overlapping edits in `summem` around `catalog_text` / `heal_view`.
