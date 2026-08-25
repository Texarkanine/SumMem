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

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan: raw-JSON `_digests_of_dict` plus threaded `list_view`/`knobs` on `note`/`nap`.
    - Existing zipper and overlapping `write_nap` tests stay the behavior lock. New tests monkeypatch `loads_tree` and count `list_view`/`knobs` calls. No wall-clock assertion.
* Decisions made
    - `list_view` stays closed (`os.scandir` out).
    - `fold_request` after `nap` re-lists because the view changed. Only the pre-write list is reused.
    - `_digests_of_dict` touches the same keys as `_tree_from_dict` so malformed packs still yield `None`.
* Insights
    - `surgery.py` keeps calling `heal_view(parent)` / `fold_request(parent, wake_lines)`; new parameters are optional.

## 2026-08-25 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the plan against TDD, convention, dependency, and completeness requirements.
    - Preflight status: PASS WITH ADVISORY
* Decisions made
    - No changes required to the implementation plan.
* Insights
    - Advisory: Suggested encapsulating view state into a `StoreContext` object to simplify threading through the write path. Declined for build: extra type for two optional kwargs.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - `_digests_of_dict` walks raw tree JSON; `leaf_digests` no longer calls `loads_tree`.
    - `heal_view` returns the final view and re-lists only after a mutation.
    - `write_nap` / `fold_request` take optional `nodes` and `entry_chars`; `note_locked` / `nap_locked` thread them. Fold after `nap` still lists once.
    - tox py311–py314: 290 passed.
* Decisions made
    - Declined StoreContext. Optional kwargs keep `surgery.py` and existing callers unchanged.
    - `fold_request` still defaults `wake_lines` to the script constant when omitted; only `ENTRY_CHARS` comes from knobs unless passed in.
* Insights
    - Parse-equivalence needs the same keys as `_tree_from_dict` so a nameless note still yields `None` and heal does not rematerialize a pack `_as_child` cannot load.

## 2026-08-25 - QA - COMPLETE

* Work completed
    - Reviewed the implementation against the Level 2 plan for KISS, DRY, YAGNI, completeness, regressions, integrity, and documentation.
    - Confirmed the raw-JSON walker preserves the Tree parser's required key access and parse-error behavior without materializing `Tree`.
    - Confirmed the `note` and `nap` write paths reuse the healed view and loaded knobs, with the required post-write re-list for `nap`.
    - Ran `uvx --with tox tox`: py311, py312, py313, and py314 each passed all 290 tests.
* Decisions made
    - QA result: PASS.
    - The nap CLI test's lack of direct call-count assertions is a non-blocking advisory because the simple implementation satisfies the planned count by inspection.
* Insights
    - The duplicated raw-dict traversal is intentional and smaller than introducing a shared abstraction that would compromise either digest-only performance or materialization clarity.
