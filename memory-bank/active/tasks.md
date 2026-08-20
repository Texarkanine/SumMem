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
- Prompt invariants: `prompt_text()` tells agents to run `.summem/summem`; skip if a root wake is already in the conversation; public notes only; no `before any other tool call`; no `AGENTS.md or CLAUDE.md`
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
2. Stub interface: `ensure_store` still creates `notes/`, `naps/`, default `config.toml`; drop the copy branch (leave a comment-free no-op on the driver path).
3. Write tests and run red: `test_first_note_creates_config_notes_and_driver` no longer expects a driver file; add `test_ensure_store_does_not_create_driver`; `test_first_wake_creates_store` and git-root auto-create in `test_scopes.py` drop `(store / "summem").is_file()`. Keep `test_existing_driver_is_not_overwritten`.
4. Write code and run green: delete `shutil.copy2` / chmod of `driver` in `ensure_store`. Leave `notes/`, `naps/`, and missing-config write.

### 2. Baked prompt and this repo’s `AGENTS.md` — executable + prose

- Files: `tests/test_init.py`, `summem`, `AGENTS.md`

1. Stub tests: invert the `.summem/summem` forbidden substring; keep lockstep.
2. Stub interface: `prompt_text()` still returns a string.
3. Write tests and run red: `prompt_text()` contains `.summem/summem` and does not contain `before any other tool call`; lockstep against `AGENTS.md`.
4. Write code and run green: rewrite `prompt_text()` to the operator’s `AGENTS.md` shape (`# Project Memory`, mandatory wake/note, other commands) with invoke path `.summem/summem` (not `./summem/summem`). Land that same string at the top of `AGENTS.md`; keep `# Agent context` under it. `CLAUDE.md` stays `@AGENTS.md`.

### 3. Docs and persistent memory-bank — prose/policy

- Files: `VISION.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. `VISION.md` Onboarding: git-root auto-create is dirs + default config, not a driver. Operator places `.summem/summem`, runs `init`, pastes. `start` same: store dirs + config, no driver copy.
2. `VISION.md` Activation sample: invoke `.summem/summem wake` (session start, once, skip if a root wake is already in the conversation).
3. `systemPatterns.md` / `techContext.md`: stop saying `ensure_store` copies the driver. This repo: record is repo-root `summem`; `.summem/summem` is a symlink. Agents invoke `.summem/summem`.
4. Do not rewrite archives.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `ensure_store` callers (`wake`, `note`, `nap`, `zoom`, `recall`, `start`)
- Lockstep `prompt_text()` ↔ `AGENTS.md`
- [Issue #2](https://github.com/Texarkanine/SumMem/issues/2) wake/note rules; invoke-path comments there are superseded by this rework

## Challenges & Mitigations

- Tests that treat “store exists” as “`.summem/summem` is a file”: change those assertions in the same unit as the copy removal.
- `start` without a nested driver: agents still run root `.summem/summem` and pass `--path`; do not invent a nested copy.
- Operator `AGENTS.md` currently says `./summem/summem` (a `summem/` directory). Prompt uses `.summem/summem`.
- Catalog vs prompt: `usage_text` keeps the product name `summem` so substring tests on `.summem/summem` in the catalog stay valid.

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
- [ ] Preflight
- [ ] Build
- [ ] QA
