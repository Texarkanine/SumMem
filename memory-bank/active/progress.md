# Progress

Require an explicit `--root` or `--path` store flag on `note`, `nap`, `zoom`, `recall`, and `surgery.py`, format all printed paths relative to the git root, hide empty child stores from root-wake catalogs, make `-h`/`--help`/`help` unconditionally side-effect-free, and update prompt, `AGENTS.md`, `README.md`, and docs surfaces ([Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103)).

**Complexity:** Level 2

## 2026-11-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Read persistent memory bank (`productContext.md`, `systemPatterns.md`, `techContext.md`) and [Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103).
    - Confirmed intent restatement with operator (including opening a draft PR when done).
    - Assessed scope across `summem`, `surgery.py`, `tests/`, `AGENTS.md`, `README.md`, and `docs/`, classifying as Level 2.
* Decisions made
    - Classified as Level 2 because #103 settles every CLI, output, help, and error requirement without touching store layout, payload schema, or CRDT folding/healing rules.
* Insights
    - `migrate.py` calls `resolve_parent(Path.cwd(), args.path)` directly with `args.path=None` meaning `$PWD`/`git_root` scan when `--path` is passed; keeping `resolve_parent` backward-compatible for `wake` and `migrate.py` avoids breaking out-of-scope callers.

## 2026-11-19 - PLAN - COMPLETE

* Work completed
    - Mapped all CLI, path-formatting, catalog, prompt/how-to/usage, test, and ProperDocs surfaces affected by #103.
    - Created complete Level 2 TDD implementation plan in `memory-bank/active/tasks.md` covering 15 behavioral assertions across 4 executable units plus 1 prose/policy documentation unit.
* Decisions made
    - Intercept `-h` and `--help` before `"--"` (plus leading `help`) at the top of `main()` before `import argparse`, preserving lazy-import and zero-side-effect guarantees (`FR-7`, `NFR-4`) while honoring POSIX `--` (`cli-help-patterns.html`).
    - Keep `resolve_parent` and `_listed_store_counts` / `started_stores` intact for `wake` and `migrate.py` (`FR-2`, `C-2`), enforcing `--root` vs `--path` at the CLI layer in `summem` and `surgery.py`.
    - Sequence `surgery.py` immediately after `summem` store-flag/path changes so `test_surgery.py`'s `fold_request` assertions move in lockstep before catalog/prompt updates.
* Insights
    - `Saved to` uses backticked `./<rel>/.summem` with no trailing period (``Saved to `./packages/cli/.summem` `` and ``Saved to `./.summem` ``), whereas `Run:` uses `nap --root` or `nap --path <rel-store-dir>` without `./` or `.summem`.
    - Six existing tests in `tests/test_scopes.py` relied on `0:` empty child stores appearing in root `wake` and are explicitly scheduled for update in Unit 4.
## 2026-11-19 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the plan against `summem`, `surgery.py`, `migrate.py`, `tests/`, and `docs/`. `.preflight-status` first line: `PASS WITH ADVISORY`.
* Decisions made
    - No in-phase plan edits: no TDD ordering swaps and no whole-step strikes were needed.
