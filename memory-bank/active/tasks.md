# Task: pytest-xdist

* Task ID: pytest-xdist
* Complexity: Level 2
* Type: simple enhancement

Investigate whether `pytest-xdist` is safe inside each tox env, then enable it by default on `[testenv]` if the investigation passes. Specified by [issue #64](https://github.com/Texarkanine/SumMem/issues/64). Parallel tox *environments* stay #63; this is within-env workers only.

**Investigation outcome (Plan PoC, pytest-xdist 3.8.0, `.tox/py311`):** safe with no serial markers. 355 passed at `-n auto` (16 workers, 26.65s) and `-n 8` (22.71s); serial 36.57s. Flock, session `summem` fixture / `sys.modules["summem"]`, subprocess CLI, and git worktree/merge tests were in that run. Coverage env stays serial (its `commands` already override `[testenv]`).

## Test Plan (TDD)

### Behaviors to Verify

- Tox installs xdist: `[testenv] deps` includes `pytest-xdist` → the plugin is present in every declared testenv (coverage inherits deps).
- Default env is parallel: `[testenv] commands` is `pytest` then `-n` `auto` then `{posargs}` → `tox -e py311` distributes tests; posargs can still select tests or override `-n`.
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
3. Write tests and run red: `tox -e py311 -- tests/test_tox_runner.py` — deps list includes `pytest-xdist`; `[testenv] commands`.split() has `-n` immediately followed by `auto` and still contains `{posargs}`; coverage command tokens do not include `-n`.
4. Write code and run green: add `pytest-xdist` under `[testenv] deps`; set `[testenv] commands = pytest -n auto {posargs}`. Leave `[testenv:coverage] commands` without `-n`. Re-run the same file, then `tox -e py311`.

### 2. Docs — prose/policy

- Files: `README.md`, `memory-bank/techContext.md`, `.cursor/rules/SumMem-testing.mdc`
- No tests: prose/policy artifact

1. Note that a full env run (`tox -e py311`, `tox run-parallel`, CI `tox -e …`) uses xdist `-n auto`.
2. Keep the iteration command as `tox -e py311` (and single-test posargs). Mention `-n0` (or `-n 1`) via posargs when a serial rerun is wanted.
3. Do not claim coverage is parallel; `tox -e coverage` stays serial.

### 3. Matrix confirmation — executable

- Files: none new (verification only)

1. Stub tests: none.
2. Stub interface: none.
3. Write tests and run red: none — this step is the suite itself.
4. Write code and run green: `uvx --with tox tox -e py311`, then `uvx --with tox tox run-parallel`, then `uvx --with tox tox -e coverage` once to confirm lcov still writes and no xdist workers start. If a race appears, mark the minimum tests (`@pytest.mark.xdist_group` plus `--dist loadgroup` only if grouping is required) and justify the count; do not delete proofs.

## Technology Validation

New dependency: `pytest-xdist` (Plan installed 3.8.0; transitive `execnet>=2.1`). Plugin loads next to existing `pytest-cov`.

PoC (not committed): `.tox/py311/bin/pip install pytest-xdist` then `.tox/py311/bin/pytest -n auto` → 355 passed. Repeat at `-n 8` → 355 passed. Serial baseline 355 passed in 36.57s.

`--maxprocesses` exists to cap `auto`/`logical`. Not used in the default: `-n auto` is what #64 asked for; 16-wide was still faster than serial here. Posargs can pass `-n 8` if a machine wants the measured local sweet spot.

pytest-cov documents combining coverage across xdist workers. Out of scope: coverage env stays serial.

## Dependencies

- Issue #63 session `summem` fixture / `conftest._SUMMEM` — already on the tree; each xdist worker is a process and loads its own session fixture. FileLock-once-across-workers is the wrong pattern here.
- `tests/test_tox_runner.py` — existing tox.ini contract tests.
- `pytest-xdist` (new tox dep).

## Challenges & Mitigations

- Flock tests in `tests/test_zipper.py`: they flock `tmp_path` store `naps/`, and `fcntl.flock` monkeypatches are per-worker. Plan PoC included them (green). If a later run races, mark that test only.
- `sys.modules["summem"]`: cache is `conftest._SUMMEM`; workers do not share memory. Fixture tests passed under xdist.
- Git worktrees: created under `tmp_path` via `init_repo` (local `user.name`/`user.email`, not `--global`). No shared `.git` of the clone.
- Nested `python -m pytest` in `tests/test_coverage_collection.py`: xdist autoloads when installed but does not parallelize without `-n`. Those tests passed under a parent xdist run.
- Unbounded `-n auto` on a high-core host can be slightly slower than a mid cap (16-wide 26.65s vs 8-wide 22.71s here): keep `-n auto`; override via posargs. Do not bake a machine-specific `--maxprocesses`.
- One/two green runs can miss a flake: Build ends with `tox run-parallel`; CI is the longer soak.

## Pre-Mortem

- Investigation hid a race that only shows under the full matrix or CI: already covered by Challenge (matrix + mark-minimum). Do not pre-mark flock tests.
- `-n auto` put in `pytest.ini` `addopts` would also hit `tox -e coverage` and nested pytest: plan keeps `-n auto` only on `[testenv] commands`.
- Contract tests on `tox.ini` dismissed as change-detectors: they match the existing runner-lock tests; they fail when the advertised contributor command stops being parallel (or coverage accidentally becomes parallel).
- Task is secretly L3 (design fork: loadfile vs loadgroup vs serial marks): investigation found default `--dist load` + no marks is enough. Stays L2.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
