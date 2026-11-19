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
