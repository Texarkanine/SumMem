# Task: multi-store-filing

* Task ID: multi-store-filing
* Complexity: Level 2
* Type: simple enhancement

Require an explicit `--root` or `--path` store flag on `note`, `nap`, `zoom`, `recall`, and `surgery.py`, format every printed path (`Saved to`, `Run:`, catalog, `start`) relative to the git root with forward slashes, hide empty (`0`-count) child stores from the root-wake catalog while teaching `--root` and `--path` on every root wake, make `-h`/`--help`/`help` unconditionally safe and side-effect-free, and update `prompt_text()`, `how_to_text()`, `usage_text()`, `AGENTS.md`, and `docs/` ([Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103)).

## Test Plan (TDD)

### Behaviors to Verify

- Help anywhere before `--`: `main(["note", "--help"])`, `main(["note", "--root", "x", "--help"])`, `main(["-h"])`, `main(["--help"])`, `main(["help"])`, `main(["help", "note"])`, and `main(["help", "start"])` → print `usage_text()` to stdout, write nothing to stderr, exit `0`, import no command-only modules (`argparse`, `tomllib`, `fcntl`, `subprocess`), take no lock, create no directories, and write no files (`FR-7`, `NFR-4`).
- Literal help text preserved: `main(["note", "--root", "help"])` records `"help\n"`, and `main(["note", "--root", "--", "--help"])` records `"--help\n"` (`FR-7`).
- Operator help catalog (`usage_text()`): `main(["-h"])` / `usage_text()` → lists `(--root | --path FILE)` on `note`, `(--root | --path STORE)` on `nap`/`zoom`/`recall`, `[--path PATH]` on `wake`, omits `<command> -h` and `$PWD` default prose, and contains no `git`, `notes/`, or `naps/` (`FR-10`).
- Missing store flag rejected: `note "x"`, `nap <a> <b> "c"`, `zoom <id>`, and `recall <pat>` with neither `--root` nor `--path` → exit `2`, write one non-empty line to stderr mentioning `--root` and `--path`, and write/create no store files (`FR-1`, `FR-3`, `NFR-5`, `NFR-7`).
- Both store flags rejected: `note`, `nap`, `zoom`, and `recall` given both `--root` and `--path <p>` → exit `2`, write one non-empty line to stderr, and write/create no store files (`FR-1`, `C-3`).
- Unchanged non-store/wake option sets: `wake --root`, `start --root pkg`, `init --root`, and `version --root` → exit `2` (`FR-2`, `C-6`); bare `wake` and `wake --path <dir>` continue working as today (`FR-2`).
- `--root` from subdirectory: `note --root "x"` run from a nested subdirectory (including inside a started child store) → writes to the git-root `.summem/notes/`, leaves the child store untouched, and prints ``Saved to `./.summem` `` (`FR-1`, `FR-4`).
- `--path` walk-up and `Saved to` line: `note --path packages/cli/src/index.ts "x"` when `packages/cli` is started → writes to `./packages/cli/.summem` and prints ``Saved to `./packages/cli/.summem` ``; when run from `packages/cli/src` as `note --path index.ts "x"`, prints the identical root-relative ``Saved to `./packages/cli/.summem` ``; when no child store sits above `--path`, writes to `./.summem` and creates no child store (`FR-1`, `FR-4`, `FR-5`, `C-1`, `NFR-6`).
- `nap` `Saved to` line: `nap` on a valid pair and `nap` on an already-folded pair → both print ``Saved to `<store>` `` before the next fold request or `Nothing left to compress.` (`FR-4`).
- Root-relative `Run:` line: `fold_request` after `note --path foo/bar/baz/fee.c "…"` (including when `$PWD` is inside `foo/bar/baz`) → prints `Run: <invoke> nap --path foo/bar/baz <id-a> <id-b> "<your line>"` which runs unchanged from the git root; for the root store (from any `$PWD`), prints `Run: <invoke> nap --root <id-a> <id-b> "<your line>"` (`FR-5`).
- Root-relative `start` output: running `start cli` and `start missing` from `cwd = repo/packages` → prints `There is a store in ./packages/cli.` and `not a directory: ./packages/missing` relative to the git root (`FR-2`, `FR-5`, `NFR-6`).
- Single-store uncut `recall`: `recall --root <pat>` and `recall --path <store> <pat>` search only that target store, and matching all notes in a store larger than `WAKE_LINES` prints every matching note without cutting (`FR-3`, `NFR-3`, `C-7`).
- `surgery.py` mandatory store flag and fold request: `surgery.py` with neither `--root` nor `--path`, or with both, → exits `2` and deletes nothing; with `--root` (including from a subdirectory) or `--path`, excises the target note and, when over budget, prints a `Run:` line carrying `--root` or root-relative `--path <store>` (`FR-11`).
- Catalog hides empty child stores: root `wake` omits started child stores whose count is `0` and omits `== Additional SumMem Catalogs ==` when all child stores are empty, while `started_stores(repo)` still includes empty started stores (`FR-6`, `C-2`).
- Unconditional Usage flags, prompt store sentence, read-wake-whole, and `AGENTS.md` lockstep: `how_to_text()` (both `catalog=False` and `catalog=True`) teaches `--root`, `--path`, and reading wake to the end without `head`/`tail`/pager; `prompt_text()` includes the read-wake-whole sentence and the store-choice sentence without command flags; `AGENTS.md` starts with `prompt_text()` (`FR-6`, `FR-8`, `FR-9`, `FR-10`).

