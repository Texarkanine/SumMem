# Task: note-ack

* Task ID: note-ack
* Complexity: Level 2
* Type: bug fix

Match OptMem on the wire for `summem note`: write first, always print that the note was recorded, then maybe a fold request. Reword `prompt_text()` so a nap cannot be read as a failed note. Spec: [SumMem#27](https://github.com/Texarkanine/SumMem/issues/27).

Default ACK text: `Saved.` (OptMem's first word). Not a `notes/` path. Not a content-id prefix (those look like nap targets). Not inside `fold_request` (`nap` also prints that helper).

## Test Plan (TDD)

### Behaviors to Verify

- Under-budget `note`: `main(["note", text])` → exit 0, stdout starts with `Saved.`, no fold request (`Run:` / `Compress these two` absent).
- Over-budget `note` with an equal-grain pair: stdout contains `Saved.` before the fold request; the fold request still names the two oldest equal-grain ids; four notes on disk; no nap written.
- Over-budget `note` with no equal-grain pair (16-pack + 1 at `WAKE_LINES=1`): stdout is the success marker only (not empty); exit 0.
- Config `WAKE_LINES` over-budget `note`: stdout contains `Saved.` before `Run: .summem/summem nap`.
- Rejected `note` (too long): exit 1, stdout does not contain `Saved.`.
- Successful `nap` at or under budget: stdout still empty (no `Saved.`).
- Successful `nap` over budget: stdout is still only `fold_request` (no leading `Saved.`).

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini` `package=skip`, `py311`–`py314`). Do not use this machine's bare `python3` (3.10).
- Test location: `tests/`
- Conventions: `load_summem()` + `init_repo(tmp_path / "r")`; CLI via `main([...])` and `capsys`; monkeypatch `WAKE_LINES` or write `config.toml`.
- New test files: none
- Do not add phrase-lock tests on `prompt_text()` wording. Existing lockstep tests (`test_shipped_prompt_matches_prompt_text`, `test_agents_md_starts_with_prompt_text`) are the prompt contract.

## Implementation Plan

### 1. note ACK on the note command path — executable

- Files: `summem` (`main` note branch / nested `note_locked`), `tests/test_fold.py`, `tests/test_cli.py`, `tests/test_scopes.py`

1. Stub tests: in `tests/test_fold.py`, rename `test_over_budget_note_prints_nothing_when_16_plus_1` to a name that expects a success marker; add empty `test_under_budget_note_prints_saved` and `test_rejected_note_does_not_print_saved` (fold or cli file). Leave bodies empty (`pass`).
2. Stub interface: no new public function. Note branch still calls `write_note` then `heal_view` then `fold_request`. ACK is a stdout prefix on that branch only.
3. Write tests and run red: over-budget 16+1 asserts `Saved.` in stdout (not `out == ""`); `test_over_budget_note_requests_equal_grain_ones` and `test_config_toml_wake_lines_is_read` assert stdout starts with `Saved.` and still contains the fold lines; `test_config_wake_lines_is_per_store` stops requiring empty `pkg_out` and requires `Saved.` without `Run:` for the under-budget store; under-budget `note` is `Saved.` only; rejected `note` stdout has no `Saved.`; existing `test_nap_prints_nothing_when_at_or_under_budget` and `test_nap_prints_remaining_ones_not_parent_plus_one` stay as they are (no `Saved.`). Run `tox -e py311 -- tests/test_fold.py tests/test_cli.py tests/test_scopes.py` (or the subset that contains the new cases). New and retargeted note-ACK assertions fail.
4. Write code and run green: after a successful `with_store_lock` on the `note` branch in `main`, write `Saved.\n`; if `fold_request` is non-empty, write a blank line then that text. Do not change `fold_request`. Do not print `notes/`. Write still happens inside `note_locked` before ACK. Re-run the same tox selection until green.

### 2. prompt nap sentence — prose/policy

- Files: `summem` (`prompt_text()`), `docs/agents-prompt.md`, `AGENTS.md`, `README.md`
- No tests: prose/policy artifact. Do not add phrase-lock tests. Keep existing lockstep tests green by copying the new `prompt_text()` into `docs/agents-prompt.md` and keeping `AGENTS.md` a prefix of that string. Do not hard-wrap the shipped prompt. `init` still prints and does not write `AGENTS.md`.

1. Reword the Register Memories nap sentence in `prompt_text()` so a nap cannot be read as a failed `note`: the note is already stored; the nap is extra work on two older view nodes; do that nap before the next action; do not retry the same note.
2. Copy the new `prompt_text()` bytes into `docs/agents-prompt.md`. Update this repo's `AGENTS.md` prefix to match (leave `# Agent context` and below).
3. Update README's day-to-day sentence that currently says `If note asks for a nap, do that nap before the next action.` so it matches the same protocol (already stored; nap then continue; do not retry).

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `fold_request`, `write_note`, `heal_view`, `with_store_lock`
- Existing lockstep tests in `tests/test_init.py` (unchanged assertions)

## Challenges & Mitigations

- ACK inside `fold_request` would make `nap` print `Saved.`: keep ACK in `main`'s `note` branch only; leave nap tests asserting no `Saved.`.
- `test_config_wake_lines_is_per_store` currently requires empty under-budget `pkg_out`: retarget in unit 1, not only the three fold tests named in the issue.
- Combined `capsys` in `test_note_subcommand_writes_and_wake_reads` will include `Saved.` before wake text: that test uses `in`, not exact equality; do not tighten it to `out ==`.
- A wake-style short id on the ACK line could be copied as a nap target: print `Saved.` instead.

## Pre-Mortem

- Plan puts ACK in `fold_request` and `nap` lies: already covered by Challenge 1 and unit 1 step 4.
- Tests still encode silent success (`out == ""` on over-budget `note`): unit 1 names the retargets; also `test_config_wake_lines_is_per_store`.
- Prompt still trains retry (`If note asks for a nap` with no "already stored"): unit 2 rewords `prompt_text()` and README.
- Write delayed until after nap: unit 1 keeps `write_note` inside `note_locked` before ACK or fold.
- New phrase-lock tests on `prompt_text()` fire on the next wording edit: Test Plan forbids them; lockstep is the contract.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

## QA Results

PASS. Implementation matches the plan as-is.

- KISS: ACK is two `stdout.write` calls on `main`'s `note` branch after a successful lock. No new public function.
- DRY: `fold_request` is unchanged. `nap` still prints only that helper.
- YAGNI: marker is the planned `Saved.`; no phrase-lock tests on `prompt_text()`.
- Completeness: successful `note` always prints `Saved.` before any fold text; write stays inside `note_locked`; rejected `note` has no `Saved.`; named silent-stdout tests retargeted; prompt lockstep and README nap sentence updated.
- Regression: under-budget `nap` still empty; over-budget `nap` still only `fold_request` (now also asserts no `Saved.`).
- Integrity: no `notes/` path, no content-id prefix, no leftover stubs.
- Documentation: `prompt_text()`, `docs/agents-prompt.md`, `AGENTS.md`, README updated as planned.

Advisories (do not block): ACK after the whole lock (heal hang still looks silent); atlas fold section does not mention `Saved.`.
