---
task_id: pytest-xdist
date: 2026-08-25
complexity_level: 2
---

# Reflection: pytest-xdist

## Summary

Within-env pytest-xdist is on by default as `pytest -n auto --maxprocesses=4`. Investigation found the suite safe with zero serial markers. First preflight failed because unbounded `-n auto` made `tox run-parallel` slower; the cap that fixed the matrix was also the fastest single-env width. QA PASS.

## Requirements vs Outcome

Delivered as specified in [issue #64](https://github.com/Texarkanine/SumMem/issues/64): investigation written, xdist in tox deps, default worker args, py311–py314 green, serial-marker count 0 justified on the issue, docs updated. Added `--maxprocesses=4` after preflight measured the #63 interaction; that was in scope, not extra product work. Coverage stayed serial.

## Plan Accuracy

The first plan measured only `tox -e py311`. The documented end-of-work command is `tox run-parallel`; that is where unbounded auto lost. File list and TDD sequence were otherwise right. Flock/`sys.modules`/worktree risks in the issue did not materialize. AC3 needed an explicit Build `gh issue comment` because L2 never writes the PR.

## Build & QA Observations

Build was linear after the cap was chosen. One TDD quirk: `test_coverage_env_runs_serial` was already green (lock on absence of `-n`). QA reverified the matrix (28.83s) and did not fail. Advisories: restore dirty tracked coverage files (done); single-file runs pay ~1.3s of worker startup (`-n0` is the fast path); `commands.index("-n")` fails as `ValueError`.

## Insights

### Technical

- Two parallelism dials multiply. `-n auto` inside each of four concurrent tox envs is ~64 workers on a 16-core host and made the documented matrix *slower*. Cap workers so `env_count × cap` stays near one core budget; here 4 was also the git-heavy suite's fastest single-env width.
- Session-scoped `summem` is safe under xdist because each worker is a process with its own `conftest._SUMMEM`. FileLock-once-across-workers is the wrong pattern for a loaded module.

### Process

- Technology validation must run the documented *end-of-work* command, not only the iteration env. Preflight FAIL was that miss.
- If an acceptance criterion is "justify X in the PR or issue comment," L2 Build must `gh` it. Archive does not own that.

### Million-Dollar Question

If xdist and `tox run-parallel` had been designed together, `[testenv]` would have shipped `pytest -n auto --maxprocesses=<env_list length>` from the start, with coverage overriding `commands` so it stays serial. That is what landed. A `PYTEST_WORKERS` env var would have made the unsafe value the default people forget to override.