### Test Infrastructure

- Framework: `pytest` (with `pytest-xdist`) orchestrated by `tox` (`tox -e py311` for iteration, `tox run-parallel` across `py311`–`py314` for final verification).
- Test location: `tests/` (`pytest.ini` `testpaths = tests`).
- Conventions: Function-based `test_*` cases using `tmp_path`, `monkeypatch`, `capsys`, the session `summem` module fixture (`conftest.py`), `load_surgery()` (`test_surgery.py`), and `init_repo` / helpers in `tests/gitutil.py`. Error tests assert exit codes and store non-mutation without pinning prose wording (`NFR-7`).
- New test files: none (all new cases belong in existing suites `tests/test_cli.py`, `tests/test_scopes.py`, `tests/test_fold.py`, `tests/test_recall.py`, `tests/test_init.py`, and `tests/test_surgery.py`).

## Implementation Plan

### 1. Side-Effect-Free Help Interception and `usage_text()` — executable [DONE]

- Files: `summem`, `tests/test_cli.py`, `tests/test_init.py`, `tests/test_version.py`

1. Stub tests: Add empty test functions in `tests/test_cli.py` for `note --help`, `note --root "x" --help`, `help <subcommand>`, and store/lock non-mutation on help requests (`test_subcommand_help_prints_root_usage_without_touching_store`).
2. Stub interface: No new public signature needed (`usage_text()` and `main()` already exist in `summem`).
3. Write tests and run red: Implement `test_subcommand_help_prints_root_usage_without_touching_store` (verifying `note --help`, `note --root "x" --help`, `-h`, `help`, `help note`, `help start` all print `usage_text()` on stdout, exit `0`, import no command-only modules via `_fresh_imported`, create no `.summem` dir or runtime lock file, and write no notes) and update existing per-subcommand help / `usage_text()` tests in `tests/test_cli.py` (`test_help_flag_prints_catalog`, `test_catalog_does_not_list_the_help_command`, `test_help_note_matches_note_help_flag`, `test_help_start_prints_help_and_creates_nothing`, `test_help_before_command_prints_command_help`, `test_command_help_still_shows_path`, `test_start_help_omits_path`), `tests/test_init.py` (`test_init_rejects_path_flag`, `test_help_before_init_prints_init_help`), and `tests/test_version.py` (`test_version_rejects_path_flag`, `test_help_before_version_prints_version_help`) to expect root `usage_text()` with `(--root | --path ...)` and without `<command> -h` or `$PWD`. Run `tox -e py311 -- tests/test_cli.py tests/test_init.py tests/test_version.py` and confirm red.
4. Write code and run green: Update `usage_text()` in `summem` to show `(--root | --path FILE)` on `note`, `(--root | --path STORE)` on `nap`/`zoom`/`recall`, drop `For a command's options: summem <command> -h`, and replace the `$PWD` footer; update `main()` in `summem` to scan tokens before `"--"` for `"-h"` or `"--help"` (plus `args_list[0] == "help"`), writing `usage_text()` to stdout and returning `0` before `import argparse`, and remove unused `_COMMANDS`. Run `tox -e py311 -- tests/test_cli.py tests/test_init.py tests/test_version.py tests/test_nap_reject.py` and confirm green.

