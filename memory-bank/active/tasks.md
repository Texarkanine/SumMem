# Task: pytest-xdist

* Task ID: pytest-xdist
* Complexity: Level 2
* Type: simple enhancement

Investigate whether `pytest-xdist` is safe inside each tox env, then enable it by default on `[testenv]` if the investigation passes. Specified by [issue #64](https://github.com/Texarkanine/SumMem/issues/64). Parallel tox *environments* stay #63; this is within-env workers only.

**Investigation outcome (pytest-xdist 3.8.0):** safe with **0 serial markers**. 355 passed at `-n auto` (16 workers, 26.65s), `-n 8` (22.71s), `-n 4` (19.55s); serial 36.57s. Flock, session `summem` fixture / `sys.modules["summem"]`, subprocess CLI, and git worktree/merge tests were in those runs. py312–py314 also 355 passed under xdist (preflight).

**Parallelism trade-off (preflight FAIL #1, re-measured):** unbounded `-n auto` inside `tox run-parallel` is 4 envs × N cores (here ~64 workers, 67s wall vs 53s serial-within-env). Default will be `pytest -n auto --maxprocesses=4 {posargs}`: 4 is this git-heavy suite's fastest single-env width *and* keeps four concurrent envs at 16 workers. Measured `tox run-parallel -- -n 4`: 355 passed ×4 in 31.49s. CI stays one env per job; `-n auto` on a 2-core runner is 2, the cap does not inflate it. Coverage env stays serial (its `commands` already override `[testenv]`).

## Test Plan (TDD)

### Behaviors to Verify

- Tox installs xdist: `[testenv] deps` includes `pytest-xdist` → the plugin is present in every declared testenv (coverage inherits deps).
- Default env is capped-parallel: `[testenv] commands` tokens are `pytest`, `-n`, `auto`, `--maxprocesses=4`, `{posargs}` → `tox -e py311` distributes with at most 4 workers; posargs can still select tests or override `-n`.
- Coverage stays serial: `[testenv:coverage] commands` do not pass `-n` → `tox -e coverage` does not start xdist workers.
- Edge — existing runner contracts still hold: `{posargs}` present, no `--cov` on default commands, no `--basetemp` (already tested in `tests/test_tox_runner.py`).

No product (`summem`) behavior change. Do not add a change-detector that pytest-xdist is imported, or that named tests carry serial marks (investigation count is 0).

### Test Infrastructure

- Framework: pytest via tox (`tox.ini`, `pytest.ini`)
- Test location: `tests/`
- Conventions: runner contracts live in `tests/test_tox_runner.py` (ConfigParser, `interpolation=None`); nested live pytest is `tests/test_coverage_collection.py`
- New test files: none

## Implementation Plan

### 1. Tox runner contract — executable

- Files: `tests/test_tox_runner.py`, `tox.ini`

1. Stub tests: empty `test_tox_deps_include_pytest_xdist`, `test_tox_commands_enable_xdist`, `test_coverage_env_runs_serial` in `tests/test_tox_runner.py`.
2. Stub interface: none — no new Python API; `[testenv]` already has `deps` and `commands`.
3. Write tests and run red: `uvx --with tox tox -e py311 -- tests/test_tox_runner.py` — deps list includes `pytest-xdist`; `[testenv] commands`.split() has `-n` immediately followed by `auto` and contains `--maxprocesses=4`; coverage command tokens do not include `-n`. Do not re-assert `{posargs}` here (`test_tox_commands_run_pytest_with_posargs` already does).
4. Write code and run green: add `pytest-xdist` under `[testenv] deps`; set `[testenv] commands = pytest -n auto --maxprocesses=4 {posargs}`. Leave `[testenv:coverage] commands` without `-n`. Re-run the same file, then `uvx --with tox tox -e py311`.

### 2. Docs — prose/policy

- Files: `README.md`, `memory-bank/techContext.md`, `.cursor/rules/SumMem-testing.mdc`
- No tests: prose/policy artifact

1. Keep the iteration command as `tox -e py311` (and single-test posargs). Note that a full env run uses xdist `-n auto --maxprocesses=4`.
2. Keep the full-matrix command as `tox run-parallel`. State that the cap exists so four concurrent envs do not each take every core (unbounded `-n auto` made that command slower here).
3. Mention `-n0` via posargs when a serial rerun is wanted (argparse last-wins; preflight verified `pytest -n auto -n 0` starts no workers).
4. Do not claim coverage is parallel; `tox -e coverage` stays serial.

### 3. Serial-marker justification — prose/policy

- Files: GitHub issue #64 comment; `memory-bank/active/progress.md` (Build append)
- No tests: prose/policy artifact

1. After the suite is green under the default tox command, `gh issue comment 64` with: investigation result (safe); serial-marker count **0**; justification (flock/`sys.modules`/subprocess/worktree tests ran under xdist on isolated `tmp_path` / per-worker processes; 355 passed). Quote the worker cap and the run-parallel times so the issue records the trade-off.
2. Append the same count and justification to `progress.md` so archive/PR can copy it. This step owns [issue #64](https://github.com/Texarkanine/SumMem/issues/64) Acceptance Criterion 3; do not defer it to the operator or to `/niko-archive`.

### 4. Matrix confirmation — prose/policy

- Files: none new (verification only)
- No tests: verification of the suite, not new behavior

1. `uvx --with tox tox -e py311` green (iteration path).
2. `uvx --with tox tox run-parallel` green. Record wall time in `progress.md`. If it is slower than a same-session serial-within-env control (`tox run-parallel -- -n0`), stop and re-cap; do not ship a matrix regression.
3. `uvx --with tox tox -e coverage` once: lcov still writes; pytest must not create xdist workers.
4. If a race appears, mark the minimum tests and update the issue comment's count; do not delete proofs.

## Technology Validation

New dependency: `pytest-xdist` (3.8.0 in the PoC envs; transitive `execnet>=2.1`). Plugin loads next to existing `pytest-cov`.

PoC (not committed): `.tox/py311/bin/pip install pytest-xdist` then pytest at several widths, all 355 passed:

| command | workers | py311 wall |
| --- | --- | --- |
| serial | 1 | 36.57s |
| `-n auto` | 16 | 26.65s |
| `-n 8` | 8 | 22.71s |
| `-n 4` | 4 | 19.55s |

`tox run-parallel` (four envs, 355 passed each):

| within-env | wall |
| --- | --- |
| serial (`-n0`) | 53s (preflight) |
| `-n auto` | 67s (preflight) |
| `-n 4` | 31.49s (replan) |

`--maxprocesses=4` with `-n auto` is the accepted default: same cap as the fastest single-env width; CI 2-core still gets 2 workers. Rejected: unbounded `-n auto` (matrix regression); `PYTEST_WORKERS` env var (forgettable; the safe value must be the default).

pytest-cov can combine xdist workers. Out of scope: coverage env stays serial.

## Dependencies

- Issue #63 session `summem` fixture / `conftest._SUMMEM` — already on the tree; each xdist worker is a process and loads its own session fixture. FileLock-once-across-workers is the wrong pattern here.
- `tests/test_tox_runner.py` — existing tox.ini contract tests.
- `pytest-xdist` (new tox dep).
- `gh` authenticated for the issue comment in step 3.

## Challenges & Mitigations

- Flock tests in `tests/test_zipper.py`: they flock `tmp_path` store `naps/`, and `fcntl.flock` monkeypatches are per-worker. PoC included them (green). If a later run races, mark that test only and update the issue-comment count.
- `sys.modules["summem"]`: cache is `conftest._SUMMEM`; workers do not share memory. Fixture tests passed under xdist.
- Git worktrees: created under `tmp_path` via `init_repo` (local `user.name`/`user.email`, not `--global`). No shared `.git` of the clone.
- Nested `python -m pytest` in `tests/test_coverage_collection.py`: xdist autoloads when installed but does not parallelize without `-n`. Those tests passed under a parent xdist run.
- `-n auto` × `tox run-parallel` oversubscribes: **cap `--maxprocesses=4` in tox.ini**, do not leave recovery to posargs. Step 4 fails the build if the matrix is slower than `-n0`.
- `--maxprocesses=4` is a suite cap (git-heavy tests + four tox envs), not this machine's `nproc`. A 2-core CI job still uses `-n auto` → 2.
- One/two green runs can miss a flake: Build ends with `tox run-parallel`; CI is the longer soak.
- `gh issue comment` needs network/auth: if it fails, stop; the AC3 artifact is not optional.

## Pre-Mortem

- Investigation hid a race that only shows under the full matrix or CI: already covered by Challenge (matrix + mark-minimum + issue-comment update). Do not pre-mark flock tests.
- `-n auto` put in `pytest.ini` `addopts` would also hit `tox -e coverage` and nested pytest: plan keeps xdist args only on `[testenv] commands`.
- Unbounded `-n auto` ships and `tox run-parallel` gets slower: the first preflight already caught this; default now includes `--maxprocesses=4` and step 4 compares to `-n0`.
- AC3 never lands because archive does not open the PR: step 3 comments on the issue during Build.
- Contract tests on `tox.ini` dismissed as change-detectors: they match the existing runner-lock tests; they fail when the advertised command drops xdist or drops the cap (matrix regression waiting to happen).
- Task is secretly L3 (design fork: loadfile vs loadgroup vs serial marks vs PYTEST_WORKERS): investigation found default `--dist load`, 0 marks, and a fixed cap. Stays L2.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
