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

## 2026-11-19 - PLAN (REVISION 2) - COMPLETE

* Work completed
    - Updated `memory-bank/active/tasks.md` to fix the vacuous `splitlines()[-2]` assertion in Unit 2 step 4 (`assert "compression" not in out` with `nodes=nodes[1:]`) and fold in all six actionable Preflight advisories.
* Decisions made
    - Fold `test_help_note_matches_note_help_flag` and `test_help_start_prints_help_and_creates_nothing` into `test_subcommand_help_prints_root_usage_without_touching_store` (`test_cli_help.py`: 11 tests; expected post-build collected suite: 445 tests).
    - Pass `wake_lines=0` in `test_fold_request_is_empty_after_healing_identical_notes` so `_fold_pair` runs instead of hitting `len(nodes) <= wake_lines`.
    - Put `COMMAND_ONLY` and `fresh_imported` in `tests/gitutil.py` and point `test_surgery.py` and `test_nap.py` at promoted `gitutil` helpers.
* Insights
    - Passing `nodes=nodes[1:]` (`["b", "c"]`) against an on-disk 3-note store (`"a"`, `"b"`, `"c"`) verifies `nodes=` reuse via two independent observables (`"  a\n" not in out` and `"compression" not in out`).

## 2026-11-19 - PREFLIGHT (REVISION 2) - COMPLETE (FAIL (fixable))

* Work completed
    - Re-validated the revised rework plan against `tests/`, `summem`, `surgery.py`, `docs/`, and the SLOBAC audit. `.preflight-status` first line: `FAIL (fixable)`.
* Decisions made
    - No in-phase plan edits: no TDD ordering swaps and no whole-step strikes were needed.
* Insights
    - Deleting `test_agents_md_starts_with_prompt_text` makes `docs/contributing/index.md` line 24 ("A test checks this.") false; Unit 5 must cover that doc (or the AGENTS.md sync check must move to a non-pytest CI step).
    - Prior Preflight defects are fixed: Finding 17 assertion is no longer vacuous, and the 459 -> 445 count reconciles (14 deletions).
    - Advisories: `_balanced_4` return-shape mismatch between `test_zipper.py` and `test_surgery.py`; `test_wake_expand.py` duplicate `_payload_names`; `test_zipper.py` partition assignment detail; overlapping-pack planting for Finding 33 needs a variant helper.

## 2026-11-19 - PLAN (REVISION 3) - COMPLETE

* Work completed
    - Updated `memory-bank/active/tasks.md` Unit 5 to remove the `AGENTS.md` sync bullet in `docs/contributing/index.md` alongside the `memory-bank/techContext.md` update, and spelled out the remaining helper/partition details in Units 1, 2, and 4.
* Decisions made
    - Remove the `AGENTS.md`-matches-`init` bullet in `docs/contributing/index.md` rather than moving the check to a CI script, matching the operator's ruling that this repository's `AGENTS.md` is operator-owned.
* Insights
    - Searching for `"in step with"` in addition to `"lockstep"` caught the remaining contributor-doc reference to `test_agents_md_starts_with_prompt_text`.


## 2026-11-19 - PREFLIGHT (REVISION 3) - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-validated the Revision 3 rework plan against `tests/`, `summem`, `surgery.py`, `docs/`, `.github/workflows/pr.yaml`, and the SLOBAC audit. `.preflight-status` first line: `PASS WITH ADVISORY`.
* Decisions made
    - No in-phase plan edits: no TDD ordering swaps and no whole-step strikes were needed.
* Insights
    - Confirmed baseline of 459 collected tests and the 459 -> 445 reconciliation (14 deletions); intermediate checkpoints are 458 / 456 / 449 / 445 after Units 1-4.
    - Finding 33's planted overlapping packs must hold valid, heal-eligible trees, or "pairs stay on disk" is vacuous against a `heal_view` call.
    - `fold_balanced`, `plant_abd_abe`, and the heal-only helpers have a single consumer, so promoting them to `gitutil` is not needed.
    - Advisory: a throwaway mutation sweep would show the strengthened tests can actually go red.

