# Task: agent-display-unify

* Task ID: agent-display-unify
* Complexity: Level 2
* Type: simple enhancement (display/prompt rework on PR #37)

Make recall and zoom print the same line grammar as wake (`format_wake_line`): dated leaves, unique-prefix packs. Recall matches note text and nap captions, not the formatted line. Reword Register Memories so clone-portability cannot be read as eternal currency. Agent stdout never prefers 64-hex; `short_id` among `named_ids` is the zoom handle.

Rework after preflight FAIL (fixable): proof walkers must not parse zoom stdout for child ids; leftover `{id}  text` assertions are retargeted, not left beside new tests.

## Test Plan (TDD)

### Behaviors to Verify

- Proof walk enqueue: `reaches` / `zoom_reaches` find a nested original when `zoom_text` prints wake grammar (dated leaves / `xN prefix:`), without treating `x1`/`xN` as an id
- Recall loose note: `recall_text` on a still-loose sentence → one `dated_leaf` line; regex that hits only the prefix/day does not match
- Recall nested note: after a two-note nap, `recall_text` on the original sentence → `dated_leaf` from `NoteChild.name`, not `{64hex}  text`
- Recall nested caption: after a nap-of-naps, `recall_text` on an inner caption → `xN <short_id(named_ids)>: caption`; that prefix `zoom_text`s
- Recall prefix-only: view pack line contains hex `b` in the prefix, caption does not → `recall_text(..., "b")` does not include that pack
- Zoom two-note nap: `zoom_text` of the pack → two dated leaf lines, no content id (`test_zoom_two_note_nap_prints_both_texts` retargeted)
- Zoom loose note: `zoom_text` of a note id → one `dated_leaf` line (`test_zoom_loose_note_id_prints_the_note` retargeted)
- Zoom nap-of-naps: `zoom_text` of the parent → two pack lines with `short_id` prefixes, not 64-hex by default (`test_zoom_nap_of_naps_prints_two_children_not_leaves` retargeted; stop splitting on two spaces)
- Zoom nested leaf id: zoom of a note id found only inside a children file → dated leaf line
- Nap-of-naps payload: `test_nap_of_two_naps_nests_napchild_and_unions_digests` still checks `.tree` bytes; its zoom assertion uses dated leaves, not `split("  ")`
- Prompt membership: `prompt_text()` still signals clone-portability (another machine / fresh clone) and does not contain `must still be true after a fresh clone`
- Wake regression: existing `test_wake.py` / `test_fold.py` dated-leaf cases stay green

### Test Infrastructure

- Framework: pytest via `tox` (or `uvx --with tox tox`); `pytest.ini` `testpaths = tests`
- Test location: `tests/`
- Conventions: `load_summem()` + `init_repo`; `dated_leaf(stamp, text)` in `tests/conftest.py`; one behavior per test function
- New test files: `tests/test_gitutil.py` (walker enqueue under wake-grammar zoom output)

## Implementation Plan

### 1. Proof walkers enqueue from trees, not stdout — executable

- Files: `tests/test_gitutil.py`, `tests/gitutil.py` (`reaches`, `zoom_reaches`)

1. Stub tests: `tests/test_gitutil.py` empty `test_reaches_nested_leaf_when_zoom_prints_wake_grammar`.
2. Stub interface: `tests/gitutil.py` `_nap_child_ids(m, parent, cid) -> list[str]` (direct `NapChild.id`s of one zoom level; empty for notes / missing trees).
3. Write tests and run red: nap-of-naps; monkeypatch `zoom_text` to `format_wake_line` of `_projected_child` rows with `named_ids`; `reaches(m, repo, "a1")` is True. Current `line.split()[0]` enqueues `x2` and fails.
4. Write code and run green: `reaches` and `zoom_reaches` still treat `sentence in` zoom output as the hit (CLI for `zoom_reaches`, `zoom_text` for `reaches`). Child ids come from `_nap_child_ids` / `Tree.kids`, never from stdout. Change **both** helpers in this unit so `split()[0]` does not survive on the CLI walker. `zoom_reaches` loads the driver via `SourceFileLoader` on `SCRIPT` (do not import `conftest`). Do not enqueue leaves.

### 2. Zoom children use format_wake_line — executable

- Files: `tests/test_zoom.py`, `tests/test_nap.py`, `summem` (`_zoom_kids`, `_find_in_tree`, `zoom_text`, drop `_zoom_note_line` if unused)

1. Stub tests: retarget (do not duplicate) `test_zoom_two_note_nap_prints_both_texts`, `test_zoom_loose_note_id_prints_the_note`, `test_zoom_nap_of_naps_prints_two_children_not_leaves`; retarget the zoom suffix parse in `test_nap_of_two_naps_nests_napchild_and_unions_digests`; add/empty `test_zoom_nested_note_id_prints_dated_leaf`. Keep error-path tests.
2. Stub interface: `_find_in_tree` returns `NoteChild | NapChild | None` (not `str`); `_zoom_kids(tree, ids)` keeps its return type; no new public command.
3. Write tests and run red: two-note zoom `==` `dated_leaf` for each child's stamp; loose-note zoom is `dated_leaf`; nap-of-naps lines equal `format_wake_line` of projected children with `named_ids` (no `split("  ")`); nested note id is dated; nap payload test zoom lines are dated `a1`/`a2`; assert 64-hex absent when `short_id` is 8.
4. Write code and run green: `_zoom_kids` is only `_projected_child` plus `format_wake_line` — no new f-string line shapes. View-note zoom uses `format_wake_line` on that `ViewNode`. Prefix uniqueness is `named_ids`, not view-only ids. Drop `_zoom_note_line` if unused.

### 3. Recall matches sentences, prints the same grammar — executable

- Files: `tests/test_recall.py`, `summem` (`recall_text`, `_recall_nested`)

1. Stub tests: add/empty prefix-false-positive and dated nested-leaf cases; retarget `test_recall_matches_nested_nap_caption` off `{id}  caption`.
2. Stub interface: `_recall_nested` gains `ids: list[str]` so nested packs can `short_id`; no new CLI flags.
3. Write tests and run red: nested note → `dated_leaf`; nested caption → `xN prefix: caption` zoomable via `resolve_id`/`zoom_text`; hex that appears only in a view prefix does not hit; loose-note match still finds the sentence and prints dated.
4. Write code and run green: view pass `rx.search(node.caption)` then append `format_wake_line(node, named_ids)`; nested pass `rx.search(child.text|child.sum)` then append `format_wake_line(_projected_child(child), ids)` with `ids = named_ids(parent)`. `_recall_nested` prints only through `_projected_child` plus `format_wake_line` — no new f-string line shapes.

### 4. Register Memories wording — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text`), `docs/agents-prompt.md`, `AGENTS.md`

1. Stub tests: extend `test_prompt_text_invariants` (or a sibling) for the membership sentence.
2. Stub interface: none — still `prompt_text() -> str`.
3. Write tests and run red: `prompt_text()` must not contain `must still be true after a fresh clone`; must still exclude machine-local membership (clone / another machine / personal). Existing lockstep tests stay.
4. Write code and run green: one or two word changes to the Register Memories sentence so it means write-time truth plus clone-portability, not eternal currency. Copy the same bytes into `docs/agents-prompt.md` and the `AGENTS.md` prefix.

### 5. Atlas and briefing — prose/policy

- Files: `docs/architecture/index.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Atlas § Zoom and recall: listings share `format_wake_line`; recall searches sentences; prefixes are unique among `named_ids`; 64-hex stays on disk. Proof/surgery tests walk `Tree.kids` for nested ids, not zoom stdout.
2. `systemPatterns.md` Wake-dates-leaves section: the same grammar is wake, recall hits, and zoom children. Do not claim nested recall stays `{id}  text`.

## Technology Validation

No new technology - validation not required

## Dependencies

- `format_wake_line`, `_projected_child`, `short_id`, `named_ids`, `dated_leaf` already on this branch
- Prompt lockstep: `test_agents_md_starts_with_prompt_text`, `test_shipped_prompt_matches_prompt_text`
- `tests/gitutil.py` is imported by `conftest.py`; walker code must not import `conftest`

## Challenges & Mitigations

- Prefix not zoomable: if recall/zoom `short_id` against view ids only, a nested pack can collide with a hidden tree id. Mitigation: always `named_ids(parent)` for any printed pack prefix. Wake still unique-prefixes against view ids; a recall view-pack line can be a longer prefix than wake. Do not reopen the wake printer.
- Proofs break if walkers keep `line.split()[0]`. Mitigation: unit 1 before zoom code; enqueue `NapChild.id` from the children file; keep `sentence in` zoom output as the display check so proof 4 still exercises zoom after squash.
- Leftover `{id}  text` tests sit beside new names and stay red. Mitigation: retarget the existing functions in unit 2; do not add parallel dated_* copies.
- `conftest` ↔ `gitutil` import cycle if `zoom_reaches` calls `load_summem`. Mitigation: `SourceFileLoader` on `SCRIPT` inside `gitutil`.
- Matching `node.caption` drops recall-by-day and recall-by-prefix. That is the requirement. Mitigation: do not add tests that search formatted fields; add the prefix-false-positive test so it cannot silently return.
- Prompt too timid: a synonym of “must remain true” would fail the same misreading. Mitigation: forbid the old substring in `test_prompt_text_invariants`; choose words that locate the test in clone-portability, not currency over time.

## Pre-Mortem

- Plan treated 64-hex as still required for zoom children: already covered — agent handles are `short_id`; disk stays 64-hex.
- Recalling the formatted line because a helper was reused naively: split match haystack (caption/text) from print in unit 3.
- Prompt lockstep files updated by hand out of order: existing lockstep tests are the gate; unit 4 changes `prompt_text()` first, then the two documents to match.
- Parsing the new wake grammar in `reaches` instead of walking trees: unit 1 forbids stdout-as-id; a future display change should not retouch proofs.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [ ] Build
- [ ] QA
