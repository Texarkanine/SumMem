# Active Context

## Current Task: catalog-grain-count
**Phase:** BUILD - COMPLETE

## What Was Done
- `_listed_store_grains` parses one `git ls-files` pass: loose notes +1, nap stems add encoded grain once. `catalog_text` prints `N: ./path`. `started_stores` is still `list[Path]`.
- Catalog how-to names `N:` and the `./` token; dropped the uncommitted `note --path <catalog>` draft.
- Surgical briefing in `memory-bank/systemPatterns.md` and `docs/architecture/index.md`. README had no paths-only sentence.
- Tests: 393 passed on py311–py314 (`tox run-parallel`).

## Next Step
- QA review.

## Files modified
- `/home/mobaxterm/git/SumMem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_scopes.py`
- `/home/mobaxterm/git/SumMem/tests/test_init.py`
- `/home/mobaxterm/git/SumMem/memory-bank/systemPatterns.md`
- `/home/mobaxterm/git/SumMem/docs/architecture/index.md`

## Key implementation decisions
- Root is a store only via `is_store` (`.summem` directory). Indexed `.summem/…` after the directory is gone must not list the git root (existing `started_stores` test).
- `catalog_text` calls `_listed_store_grains` once; `started_stores` is a sorted-keys wrapper for migrate/tests.

## Deviations from plan
- `assert "./pkg" in lines` is an exact line match, not a suffix check; retargeted that labeled-paths test to `1: ./pkg`.
- Did not parse root-relative `.summem/` paths for grain; catalog skips root anyway, and doing so broke the phantom-root test.
