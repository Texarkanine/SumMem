# Task: wake-listing

* Task ID: wake-listing
* Complexity: Level 2
* Type: simple enhancement

Cap `wake` at `WAKE_LINES` lines with short dated rows. Keep full SHA-256 on disk. Print OptMem-style nap prompts from `note`/`nap` only.

## Test Plan (TDD)

### Behaviors to Verify

- Bounded wake: 11 notes, `WAKE_LINES=4` → `wake_text` has 4 lines (newest), no nap prompt, no 64-hex
- Note line: one note → `2026-08-18: hello` (stamp's UTC date, caption)
- Pack line: 16-leaf nap → `YYYY-MM-DD x16 <prefix>: caption` (`xN` only when `leaves > 1`)
- Missing `.sum`: pack line is `YYYY-MM-DD xN <prefix>:` with no caption
- Conflict `.sum`: same as missing caption (skip caption, still print date/grain/prefix)
- Prefix length: default 8 hex; two view ids sharing 8 hex → print shortest unique longer prefix
- `wake` never includes `Run:` or `nap `
- Over-budget `note`: stdout is the prompt (two child bodies, invent-nothing, `Run: .summem/summem nap <p> <p> "<your line>"`); fourth note at budget 3 still writes the note and no nap files
- Remaining: five notes, budget 3 → prompt says compressions remain after this one
- Under-budget `note`/`nap`: stdout empty
- `nap`/`zoom` accept unique prefix of a view id
- Ambiguous prefix: `main(["nap", …])` and `zoom` exit 1, stderr names the clash, no write
- Unknown prefix: exit 1, no write
- Range tokens still rejected (`#16-31`)
- Expand under budget unchanged except printed form and a hard cap: never more than `WAKE_LINES` lines
- Over budget: do not expand `.tree`; slice to newest `WAKE_LINES` files

### Test Infrastructure

- Framework: pytest via `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `test_<unit>.py`, one behavior per `test_*`, docstring is the spec; load driver with `SourceFileLoader`; proofs in `tests/test_proof_*.py`
- New test files: none. Extend `tests/test_wake.py`, `tests/test_wake_expand.py`, `tests/test_fold.py`, `tests/test_cli.py`, `tests/test_zoom.py`, `tests/test_nap.py`. Invert exact-string asserts in `tests/test_proof_conflict.py`, `tests/test_proof_branches.py`, `tests/test_proof_squash.py`.

## Implementation Plan

### 1. Unique prefix — executable

- Files: `.summem/summem`, `tests/test_wake.py`

1. Stub tests: `test_short_id_is_8_hex_when_unique`, `test_short_id_lengthens_until_unique`
2. Stub interface: `short_id(cid: str, ids: list[str], floor: int = 8) -> str`, `resolve_id(token: str, ids: list[str]) -> str` (raise `ValueError` if none or many)
3. Write tests and run red: 8 hex when unique among `ids`; `aa…` vs `ab…` stays 8; two ids sharing 8 hex → 9+; `resolve_id("a3f2c1b8", ids)` returns the full id; two matches raise; zero matches raise
4. Write code and run green: prefix scan over the given id list (view ids). Do not shorten bytes on disk

### 2. Wake line format and cap — executable

- Files: `.summem/summem`, `tests/test_wake.py`, `tests/test_wake_expand.py`

1. Stub tests: `test_wake_line_is_date_and_text_for_a_note`, `test_wake_pack_line_is_date_grain_prefix_caption`, `test_wake_prints_at_most_wake_lines_newest`, `test_wake_does_not_print_a_nap_request`
2. Stub interface: `format_wake_line(node, ids) -> str`; change `expand_frontier` to return at most `budget` nodes (newest = tail after filename sort, which `list_view` already is)
3. Write tests and run red: note `2026-08-18: hello`; pack `2026-01-01 x2 <8hex>: pair`; 11 notes budget 4 → 4 lines, last four captions; `wake_text` has no `Run:`
4. Write code and run green: `wake_text` uses `format_wake_line`; over-budget skip expand and slice `nodes[-budget:]`; under-budget expand then if still over (should not) slice. Invert existing grain-prose asserts in `test_wake.py`

### 3. Fold prompt — executable

- Files: `.summem/summem`, `tests/test_fold.py`, `tests/test_cli.py`

1. Stub tests: `test_over_budget_note_prints_nap_prompt`, `test_fold_request_names_child_bodies`, `test_fold_request_mentions_remaining`
2. Stub interface: rewrite `fold_request` to return the prompt string (empty when `len(view) <= budget` or no equal-grain pair)
3. Write tests and run red: prompt contains both child texts, `invent nothing` (or the locked sentence), `Run: .summem/summem nap `, two unique prefixes, quoted `"<your line>"`; not two raw 64-hex tokens as the whole stdout; remaining line when `len(nodes) - 1 > budget`
4. Write code and run green: build prompt from `list_view` captions of the pair; `Run:` uses `short_id`. Invert `test_over_budget_note_requests_equal_grain_ones` and `test_config_toml_wake_lines_is_read` (they currently split stdout into two hashes)

Prompt shape (lock):

```text
Compress these two into one line of at most 280 characters.
Keep what has lasting effect, drop what does not. Invent nothing.

  YYYY-MM-DD: first child
  YYYY-MM-DD: second child

Run: .summem/summem nap <prefix-a> <prefix-b> "<your line>"
N compressions remain after this one.
```

Last line only when more naps will still be required. Child lines use the same formatter as wake (so a pack child shows `xN`).

### 4. Prefix on nap and zoom — executable

- Files: `.summem/summem`, `tests/test_cli.py`, `tests/test_zoom.py`

1. Stub tests: `test_nap_accepts_unique_prefix`, `test_zoom_accepts_unique_prefix`, `test_ambiguous_prefix_is_error`
2. Stub interface: none new; `main` and `zoom_text` call `resolve_id` against current view ids (zoom also searches nested tree ids: collect ids `zoom_text` can already see)
3. Write tests and run red: 8-hex prefix naps; ambiguous 8 hex exits 1 and writes no `.sum`; zoom prefix on a pack prints children
4. Write code and run green: resolve before `is_range_token` full-id checks; range tokens still `#…` / digit-digit. Nested zoom: resolve among view ids plus ids `zoom_text` already walks in `.tree`

### 5. Proofs and VISION — mixed

- Files: `tests/test_proof_*.py`, `tests/test_nap.py`, `VISION.md`, `memory-bank/systemPatterns.md`

- No tests: `VISION.md` and `systemPatterns.md` are prose/policy (`No tests: prose/policy artifact`)

1. Invert proof/wake string asserts that expect `64hex  (N notes, from …)` so they match the new lines (still check captions, grain `xN` on packs, squash zoom)
2. Rewrite VISION “Wake prints the content id…” to: wake prints date, `xN` for packs, unique prefix on packs; `note`/`nap` print the Run prompt; `nap`/`zoom` accept unique prefixes; stored id remains 64 hex
3. Rewrite `systemPatterns.md` “Wake prints content ids, never positional ranges” to the same contract (still never positional ranges)

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing: `list_view`, `expand_frontier`, `equal_grain_pair`, `fold_request`, `wake_text`, `zoom_text`, `WAKE_LINES`
- Prefix uniqueness is among ids the command can already name (view + zoom-walkable tree ids), not the global SHA-256 space

## Challenges & Mitigations

- Proofs and unit tests hard-code `id  (N notes, from date)`: invert those asserts in the same units as the format change, not with a compatibility shim
- `test_config_toml_wake_lines_is_read` assumes stdout is two whitespace-separated hashes: assert on `Run:` prefixes instead
- Nested zoom ids vs view ids: collect the same id set `zoom_text` searches today before resolving prefixes
- Over-budget 8+2+1 with no equal-grain pair: `fold_request` stays empty; wake still caps at `WAKE_LINES` (newest files). Already accepted: not a full cover
- Operator's live store in this clone is gitignored data: do not commit `.summem/notes/` or a local `WAKE_LINES = 4`

## Pre-Mortem

- Wake cap implemented as “expand until budget” only, still dumping 11 notes when already over: slice `nodes[-budget:]` when `len(nodes) >= budget` before expand
- Prompt still two hashes because CLI writes `fold_request` unchanged: unit 3 owns stdout shape; CLI already prints that string
- Prefix resolver uses the first 8 hex of SHA-256 without uniqueness: unit 1 must lengthen; ambiguous is an error
- Treating this as a stored-id truncation: do not rename files; only print/accept prefixes

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
