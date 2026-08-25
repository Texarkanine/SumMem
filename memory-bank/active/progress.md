# Progress

Heal overlap checks walk raw tree JSON instead of building unused `Tree` dataclasses, and the `note`/`nap` write path threads one `list_view` and one `knobs` result.

**Complexity:** Level 2

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed the hole on `feat/heal-raw-json` at `ddc239e`: `leaf_digests` calls `loads_tree` then `_digests_of_tree`; `heal_view` re-lists every pass; `nap_locked` lists again for ids, `write_nap`, and `fold_request`; `note_locked` lists again in `fold_request`; `fold_request` re-parses `config.toml` for `ENTRY_CHARS`.
    - Classified as Level 2: self-contained enhancement of the heal/write path. Not L1 (several functions and a performance contract). Not L3 (issue already chose raw-dict walk + threading; rematerialize still uses `Tree`).
* Decisions made
    - Implement. Hole is real and grows with history. Stay off #49/#50/#52/#53.
    - `os.scandir` stays out unless `list_view` must be opened for another reason. `Path.iterdir` already uses scandir.
* Insights
    - Sibling PRs #54 and #55 must three-way merge; this branch stays on heal/`note`/`nap` only.
