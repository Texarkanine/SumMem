# Task: prompt-commit-notes

* Task ID: prompt-commit-notes
* Complexity: Level 2
* Type: simple enhancement

Tweak `prompt_text()` so agents `git add` and commit the files the script just wrote, keep the script as the only writer, lockstep `AGENTS.md`, and fix briefing that currently says this repo ignores store data (and that the agent interface must never mention git).

## Test Plan (TDD)

### Behaviors to Verify

- Publish instruction: `prompt_text()` → contains `git add` and `commit`
- Writer-only: `prompt_text()` → still forbids inventing filenames, rewriting note bytes, or deleting store files by hand (or equivalent "never edit or delete by hand" + script-is-writer)
- No "tool manages them" alone: `prompt_text()` → does not contain `the tool manages them` (that phrase is what made agents skip `git add`)
- Lockstep: this repo's `AGENTS.md` → starts with `prompt_text().strip()`
- CLI stays silent: existing `test_wake_output_omits_notes_naps_and_git` and recall counterpart → still pass; `usage_text()` is not taught to mention git

### Test Infrastructure

- Framework: pytest
- Test location: `tests/`
- Conventions: `test_*.py`, load via `conftest.load_summem` / `SourceFileLoader`; prompt contracts live in `tests/test_init.py` (`test_prompt_text_invariants`, `test_agents_md_starts_with_prompt_text`)
- New test files: none

## Implementation Plan

### 1. Prompt publish instruction — executable — done

- Files: `tests/test_init.py`, `summem` (`prompt_text`), `AGENTS.md`

1. Stub tests: add cases on `test_prompt_text_invariants` (or a sibling in `tests/test_init.py`) for publish tokens and the retired "tool manages them" phrase. No new functions.
2. Stub interface: none. `prompt_text()` already exists.
3. Write tests and run red: `assert "git add" in prompt` and `assert "commit" in prompt.lower()`; assert the writer-only constraint is present; `assert "the tool manages them" not in prompt`; existing `.summem/summem` / no-FIRST invariants stay. Run `uv run --python 3.11 --with pytest pytest tests/test_init.py` — new asserts fail.
4. Write code and run green: rewrite the Register Memories closer in `prompt_text()` so the script remains the only writer and agents `git add` the files it just wrote, then commit with the rest of the work or as their own commit. Do not name `notes/`, `naps/`, or hashes. Copy the new `prompt_text()` into the top of `AGENTS.md`. Do not teach `usage_text` or CLI prints to mention git.

### 2. techContext store-data sentence — prose/policy — done

- Files: `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. Replace "Generated store data in this repository is ignored." with a sentence that matches the tree: this repo commits `.summem/notes/` (and naps when present); `.gitignore` does not ignore them.

### 3. Agent-interface briefing — prose/policy — done

- Files: `memory-bank/productContext.md`, `docs/architecture/index.md`
- No tests: prose/policy artifact

1. Narrow "The agent interface does not mention … git" so it still binds CLI output (wake/recall/usage) and store paths, and so the activation block may tell agents to publish via git. Same correction on the architecture change-surface row that currently says "Do not leak store paths or git into the agent interface."

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `prompt_text()` / `AGENTS.md` lockstep test
- Existing wake/recall "no git in CLI output" tests

## Challenges & Mitigations

- Leftover "the tool manages them" still reads as "do not `git add`": delete that phrase; say script-writes / git-publishes as two adjacent sentences.
- Naming `notes/` or `naps/` in the prompt leaks store paths: say "the files the script just wrote."
- `productContext` and the atlas currently forbid git in the agent interface: step 3 narrows that to CLI output, or the new prompt is "wrong content" in the briefing.
- Prompt-content asserts that lock a whole paragraph become change-detectors: assert the contract tokens (`git add`, `commit`, no `the tool manages them`), not the full closer.

## Pre-Mortem

- Agents still leave notes untracked because the closer still sounds like "hands off git": already covered by Challenge 1 (retire "the tool manages them").
- QA FAIL because the atlas / productContext still say never mention git: already covered by Challenge 3 / step 3.
- Tests fail on a later wording tweak that still teaches publish: already covered by Challenge 4.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] Build (rework)
- [x] QA - PASS

## QA Findings

### Round 1 - FAIL (resolved)

- **Blocking:** `test_prompt_text_teaches_git_publish` checked only that `"commit"` appeared somewhere in the prompt, which is too loose to protect the instruction.
- **Correction applied by Build rework:** the test now asserts `commit them` and `own commit`.

### Round 2 - PASS

- **Resolved:** `commit them`, `own commit`, and `git add` each occur only in the publish sentence, so deleting that sentence turns the test red. The prior blocker is closed.
- **Completeness:** all four acceptance criteria met - publish instruction, writer-only rule, `techContext.md` correction, lockstep and invariant tests.
- **Regression:** the "script is the only writer" invariant in `systemPatterns.md` and `docs/architecture/index.md` still holds; `git add` does not write store files. CLI output remains silent on git.
- **Documentation:** `productContext.md` and the architecture change-surface row were narrowed in step with the prompt, so no briefing now contradicts the code.
- **Integrity:** no debris, no TODOs, no placeholders. The committed `.summem/notes/` entry is a genuine dogfood note consistent with the new `techContext.md` sentence.
- **Advisory (non-blocking):** `assert "rewrite" in lower` is a weak token; the adjacent `invent filenames` and `the only writer` asserts carry the writer-only contract.
- **Advisory (non-blocking):** README's "Never edit store files by hand" says nothing about publishing. Out of scope; README defers to `AGENTS.md`.
- **Tests:** 208 passed.
