---
task_id: pytest-xdist
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: pytest-xdist

## SUMMARY

Each tox py3xx env runs pytest-xdist as `pytest -n auto --maxprocesses=4 {posargs}`. The suite is safe with **0 serial markers**. Unbounded `-n auto` made `tox run-parallel` slower (67s vs 53s serial-within-env); the cap of 4 is also this git-heavy suite's fastest single-env width. Coverage stays serial. `.coverage` and `coverage/lcov.info` are no longer tracked (already gitignored). Product CLI unchanged. [PR #66](https://github.com/Texarkanine/SumMem/pull/66) closes #64.

## REQUIREMENTS

- Investigate whether pytest-xdist is safe inside each tox env ([issue #64](https://github.com/Texarkanine/SumMem/issues/64)).
- If safe: add it to tox deps; default testenv passes parallel worker args; py311–py314 green.
- Serial tests explicitly marked; count justified on the issue or PR.
- README, `techContext.md`, `.cursor/rules/SumMem-testing.mdc` updated if the default iteration command changes.
- Within-env only; do not delete proofs; coverage may stay serial.

## IMPLEMENTATION

Level 2. [`tox.ini`](../../../tox.ini) `[testenv]` deps include `pytest-xdist`; commands are `pytest -n auto --maxprocesses=4 {posargs}`. [`tests/test_tox_runner.py`](../../../tests/test_tox_runner.py) locks the dep, the `-n auto` + cap, and that coverage commands have no `-n`. Docs: [README.md](../../../README.md) Developing, [`memory-bank/techContext.md`](../../techContext.md) Testing Process, [`.cursor/rules/SumMem-testing.mdc`](../../../.cursor/rules/SumMem-testing.mdc). Session `summem` fixture is per-worker (each xdist process has its own `conftest._SUMMEM`). Follow-up: `git rm --cached` `.coverage` and `coverage/lcov.info`; no test that git does not contain them (`.gitignore` is the gate).

## TESTING

Investigation: 355 passed at `-n auto` / `-n 8` / `-n 4` on py311; py312–py314 also 355 under xdist. First preflight FAIL (fixable): unbounded auto × `tox run-parallel`. Rework then PASS WITH ADVISORY. Build: 358 passed `tox -e py311` (4 workers, 19.96s); `tox run-parallel` 28.77s vs `-n0` 38.78s; `tox -e coverage` 358 serial, lcov written, no workers. Serial-marker count **0** on [issue #64](https://github.com/Texarkanine/SumMem/issues/64#issuecomment-5419816806). QA PASS (matrix reverified 28.83s).

## LESSONS LEARNED

- Two parallelism dials multiply. Cap workers so `env_count × cap` stays near one core budget; here 4 was also the fastest single-env width.
- Session-scoped `summem` is safe under xdist because each worker is a process. FileLock-once-across-workers is the wrong pattern for a loaded module.
- A `git ls-files` assertion that coverage artifacts are absent is a change-detector; `.gitignore` is the gate.

## PROCESS IMPROVEMENTS

- Technology validation must run the documented end-of-work command (`tox run-parallel`), not only `tox -e py311`.
- If an acceptance criterion is "justify X in the PR or issue comment," L2 Build must `gh` it. Archive does not own that.

## TECHNICAL IMPROVEMENTS

Preflight advisory (not applied): a scheduled py311 soak at worker counts 2 and 4 after this proves stable. Single-file iteration pays ~1.3s of worker startup; `-n0` is the fast path.

## NEXT STEPS

- [PR #66](https://github.com/Texarkanine/SumMem/pull/66) on `parallel-test`. Review, then squash-merge when ready.
