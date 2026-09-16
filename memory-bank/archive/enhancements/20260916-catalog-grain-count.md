---
task_id: catalog-grain-count
complexity_level: 2
date: 2026-09-16
status: completed
---

# TASK ARCHIVE: catalog-grain-count

## SUMMARY

Root-wake catalog lines are `N: ./path`: `N` is a filename note count on the same `git ls-files` pass that discovers nested stores. Empty children stay `0:`; no digit padding; pulls still omit the catalog. How-to calls `N` a count and teaches `note --path <file>` walk-up so a catalog can receive writes. Draft [PR #85](https://github.com/Texarkanine/SumMem/pull/85) on `multistore`.

## REQUIREMENTS

- Catalog lines `N: ./path` with a single space after the colon and no digit padding
- `N` from filenames: loose note +1; nap stem adds encoded leaf count once (`.tree` and `.summ` share a stem)
- Empty started stores print `0:`
- One `git ls-files` scan; no `list_view`/`heal`/`iterdir` of stores; do not open `.tree`/`.summ` to count
- Pulls stay document-only
- Catalog how-to must not claim the whole line is a path; do not ship `note --path <catalog>` topic-filing
- `started_stores()` stays `list[Path]` for migrate

## IMPLEMENTATION

Level 2. `_listed_store_counts` (first named `_listed_store_grains`) walks one `git ls-files -z --cached --others --exclude-standard`. Nested discovery is `/.summem/` via `_store_file_parts`; root membership stays `is_store` only. Notes/naps share one flat-file check (`partition`, no nested path, no `"."` leftover). `catalog_text` reads that dict once and emits `N: ./rel`. Listed paths gone from the worktree do not add (`(root / rel).is_file()`), so committed notes `nap` unlinked no longer double-count until `git add -u`.

Post-reflect: how-to dropped the `./` token sentence, calls `N` a count, and teaches `note --path <file>` walk-up (same `--path` on nap, recall, zoom). Usage nap line is sequencing only; `Saved.` owns the ACK. Persistent briefings were sectioned (invoke, entry, ACK).

- [`summem`](../../../summem) — `_listed_store_counts`, `catalog_text`, `how_to_text`
- [`tests/test_scopes.py`](../../../tests/test_scopes.py) — `0:` / `1:` / folded `2:` / no padding / no `list_view` / cached-unlinked skip
- [`tests/test_init.py`](../../../tests/test_init.py) — catalog how-to and nap Usage leftover pins
- [`docs/architecture/index.md`](../../../docs/architecture/index.md), [`memory-bank/systemPatterns.md`](../../systemPatterns.md), [`productContext.md`](../../productContext.md), [`techContext.md`](../../techContext.md)

## TESTING

TDD per unit. Catching tests red on missing `N:` lines, then green. `assert "./pkg" in lines` is an exact line, not a suffix — retargeted to `1: ./pkg`. Preflight: PASS WITH ADVISORY (opt-in grain-sorted catalog not built). `/niko-qa`: PASS (build-phase helper name `_listed_store_grains`). Cursor review: cached unlinked notes overcounted; catching test `test_catalog_skips_cached_notes_nap_unlinked` red then green. `tox -e py311`: 394 passed after the worktree skip (`tox run-parallel` py311–py314, 393 passed on the catalog commits).

## LESSONS LEARNED

- Nested-store discovery keys on `/.summem/`. Root-relative `.summem/` is a different path shape; unifying them listed a phantom root after `rmtree`.
- `in lines` is not a suffix check. A plan that says “substring still matches” must name `in out` vs `in lines`.
- A catalog that is only a pull list stays empty if agents always `note` from the git root. File-walk `--path` is how nested stores get content.
- The fold catalog test that never commits cannot see `--cached` ghosts. `N` as a note count needs a worktree existence check on listed names, not a second store walk.
- `Saved.` owns the note ACK. Usage only needs “if `note` asks for a nap, do that nap before your next action.”

## PROCESS IMPROVEMENTS

QA ran on the build-phase name `_listed_store_grains`. Post-reflect rename and review fix landed after QA; archive must cover them, not pretend the reflect snapshot was the ship.

## TECHNICAL IMPROVEMENTS

Preflight advisory still stands: an opt-in grain-sorted catalog could use the count without loading child stores. Not in this task.

This is the original `store_stats` count living inside the listing wake already paid for, with the #10 “not a command” catalog shape.

## NEXT STEPS

- Draft PR #85: review and squash-merge
- Preflight advisory: grain-sorted catalog (follow-up)
- `/niko` for the next task
