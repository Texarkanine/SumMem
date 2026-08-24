# Task: agent-display-unify

* Task ID: agent-display-unify
* Complexity: Level 2
* Type: simple enhancement (display/prompt rework on PR #37)

Make recall and zoom print the same line grammar as wake (`format_wake_line`): dated leaves, unique-prefix packs. Recall matches note text and nap captions, not the formatted line. Reword Register Memories so clone-portability cannot be read as eternal currency. Agent stdout never prefers 64-hex; `short_id` among `named_ids` is the zoom handle.

Re-plan after preflight FAIL (fixable). Preflight on this re-plan: PASS WITH ADVISORY.

## Test Plan (TDD)

### Behaviors to Verify

- Walker `reaches`: with `zoom_text` patched to `format_wake_line` of `_projected_child` rows (no 64-hex on the line), `reaches` still finds a nested original in a nap-of-naps
- Walker `zoom_reaches`: same enqueue rule (NapChild ids from the tree, not `line.split()[0]`); CLI zoom still observes the sentence
- Recall loose note: `recall_text` on a still-loose sentence → one `dated_leaf` line; regex that hits only the prefix/day does not match
- Recall nested note: after a two-note nap, `recall_text` on the original sentence → `dated_leaf` from `NoteChild.name`, not `{64hex}  text`
- Recall nested caption: after a nap-of-naps, `recall_text` on an inner caption → `xN <short_id(named_ids)>: caption`; that prefix `zoom_text`s
- Recall prefix-only: view pack line contains hex `b` in the prefix, caption does not → `recall_text(..., "b")` does not include that pack
- Zoom two-note nap: `zoom_text` of the pack → two dated leaf lines, no content id
- Zoom nap-of-naps: `zoom_text` of the parent → two pack lines with `short_id` prefixes (floor 8 when unique), not 64-hex by default
- Zoom nested leaf id: zoom of a note id found only inside a children file → dated leaf line
- Prompt membership: `prompt_text()` still signals clone-portability (another machine / fresh clone) and does not contain `must still be true after a fresh clone`
- Wake regression: existing `test_wake.py` / `test_fold.py` dated-leaf cases stay green
- Leftover success-path retargets (existing names): `test_zoom_two_note_nap_prints_both_texts`, `test_zoom_loose_note_id_prints_the_note`, `test_zoom_nap_of_naps_prints_two_children_not_leaves`, `test_nap_of_two_naps_nests_napchild_and_unions_digests`, `test_recall_matches_nested_nap_caption`

### Test Infrastructure

- Framework: pytest via `tox` (or `uvx --with tox tox`); `pytest.ini` `testpaths = tests`
- Test location: `tests/`
- Conventions: `load_summem()` + `init_repo`; `dated_leaf(stamp, text)` in `tests/conftest.py`; one behavior per test function
- New test files: `tests/test_gitutil.py` (walker behavior only)

## Implementation Plan

### 1. Proof walkers enqueue from the children tree — executable

- Files: `tests/test_gitutil.py`, `tests/gitutil.py`

1. Stub tests: empty `test_reaches_nested_sentence_when_zoom_prints_wake_lines` in `tests/test_gitutil.py`.
2. Stub interface: `_nap_child_ids(m, parent, cid) -> list[str]` returns `[]`; `_load_driver()` loads repo-root `summem` via `SourceFileLoader` on `SCRIPT` (do not import `conftest` from `gitutil`).
3. Write tests and run red: build a nap-of-naps (`a1`/`a2` + `b1`/`b2`); monkeypatch `zoom_text` to join `format_wake_line(_projected_child(child), named_ids)` for that zoom; `reaches(m, repo, "a1")` is True. This is red while walkers use `line.split()[0]`.
4. Write code and run green: `reaches` and `zoom_reaches` enqueue `_nap_child_ids` (`NapChild.id` from `loads_tree` / nested `NapChild.tree`) after the sentence check. They do not parse zoom stdout for ids. Dated leaf lines are never enqueued. `zoom_reaches` still invokes CLI `zoom` to observe the sentence; it uses `_load_driver()` so it does not import `conftest`.

### 2. Zoom children use format_wake_line — executable

- Files: `tests/test_zoom.py`, `tests/test_nap.py`, `summem` (`_zoom_kids`, `_find_in_tree`, `zoom_text`, drop `_zoom_note_line` if unused)

1. Stub tests: empty-and-retarget `test_zoom_two_note_nap_prints_both_texts`, `test_zoom_loose_note_id_prints_the_note`, `test_zoom_nap_of_naps_prints_two_children_not_leaves`; add/empty `test_zoom_nested_note_id_prints_dated_leaf`; empty the zoom-suffix assertion in `test_nap_of_two_naps_nests_napchild_and_unions_digests`. Keep existing error-path zoom tests. Do not add parallel `dated_*` names for the retargeted tests.
2. Stub interface: `_find_in_tree` returns `NoteChild | NapChild | None` (not `str`); `_zoom_kids(tree, ids)` keeps returning a string; no new public command.
3. Write tests and run red: two-note zoom `==` `dated_leaf` for each child's stamp; loose-note zoom `==` `dated_leaf` plus newline if today's helper returns a trailing newline; nap-of-naps lines equal `format_wake_line` of `_projected_child` rows with `named_ids`; nested note id is dated; 64-hex absent when `short_id` is 8; nap test zoom of nested pack is two `dated_leaf` lines for `a1`/`a2`.
4. Write code and run green: `_zoom_kids` prints `format_wake_line(_projected_child(child), ids)` for each child with `ids = named_ids(parent)`; view-note zoom uses `format_wake_line` on that view node; nested note zoom uses `_projected_child` on the found `NoteChild`. No third listing f-string.

### 3. Recall matches sentences, prints the same grammar — executable

- Files: `tests/test_recall.py`, `summem` (`recall_text`, `_recall_nested`)

1. Stub tests: add/empty prefix-false-positive and dated nested-leaf cases; empty `test_recall_matches_nested_nap_caption` off `{id}  caption`.
2. Stub interface: `_recall_nested` gains `ids: list[str]` so nested packs can `short_id`; no new CLI flags.
3. Write tests and run red: nested note → `dated_leaf`; nested caption → `xN prefix: caption` zoomable via `resolve_id`/`zoom_text`; hex that appears only in a view prefix does not hit; loose-note match still finds the sentence and prints dated.
4. Write code and run green: view pass `rx.search(node.caption)` then append `format_wake_line(node, named_ids)`; nested pass `rx.search(child.text|child.sum)` then append `format_wake_line(_projected_child(child), ids)` with `ids = named_ids(parent)`. Same printer as zoom; no new line shape.

### 4. Register Memories wording — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text`), `docs/agents-prompt.md`, `AGENTS.md`

1. Stub tests: extend `test_prompt_text_invariants` (or a sibling) for the membership sentence.
2. Stub interface: none — still `prompt_text() -> str`.
3. Write tests and run red: `prompt_text()` must not contain `must still be true after a fresh clone`; must still exclude machine-local membership (clone / another machine / personal). Existing lockstep tests stay.
4. Write code and run green: replace that clause so it means write-time truth plus clone-portability, not eternal currency. Copy the same bytes into `docs/agents-prompt.md` and the `AGENTS.md` prefix.

### 5. Atlas and briefing — prose/policy

- Files: `docs/architecture/index.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Atlas § Zoom and recall: listings share `format_wake_line`; recall searches sentences; prefixes are unique among `named_ids`; 64-hex stays on disk.
2. `systemPatterns.md` Wake-dates-leaves section: the same grammar is wake, recall hits, and zoom children. Do not claim nested recall stays `{id}  text`. Do not claim proofs parse zoom stdout for child ids.

## Technology Validation

No new technology - validation not required

## Dependencies

- `format_wake_line`, `_projected_child`, `short_id`, `named_ids`, `dated_leaf` already on this branch
- Prompt lockstep: `test_agents_md_starts_with_prompt_text`, `test_shipped_prompt_matches_prompt_text`
- `tests/gitutil.py` `reaches` / `zoom_reaches` used by `tests/test_proof_squash.py`, `tests/test_proof_branches.py`, `tests/test_zipper.py`, `tests/test_surgery.py`

## Challenges & Mitigations

- Prefix not zoomable: if recall/zoom `short_id` against view ids only, a nested pack can collide with a hidden tree id. Mitigation: always `named_ids(parent)` for any printed pack prefix.
- Leftover two-space splits: rewrite those assertions to the pack/dated grammar; do not keep the `{id}  caption` parser.
- Matching `node.caption` drops recall-by-day and recall-by-prefix. That is the requirement. Mitigation: prefix-false-positive test.
- Prompt synonym of “must remain true”: forbid the old substring in `test_prompt_text_invariants`.
- Proof walkers enqueue `xN` after the printer change. Mitigation: unit 1 walks `NapChild` ids from the children tree before unit 2 changes zoom. Do not retarget `split()[0]` onto a second stdout grammar.
- `zoom_reaches` importing `conftest` via `load_summem`. Mitigation: `SourceFileLoader` on `SCRIPT`.
- A third listing printer. Mitigation: `_zoom_kids` and `_recall_nested` are only `_projected_child` plus `format_wake_line`.
- Wake vs recall prefix length (preflight advisory): recall/zoom use `named_ids`; a view pack line from recall can be longer than wake printed for the same row. Do not reopen the wake printer.

## Pre-Mortem

- Plan treated 64-hex as still required for zoom children: agent handles are `short_id`; disk stays 64-hex.
- Recall view pass still regexed `format_wake_line`: split haystack from print in unit 3.
- Prompt lockstep out of order: `prompt_text()` first, then the two documents.
- Leftover `{id}  text` tests omitted: unit 2/3 name those functions and retarget them; no parallel dated_* names.
- Walkers scheduled after zoom code: unit 1 is first; its red test is `reaches` under a `zoom_text` monkeypatch; both helpers change in that unit.
- Walkers enqueue grain `x1`: `_nap_child_ids` yields only `NapChild.id`.
- Advisory taken as product addressing: test-infra only (`tests/gitutil.py`).

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [x] Build
- [x] QA (PASS)
