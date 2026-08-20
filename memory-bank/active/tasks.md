# Task: agents-prompt

* Task ID: agents-prompt
* Complexity: Level 2
* Type: simple enhancement (rework)

Strike driver copy from `ensure_store`. Align the baked prompt, this repo’s `AGENTS.md`, and docs with onboarding: place `.summem/summem`, run `init`, paste. This repo’s record stays repo-root `summem`; store drivers symlink to it.

## Test Plan (TDD)

### Behaviors to Verify

- `ensure_store` does not place the driver: no `.summem/summem` beforehand → dirs + config exist, no `summem` file
- Existing driver is still left alone: pre-placed bytes or symlink unchanged
- First `wake` / `note` at git root still auto-creates dirs + config, not a driver
- `start` creates a nested store’s dirs + config, not a nested driver
- Prompt invariants in `test_prompt_text_invariants`: drop `"## SumMem"` and `"repository root"`; require `.summem/summem`; keep `summem`, `wake`, `root` (root wake), `conversation`, stranger/public, no `before any other tool call`, no `AGENTS.md or CLAUDE.md`. Do not add a heading-string change-detector.
- Lockstep: this repo’s `AGENTS.md` starts with `prompt_text()`
- Catalog `usage_text` still names the product `summem`, not `.summem/summem` (CLI help vs agent invoke path)

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`, run with `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `load_summem()` from `conftest`; store cases in `tests/test_store.py`; CLI/prompt in `tests/test_init.py`; git-root auto-create in `tests/test_wake.py` and `tests/test_scopes.py`
- New test files: none

## Implementation Plan

### 1. `ensure_store` does not copy the driver — executable

- Files: `tests/test_store.py`, `tests/test_wake.py`, `tests/test_scopes.py`, `summem`

1. Stub tests: empty cases that missing driver stays missing; existing driver/symlink unchanged; first wake/note/start do not create `summem`.
2. Write tests and run red:
   - `test_first_note_creates_config_notes_and_driver`: drop the driver-file assertion; rename if the name still says “and driver”.
   - Add `test_ensure_store_does_not_create_driver`.
   - `test_first_wake_creates_store`: drop `(store / "summem").is_file()`.
   - `test_start_creates_store_in_dir` in `tests/test_scopes.py` (the only `(store / "summem").is_file()` there): drop that assertion.
   - Keep `test_existing_driver_is_not_overwritten` and `test_ensure_store_creates_naps_dir` as no-clobber guards (pre-placed driver still untouched).
3. Write code and run green: in `ensure_store`, delete the driver local, the `if not driver.exists()` branch, the copy/chmod, and unused `import shutil`. Leave `notes/`, `naps/`, and missing-config write.

### 2. Baked prompt and this repo’s `AGENTS.md` — executable + prose

- Files: `tests/test_init.py`, `summem`, `AGENTS.md`

1. Stub tests: empty cases covering the revised `test_prompt_text_invariants` list above; keep lockstep.
2. Stub interface: `prompt_text()` still returns a string.
3. Write tests and run red: invariants as listed; lockstep against `AGENTS.md`. Lockstep is already red in the worktree (`AGENTS.md` was edited to the draft while `prompt_text()` still returns the old string) — treat that as this unit’s red, not a surprise.
4. Write code and run green: rewrite `prompt_text()` so every invoke is `.summem/summem` (wake, note, recall, zoom, start). Do not say the driver is a `summem` file at the repository root — that is this development repo’s record, not a stranger clone. Opening line: shared memory; run `.summem/summem`; `--path` aims at a store. Session-start / notes / other-commands follow the operator’s section shape (`# Project Memory`, mandatory wake/note). Land that same string at the top of `AGENTS.md`; keep `# Agent context` under it. `CLAUDE.md` stays `@AGENTS.md`. Do not parameterize `prompt_text()`.

### 3. Docs and persistent memory-bank — prose/policy