### 2. Mandatory `--root` / `--path` Flags and Root-Relative Paths in `summem` — executable [DONE]

- Files: `summem`, `tests/gitutil.py`, `tests/test_cli.py`, `tests/test_scopes.py`, `tests/test_fold.py`, `tests/test_recall.py`, `tests/test_zipper.py`, `tests/test_nap_reject.py`, `tests/test_path_walkup_and_catalog.py`, `tests/test_caption_conflict.py`, `tests/test_worktree_note_merge.py`, `tests/test_nap_variants.py`

1. Stub tests: Add empty test functions in `tests/test_cli.py` (`test_store_commands_require_root_or_path_flag`, `test_store_commands_reject_both_root_and_path`, `test_wake_start_init_version_reject_root_flag`), `tests/test_scopes.py` (`test_note_root_from_subdir_writes_git_root_store`, `test_saved_to_and_start_paths_are_root_relative_from_subdir`), `tests/test_fold.py` (`test_fold_request_run_line_names_store_dir_or_root_from_any_cwd`), and `tests/test_recall.py` (`test_recall_prints_all_matches_uncut_above_wake_budget`).
2. Stub interface: Add stubbed helpers `_store_flag_error(cmd: str) -> str`, `_root_path(path: Path, root: Path | None = None) -> str`, and `_fold_store_flag(parent) -> str` (replacing `_cli_path` and `_fold_path_flag`) in `summem` with docstrings and `raise NotImplementedError`.
3. Write tests and run red: Fill in the new test functions (asserting exit code `2` and zero writes on missing/both store flags without pinning prose beyond `--root`/`--path`, ``Saved to `<store>` `` on `note`, `nap`, and already-folded `nap`, root-relative `start` and `Run:` output from subdirectories, and uncut single-store `recall`), and update existing CLI invocations and `Saved.` / `Run:` assertions across `tests/gitutil.py`, `tests/test_cli.py`, `tests/test_scopes.py`, `tests/test_fold.py`, `tests/test_recall.py`, `tests/test_zipper.py`, `tests/test_nap_reject.py`, `tests/test_path_walkup_and_catalog.py`, `tests/test_caption_conflict.py`, `tests/test_worktree_note_merge.py`, and `tests/test_nap_variants.py`. Run those test suites under `tox -e py311` and confirm red.
4. Write code and run green: Implement `_store_flag_error`, `_root_path`, and `_fold_store_flag` in `summem`; add `--root` (`action="store_true"`) to `note`, `nap`, `zoom`, and `recall` subparsers; enforce `args.root != (args.path is not None)` with exit `2` before resolving the store; resolve `--root` via `find_store_parent(Path.cwd())` and `--path` via `resolve_parent(Path.cwd(), args.path)`; update `start` to format paths with `_root_path`; update `note` and `nap` to print ``Saved to `{_root_path(Path(parent) / '.summem', root)}`\n``; and update `fold_request` to use `_fold_store_flag(parent)`. Run all modified test files under `tox -e py311` and confirm green.

### 3. Mandatory `--root` / `--path` and FR-5 Fold Requests in `surgery.py` — executable

- Files: `surgery.py`, `tests/test_surgery.py`

1. Stub tests: Add empty test functions in `tests/test_surgery.py` (`test_main_requires_root_or_path_flag`, `test_main_rejects_both_root_and_path`, `test_main_root_from_subdir_excises_root_store`, `test_main_subdir_path_fold_request_is_root_relative`).
2. Stub interface: No new public function signatures in `surgery.py` (`main(argv)` and `_usage()` already exist).
3. Write tests and run red: Implement the new `surgery.py` tests (checking exit `2` and unchanged store bytes when neither or both store flags are passed, `--root` excision from inside a started child directory, and root-relative `Run:` fold output from a subdirectory) and update existing `s.main(...)` calls and `f"nap --root {pa} {pb} "` assertion in `tests/test_surgery.py`. Run `tox -e py311 -- tests/test_surgery.py` and confirm red.
4. Write code and run green: Add `--root` (`action="store_true"`) to `surgery.py`'s `ArgumentParser` and update `_usage()`; check `args.root == (args.path is not None)` after `parse_args`, writing `m._store_flag_error("surgery")` to `sys.stderr` and returning `2`; resolve `parent` via `m.find_store_parent(Path.cwd())` for `--root` and `m.resolve_parent(Path.cwd(), args.path)` for `--path`. Run `tox -e py311 -- tests/test_surgery.py` and confirm green.

