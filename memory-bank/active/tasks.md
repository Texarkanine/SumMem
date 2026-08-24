# Task: agent-display-unify

* Task ID: agent-display-unify
* Complexity: Level 2
* Type: simple enhancement (display/prompt rework on PR #37)

Make recall and zoom print the same line grammar as wake (`format_wake_line`): dated leaves, unique-prefix packs. Recall matches note text and nap captions, not the formatted line. Reword Register Memories so clone-portability cannot be read as eternal currency. Agent stdout never prefers 64-hex; `short_id` among `named_ids` is the zoom handle.

## Test Plan (TDD)

### Behaviors to Verify

- Recall loose note: `recall_text` on a still-loose sentence → one `dated_leaf` line; regex that hits only the prefix/day does not match
- Recall nested note: after a two-note nap, `recall_text` on the original sentence → `dated_leaf` from `NoteChild.name`, not `{64hex}  text`
- Recall nested caption: after a nap-of-naps, `recall_text` on an inner caption → `xN <short_id(named_ids)>: caption`; that prefix `zoom_text`s
- Recall prefix-only: view pack line contains hex `b` in the prefix, caption does not → `recall_text(..., "b")` does not include that pack
- Zoom two-note nap: `zoom_text` of the pack → two dated leaf lines, no content id
- Zoom nap-of-naps: `zoom_text` of the parent → two pack lines with `short_id` prefixes (floor 8 when unique), not 64-hex by default
- Zoom nested leaf id: zoom of a note id found only inside a children file → dated leaf line
- Prompt membership: `prompt_text()` still signals clone-portability (another machine / fresh clone) and does not contain `must still be true after a fresh clone`
- Wake regression: existing `test_wake.py` / `test_fold.py` dated-leaf cases stay green

### Test Infrastructure

- Framework: pytest via `tox` (or `uvx --with tox tox`); `pytest.ini` `testpaths = tests`
- Test location: `tests/`
- Conventions: `load_summem()` + `init_repo`; `dated_leaf(stamp, text)` in `tests/conftest.py`; one behavior per test function
- New test files: none

## Implementation Plan

### 1. Zoom children use format_wake_line — executable

- Files: `tests/test_zoom.py`, `summem` (`_zoom_kids`, `_find_in_tree`, `zoom_text`, drop `_zoom_note_line` if unused)

1. Stub tests: in `tests/test_zoom.py`, add/empty `test_zoom_two_note_nap_prints_dated_leaves`, `test_zoom_nap_of_naps_prints_prefixed_packs`, `test_zoom_nested_note_id_prints_dated_leaf`; keep existing error-path tests.
2. Stub interface: `_find_in_tree` returns `NoteChild | NapChild | None` (not `str`); `_zoom_kids(tree, ids)` keeps its return type; no new public command.
3. Write tests and run red: two-note zoom `==` `dated_leaf` for each child's stamp; nap-of-naps lines equal `format_wake_line` of projected children with `named_ids`; nested note id is dated; assert 64-hex absent when `short_id` is 8.
4. Write code and run green: project each child with `_projected_child`; print `format_wake_line(row, named_ids(parent))`. View-note zoom uses `format_wake_line` on that `ViewNode`. Prefix uniqueness is `named_ids`, not view-only ids.

### 2. Recall matches sentences, prints the same grammar — executable

- Files: `tests/test_recall.py`, `summem` (`recall_text`, `_recall_nested`)

1. Stub tests: add/empty prefix-false-positive and dated nested-leaf cases; retarget `test_recall_matches_nested_nap_caption` off `{id}  caption`.
2. Stub interface: `_recall_nested` gains `ids: list[str]` so nested packs can `short_id`; no new CLI flags.
3. Write tests and run red: nested note → `dated_leaf`; nested caption → `xN prefix: caption` zoomable via `resolve_id`/`zoom_text`; hex that appears only in a view prefix does not hit; loose-note match still finds the sentence and prints dated.
4. Write code and run green: view pass `rx.search(node.caption)` then append `format_wake_line(node, named_ids)`; nested pass `rx.search(child.text|child.sum)` then append `format_wake_line(_projected_child(child), ids)` with `ids = named_ids(parent)`.

### 3. Register Memories wording — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text`), `docs/agents-prompt.md`, `AGENTS.md`

1. Stub tests: extend `test_prompt_text_invariants` (or a sibling) for the membership sentence.
2. Stub interface: none — still `prompt_text() -> str`.
3. Write tests and run red: `prompt_text()` must not contain `must still be true after a fresh clone`; must still exclude machine-local membership (clone / another machine / personal). Existing lockstep tests stay.
4. Write code and run green: one or two word changes to the Register Memories sentence so it means write-time truth plus clone-portability, not eternal currency. Copy the same bytes into `docs/agents-prompt.md` and the `AGENTS.md` prefix.

### 4. Atlas and briefing — prose/policy

- Files: `docs/architecture/index.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Atlas § Zoom and recall: listings share `format_wake_line`; recall searches sentences; prefixes are unique among `named_ids`; 64-hex stays on disk.
2. `systemPatterns.md` Wake-dates-leaves section: the same grammar is wake, recall hits, and zoom children. Do not claim nested recall stays `{id}  text`.

## Technology Validation

No new technology - validation not required

## Dependencies

- `format_wake_line`, `_projected_child`, `short_id`, `named_ids`, `dated_leaf` already on this branch
- Prompt lockstep: `test_agents_md_starts_with_prompt_text`, `test_shipped_prompt_matches_prompt_text`

## Challenges & Mitigations

- Prefix not zoomable: if recall/zoom `short_id` against view ids only, a nested pack can collide with a hidden tree id. Mitigation: always `named_ids(parent)` for any printed pack prefix.
- `test_zoom_nap_of_naps_prints_two_children_not_leaves` splits on two spaces. Mitigation: rewrite that assertion to the pack grammar; do not keep the `{id}  caption` parser.
- Matching `node.caption` drops recall-by-day and recall-by-prefix. That is the requirement. Mitigation: do not add tests that search formatted fields; add the prefix-false-positive test so it cannot silently return.
- Prompt too timid: a synonym of “must remain true” would fail the same misreading. Mitigation: forbid the old substring in `test_prompt_text_invariants`; choose words that locate the test in clone-portability, not currency over time.

## Pre-Mortem

- Plan treated 64-hex as still required for zoom children: already covered by Challenge 1 — agent handles are `short_id`; disk stays 64-hex.
- Recall view pass still regexed `format_wake_line` because a helper was reused naively: split match haystack (caption/text) from print (`format_wake_line`) in step 2 explicitly.
- Prompt lockstep files updated by hand out of order: existing lockstep tests are the gate; step 3 changes `prompt_text()` first, then the two documents to match.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