- Files: `VISION.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. `VISION.md` Onboarding: git-root auto-create is dirs + default config, not a driver. Operator places `.summem/summem`, runs `init`, pastes. `start` same: store dirs + config, no driver copy.
2. `VISION.md` Activation sample: invoke `.summem/summem wake` (session start, once, skip if a root wake is already in the conversation).
3. `systemPatterns.md` / `techContext.md`: stop saying `ensure_store` copies the driver. This repo: record is repo-root `summem`; `.summem/summem` is a symlink. Agents invoke `.summem/summem`.
4. `ROADMAP.md`: already places the script at `.summem/summem`; no edit.
5. Do not rewrite archives.

### 4. Instrument Composer 2.5 — prose/policy

- Files: none required
- No tests: prose/policy artifact (external semantic check, not pytest)

1. After units 1–3, spawn cheap Composer 2.5 (not fast) subagents. Tell them they are a subagent and not to run `memo`. Give them the rewritten SumMem block (`prompt_text()` / top of `AGENTS.md`).
2. Probe A: no prior root wake in their prompt — do they invoke `.summem/summem` (not repo-root `./summem` or `./summem/summem`) and run a root wake?
3. Probe B: a prior root wake already in their prompt — do they skip a second root wake?
4. Record what they did in `progress.md`. If they miss because the prompt is wrong, fix the prompt (and lockstep). Do not treat a confused subagent as a pytest failure.

The earlier Composer probe in this task used the pre-rework prompt and does not count.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `ensure_store` callers (`wake`, `note`, `nap`, `zoom`, `recall`, `start`)
- Lockstep `prompt_text()` ↔ `AGENTS.md`
- [Issue #2](https://github.com/Texarkanine/SumMem/issues/2) wake/note rules; invoke-path comments there are superseded by this rework

## Challenges & Mitigations

- Tests that treat “store exists” as “`.summem/summem` is a file”: change those assertions in the same unit as the copy removal.
- `start` without a nested driver: agents still run root `.summem/summem` and pass `--path`; do not invent a nested copy.
- Operator `AGENTS.md` currently says `./summem/summem` and that the driver lives at repo root. Prompt uses `.summem/summem` everywhere and does not claim a repo-root executable.
- Catalog vs prompt: `usage_text` keeps the product name `summem` so `test_catalog_omits_store_driver_path` stays valid.

## Pre-Mortem

- First `wake` in a clone with no driver still works (dirs + config) but agents cannot find `.summem/summem` until someone places it: that is the onboarding sequence, not a bug.
- Docs still say “copies the driver”: covered by unit 3.
- Prompt and `AGENTS.md` drift: lockstep.
- Nested `start` store has no script and someone tries to run it: prompt says run `.summem/summem` (repo store), `--path` for scope.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [x] Build
- [x] QA (PASS)

Build units 1–4 done. pytest 205 passed. Composer 2.5 Probe A ran `.summem/summem wake` (then catalog `wake --path dogfood`). Probe B skipped a second root wake. Did not take the nested-store symlink advisory.

### QA findings

- **PASS.** The rework matches the plan and is acceptable as-is.
- `ensure_store` only creates `notes/`, `naps/`, and missing config. `shutil`/`copy2`/`chmod` are gone. First wake, first note, and `start` do not place a driver; a pre-placed driver is still left alone.
- `prompt_text()` and this repo’s `AGENTS.md` lockstep on `.summem/summem`. Invariants dropped `"## SumMem"` and `"repository root"`; they require `.summem/summem` and still forbid OptMem wake-first / dual-paste wording. `CLAUDE.md` remains `@AGENTS.md`. Catalog `usage_text` still names `summem`.
- `VISION.md` Onboarding/Activation, `systemPatterns.md`, and `techContext.md` no longer say the script copies the driver. `ROADMAP.md` was correctly left alone. Archives were not rewritten.
- Composer 2.5 Probe A invoked `.summem/summem wake` (not `./summem` or `./summem/summem`). Probe B skipped a second root wake.
- Advisory (non-blocking): catalog lines still look like commands, so Probe A also pulled dogfood. Out of this rework’s scope.
- Nested-store driver symlink was a preflight radical-innovation advisory. Build correctly did not add it.