### 4. Non-Empty Catalog Filtering, `how_to_text()`, `prompt_text()`, and `AGENTS.md` Lockstep — executable

- Files: `summem`, `AGENTS.md`, `tests/test_scopes.py`, `tests/test_init.py`

1. Stub tests: Add empty test functions in `tests/test_scopes.py` (`test_catalog_omits_empty_child_stores_and_header_when_none_remain`) and `tests/test_init.py` (`test_prompt_text_names_nearest_store_and_read_wake_whole`, `test_how_to_text_always_explains_root_path_and_read_wake_whole`).
2. Stub interface: No new function signatures (`catalog_text`, `how_to_text`, and `prompt_text` keep their signatures in `summem`).
3. Write tests and run red: Implement the new tests in `tests/test_scopes.py` and `tests/test_init.py`, and update existing catalog/how-to tests in `tests/test_scopes.py` (`test_empty_root_omits_project_root_header`, `test_catalog_empty_store_prints_zero` → `test_catalog_hides_zero_count_child_store`, `test_catalog_does_not_pad_count_width`, `test_gitignore_store_omitted_from_catalog`, `test_catalog_does_not_os_walk`, `test_catalog_requires_config_toml_sentinel`) and `tests/test_init.py` (`test_how_to_text_catalog_is_opt_in`) for FR-6, FR-8, and FR-9. Run `tox -e py311 -- tests/test_scopes.py tests/test_init.py` and confirm red.
4. Write code and run green: Filter `count > 0` in `catalog_text()` (leaving `_listed_store_counts` and `started_stores` intact per `C-2`); update `how_to_text()` so base text always explains `--path <file>` / `--path <store>`, `--root`, and reading wake output to the end without `head`/`tail`/pager while `catalog=True` still appends catalog-line and `wake --path <path>` pull guidance; update `prompt_text()` with the read-wake-whole sentence and the store-choice sentence; update the top of `AGENTS.md` to match `prompt_text()`. Run full `tox -e py311` and confirm green.

### 5. Documentation Site, `README.md` Verification, and Memory Bank Briefing Updates — prose/policy

