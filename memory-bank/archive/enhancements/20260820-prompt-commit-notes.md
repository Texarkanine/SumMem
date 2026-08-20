---
task_id: prompt-commit-notes
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: prompt-commit-notes

## SUMMARY

Closed the publish gap in [SumMem#14](https://github.com/Texarkanine/SumMem/issues/14). Agents were treating "the tool manages them" as "do not `git add`," so notes stayed untracked. The baked prompt now keeps the script as the only writer and says the files it writes are part of your work; do not leave them untracked. First pass taught an After-`note` `git add` / own-commit recipe; operator rework dropped that as a second procedure. `techContext.md` no longer claims this repo ignores store data. Draft [PR #15](https://github.com/Texarkanine/SumMem/pull/15). 208 pytest.

## REQUIREMENTS

- Agents must not leave script-written note/nap files untracked. Those files ride with the work that inspired them.
- Script remains the only writer: no invented filenames, rewritten note bytes, or hand-deleted store files.
- `AGENTS.md` stays lockstep with `prompt_text()`.
- `techContext.md` must not say this repository ignores generated store data.
- Out of scope: the script committing, harness hooks, changing note/nap identity.

## IMPLEMENTATION

`prompt_text()` Register Memories closer (and lockstep `AGENTS.md`): "Never invent filenames, rewrite note bytes, or delete memory files by hand. The script is the only writer. The files it writes are part of your work; do not leave them untracked." Retired "the tool manages them." Does not name `notes/`, `naps/`, or a `git add` step.

Briefing: `techContext.md` records that this repo commits `.summem/notes/` (and naps when written). `productContext.md` and the architecture change-surface row bind "no git" to CLI output; the activation block treats script-written files as part of your work. `systemPatterns.md` only-writer section: leaving them untracked is a publish failure, not a writer-boundary success.

## TESTING

`tests/test_init.py::test_prompt_text_notes_are_part_of_the_work` asserts `part of your work`, `untracked`, writer-only tokens, and the absence of `git add`, `own commit`, `the tool manages them`, `notes/`, and `naps/`. Lockstep and existing prompt invariants remain.

QA FAIL on the first closer: `assert "commit" in lower` was too loose (QA cited `committed AGENTS.md`, which is not in `prompt_text()`). Tightened, then the operator replaced the procedure; the test now guards the ride-along constraint. `/niko-qa` PASS after the assertion rework. Full suite: 208 on Python 3.11.

## LESSONS LEARNED

- "The tool manages them" reads as hands off git. Name the failure (untracked) without inventing a publish procedure.
- An After-`note` `git add` / own-commit recipe layers a second tool-call sequence. Notes should ride on the commits the work already makes.
- A prompt-content assert has to name the instruction (`part of your work`), not a word other sentences can grow (`commit` / `committed`).

## PROCESS IMPROVEMENTS

The first QA finding named the wrong witness and still found a real hole. Token width is the lesson, not the cited phrase.

## TECHNICAL IMPROVEMENTS

README still says only "Never edit store files by hand" and defers to `AGENTS.md`. Out of scope for this task.

## NEXT STEPS

Land or continue draft [PR #15](https://github.com/Texarkanine/SumMem/pull/15).
