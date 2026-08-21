# Project Brief

## User Story

As a coding agent, I want `summem note` to acknowledge that the line was recorded before any nap request, so that I do not treat a fold prompt as a failed write and retry the same note.

## Use-Case(s)

### Use-Case 1

An agent records a fact. The view is over `WAKE_LINES`. Stdout prints a success marker, then a fold request for two older equal-grain nodes. The agent naps those nodes and continues. It does not run the same `note` again.

### Use-Case 2

An agent records a fact. The view is at or under budget, or over budget with no equal-grain pair. Stdout still prints the success marker. Empty-looking success is gone.

## Requirements

1. Fix [SumMem#27](https://github.com/Texarkanine/SumMem/issues/27) as written.
2. `note` still writes first, then ACK, then maybe a fold request. Do not delay the write until after the nap.
3. Always print that the note was recorded before any fold request. Prefer `Saved.` or a wake-style short id. Do not print a `notes/` path.
4. Put the ACK on the `note` command path (`note_locked` / `main`), not inside `fold_request`. `nap` also prints `fold_request`; putting "Saved." there would lie.
5. Reword `prompt_text()` so a nap cannot be read as a failed `note`. Keep `docs/agents-prompt.md` in lockstep. This repo's `AGENTS.md` stays a prefix of `prompt_text()`.
6. Retarget tests that encode silent success, especially `tests/test_fold.py`: `test_over_budget_note_prints_nothing_when_16_plus_1`, `test_over_budget_note_requests_equal_grain_ones`, and `test_config_toml_wake_lines_is_read`. Over-budget `note` still contains a success marker.
7. If agent-facing protocol docs are touched, update README's "If note asks for a nap…" sentence.

## Constraints

1. Script is the only writer of store files.
2. Do not add delete/surgery to the shipped CLI. Do not create `surgery.py`. Do not edit files for issue #28.
3. `init` must not write `AGENTS.md`. Do not hard-wrap the shipped prompt. Phrase-lock tests on `prompt_text()` are change-detectors; the lockstep is the contract.
4. `usage_text` stays `CLI_NAME`; `prompt_text` / `fold_request` stay `AGENT_BIN`.
5. CLI output does not mention store files, hashes as paths, or git.
6. Python 3.11+; `tox` is the suite. Do not use this machine's bare `python3` (3.10).
7. Executable behavior is TDD.

## Acceptance Criteria

1. Successful `note` always prints a success marker on stdout before any fold request, including when `fold_request` is empty.
2. `nap` stdout is unchanged: under budget still silent; over budget still only `fold_request`.
3. The note file exists before ACK is printed. Retrying the same text is not required by the protocol.
4. `prompt_text()` states that a nap after `note` is extra work on already-stored memory, not a failed write.
5. `docs/agents-prompt.md` equals `prompt_text()`. `AGENTS.md` starts with `prompt_text()`.
6. Tests that asserted empty over-budget `note` stdout now require a success marker.
