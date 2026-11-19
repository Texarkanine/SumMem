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
