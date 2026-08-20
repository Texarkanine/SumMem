# Active Context

## Current Task: agents-prompt
**Phase:** REFLECT - COMPLETE

## What Was Done
- Struck driver copy from `ensure_store`. It still creates `notes/`, `naps/`, and default config. It does not place `.summem/summem`.
- Rewrote `prompt_text()` and the top of `AGENTS.md` to invoke `.summem/summem`. Lockstep test holds. `CLAUDE.md` still `@AGENTS.md`.
- Updated `VISION.md` Onboarding/Activation, `memory-bank/systemPatterns.md`, and `memory-bank/techContext.md`. This repo’s record is repo-root `summem`; store drivers are symlinks. `.summem/summem` is now that symlink.
- Composer 2.5 Probe A: `.summem/summem wake`. Probe B: skipped second root wake.
- pytest 205 passed.
- After reflect, operator asked to label the root-wake catalog so it is not read as an instruction. Catalog is now `== Additional memory catalogs ==` plus `./path` lines; root document sits under `== Project-root memories ==`. No `summem wake --path` command line. Pull wakes unchanged. pytest 206 passed.

## Files created or modified
- `/home/mobaxterm/git/SumMem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_store.py`
- `/home/mobaxterm/git/SumMem/tests/test_wake.py`
- `/home/mobaxterm/git/SumMem/tests/test_scopes.py`
- `/home/mobaxterm/git/SumMem/tests/test_init.py`
- `/home/mobaxterm/git/SumMem/AGENTS.md`
- `/home/mobaxterm/git/SumMem/VISION.md`
- `/home/mobaxterm/git/SumMem/memory-bank/systemPatterns.md`
- `/home/mobaxterm/git/SumMem/memory-bank/techContext.md`
- `/home/mobaxterm/git/SumMem/.summem/summem` (file → symlink to `../summem`)
- `/home/mobaxterm/git/SumMem/memory-bank/active/tasks.md`
- `/home/mobaxterm/git/SumMem/memory-bank/active/activeContext.md`
- `/home/mobaxterm/git/SumMem/memory-bank/active/progress.md`

## Key implementation decisions
- Nested `start` does not get a driver. Agents run root `.summem/summem` and pass `--path`.
- Catalog `usage_text` still names the product `summem`. The prompt names `.summem/summem`.
- Did not add nested-store driver symlinks (preflight radical-innovation advisory).
- After reflect: catalog is a labeled path list, not pull commands. When-to-pull stays in `AGENTS.md`.

## Next Step
- Archive (`/niko-archive`). Catalog-header fix is in the tree and still unarchived with this task.
