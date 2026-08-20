# Task: agents-prompt

* Task ID: agents-prompt
* Complexity: Level 2
* Type: simple enhancement

Bake one agent prompt into the driver. `summem init` prints it. This repo puts that block at the top of `AGENTS.md`. Cheap Composer 2.5 subagents are the instrument, not a pytest.

## Test Plan (TDD)

### Behaviors to Verify

- Catalog names `init`: `usage_text()` / bare invocation / `-h` → a `summem init` line with no `--path`
- `init` prints: `main(["init"])` → exit 0, stdout contains a paste-at-top-of-`AGENTS.md` recipe and `prompt_text()`
- `init` is not a store command: `main(["init"])` outside a repository → exit 0, no `.summem`, no `AGENTS.md` written
- `init` extra args: `main(["init", "x"])` → nonzero
- `init` has no `--path`: `main(["init", "--path", "."])` → nonzero; `init -h` does not list `--path`
- `-h init` dispatches: `main(["-h", "init"])` → exit 0, not the top-level catalog only
- Prompt invariants: `prompt_text()` mentions repo-root `summem`, `wake`, skip if a root wake is already in the conversation, and stranger-clone / public facts; it does not contain `before any other tool call`, `.summem/summem`, or `AGENTS.md or CLAUDE.md`
- Lockstep: this repo’s `AGENTS.md` starts with `prompt_text()` (strip trailing newlines for compare)
- Existing path-flag contract: `--path` still on wake/note/nap/zoom/recall; still omitted on `start`; now also omitted on `init`

No tests: subagent instrument (manual in Build). No golden-file of the whole prompt.

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`, run with `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `load_summem()` from `conftest`; CLI cases in `tests/test_cli.py`; one file per command family (`test_scopes.py`, `test_wake.py`)
- New test files: `tests/test_init.py`

## Implementation Plan

### 1. `init` command and baked prompt — executable

- Files: `tests/test_cli.py`, `tests/test_init.py`, `summem`

1. Stub tests: add empty cases in `tests/test_init.py` for print, outside-repo, extra args, no `--path`, `-h init`. Extend `test_bare_invocation_prints_command_catalog` and `test_path_flag_is_known_on_all_non_start_commands` in `tests/test_cli.py` with empty/failing `init` assertions.
2. Stub interface: `prompt_text() -> str`, `init_text() -> str` in `summem`; register `init` in `_COMMANDS` and argparse with no `--path`.
3. Write tests and run red: catalog lists `init` without `--path`; `main(["init"])` is 0 and includes paste recipe + `prompt_text()`; outside a repo writes nothing; extra args and `--path` fail; `prompt_text()` holds the invariants above.
4. Write code and run green: `usage_text()` gains an `init` line; `main` handles `init` before `resolve_parent` (help-shaped). Author `prompt_text()` with the prompt-authoring skill: composite of a numbered session-start workflow and a short reference (find repo-root `summem`, `--path` aims at a store, note policy, nap/zoom/recall, `start` only when asked). Tight. Heading `## SumMem`, not OptMem’s `## Memory`. Paste recipe names `AGENTS.md` and may mention a thin `CLAUDE.md` pointer as a second sentence, never “or CLAUDE.md.”

### 2. This repo’s `AGENTS.md` — prose/policy

- Files: `AGENTS.md`, `CLAUDE.md`
- No tests: prose/policy artifact

1. Put `prompt_text()` at the top of `AGENTS.md`.
2. Keep the existing memory-bank section under it.
3. Leave `CLAUDE.md` as `@AGENTS.md`.

### 3. AGENTS.md lockstep — executable

- Files: `tests/test_init.py`, `AGENTS.md`

1. Stub tests: empty case that `AGENTS.md` starts with `prompt_text()`.
2. Stub interface: none (readers already exist).
3. Write tests and run red: `Path(ROOT, "AGENTS.md").read_text()` starts with `prompt_text().strip()` / leading content equal after newline normalize. This is a cross-file contract (init paste vs this tree), not a change-detector on a heading.
4. Write code and run green: if unit 2 already landed the same string, this goes green; if not, fix `AGENTS.md` to match `prompt_text()`. Do not copy by hand a second time if a test already proves equality.

### 4. Design-contract docs — prose/policy

- Files: `VISION.md`, `ROADMAP.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. `VISION.md` Agent interface: add `init` (print the paste block; not a store command; no `--path`). Change “every command except `start` takes `--path`” to except `start` and `init`. Outside a repository, store commands fail; `init` and help still print.
2. `VISION.md` Activation: replace the quoted “before any other tool call” sample with the shipped rule (session start, once, skip if a root wake is already in the conversation). Do not paste the whole `prompt_text()` into VISION.
3. `ROADMAP.md` Later: drop or mark done the “shipping the agent prompt” bullet.
4. `techContext.md`: activation is the `AGENTS.md` block; presence of the driver is not.
5. `systemPatterns.md`: root wake is mandatory because of that block, not a hook.

### 5. Instrument Composer 2.5 — prose/policy

- Files: none required
- No tests: prose/policy artifact

1. Spawn cheap Composer 2.5 (not fast) subagents. Tell them they are a subagent and not to run `memo`. Give them the `AGENTS.md` SumMem block (or `prompt_text()`).
2. Probe A: fresh session, no prior wake in their prompt — do they find repo-root `summem` and run a root wake?
3. Probe B: prior root wake already in their prompt — do they skip a second root wake?
4. Record what they did in `progress.md`. Do not treat a confused subagent as a pytest failure; fix the prompt if the miss is the prompt’s fault.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing CLI catalog / `_COMMANDS` / argparse help dispatch (`-h <command>`)
- [Issue #2](https://github.com/Texarkanine/SumMem/issues/2) and its find-the-driver comments
- `memo init` as the print-and-paste shape, not the wake-first or AGENTS-or-CLAUDE wording
- Prompt-authoring skill at Build for `prompt_text()`

## Challenges & Mitigations

- Existing tests assume “every command except start takes `--path`”: update `test_path_flag_is_known_on_all_non_start_commands` and `test_bare_invocation_prints_command_catalog` in the same executable unit as `init`.
- `init` accidentally goes through `resolve_parent` and dies outside a repo: handle it before store resolution, like `-h`.
- Prompt golden-file rot: test invariants and lockstep, not the full string.
- Habitat vs VISION “no git”: the prompt may say “the directory that contains `.git`” to find the driver; it must not tell agents to write or sort the store with git. Catalog `usage_text` still omits git.
- Dual copy of the prompt: lockstep test (unit 3). `init` is the source; `AGENTS.md` is the paste.
- Composer 2.5 may ignore skip: if they re-wake, tighten the skip sentence (explicit numbered gate), do not add “before any other tool call.”

## Pre-Mortem

- Agents still never wake because they treat `AGENTS.md` as Niko-only and skip a buried block: already covered by putting SumMem first with a numbered startup workflow.
- `init` classified with store commands and fails for the operator who is not yet in a repo: already covered by help-shaped dispatch.
- Prompt teaches `$(git rev-parse)/.summem/summem` and breaks Windows / names the store copy: already covered by find-the-driver invariants.
- Instrument is inconclusive because the parent’s wake is in the child’s context: Probe A’s prompt must not include a prior SumMem wake.
- Prompt and `AGENTS.md` drift after a later wording tweak: already covered by lockstep.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
