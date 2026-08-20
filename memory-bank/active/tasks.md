# Task: noting-ratchet

* Task ID: noting-ratchet
* Complexity: Level 2
* Type: simple enhancement

Replace the bare `note is too long` rejection with an OptMem-style ratchet for `note` and `nap` ([SumMem#16](https://github.com/Texarkanine/SumMem/issues/16)). Apply the same rule to other agent-facing CLI errors that only complain, when a next step is known and not obvious. Preflight FAIL (fixable) rewrite: shared `require_entry` copy must be true for nap; `unknown id` next step attaches only at identity-miss raise sites.

## Test Plan (TDD)

### Behaviors to Verify

- Over-long note (library): `write_note` / `require_entry` with UTF-8 byte length `limit + 1` → `ValueError` whose text contains actual bytes, the store limit, `Accented characters cost 2 bytes`, and `Compress it further`; store unchanged
- Over-long UTF-8 note (library): 94 × `你` (282 bytes) → footer names `282` and the store limit (not `len(text)`)
- Over-long note (CLI): `main(["note", "x" * 281])` → exit 1, that footer on stderr, no `notes/`, `naps/`, or `git`
- Over-long nap (library): `write_nap` with caption `limit + 1` → same `ValueError` shape; payloads unchanged
- Over-long nap (CLI): `main(["nap", id_a, id_b, caption])` over limit → exit 1, same footer on stderr, no nap files
- Configured limit: store `ENTRY_CHARS = 5`, text of 6 bytes → footer names limit `5` and actual `6`, not 280
- Exact limit still accepts: 280 ASCII bytes, and a mixed UTF-8 line of exactly 280 bytes, still write
- Multi-line entry: text with `\n` or `\r` → `One line only. Merge the lines.`; store unchanged; same text for note and nap (no “note each line”)
- Empty entry: still rejected; leave `note is empty` (problem only; next step is obvious)
- Identity-miss unknown id (`resolve_id`, `_adjacent_nodes`, `zoom_text` final raise): contains `unknown id` and `Copy an id from wake.`; no `notes/`, `naps/`, or `git`
- Missing-tree unknown id (`_as_child` when `.tree` is absent; `zoom_text` when a view nap has no `.tree`): contains `unknown id`; does **not** contain `Copy an id from wake.`
- Ambiguous prefix: contains `ambiguous` and `Give a longer prefix.`
- Not adjacent: contains `not adjacent` and `Nap two ids that sit next to each other in wake.`
- Range token: `not a content id: {token}` plus `Copy an id from wake.`; proof 5 still holds
- Unreadable pack / overlapping packs / invalid pattern / not in a repository / skipped a pack / empty: problem statement only; existing substring and leak checks still hold

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini`: `py311`–`py314`, `package = skip`)
- Test location: `tests/`
- Conventions: `test_*.py`; load repo-root `summem` with `conftest.load_summem` / `SCRIPT`; CLI via `main([...])` + `capsys` or `subprocess` + `SCRIPT`; no store paths or `git` in agent-facing stderr
- New test files: none

## Implementation Plan

### 1. Length ratchet — executable

- Files: `tests/test_store.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_scopes.py`, `summem`

1. Stub tests: empty `test_note_overlong_message_is_a_ratchet` in `tests/test_store.py` (include the 94 × `你` → `282` assert in this case or a sibling in the same file); empty `test_nap_overlong_caption_message_is_a_ratchet` in `tests/test_nap.py`; empty `test_cli_nap_overlong_prints_ratchet` in `tests/test_cli.py`. Do **not** add `test_cli_note_overlong_prints_ratchet`. Extend `test_note_error_text_omits_store_paths_and_git` and `test_config_entry_chars_is_per_store_for_notes_and_naps` (add `capsys`; drain after each failing `main`).
2. Stub interface: none. Keep `require_entry(text, entry_chars=None)`.
3. Write tests and run red: assert the footer lists `len(text.encode("utf-8"))`, the configured limit, the accented-character sentence, and `Compress it further`; the UTF-8 case must fail a `len(text)` footer; CLI note path is the existing leak test plus footer facts; CLI nap is the new case; tight-store stderr is read per failure so the two `toolong` lines do not mix.
4. Write code and run green: in `require_entry`, replace `note is too long` with OptMem’s crib using `limit` (default `ENTRY_CHARS`): `Too long: %d bytes, limit %d. Accented characters cost 2 bytes. Compress it further.` Do not hardcode 280.

### 2. Other agent-facing ratchets — executable

- Files: `tests/test_store.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_zoom.py`, `tests/test_proof_reject.py`, `summem`

Copy is decided **per raise site**, not per unique string. Shared `require_entry` text must be true for both `note` and `nap`.

| Site | Today | Change |
| --- | --- | --- |
| `require_entry` empty | `note is empty` | no change |
| `require_entry` newline | `note must be one line` | `One line only. Merge the lines.` |
| `require_entry` too long | (Unit 1) | (Unit 1) |
| `resolve_id` no match | `unknown id` | `unknown id. Copy an id from wake.` |
| `_adjacent_nodes` no hits | `unknown id` | `unknown id. Copy an id from wake.` |
| `zoom_text` final raise (token not in view or nest) | `unknown id` | `unknown id. Copy an id from wake.` |
| `_as_child` missing `.tree` | `unknown id` | no change |
| `zoom_text` view nap missing `.tree` | `unknown id` | no change |
| `resolve_id` many matches | `ambiguous id` | `ambiguous id. Give a longer prefix.` |
| `_adjacent_nodes` not neighbors | `not adjacent` | `not adjacent. Nap two ids that sit next to each other in wake.` |
| CLI `is_range_token` (nap and zoom) | `not a content id: {token}` | `not a content id: {token}. Copy an id from wake.` |
| `_as_child` / `zoom_text` bad `.tree` | `unreadable pack` | no change |
| `write_nap` overlapping leaf sets | `overlapping packs` | no change |
| CLI `re.error` | `invalid pattern` | no change |
| `find_store_parent` | `not in a repository` | no change |
| `_warn_skipped_pack` | `skipped a pack` | no change |
| `require_python` | `SumMem needs Python 3.11 or newer` | no change |
| usage / argparse | catalog | no change |
| `require_utc`, `_tree_from_dict` unknown type | internal | no change |

1. Stub tests: empty cases for multi-line copy (note and nap), identity-miss next step, missing-tree `unknown id` **without** the wake clause (unlink a view nap’s `.tree`, then `zoom_text` / `write_nap`), ambiguous next step, not-adjacent next step, range-token next step.
2. Stub interface: none. Edit the listed raise / `stderr.write` strings only. Do not add a kind argument to `require_entry`.
3. Write tests and run red: assert the new next-step clauses at the identity-miss and adjacency sites; assert missing-tree `unknown id` has no `Copy an id from wake.`; keep leak checks and proof 5 (`unknown id`, range token present, no write).
4. Write code and run green: change only the “Change” column. Do not mention store files, hashes as paths, or git. Do not teach a repair for a missing `.tree`.

### 3. Atlas — prose/policy

- Files: none
- No tests: prose/policy artifact

1. `docs/architecture/index.md` already says a note and a caption have a length limit. That remains true. Do not add a change-detector or a CLI-copy paragraph.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `require_entry` (already used by `write_note`, `write_nap`, and both CLI arms)
- Per-store `knobs()["ENTRY_CHARS"]` already passed into `require_entry` at the CLI
- OptMem crib for the too-long footer only (shape, not OptMem’s on-disk log)
- `unknown id` is a shared phrase with two causes; next step is site-specific

## Challenges & Mitigations

- Library tests that only `pytest.raises(ValueError)` stay green if the footer is wrong: new tests must assert footer facts, including the 282-byte UTF-8 case
- Hardcoding 280 in the footer would fail a tight store: interpolate `limit`
- A global replace of `unknown id` would lie on the missing-tree path: change only the identity-miss sites
- Shared `require_entry` cannot say “note each line”: multi-line next step is merge-only
- Tight-store CLI stderr mixes two failures if `capsys` is read once: drain after each failing `main`

## Pre-Mortem

- Plan treated “ratchet” as rewriting every string, including warnings and internal errors: already covered by the raise-site table
- Plan tested exact wording so tightly that a later STE trim in QA looks like a product break: assert required facts (bytes, limit, accented hint, compress; distinctive substrings) not a single frozen paragraph unless the issue crib is the whole footer
- Plan taught a repair for a missing or unreadable pack we do not have: already covered by leaving those sites unchanged
- Plan used one `unknown id` message for two causes: already covered by the raise-site split

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
