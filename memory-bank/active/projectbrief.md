# Project Brief

## User Story

As an operator, I want an emergency-only repo-root `surgery.py` that zipper-excises one whole raw note from a store at the branch tip so that HEAD no longer embeds a sensitive (or duplicate/misformatted) sentence in `notes/` or remaining `.tree` files, after which I can rewrite git history myself.

Authoritative spec: https://github.com/Texarkanine/SumMem/issues/28

## Use-Case(s)

### Use-Case 1: Sensitive sentence already in git

A sentence is already in git. Run `surgery.py` on the **tip of a branch** so HEAD no longer contains that sentence in any store file (`notes/` or remaining `.tree` payloads). Commit that tip. Then rewrite git history to purge leftover blobs. `surgery.py` does the first step only.

### Use-Case 2: Cleanup

Whole-note removal of duplicates, a misformatted line, or other undesirable notes. Same zipper mechanism. Not OptMem-style “forget a summary, keep the leaf.”

### Use-Case 3: Aftercare naps

Excision can invalidate captions. `surgery.py` must not write nap captions. Leaving the over-budget hole is allowed. Operator docs explain how to run an agent to nap invalidated summaries.

## Requirements

1. Deliver a **separate repo-root `surgery.py`**, not a `summem` subcommand, not part of a normal install.
2. Zipper-shaped whole-note excision: **break out** until the target is a loose `notes/` file, **unlink** that one note via the script, **zip again**.
3. Break-out is a new walk in `surgery.py`. `heal_view` only splits overlapping view packs; it is not targeted break-out of a named leaf.
4. Implementation may *call* existing `rematerialize_child`, `_unlink_node`, `list_view`, `heal_view` by loading `summem`. Do not move helpers into `summem` in this issue.
5. “Zip again” means: after unlink, `heal_view` for a unique cover. Do **not** call `write_nap` with invented captions. Leave the over-budget hole for an agent to nap.
6. Address identical-text notes by filename/seq (or equivalent), not only leafset id. Optional: `--contains` unique substring; filename/seq only on collision. Optional: `--dry-run` prints the rematerialize chain and writes nothing.
7. After surgery, HEAD zoom/recall must not still owe the deleted sentence, and no remaining HEAD `.tree` may still embed it.
8. Operator docs must explain (1) tip-then-history-rewrite and (2) how to run an agent to nap invalidated summaries.
9. Same engineering constraints as `summem`: TDD, script is the only writer, Python 3.11+, tox. Load `summem` the way `tests/conftest.py` does (`SourceFileLoader`).

## Constraints

1. Do not edit `summem`, `prompt_text()`, `docs/agents-prompt.md`, or `AGENTS.md` (sibling builder owns #27).
2. Do not add `delete` / `forget` / `surgery` to the shipped CLI, `usage_text`, argparse, or `init`.
3. Agents never `rm` `notes/` or `.tree`. `surgery.py` is the only writer of those files for this operation.
4. Do not invent OptMem-style “forget a summary, keep the leaf.” Do not delete a nap as if it were a leaf.
5. `surgery.py` does not rewrite git history and must not write nap captions.
6. `tox -e coverage` is `--cov=summem`; surgery.py need not appear in lcov unless we choose to extend that env. Default tox stays coverage-free.
7. Executable behavior is TDD. Do not use this machine's bare `python3` (3.10).

## Acceptance Criteria

1. Repo-root `surgery.py` exists; `summem` CLI has no delete/forget/surgery command.
2. Targeted break-out rematerializes along the path to a named leaf until that note is a loose `notes/` file.
3. Unlink removes that one `NoteChild` only; sibling notes remain.
4. After unlink, `heal_view` produces a unique cover; no invented nap captions.
5. Remaining HEAD `.tree` files do not embed the deleted sentence; zoom/recall of HEAD do not owe it.
6. Duplicate-text notes are addressable by filename/seq (and optionally unique `--contains`).
7. `--dry-run` (if implemented) prints the rematerialize chain and writes nothing.
8. Operator docs cover tip-then-history-rewrite and agent aftercare naps.
9. `tox` pytest suite passes on Python 3.11+.