- Files: `docs/user-guide/commands.md`, `docs/user-guide/stores.md`, `docs/user-guide/upgrading.md`, `docs/user-guide/quickstart.md`, `docs/user-guide/what-to-remember.md`, `docs/user-guide/index.md`, `docs/user-guide/troubleshooting.md`, `docs/how-it-works/index.md`, `docs/how-it-works/no-conflicts.md`, `docs/how-it-works/why-memories-converge.md`, `docs/advanced/surgery.md`, `docs/architecture/store.md`, `docs/architecture/wake.md`, `docs/architecture/merges-and-healing.md`, `README.md`, `memory-bank/productContext.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Update `docs/user-guide/commands.md`, `docs/user-guide/stores.md`, `docs/user-guide/quickstart.md`, `docs/user-guide/what-to-remember.md`, `docs/user-guide/index.md`, and `docs/user-guide/troubleshooting.md` for mandatory `--root` / `--path`, ``Saved to `<store>` ``, root-relative paths, unconditional root-wake `--root`/`--path` how-to, hiding `0`-count stores from the catalog, dropping `<command> -h`, and adding the missing-store-flag error row.
2. Update `docs/user-guide/upgrading.md` with breaking-change upgrade guidance for mandatory `--root` / `--path` flags (`C-5`).
3. Update `docs/how-it-works/index.md`, `docs/how-it-works/no-conflicts.md`, `docs/how-it-works/why-memories-converge.md`, `docs/advanced/surgery.md`, `docs/architecture/store.md`, `docs/architecture/wake.md`, and `docs/architecture/merges-and-healing.md` so all CLI examples, `Saved to` outputs, `surgery.py` usage, and architectural invariants match the new behavior. Confirm `README.md` contains no outdated invocations.
4. Apply surgical updates to invalidated sentences in `memory-bank/productContext.md` and `memory-bank/systemPatterns.md` (`Saved.` → `Saved to`, mandatory `--root` or `--path`, root-relative printed paths, `<command> -h` dropped, catalog omits `0`-count child stores).
5. Run `uv sync --group docs --frozen --no-config` (if needed) and `uv run --no-config properdocs build --strict`, plus `tox run-parallel` (`py311`–`py314`), to verify zero warnings and full matrix pass.

## Technology Validation

No new technology - validation not required (Python 3.11+ standard library only per `NFR-2`; existing `tox` and `properdocs` toolchains).

## Dependencies

- Unit 2 depends on Unit 1 (`main()` help short-circuit and `usage_text()`).
- Unit 3 (`surgery.py`) depends on Unit 2 (`_store_flag_error` and `_fold_store_flag` / `fold_request` in `summem`).
- Unit 4 (`catalog_text`, `how_to_text`, `prompt_text`, `AGENTS.md`) builds cleanly on Unit 2's CLI behavior in `tests/test_scopes.py`.
- Unit 5 (documentation and final matrix verification) runs after all executable units are green.

## Challenges & Mitigations

- Existing CLI test blast radius across 12 test files: Over 60 existing CLI calls invoke `note`, `nap`, `zoom`, `recall`, or `surgery.py` without `--root`, or assert `"Saved.\n"` / `r" nap (\S+) (\S+)"`. Mitigated by enumerating every affected file and regex (`_FOLD_RUN` in `tests/gitutil.py`, `_RUN` in `tests/test_fold.py`, `test_zipper.py:290`, `test_surgery.py:414`) up front and migrating them inside Units 2 and 3.
- Preserving lazy imports on help requests (`test_help_skips_command_only_imports`): Routing `-h`/`--help` through `argparse` would import `argparse` and fail `_fresh_imported(["-h"])` or execute subcommand validation first. Mitigated by scanning tokens before `"--"` at the top of `main()` prior to `import argparse`, keeping zero command-only imports and zero store/lock side effects (`NFR-4`).
- Keeping `migrate.py` and `wake` working unchanged (`Out of scope`, `FR-2`, `C-2`): Changing `resolve_parent(cwd, path_arg=None)` or `started_stores(git_root)` would break `migrate.py` or bare `wake`. Mitigated by keeping `resolve_parent` and `_listed_store_counts` / `started_stores` intact, enforcing `--root` / `--path` at the CLI boundary, and filtering `count > 0` only inside `catalog_text()`.
- Forbidden words in CLI output and Mermaid sequence labels: Existing tests forbid `"git"`, `"notes/"`, and `"naps/"` in CLI stderr/usage, and Mermaid sequence diagrams break on quotes/parens in labels. Mitigated by saying `"project"` / `"repository"` instead of `"git"` in CLI messages and keeping Mermaid sequence labels plain (`Saved to store`).

## Pre-Mortem

- Subtle output formatting mismatch on `Saved to` or `Run:` (e.g., trailing period vs backticks, `./` prefix on `Run: --path`): Checked all four examples and Acceptance Criteria 4, 8, and 9 in #103 verbatim — `Saved to` wraps the `./`-prefixed `.summem` path in backticks with no trailing period (``Saved to `./packages/cli/.summem` `` and ``Saved to `./.summem` ``), whereas `Run:` uses `nap --root` or `nap --path foo/bar/baz` (store parent relative to git root without `./` or `.summem`). Pinning these exact shapes in Unit 2 tests prevents drift.
- Existing catalog tests in `tests/test_scopes.py` silently breaking when `0:` child stores are hidden: Five tests in `test_scopes.py` (`test_empty_root_omits_project_root_header`, `test_catalog_empty_store_prints_zero`, `test_catalog_does_not_pad_count_width`, `test_gitignore_store_omitted_from_catalog`, `test_catalog_does_not_os_walk`, `test_catalog_requires_config_toml_sentinel`) relied on `start pkg` appearing in root `wake` with `0` notes. Identified all of them during planning and scheduled their exact updates in Unit 4.
- ProperDocs strict build failing on renamed headings in `docs/user-guide/commands.md`: Other docs pages may link to anchors in `commands.md` or `stores.md`. Mitigated by checking incoming links before renaming headings and running `uv run --no-config properdocs build --strict` in Unit 5.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
