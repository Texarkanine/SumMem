# Task: noting-ratchet

* Task ID: noting-ratchet
* Complexity: Level 2
* Type: simple enhancement

Replace the bare `note is too long` rejection with an OptMem-style ratchet for `note` and `nap` ([SumMem#16](https://github.com/Texarkanine/SumMem/issues/16)). Apply the same rule to other agent-facing CLI errors that only complain, when a next step is known and not obvious.

## Test Plan (TDD)

### Behaviors to Verify

- Over-long note (library): `write_note` / `require_entry` with UTF-8 byte length `limit + 1` → `ValueError` whose text contains actual bytes, the store limit, `Accented characters cost 2 bytes`, and `Compress it further`; store unchanged
- Over-long note (CLI): `main(["note", text])` over default 280 → exit 1, that footer on stderr, no note file
- Over-long nap (library): `write_nap` with caption `limit + 1` → same `ValueError` shape; payloads unchanged
- Over-long nap (CLI): `main(["nap", id_a, id_b, caption])` over limit → exit 1, same footer on stderr, no nap files
- Configured limit: store `ENTRY_CHARS = 5`, text of 6 bytes → footer names limit `5` and actual `6`, not 280
- Exact limit still accepts: 280 ASCII bytes, and a mixed UTF-8 line of exactly 280 bytes, still write
- UTF-8 overflow: 94 × `你` (282 bytes) → footer names `282` bytes
- Multi-line entry: text with `\n` or `\r` → problem plus a known next step (merge the lines, or note each line); store unchanged
- Empty entry: still rejected; problem statement only (next step is obvious)
- Unknown id: still contains `unknown id`; adds a next step to copy an id from wake; no `notes/`, `naps/`, or `git`
- Ambiguous prefix: still contains `ambiguous`; adds a next step to give a longer prefix
- Not adjacent: `not adjacent` plus a next step to nap two ids that sit next to each other in wake
- Range token: `not a content id: {token}` plus a next step to copy an id from wake; proof 5 still holds
- Unreadable pack / overlapping packs / invalid pattern / not in a repository / skipped a pack: problem statement only (no invented next step); existing substring and leak checks still hold

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini`: `py311`–`py314`, `package = skip`)
- Test location: `tests/`
- Conventions: `test_*.py`; load repo-root `summem` with `conftest.load_summem` / `SCRIPT`; CLI via `main([...])` + `capsys` or `subprocess` + `SCRIPT`; no store paths or `git` in agent-facing stderr
- New test files: none

## Implementation Plan

### 1. Length ratchet — executable

- Files: `tests/test_store.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_scopes.py`, `summem`

1. Stub tests: add empty cases `test_note_overlong_message_is_a_ratchet`, `test_nap_overlong_caption_message_is_a_ratchet` (library), `test_cli_note_overlong_prints_ratchet`, `test_cli_nap_overlong_prints_ratchet` (CLI). Extend `test_config_entry_chars_is_per_store_for_notes_and_naps` only with stderr asserts (do not add a new suite).
2. Stub interface: none. Keep `require_entry(text, entry_chars=None)`. No new public function unless a one-line helper inside `summem` stays unexported.
3. Write tests and run red: assert the footer lists `len(text.encode("utf-8"))`, the configured limit, the accented-character sentence, and `Compress it further`; assert exit 1 and no new payload files on the CLI cases; assert a tight store names its own limit.
4. Write code and run green: in `require_entry`, replace `note is too long` with that footer using `limit` (default `ENTRY_CHARS`). Crib OptMem: `Too long: %d bytes, limit %d. Accented characters cost 2 bytes. Compress it further.` ISO 24495 / STE100: keep it one or two short sentences, one meaning per word. Do not hardcode 280.

### 2. Other agent-facing ratchets — executable

- Files: `tests/test_store.py`, `tests/test_nap.py`, `tests/test_cli.py`, `tests/test_proof_reject.py`, `summem`

Planned copy (keep today’s distinctive substrings so existing proofs stay green):

| Today | Change | Why |
| --- | --- | --- |
| `note is empty` | `Empty.` | Problem only; next step is obvious. Same text for note and nap. |
| `note must be one line` | `One line only. Merge the lines, or note each line.` | Next step known and not obvious. |
| `unknown id` | `unknown id. Copy an id from wake.` | Next step known and not obvious. Keep substring `unknown id`. |
| `ambiguous id` | `ambiguous id. Give a longer prefix.` | Next step known and not obvious. Keep `ambiguous`. |
| `not adjacent` | `not adjacent. Nap two ids that sit next to each other in wake.` | Next step known and not obvious. |
| `not a content id: {token}` | `not a content id: {token}. Copy an id from wake.` | Next step known and not obvious. Keep the token. |
| `unreadable pack` | no change | No known next step that is not invented. |
| `overlapping packs` | no change | Heal already ran; no known next step. |
| `invalid pattern` | no change | “Fix the pattern” is obvious from the problem. |
| `not in a repository` | no change | Next step is obvious; must not say `git`. |
| `skipped a pack` | no change | Warning, already a problem statement. |
| `SumMem needs Python 3.11 or newer` | no change | Next step is obvious. |
| usage / argparse | no change | Catalog is already a ratchet. |
| `clock must be UTC`, `unknown tree child type` | no change | Not agent-facing CLI. |

1. Stub tests: empty cases for multi-line next-step text, unknown-id / ambiguous / not-adjacent / range-token next steps (library or `main`, matching the existing file for that error).
2. Stub interface: none. Edit the existing `ValueError` / `stderr.write` strings only.
3. Write tests and run red: assert the new next-step clauses; keep leak checks (`notes/`, `naps/`, `git`); keep proof 5 (`unknown id`, range token present, no write).
4. Write code and run green: change only the rows in the table marked for change. Do not mention store files, hashes as paths, or git.

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

## Challenges & Mitigations

- Library tests that only `pytest.raises(ValueError)` stay green if the footer is wrong: new tests must assert the footer text, not only the exception type
- Hardcoding 280 in the footer would fail a tight store: interpolate `limit`
- Secondary copy could leak `git` or paths, or become an essay: STE100, one next step, keep distinctive substrings
- Walking every internal `ValueError` would dilute the must-ship work: table above is the closed set

## Pre-Mortem

- Plan treated “ratchet” as rewriting every string, including warnings and internal errors: already covered by the closed table and Challenge 4
- Plan tested exact wording so tightly that a later STE trim in QA looks like a product break: assert required facts (bytes, limit, accented hint, compress; distinctive substrings) not a single frozen paragraph unless the issue crib is the whole footer
- Plan taught a repair for `unreadable pack` we do not actually have: already covered by “no invented next step”

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
