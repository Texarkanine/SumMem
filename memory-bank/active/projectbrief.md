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

## Rework

Remediate the SLOBAC test-suite audit findings in `.slobac/2026-11-19T14-31-00/audit.md` across the `tests/` suite touched on `multi-store-filing`:

1. **Naming and fossil cleanup (`naming-lies`, `deliverable-fossils`):** Rename misleading test identifiers (`test_caption_conflict.py`, `test_cli.py`, `test_fold.py`, `test_init.py`, `test_nap_reject.py`, `test_scopes.py`, `test_surgery.py`, `test_version.py`), fold duplicate `init_text` divider assertions in `test_init.py`, and regroup scattered in-process `-h`/`--help` tests into a dedicated CLI help module.
2. **Oracle strengthening and dead-scaffolding removal (`vacuous-assertion`, `rotten-green`):** Replace self-referential `_equal_grain_pair` assertions in `test_fold.py` with real `summem.fold_request` assertions, assert exact stdout/stderr on `test_nap_reject.py::test_nap_help_prints_root_usage`, `test_recall.py`, and `test_surgery.py::test_main_usage_without_target`, verify store invariance in `test_surgery.py::test_main_dry_run_omits_fold_request`, and fix the unread `_host_needs_interpreter` stub in `test_surgery.py::test_main_prints_fold_request_when_over_budget`.
3. **Decoupling and mock cleanup (`over-specified-mock`, `implementation-coupled`, `prose-pin`):** Replace raw source-offset checks in `test_version_info_is_checked_before_import_tomllib` with an execution-based Python <3.11 import guard, replace private `_fold_grains`/`_as_child` calls in `test_fold.py` behavioral tests with public `fold_request`/`leaf_digests`, remove internal interaction-count and `boom` stubs in `test_fold.py`, `test_scopes.py`, and `test_zipper.py` in favor of observable contracts, and delete `test_agents_md_starts_with_prompt_text` (updating `memory-bank/techContext.md` and superseding AC 15's `AGENTS.md` lockstep pin, since the repo's `AGENTS.md` is operator-owned).
4. **Unconditional assertions (`conditional-logic`):** Split `test_shebang_and_executable_bit` using `@pytest.mark.skipif(os.name == "nt", ...)`, mark POSIX `fcntl` contention in `test_with_store_lock_blocks_and_writes_no_lock_file` with `@pytest.mark.skipif(os.name == "nt", ...)`, and drop the dead `else` fallback in `test_path_walkup_and_catalog.py::test_root_wake_lists_other_stores_pull_prints_only_that_store`.
5. **Layering and file modularity (`semantic-redundancy`, `monolithic-test-file`):** Preserve `tests/test_path_walkup_and_catalog.py` (and `tests/test_nap_reject.py`'s `--help` check) as child-process binary integration tests distinct from in-process `m.main(...)` unit suites (declining Findings 47 and 49 while copying `assert ".summem/summem" not in catalog` into `tests/test_scopes.py`), deduplicate in-process `-h`/`--help` calls into `tests/test_cli_help.py` (Findings 46 and 48), and split `tests/test_cli.py` (57 tests) and `tests/test_zipper.py` (45 tests, 1,101 lines) into focused capability modules.
6. **Verification:** No regressions in `summem` or `surgery.py` behavior; `tox run-parallel` passes across `py311`–`py314`.


## Rework 2: single `--path` with git `:/` root anchor + PR #104 review fixes

Design is settled in `memory-bank/active/creative/creative-store-flag-scheme.md` (rules 1-7). Supersedes `--root` everywhere in FR-1, FR-5, FR-11 and AC 1-17 above.

1. **Single store flag:** `--path P` is the only store selector; `--root` is removed with no alias. Required on `note`, `nap`, `zoom`, `recall`, `surgery.py`; optional on `wake` (bare `wake` = `:/`). Missing `--path` exits 2 with one line and mutates nothing.
2. **Git `:/` anchor:** `P` starting with `:/` is root-relative (`:/` alone = root); otherwise `$PWD`-relative; absolute accepted. Walk-up to nearest started store unchanged. Any other leading `:` exits 1 (`unknown path prefix`); a literal colon name is written `./:name`.
3. **Containment in the resolver:** the resolver resolves the path once (symlinks included) and exits 1 with one line if the result is outside the git root (covers `:/../x` and an out-of-repo `.summem` symlink; PR #104 items 3-4). Formatting runs only on checked paths; no symlink-specific code.
4. **Every printed path in `:/` form and pasteable as `--path`:** `Saved to :/packages/cli` (store directory, no `.summem`), `Run: nap --path :/packages/cli …`, catalog `N: :/dogfood`, `start` output.
5. **Shell-quote the `Run:` path** (`shlex.quote`); test with a store path containing a space (PR #104 items 1-2).
6. **One resolver** for `wake --path`, `start <dir>`, `surgery.py --path`, and `migrate.py --path`.
7. **Odd-arity heal test** in `tests/test_heal_view.py` plants partially overlapping naps so it exercises the split branch; keep the iteration cap; assert every leaf reachable and unique cover (PR #104 item 5).
8. **Docs:** `docs/user-guide/commands.md` states that a store command with no `--path` exits 2 before any repository check (PR #104 item 6); all docs, `usage_text()`, `how_to_text()`, `prompt_text()`, `AGENTS.md`, `upgrading.md` describe `--path` and `:/` (examples use `:/`).
9. **Verification:** `tox run-parallel` py311-py314 passes; `properdocs build --strict` clean.

## Rework 3: one formatting rule for every printed path

Operator: `There is a store in :/team docs.` prints poorly (the full stop runs into the path; spaces aren't paste-safe).

1. Every path SumMem prints goes through one formatter: `:/rel` form, then `shlex.quote` (ordinary paths print unchanged; `':/team docs'` when quoting is needed). Applies to `start`, `Saved to`, catalog lines, `Run:`, and resolver errors.
2. Paths inside sentences are wrapped in backticks: `There is a store in `…`.`, `not a directory: `…``, `outside the repository: `…``, `store outside the repository: `…``. `Saved to` already uses backticks. `Run:` and catalog lines stay bare (they are values or commands, not sentences).
3. The round-trip test shell-splits each printed path before passing it back as `--path`.
4. Docs and Usage text show the new forms. `tox run-parallel` passes; `properdocs build --strict` is clean.

## Rework 4: PR #104 review 5985942421

1. Delete the stale loose note `.summem/notes/20261119T200011Z-420729d37491f5ab`; it describes `--root` (operator: notes invalidated on this branch may be deleted).
2. Printed-path quoting also works in PowerShell: typographic single quotes (‘ ’ ‚ ‛) must not end a quoted path.
3. `commands.md`: the `--path` value works from any directory; run the `Run:` line from the repository root (the script path is relative).
4. Nested repositories: no special code. Document that a path inside a nested repository walks up within that repository to its nearest store, and that printed `:/` paths are relative to that repository.
5. Writing: ISO 24495 plain language, Orwell's six rules, the doc site's style, no needless words.

## Rework 5: refuse paths in another repository

Implements `creative/creative-nested-repo-paths.md` (option B). This replaces rework 4's "nested repositories: docs only".

1. The repository of the current directory is the repository. A `--path` or `start` target whose own repository differs is refused with ``not in this repository: `<arg>` `` (exit 1) and nothing is written. This one check also covers `:/../x`.
2. Inside the nested repository, commands work normally.
3. Docs: replace the nested-repository bullet and the outside-repository wording; update the troubleshooting rows.
