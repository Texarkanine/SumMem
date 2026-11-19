---
task_id: multi-store-filing
date: 2026-11-19
complexity_level: 2
---

# Reflection: Multi-Store Filing (`--root` / `--path`)

## Summary

Implemented [Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103) across `summem`, `surgery.py`, `AGENTS.md`, `tests/`, and `docs/`, requiring an explicit `--root` or `--path` store flag on single-store commands, formatting all printed paths relative to the repository root, hiding zero-count child stores from the root-wake catalog, and making `-h`/`--help`/`help` side-effect-free before `import argparse`. Full `properdocs build --strict` and `tox run-parallel` (`py311`–`py314`, 459 tests per env) passed with zero warnings, and QA passed on the first run.

## Requirements vs Outcome

Every functional, non-functional, constraint, and acceptance requirement in #103 was delivered without descoping. Two nuances surfaced in Preflight and were preserved intentionally: (1) the help scan stops at `--` so `note --root -- --help` continues to record literal `--help` per POSIX convention (`test_note_double_dash_records_help_flag`), and (2) `prompt_text()`/`how_to_text()` tests pin command forms and `AGENTS.md` lockstep rather than prose wording per `techContext.md` and `always-tdd.mdc`.

## Plan Accuracy

The five-unit split (help short-circuit -> `summem` flags & root-relative paths -> `surgery.py` -> catalog & prompt/how-to -> docs) sequenced cleanly without reordering. Two items outside the initial Unit 2 file list surfaced during execution: `tests/test_branch_pack_merge.py:94` (caught by Preflight) and `RUN` in `tests/test_middle_orphans.py:25` plus non-git `tmp_path` calls in `tests/test_fold_many_writers.py` (caught by grepping `fold_request(` and running the full suite).

## Build & QA Observations

Strict TDD caught two subtle interactions early: `test_catalog_requires_config_toml_sentinel` actually guards `config.toml` as the git-visible file sentinel for `started_stores()` (`git ls-files` ignores empty directories), and `test_fold_many_writers.py` exercises `fold_request()` directly on bare `tmp_path` directories without `.git`. Handling `ValueError` in `_fold_store_flag` by falling back to `"--root"` kept the pure store-layer helpers independent of `.git` while CLI entrypoints still enforce repository membership. QA passed with zero blocking findings.

## Insights

### Technical
- Pure store-layer helpers (`write_note`, `write_nap`, `heal_view`, `fold_request`) are called directly on bare `tmp_path` directories without `.git` by simulation tests (`test_fold_many_writers.py`); repository-root lookups inside those helpers must tolerate `find_store_parent` raising `ValueError`, whereas CLI handlers (`_select_store`, `wake`, `start`) enforce repository presence.
- `config.toml` in a child `.summem/` directory is load-bearing for `started_stores()` because `git ls-files` does not emit empty directories; filtering `count > 0` belongs strictly in `catalog_text()`.

### Process
- When changing `fold_request`'s `Run:` grammar, grep `re\.(compile|search).*nap` across the entire `tests/` tree up front (`tests/gitutil.py`, `tests/test_fold.py`, `tests/test_zipper.py`, and `tests/test_middle_orphans.py` each maintain their own `Run:` parser).

### Million-Dollar Question

Separating store selection (`_select_store` returning `(parent, root)`) from pure store operations (`parent`-scoped functions) and formatting every user-visible path through `_root_path(path, root)` is the exact design that would have emerged from day one if multi-store monorepo filing had been a foundational assumption.
