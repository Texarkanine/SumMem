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
