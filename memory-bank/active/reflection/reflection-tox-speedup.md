---
task_id: tox-speedup
date: 2026-08-25
complexity_level: 2
---

# Reflection: tox-speedup

## Summary

Local tox is now one `tox run-parallel` of py311–py314, iteration is `tox -e py311`, and tests load repo-root `summem` once per session. Product behavior is unchanged. QA passed after one rework.

## Requirements vs Outcome

Delivered: documented parallel matrix, agent iteration rule, session fixture, suite green on four CPythons, TDD for the tox and fixture contracts. The brief's example `-j auto` was never tox's flag; we documented `-p auto` via `run-parallel`. No product code changed. pytest-xdist, testmon, CI expansion, and proof deletion stayed out.

## Plan Accuracy

The plan's file list and sequence were right. Two assumptions were wrong: tox FAQ `--basetemp="{env_tmp_dir}"` is inside the clone (outside-repo tests then wake the real store), and an explicit `TMPDIR/summem-{env}` path is a cross-checkout clobber because pytest `rm_rf`s it with no numbering. Caching on `sys.modules["summem"]` also failed: migrate.py and surgery.py overwrite that entry. The challenges that landed were those two, not leaked `WAKE_LINES` or a recursive tox pytest.

## Build & QA Observations

Call-site conversion was mechanical and stayed green. First QA (Opus) correctly failed both the `--basetemp` regression and the pytest-private fixture-marker test. Rework dropped the flag, asserted cache identity, and moved the cache to `conftest._SUMMEM`. Second QA (GPT) passed; matrix ~48s vs ~40s per env serial.

## Insights

### Technical
- Pytest's default basetemp under tox is already outside the worktree (`TMPDIR` unset → `gettempdir()` is `/tmp`) and already isolates concurrent runs (`pytest-0`…). An explicit `--basetemp` disables that isolation.
- A test process cache keyed on `sys.modules["summem"]` is not stable while CLI helpers reload the driver into that name.

### Process
- A FAQ pattern still needs a probe against this suite's outside-repo `chdir(tmp_path)` tests and against two checkouts sharing `/tmp`.
- Asserting pytest private fixture markers is a change-detector when `deps = pytest` is unpinned; assert the cache behavior instead.

### Million-Dollar Question

What we have after rework: `tox.ini` stays `pytest {posargs}`, pytest owns temp isolation, one session fixture, a conftest-owned module cache. The FAQ `--basetemp` line was the detour. Nothing more foundational was missing.