## 2026-11-19 - BUILD - COMPLETE

* Work completed
    - Unit 1: Remediated standalone findings across `test_caption_conflict.py`, `test_nap_reject.py` (with `text=True` for cross-platform newline safety), `test_path_walkup_and_catalog.py`, `test_recall.py`, `test_scopes.py` (planting two valid equal-leafset 2-pack variants plus an invalid-UTF-8 loose note for `catalog_text`), and `test_surgery.py`.
    - Unit 2: Replaced `_equal_grain_pair`, `boom` stubs, and private `_fold_grains`/`_as_child` calls in `tests/test_fold.py` with public `fold_request` and `leaf_digests` checks.
    - Unit 3: Cleaned `tests/test_init.py` and `tests/test_version.py`, promoted `COMMAND_ONLY` and `fresh_imported` into `tests/gitutil.py`, and partitioned `tests/test_cli.py` (57 → 17) across `tests/test_cli_bootstrap.py` (10, with execution-based Python <3.11 floor import guard), `tests/test_cli_help.py` (11), `tests/test_nap.py` (+11), and `tests/test_zoom.py` (+4).
    - Unit 4: Promoted shared multi-consumer helpers (`write_notes`, `payload_names`, `plant_nap`, `balanced_4`) into `tests/gitutil.py`, deduplicated `test_surgery.py`, `test_nap.py`, and `test_wake_expand.py`, partitioned `tests/test_zipper.py` (45) into `tests/test_rematerialize.py` (11), `tests/test_heal_view.py` (16), `tests/test_cli_heal.py` (8), and `tests/test_store_lock.py` (6), and deleted `tests/test_zipper.py`.
    - Unit 5: Removed the false `AGENTS.md` sync bullet in `docs/contributing/index.md`, updated `memory-bank/techContext.md`, and ran `uv run --no-config properdocs build --strict` (0 warnings) and `uvx --with tox tox run-parallel` (`py311`–`py314`, 445 passed per environment).
* Decisions made
    - Used Finding 38's first prescribed remediation in `tests/test_surgery.py::test_main_prints_fold_request_when_over_budget` (deleting the unread `_host_needs_interpreter` monkeypatch and asserting `f"Run: {m.agent_invoke()} nap " in out`) because `tests/test_summem_fixture.py` forbids `"load_summem"` in `tests/test_*.py`.
    - Kept single-consumer helpers (`_fold_balanced`, `_plant_abd_abe`, `_plant_variant`, `_block_naps_dir_open`) local to their capability modules per Preflight Advisory 2.
* Insights
    - Full-suite verification caught the `test_summem_fixture.py` lexical check on `"load_summem"` across `py311`–`py314` and confirmed the exact 445-test reconciliation (`459 − 14 = 445`).


## 2026-11-19 - QA - COMPLETE (PASS)

* Work completed
    - Semantically reviewed the rework diff (`tests/`, `docs/contributing/index.md`, `memory-bank/techContext.md`) against the Level 2 plan; confirmed `summem`, `surgery.py`, and `migrate.py` are unchanged and `tox -e py311` passes (445 tests).
    - Wrote `.qa-validation-status` (PASS) and recorded results in `tasks.md`.
* Decisions made
    - PASS with three non-blocking advisories (redundant exists-check, retained `boom` stubs in the help test, no mutation sweep recorded).
* Insights
    - Per-module test counts reconcile exactly with the plan; no docs reference moved or deleted test files.

## 2026-11-19 - REFLECT - COMPLETE

* Work completed
    - Updated `memory-bank/active/reflection/reflection-multi-store-filing.md` covering both the initial #103 build and the SLOBAC test-suite rework.
    - Reconciled persistent memory-bank files (`techContext.md` updated in Unit 5; `productContext.md` and `systemPatterns.md` skipped with receipts).
    - Recorded durable test-suite and `AGENTS.md` norms in `.summem/` and completed the requested `nap --root` fold.
