# Active Context

**Current Task:** multi-store-filing rework 2: single `--path` with git `:/` root anchor + PR #104 review fixes
**Phase:** QA - COMPLETE (PASS)

## Files modified

- `summem` (`_input_path` new; `resolve_parent`, `_select_store`, `_store_flag_error`, `_root_path`, `_fold_store_flag`, `catalog_text`, `start` branch, argparse, `how_to_text`, `usage_text`)
- `surgery.py` (`_usage`, argparse, `_select_store` call)
- `tests/`: gitutil (`_FOLD_RUN` quoted form, `git_free`), test_scopes, test_cli, test_cli_help, test_init, test_fold, test_middle_orphans, test_surgery, test_migrate, test_heal_view, test_path_walkup_and_catalog, plus mechanical `--root` → `--path :/` across 19 files
- `docs/` (10 pages), `memory-bank/productContext.md`, `memory-bank/systemPatterns.md`, `.summem/` (superseding note + requested nap)

## Decisions and deviations

- Operator ruling during build: "as in git" may appear in CLI output as a decompression key. productContext rule reworded; `git_free()` allows only that phrase.
- `--root` never shipped (latest tag v0.14.0): docs describe `--path` only, with no migration text.
- `shlex` is imported lazily inside `_fold_store_flag` (driver lazy-import pattern).
- The odd-arity heal test needed no production change.

## Next Step

QA (subagent).
