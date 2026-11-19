# Project Brief

Reference: [Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103)

## User Story

As a repository operator whose agents use SumMem across root and child directory stores, I want every command that targets one store (`note`, `nap`, `zoom`, `recall`, and `surgery.py`) to require an explicit `--root` or `--path` store flag, print root-relative paths, hide empty child stores from the root-wake catalog, and treat help requests as side-effect-free so that agents actively choose the store nearest the code they are working on instead of defaulting everything into the root store.

## Use-Case(s)

### Filing and Fold Follow-Ups

An agent records a note with `--path <file>` or `--root`. SumMem prints ``Saved to `<store>` `` using a root-relative `./.../ .summem` path so the agent sees immediately where the note landed, and any subsequent fold request prints a `Run:` command carrying `--root` or `--path <store-dir>` relative to the git root so it runs unchanged from the root turns later.

### Querying and Emergency Excision

An agent runs `recall` or `zoom`, or an operator runs `surgery.py`, passing either `--root` or `--path`. Omitting both or passing both exits 2 with a self-explaining one-line stderr message and mutates nothing.

### Session Wake and Safe Help

At session start, bare `wake` prints Usage (always explaining `--root`, `--path`, and reading wake whole without `head`/`tail`/pager), lists only non-empty child stores in the catalog (omitting the catalog section if none have notes), and prints root memories. Passing `-h` or `--help` anywhere in `argv`, or `help` as the first word, prints top-level `usage_text()` to stdout and exits 0 without taking locks, creating directories, or writing files.

## Requirements

1. **FR-1 (Store flag):** `note`, `nap`, `zoom`, and `recall` each require concrete selection of one store via `--root` (git-root store from any directory) or `--path PATH` (nearest store at or above `PATH` via walk-up). If neither or both are given, write nothing, print one self-explaining line to stderr (`--path <file>` on `note`; `--path <store>` on `nap`, `zoom`, `recall`), and exit 2.
2. **FR-2 (Unchanged commands):** Bare `wake`, `wake --path`, `start`, `init`, and `version` keep their existing command forms, except `start`'s printed path is relative to the git root per FR-5.
3. **FR-3 (Recall flag):** `recall` searches one store as today and requires `--root` or `--path`. Multi-store recall is out of scope.
4. **FR-4 (Saved line):** `note` and `nap` print ``Saved to `<store>` `` (e.g. ``Saved to `./packages/cli/.summem` ``, or ``Saved to `./.summem` `` for root) instead of `Saved.`, including when `nap` is called on an already-folded pair. Fold requests still print after this line.
5. **FR-5 (Root-relative printed paths and runnable `Run:`):** Input paths (`--path`, `start <dir>`) resolve relative to `$PWD`. Every path SumMem prints (`Saved to`, `Run:`, catalog, `start`) is relative to the git root with forward slashes, never `$PWD`. A fold request's `Run:` line always carries `--root` for the root store or `--path <store-dir>` (root-relative, without leading `./` per spec example `nap --path foo/bar/baz` or root-relative path runnable from root) naming the store parent directory, never the file.
6. **FR-6 (Catalog hides empty stores):** Root wake omits child stores whose count is `0`, and omits `== Additional SumMem Catalogs ==` when no non-empty child store remains. Root-wake Usage (`how_to_text`) explains `--root` and `--path` on every root wake regardless of whether a catalog is printed.
7. **FR-7 (Help):** If `-h` or `--help` appears anywhere in `argv`, or `help` is the first word, print `usage_text()` to stdout, exit 0, and record nothing. All other arguments follow `argparse` rules.
8. **FR-8 (Init prompt store rule):** `prompt_text()` gains one sentence naming the store choice without command syntax (record each note in the store nearest the code it is about; use the root store only when it applies to the whole project).
9. **FR-9 (Read wake whole):** Both `how_to_text()` and `prompt_text()` gain one sentence instructing agents to read wake output to the end and never pipe it through `head`, `tail`, or a pager.
10. **FR-10 (Text surfaces):** Update `usage_text()` (drop `<command> -h` line and rewrite the `--path` / `$PWD` prose), `how_to_text()`, `prompt_text()`, repo `AGENTS.md`, `README.md`, and `docs/` (including `Saved.` ACK references, `docs/user-guide/commands.md`, and `docs/user-guide/upgrading.md`).
11. **FR-11 (`surgery.py`):** Require concrete `--root` or `--path` on `surgery.py` (neither or both exits 2 with FR-1 error and deletes nothing). Its fold request follows FR-5, and it remains compatible with driver internals.
12. **NFR-1 to NFR-7:** Fewest lines and no unneeded work in `summem`; stdlib only on Python 3.11+; single-store `recall` cost unchanged; help takes no lock and creates/writes nothing; self-explaining missing-store error; forward-slash root-relative output with no `os.name` checks; `tox` green across `py311`–`py314` without pinning error wording beyond `AGENTS.md` lockstep.

