# Project Brief

## User Story

As an agent or operator, I want the first SumMem invocation to show every command’s shape (including `--path`) so that I can succeed without guessing that `wake -h` exists.

## Use-Case(s)

### Use-Case 1

Someone runs `.summem/summem` with no arguments. They see a memo-style catalog: one line per command with its arguments, `--path` on every command except `start`, and a short note that `--path` aims at a directory. They can copy a line and run it.

### Use-Case 2

Someone runs `.summem/summem -h wake` (help flag before the command). They get wake’s help, not a reprint of the top-level page. `.summem/summem wake -h` still works.

## Requirements

1. Bare `summem` (missing command) prints a catalog inspired by bare `memo`: invocation, arguments, one-line description. Not argparse’s `{wake,note,…} ...` dead end.
2. Top-level `-h` / `--help` prints that same catalog. `--path` is visible on the lines that take it. `start` does not show `--path`.
3. `summem -h <command>` prints that command’s help. `summem <command> -h` still does.
4. Command help remains the last click for that command’s details.
5. A cross-cutting sentence after the catalog explains `--path` the way bare `memo` explains `--global`: omit it to use `$PWD`; it walks up to the nearest store.

## Constraints

1. Help and usage text only. `start`, walk-up, catalog of stores, note/nap identity, and zoom-as-`HEAD` stay as shipped.
2. The agent interface does not mention store files, hashes as paths, or git (`VISION.md`).
3. Inspiration is bare `~/.optmem/memo`: copy-paste command lines, optional args in brackets, footer for the cross-cutting flag. Do not copy OptMem’s “No such command: -h” — `-h` is help, not an unknown command.
4. First language remains the shebang driver at `.summem/summem`.

## Acceptance Criteria

1. Bare `.summem/summem` exits nonzero and prints a catalog that names every command and shows `--path` on `wake`, `note`, `nap`, `zoom`, and `recall`.
2. `.summem/summem -h` prints that catalog and does not require a command.
3. `.summem/summem -h wake` and `.summem/summem wake -h` both print wake help that includes `--path`.
4. `.summem/summem start -h` does not list `--path`.
5. Existing CLI behavior tests still pass.

## Rework

Fold in: SumMem only makes sense in a repository. Strip the no-repo fallback (`find_store_parent` returning the walk start). `wake`, `note`, `nap`, `zoom`, `recall`, and `start` error when there is no repository. Help (`summem`, `-h`, `<command> -h`) still prints without one — that is the ratchet. Error text says “repository,” not “git,” and does not name store files. Strike VISION’s “or stop at `$PWD` if not in git.”

## Rework

PR #5 review items the operator accepted (judge items 1, 2, 5, 6, 8–11, 13–15, 17–19, 21). Dogfood is a local toy store; the driver lives at repo-root `summem`; root `.summem/` stays reserved. Unknown CLI tokens already fail argparse (`summem "raw invocation…"` → invalid choice); `note` must still be an explicit branch so leftover `cmd` cannot write a note.

1. Point `tests/conftest.py` and `tests/gitutil.py` `SCRIPT` at repo-root `summem`.
2. `recall_text` searches `list_view` captions plus `.tree` originals, not the truncated wake listing.
3. `zoom_text` and `recall_text` catch `_TREE_PARSE_ERRORS` instead of traceback.
4. Fold prompt uses configured `ENTRY_CHARS`, not a hardcoded 280.
5. Tighten `test_write_nap_note_inside_adjacent_nap_raises`; drop unused unpack.
6. Add a recall test for a malformed `.tree`.
7. Make `test_unreadable_tree_does_not_split` deterministic (monkeypatch `read_bytes`).
8. Rename `test_cli_nap_overlapping_ids_exits_0_without_concat` to match exit 1.
9. VISION: `start` is the no-walk-up exception inside a repository; it does not create a store outside one.
10. VISION: remove the “explicit config command”; there is none and there will not be one.
11. VISION: one root auto-create rule; do not leave “first wake or note” vs “first command” disagreeing.
12. Add a reject test for syntactically valid, unknown nap ids.
13. Remove the dead `present` guard after `resolve_id`.
14. `if args.cmd == "note":` then write; any other leftover `cmd` must not write a note.
15. Comment why `repo_a` ids are valid in `repo_b` in the same-children nap test.