* Decisions made
    - Stopped at the Level 2 terminal node (`Reflect -> ManualArchive`).
* Insights
    - Searching contributor prose for plain words (`"in step"`, `"A test checks this"`) alongside internal terms (`"lockstep"`) catches doc claims invalidated when a test is deleted.


## 2026-11-19 - REWORK 2 - INITIATED

* Operator feedback: replace `--root` xor `--path` with one required `--path` using git's `:/` root anchor (creative-store-flag-scheme.md), and fix PR #104 review findings: shell-quote `Run:` paths, resolver containment check (symlinked store), odd-arity heal test overlap, commands.md error-order sentence.
* Complexity: Level 2 (carried over).

## 2026-11-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Level 2 rework; design settled by creative-store-flag-scheme.md.

## 2026-11-19 - PLAN - COMPLETE

* Work completed
    - Level 2 plan in tasks.md: 15 behaviors, 7 steps (resolver, selector/output, surgery, migrate, heal test, agent text, docs).
* Decisions made
    - Amended creative: bare `wake` stays `--path .` (today's behavior); resolver refusals exit 1 like `not in a repository`.
    - Store-containment check lives in `resolve_parent` (covers wake, migrate, every command); `Saved to` formats the store directory.
* Insights
    - `tests/gitutil.py::_FOLD_RUN` must learn the quoted `--path` form or every fold-driving test breaks.

## 2026-11-19 - PREFLIGHT (REWORK 2) - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the Rework 2 plan against `summem`, `surgery.py`, `migrate.py`, `tests/test_heal_view.py`, `docs/`, and `.summem/`. `.preflight-status` first line: `FAIL (fixable)`.
* Decisions made
    - No in-phase plan edits: no TDD ordering swaps and no whole-step strikes were needed.
* Insights
    - Unit 7 misses `docs/how-it-works/index.md` (`./dogfood/.summem` acks); a tracked `.summem` note still states the `--root xor --path` contract and needs superseding.
    - Advisories: `rematerialize_child` spy is implementation-coupled; brief says exit 2 where plan/creative say 1; round-trip parse/format property test suggested.

## 2026-11-19 - PLAN (re-run after preflight FAIL fixable) - COMPLETE

* Added docs/how-it-works/index.md + grep sweep, step 8 superseding stale .summem note, B16 round-trip test, observable odd-arity proof, start formatting after containment, brief exit codes -> 1.

## 2026-11-19 - PREFLIGHT (REWORK 2, re-run) - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-validated the revised Rework 2 plan. `.preflight-status` first line: `PASS WITH ADVISORY`.
* Decisions made
    - No in-phase plan edits.
* Insights
    - All prior FAIL items fixed. Advisories: stale Pre-Mortem line on rematerialize_child call counts; confirm prompt_text/AGENTS.md need no edit; non-:/ relative paths into other repos are accepted by design; keep quoted alternative first in _FOLD_RUN.

## 2026-11-19 - BUILD (in progress) - operator ruling

* Operator: "as in git" is allowed in CLI output as a decompression key. productContext rule reworded (no git operations or error text; naming git as a convention source is fine). Text tests use tests/gitutil.py git_free(), which allows only that phrase; error-path tests keep the strict check.

## 2026-11-19 - BUILD - COMPLETE

* All 8 steps done. tox run-parallel py311-py314 OK (460 tests each); properdocs build --strict clean.

## QA (rework 2)

- QA PASS: plan steps 1-8 implemented; `tox -e py311` 460 passed; no leftover `--root`/`./x` output forms in docs or scripts. Advisories: local `import shlex`; stale Pre-Mortem wording on rematerialize_child.

## 2026-11-19 - REFLECT - COMPLETE (rework 2)

* Reflection appended; techContext gains git_free oracle sentence; productContext and systemPatterns were updated in build (skip).
