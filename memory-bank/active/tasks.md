# Task: ship-prompt-file

* Task ID: ship-prompt-file
* Complexity: Level 2
* Type: simple enhancement

Ship the baked agent prompt as `docs/agents-prompt.md` (exact `prompt_text()`) so onboarding copies a file instead of selecting wrapped `init` output. Keep `init` as a wrap-safe print/redirect of the same text. Do not hard-wrap the file. Do not have `init` write `AGENTS.md`.

## Test Plan (TDD)

### Behaviors to Verify

- [Shipped prompt lockstep]: `docs/agents-prompt.md` bytes as text → equal to `prompt_text()`
- [init still prints the prompt]: `main(["init"])` → exit 0, stdout contains `prompt_text()`, names `PROMPT_DOC` and `AGENTS.md`, does not say to paste
- [init writes nothing]: `init` outside a repository → no `.summem/`, no `AGENTS.md` (existing)
- [AGENTS.md prefix]: this repo's `AGENTS.md` starts with `prompt_text()` (existing; restore the wrap-damaged spaces so it holds)
- [catalog]: `usage_text()` init line → does not say "paste"

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` / `tox.ini`
- Test location: `tests/`
- Conventions: `test_*.py`; load repo-root `summem` via `conftest.load_summem`; `ROOT` is the repository root; CLI tests use `capsys` and `m.main([...])`
- New test files: none

## Implementation Plan

### 1. Shipped prompt lockstep — executable

- Files: `summem`, `tests/test_init.py`, `docs/agents-prompt.md`, `AGENTS.md`

1. Stub tests: add `test_shipped_prompt_matches_prompt_text` in `tests/test_init.py` (empty body). Keep `test_agents_md_starts_with_prompt_text`.
2. Stub interface: add `PROMPT_DOC = "docs/agents-prompt.md"` next to `AGENT_BIN` in `summem`.
3. Write tests and run red: `Path(ROOT, m.PROMPT_DOC).read_text(encoding="utf-8") == m.prompt_text()`. Do not assert on prompt wording. Run `tox -e py311 -- tests/test_init.py::test_shipped_prompt_matches_prompt_text` — expect fail (missing file).
4. Write code and run green: write `docs/agents-prompt.md` as exact `prompt_text()` (one paragraph per line; no hard wrap). Restore this repo's `AGENTS.md` baked prefix so `clone on` / `nap before` match `prompt_text()`. Leave the `# Agent context` suffix in place. Rewrite the `prompt_text()` docstring so it does not say the prompt is "pasted". Rewrite `test_agents_md_starts_with_prompt_text`'s docstring so it does not say "the paste does not drift". No tests on those comments.

### 2. init recipe and catalog — executable

- Files: `summem`, `tests/test_init.py`, `tests/test_cli.py` (only if a catalog assertion breaks)

1. Stub tests: rename/extend `test_init_prints_paste_recipe_and_prompt` to assert the new recipe; add `test_usage_init_line_does_not_say_paste`.
2. Stub interface: no new functions. `init_text()` and `usage_text()` signatures stay.
3. Write tests and run red: `PROMPT_DOC` in `init_text()`; `"paste"` not in `init_text().lower()` and not in the `usage_text()` init catalog line; `prompt_text()` still in `main(["init"])` stdout; existing write-nothing / extra-args / `--path` tests unchanged.
4. Write code and run green: `init_text()` tells the operator to insert `PROMPT_DOC` from the SumMem repository at the top of `AGENTS.md`, notes that this print is the same text, keeps the CLAUDE.md `@AGENTS.md` sentence, still appends `prompt_text()`. Rewrite the `init_text()` docstring so it does not say "paste recipe". `usage_text()` init line becomes `print the agent prompt` (no "to paste").

### 3. Onboarding docs and briefing — prose/policy

- Files: `README.md`, `docs/architecture/index.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. README Quick Start step 2: insert [`docs/agents-prompt.md`](docs/agents-prompt.md) at the top of committed `AGENTS.md` (not "run init and paste"). Command table: `init` prints the prompt. Docs list: link the shipped file; `AGENTS.md` remains this repo's activation plus extra agent context.
2. Architecture activation paragraph: the copyable block is `docs/agents-prompt.md`; `init` still prints it; presence of the driver is still not activation.
3. Surgical briefing lines only if the current "init prints / paste" wording would send a later reader down the wrap-paste path. Do not rewrite those files.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `prompt_text()` / `init_text()` / `usage_text()` / `test_init.py` lockstep
- README onboarding is the operator-facing path; `init` is a print of the same bytes

## Challenges & Mitigations

- `PROMPT_DOC` is a path in the SumMem source tree, not in the repo being onboarded: the recipe must say "from the SumMem repository" so a copied `.summem/summem` is not taken to contain that file.
- This repo's `AGENTS.md` is not the shippable file (it has a Niko `# Agent context` suffix): ship a dedicated exact copy.
- `init` must not write `AGENTS.md`: keep `test_init_outside_repository_writes_nothing`; do not add a write path.
- Prompt-wording tests are change-detectors: lockstep equality only; do not add sentence asserts.

## Pre-Mortem

- Plan ships this repo's `AGENTS.md` as the copyable file and installers get Niko memory-bank instructions: already covered by Challenge 2 (dedicated file).
- Plan adds the file but README still says "run init and paste": the bug remains the documented path — step 3 is required, not optional docs.
- Plan hard-wraps the shipped file to look nicer: insertion fights destination wrap style (the issue's rejected fix) — step 1 writes `prompt_text()` as-is.
- Plan treats `init` as dead and removes the print: operators who redirect stdout lose a wrap-safe dump of the same bytes — keep the print, drop the paste instruction.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY; did not take `--raw` / tty split)
- [ ] Build
- [ ] QA