## Constraints

1. **C-1:** `--path` never creates a child store; if no child store sits at or above `PATH`, walk-up resolves to the git-root store. Only `start` creates a child store.
2. **C-2:** Walk-up mechanics and the set of stores scanned for the catalog do not change (only `0`-count stores are filtered from catalog display).
3. **C-3:** Exit codes keep their meaning: `2` for usage errors, `1` for validation errors.
4. **C-5:** Breaking change released as `feat!:`, with upgrade instructions in `docs/user-guide/upgrading.md`.
5. **C-6:** Write the least code that meets the requirements; add no option not named in the requirements.
6. **C-7:** `recall` output is never truncated.
7. **Out of scope:** Moving existing notes out of root store, multi-store `recall`, per-command help pages, and changing `migrate.py`'s `--path` filter.

## Acceptance Criteria

1. `note "x"` with no store flag exits 2, prints an error to stderr, and writes no file; the same holds for `nap`, `zoom`, and `recall`.
2. `note --root --path a "x"` exits 2 and writes no file (and likewise for `nap`, `zoom`, `recall`).
3. `note --root "x"`, run from any subdirectory, writes to the git-root store.
4. `note --path packages/cli/src/index.ts "x"` writes to `./packages/cli/.summem` and prints ``Saved to `./packages/cli/.summem` ``.
5. `note --path` on a file with no child store above it writes to the root store and creates no new child store.
6. Bare `wake` and `wake --path` behave as today apart from FR-6 (hiding `0`-count stores and unconditional `--root`/`--path` how-to) and FR-9 (read wake whole).
7. `recall --root PATTERN` and `recall --path packages/cli PATTERN` search that one store.
8. `nap` prints the same ``Saved to `…` `` line as `note`, including for an already-folded pair.
9. After `note --path foo/bar/baz/fee.c`, a fold request's `Run:` line says `nap --path foo/bar/baz ...` and runs unchanged from the git root; for the root store it says `nap --root ...`.
10. Run from a subdirectory, `note`, `nap`, the `Run:` line, and `start` print paths relative to the git root, not `$PWD`.
11. `surgery.py` with no store flag or with both exits 2 and deletes nothing; with one flag it works as today and its fold request follows FR-5.
12. `recall` matching every note in a store prints every note without cutting.
13. Root `wake` omits child stores with count `0` and omits `== Additional SumMem Catalogs ==` when none remain, while Usage still explains `--root` and `--path`.
14. `note --help`, `note --root "x" --help`, `-h`, and `help` all print root `usage_text()` to stdout, exit 0, and leave the store unchanged with no lock file and no new directories.
15. `usage_text()`, `how_to_text()`, `prompt_text()`, `AGENTS.md`, `README.md`, and `docs/` match the new rules, and `AGENTS.md` locksteps with `prompt_text()`.
16. `tox run-parallel` passes on `py311`–`py314`.
17. Commit/PR uses `feat!:` and `docs/user-guide/upgrading.md` documents the new required flags.