* Insights
    - `tests/test_branch_pack_merge.py:94` calls `note` with no store flag and is missing from Unit 2's file list.
    - `prompt_text()` phrase assertions conflict with the `techContext.md` rule that tests do not pin write-rule wording.
    - `start` outside a repository needs the root before it formats `not a directory:`.
    - The root-relative `Run: nap --path <dir>` line resolves against `$PWD` and fails from sibling directories (inherited from #103 FR-5).

## 2026-11-19 - BUILD - COMPLETE

* Work completed
    - Unit 1: Short-circuited `-h` / `--help` before `"--"` (plus leading `help`) at the top of `main()` before `import argparse` with zero command-only imports and zero store/lock side effects; updated `usage_text()`.
    - Unit 2: Enforced mandatory `--root` xor `--path` (`_select_store`) on `note`, `nap`, `zoom`, and `recall`; added `_root_path` and `_fold_store_flag`; updated `note` and `nap` acknowledgements to ``Saved to `<store>` ``; migrated CLI test calls across 13 test files (including `test_branch_pack_merge.py` and `test_middle_orphans.py`).
    - Unit 3: Updated `surgery.py` (`_usage`, `--root`, `m._select_store`) and `tests/test_surgery.py`.
    - Unit 4: Filtered `count > 0` in `catalog_text()` while keeping `started_stores()` intact; updated `how_to_text()`, `prompt_text()`, and `AGENTS.md` in lockstep.
    - Unit 5: Updated all affected `docs/` pages and persistent `memory-bank/` briefings (`productContext.md`, `systemPatterns.md`); verified `properdocs build --strict` (0 warnings) and `tox run-parallel` (`py311`–`py314`, 459 passed).
* Decisions made
    - Shared `_select_store(cwd, root_flag, path_arg, cmd)` between `summem` and `surgery.py` for single-source flag validation and root/walk-up resolution.
    - Kept `_fold_store_flag(parent)` safe for standalone non-git library callers (`test_fold_many_writers.py`) by falling back to `"--root"` when `find_store_parent(parent)` raises `ValueError`.
* Insights
    - `test_catalog_requires_config_toml_sentinel` exercises `config.toml` as the git-visible file sentinel that lets `git ls-files` (`started_stores`) discover empty started directories without `os.walk`, even though `catalog_text()` hides `0`-count child stores.

## 2026-11-19 - QA - COMPLETE (PASS)

* Work completed
    - Semantically reviewed `summem`, `surgery.py`, `AGENTS.md`, the full `tests/` diff, all `docs/` changes, and the persistent memory-bank updates against the Level 2 plan: KISS, DRY, YAGNI, completeness, regression, integrity, and documentation all pass.
    - Wrote `.qa-validation-status` (PASS with three non-blocking advisories) and recorded QA results in `tasks.md`.
* Decisions made
    - Accepted the narrowed FR-8/FR-9 test coverage (command forms pinned, prose unpinned) as the correct application of Preflight advisory 2 and the `techContext.md` no-write-rule-wording rule; the sentences themselves are present in `prompt_text()`, `how_to_text()`, and `AGENTS.md`.
    - Confirmed Preflight advisory 7 was applied: `_select_store` is the single store-selection helper shared by `summem` and `surgery.py`.
* Insights
    - `README.md` needed no edits: it contains no CLI invocations, so FR-10's README surface was already clean.
    - Two informational items ride to the operator with the PASS: the help scan's `--` boundary (FR-7 refinement, pinned by `test_note_double_dash_records_help_flag`) and the `Run: nap --path <dir>` sibling-cwd walk-up limit inherited from #103 FR-5.

## 2026-11-19 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-multi-store-filing.md`.
    - Reconciled persistent files (`productContext.md` and `systemPatterns.md` updated; `techContext.md` skipped — toolchain, lazy-import floor, test runner, and no-wording-pin oracle remain accurate).
    - Recorded durable gotcha/contract note in `.summem/` and completed the requested `nap --root` fold.
* Decisions made
    - Stopped Niko workflow at the Level 2 terminal node (`Reflect -> ManualArchive`) before opening the draft pull request requested by the operator.
* Insights
    - Store-layer functions (`fold_request`) must remain usable on bare non-git `tmp_path` directories (`test_fold_many_writers.py`), while CLI entrypoints enforce `.git` presence.

## 2026-11-19 - REWORK INITIATION - COMPLETE

* Work completed
    - Initiated rework on `multi-store-filing` (current complexity: Level 2) to remediate the SLOBAC test-suite audit findings in `.slobac/2026-11-19T14-31-00/audit.md`.
    - Cleared stale ephemeral state (`tasks.md`, `activeContext.md`, `.qa-validation-status`, `.preflight-status`).
* Decisions made
    - Delete `test_agents_md_starts_with_prompt_text` (Finding 25): the repository's own `AGENTS.md` is operator-owned and need not start with `prompt_text()`; update `memory-bank/techContext.md` accordingly.
    - Keep `tests/test_path_walkup_and_catalog.py` as a child-process binary integration test file alongside in-process `tests/test_scopes.py` (skipping Findings 47 and 49 because in-process unit calls and binary-invoking child-process integration tests walk two distinct layers), and fix Finding 29 (`conditional-logic`) in place; apply the same unit-vs-binary rule to keep `tests/test_nap_reject.py::test_nap_help_exits_zero` as a strengthened child-process `--help` test (Findings 27 and 28) while deduplicating in-process `-h`/`--help` calls across `test_init.py`, `test_version.py`, and `test_cli.py` (Findings 7, 8, 24, 40, 46, 48).
* Insights
    - `.slobac/` is an untracked local audit artifact directory and stays out of git commits.

## 2026-11-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Evaluated rework scope against `.slobac/2026-11-19T14-31-00/audit.md` and classified as Level 2.
    - Created `activeContext.md` and stub `tasks.md` for Level 2 planning.
* Decisions made
    - Kept `**Complexity:** Level 2`: all changes are test-suite remediations and test-file splits with zero product CLI or store-engine changes.
* Insights
    - Since `summem` and `surgery.py` executable behavior is unchanged (`always-tdd.mdc`), test refactoring and test-file reorganization do not alter product behavior; test-only units must still be verified directly against `tox -e py311` so zero assertions or coverage are lost.

## 2026-11-19 - PLAN - COMPLETE

* Work completed
    - Surveyed all 15 audited test files plus `summem`, `surgery.py`, `conftest.py`, and `gitutil.py`.
    - Wrote the Level 2 rework plan in `memory-bank/active/tasks.md` across 5 units (4 test-refactor units + 1 persistent `memory-bank/techContext.md` sync unit), accounting for every one of the 49 SLOBAC findings.
* Decisions made
    - Partition `tests/test_cli.py` (57 tests) into `tests/test_cli_bootstrap.py` (10), `tests/test_cli_help.py` (13), `tests/test_nap.py` (+11), `tests/test_zoom.py` (+4), and `tests/test_cli.py` (17), folding 5 duplicate in-process `-h`/`--help` functions into `test_subcommand_help_prints_root_usage_without_touching_store`.
    - Partition `tests/test_zipper.py` (45 tests) into `tests/test_rematerialize.py` (11), `tests/test_heal_view.py` (16), `tests/test_cli_heal.py` (8), and `tests/test_store_lock.py` (6), promoting shared fixture helpers into `tests/gitutil.py` and deleting 4 over-specified-mock / duplicate tests.
    - Replace raw source-byte offset assertions in `test_version_info_is_checked_before_import_tomllib` with an in-process `SourceFileLoader` execution check under patched `sys.version_info = (3, 10, 0)` and a `builtins.__import__` guard.
* Insights
    - `summem.leaf_digests(node)` already wraps `_as_child(node)` and returns `None` on `(OSError, ValueError)`, cleanly replacing all 4 private `_as_child` assertions in `tests/test_fold.py`.

## 2026-11-19 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the rework plan against `tests/`, `summem`, `surgery.py`, `memory-bank/`, CI config, and the SLOBAC audit. `.preflight-status` first line: `FAIL (fixable)`.
* Decisions made
    - No in-phase plan edits: no TDD ordering swaps and no whole-step strikes were needed.
* Insights
    - Unit 2 step 4 (Finding 17): `out.splitlines()[-2]` is never the remaining-compressions line, so `"compression" not in out.splitlines()[-2]` is vacuous; assert `"compression" not in out` instead.
    - Advisories: retained `note -h`/`start -h` duplicates beside the extended help loop; trivially-green identical-notes `fold_request(repo, 1)`; identical helper copies in `test_surgery.py`/`test_nap.py`/`test_wake_expand.py` after promotion; leftover `_try_fcntl() is None` branch in the store-lock body.
    - Baseline is 459 collected tests; the plan's deletions and one split imply 447 after build.
