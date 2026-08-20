# Task: recall-zoom-packs

* Task ID: recall-zoom-packs
* Complexity: Level 2
* Type: simple enhancement

`recall` searches nested nap captions that have left the view ([#8](https://github.com/Texarkanine/SumMem/issues/8)). Zoom and recall print one agent-safe stderr line when they skip an unreadable sibling children file, and still succeed if another pack answered ([#7](https://github.com/Texarkanine/SumMem/issues/7)). Wake stays silent.

## Test Plan (TDD)

### Behaviors to Verify

- Nested caption recall: fold two naps into a parent, then `recall_text` of an inner caption (`NapChild.sum` that is no longer a view row) → that caption text appears in stdout
- Nested caption line shape: same inner-caption hit → a line shaped like zoom's nap child (`{leaf-set id}  {caption}`), not a wake `xN prefix:` row
- Nested caption still omits habitat: that hit → stdout has no `notes/`, `naps/`, or `git`
- Existing deep recall: search an original sentence inside a children file → still matches; a view caption that does not contain that sentence still does not appear
- Sibling skip in recall: two view naps, one children file unreadable, search a unique original from the good pack → stdout matches, command does not raise, stderr has one line containing `skipped a pack`, and that line has no path, no `notes/`, no `naps/`, no `git`, no traceback
- Sibling skip in zoom: two view naps, first children file unreadable, zoom a nested id from the second → exit 0 / `zoom_text` returns the child, stderr has the same skip line, no paths/traceback
- Asked-for pack still fatal: `zoom_text` of a view nap whose own children file is unreadable → `ValueError("unreadable pack")`, no skip line required
- Lone unreadable pack still non-fatal for recall: one malformed children file, `recall_text` of a leaf that lives only in that file → no raise (existing), and stderr has the skip line
- Wake unchanged: existing wake degrade tests → still silent (no new warning contract)

### Test Infrastructure

- Framework: pytest via `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `test_<behavior>` functions, `load_summem()` + `init_repo`, datetime/Random fixtures, CLI tests use `monkeypatch.chdir` + `capsys`
- New test files: none

## Implementation Plan

### 1. Nested nap caption recall — executable

- Files: `tests/test_recall.py`, `summem`

1. Stub tests: add empty `test_recall_matches_nested_nap_caption` and `test_recall_nested_caption_omits_notes_naps_and_git` in `tests/test_recall.py`
2. Stub interface: add `_recall_nested(tree, rx, lines, seen)` on `summem` with the same signature the walk will use; leave the body empty/`pass`. Do not change `_note_children` (it remains the note-leaf walker for `_nap_stem` / rematerialize)
3. Write tests and run red: nap-of-naps fixture (four notes → two naps with captions `pack-a` / `pack-b` → parent `both`); `recall_text(repo, "pack-a")` contains `pack-a` and a `{id}  pack-a` line; second test asserts no `notes/`, `naps/`, `git`. Run those two tests; they fail because `_note_children` never yields `NapChild.sum`
4. Write code and run green: implement `_recall_nested` to walk `NoteChild.text` (existing `{cid}  text` line) and `NapChild.sum` (`{child.id}  {child.sum}`), then recurse; `recall_text` calls it instead of `_note_children`. Dedup via the existing `seen` set. Run the new tests plus `tests/test_recall.py`

### 2. Sibling pack skip warning — executable

- Files: `tests/test_recall.py`, `tests/test_zoom.py`, `tests/test_cli.py`, `summem`

1. Stub tests: add empty `test_recall_skips_unreadable_sibling_warns` (capsys) in `tests/test_recall.py`; add empty `test_zoom_skips_unreadable_sibling_warns` (capsys) in `tests/test_zoom.py`; extend `test_cli_zoom_nested_id_skips_sibling_bad_tree` and `test_recall_malformed_tree_does_not_raise` only after the new cases exist (modify existing tests in write-tests, not as a silent contract change in the stub step)
2. Stub interface: add `_warn_skipped_pack()` on `summem` that writes nothing yet
3. Write tests and run red: two-nap fixtures; corrupt one sibling children file; recall a unique leaf from the good pack / zoom a nested id from the good pack; assert stdout still answers and stderr is exactly one agent-safe line `skipped a pack\n` (or contains that phrase as the whole line) with no paths/traceback. Update `test_cli_zoom_nested_id_skips_sibling_bad_tree` to assert the same on CLI stderr while exit stays 0. Update `test_recall_malformed_tree_does_not_raise` to accept/require the skip line when the only children file is unreadable. Run the new tests; they fail because `continue` is silent
4. Write code and run green: `_warn_skipped_pack` writes `skipped a pack\n` to stderr. Call it on the `except _TREE_PARSE_ERRORS: continue` paths in `recall_text` and in `zoom_text`'s *second* loop only (sibling walk). Do not call it on `zoom_text`'s first loop (asked-for view nap still raises `unreadable pack`). Do not touch wake, `named_ids`, or heal. Run `tests/test_recall.py`, `tests/test_zoom.py`, `tests/test_cli.py`, then the full suite

### 3. Atlas zoom/recall sentences — prose/policy

- Files: `docs/architecture/index.md`
- No tests: prose/policy artifact

1. In § Zoom and recall, state that deep recall also matches nested nap captions in children files, not only original note sentences
2. State that zoom and recall print one agent-safe stderr line when they skip an unreadable sibling children file, and do not fail if another pack answered; wake stays silent
3. Do not edit README Developing, tox/pytest runners, or techContext Testing Process

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `loads_tree` / `_TREE_PARSE_ERRORS` / `list_view` / `NapChild` / `NoteChild`
- Existing nap-of-naps fixture pattern in `tests/test_zoom.py`
- Existing silent-skip fixtures: `test_recall_malformed_tree_does_not_raise`, `test_cli_zoom_nested_id_skips_sibling_bad_tree`

## Challenges & Mitigations

- Changing `_note_children` to yield naps would break `_nap_stem` (`leftmost.name`): do not change it; add `_recall_nested`
- Skip warning on the asked-for pack would collide with fatal `unreadable pack`: warn only on `continue` sibling paths
- Nested caption formatted as a wake `xN prefix:` line needs view grain/prefix: use zoom's `{id}  {caption}` instead
- `seen` will not collapse a view `xN prefix: caption` line with a nested `{id}  caption` line: that is correct (different rows); an inner caption is not still a view row
- CLI tests that assert `"unreadable pack" in err` on success would flake if the skip line reused that phrase: skip line is `skipped a pack`, distinct from the fatal message

## Pre-Mortem

- Plan treated `_note_children` as the recall API and "just extended" it: already covered by Challenge 1; step 1 forbids that
- QA fails because architecture still says deep recall is originals only: step 3 updates the atlas before QA
- Warning leaks a path via exception text: `_warn_skipped_pack` writes a constant; it does not interpolate the exception or the path
- Full suite fails because `named_ids` or wake now warn: those paths are explicitly out of step 2

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
