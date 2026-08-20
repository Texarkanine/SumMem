# Task: tox-pytest-runner

* Task ID: tox-pytest-runner
* Complexity: Level 2
* Type: simple enhancement

Add `tox.ini` as the one documented way to run pytest on every non-EOL CPython from the 3.11 floor (3.11–3.14). Do not add a hatchling/PyPI package. Skip a test-result cache. Do not change the product CLI.

## Test Plan (TDD)

### Behaviors to Verify

- Declared matrix: reading `tox.ini` `env_list` → exactly `py311`, `py312`, `py313`, `py314` (no `py310`)
- No packaging: reading `tox.ini` `[testenv] package` → `skip`
- Runner invokes pytest: reading `tox.ini` `[testenv] commands` → the command runs `pytest` and forwards `{posargs}`
- Collection root: reading `pytest.ini` `testpaths` → `tests`
- Recursion: these tests parse config only; they must not spawn `tox` (the suite will later run under tox)

### Test Infrastructure

- Framework: pytest (existing `pytest.ini`)
- Test location: `tests/`
- Conventions: `test_*.py`, `test_*` functions, docstrings that state the behavior, `from conftest import ROOT` when a path is needed; no parallel runner
- New test files: `tests/test_tox_runner.py`

## Implementation Plan

### 1. Tox runner contract — executable

- Files: `tests/test_tox_runner.py`, `tox.ini`, `.gitignore`

1. Stub tests: add `tests/test_tox_runner.py` with empty `test_tox_env_list_is_non_eol_cpython_from_3_11`, `test_tox_skips_packaging_the_project`, `test_tox_commands_run_pytest_with_posargs`, `test_pytest_collects_from_tests_directory`
2. Stub interface: add `tox.ini` with `[tox]` and `[testenv]` sections present but `env_list` / `package` / `commands` not yet the intended values (so step 3 is red)
3. Write tests and run red: `uv run --python 3.11 --with pytest pytest tests/test_tox_runner.py`
    - `env_list` splits to exactly `["py311", "py312", "py313", "py314"]`
    - `package` is `skip`
    - `commands` is `pytest` plus `{posargs}` (stdlib `configparser` on repo-root `tox.ini`)
    - `pytest.ini` `testpaths` is `tests`
    - Do not subprocess tox
4. Write code and run green: set `min_version = 4.0`, `env_list = py311, py312, py313, py314`, `skip_missing_interpreters = true`, `[testenv] package = skip`, `deps = pytest`, `commands = pytest {posargs}`. Append `.tox/` to `.gitignore`. Re-run the new tests.

### 2. Document the one command — prose/policy

- Files: `README.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. README Developing: the command is `tox`. Say how to get tox without a global install (`uvx --with tox tox`) and that `tox -e py311` is the single-interpreter form. Do not keep `uv run --python 3.11 --with pytest pytest` as the documented command.
2. techContext Testing Process: same command. Environment Setup's "use `uv run --python 3.11`" test sentence must match so the two sections do not disagree.
3. Record the cache skip: no pytest-testmon / no custom cache. This suite is heavy on `tmp_path`, git worktrees, and a no-suffix `SourceFileLoader` script; coverage-based selection is not proven not to skip a test that should run.
4. Record the 3.14 machine gap: this uv (0.8.22) provisioned `3.14.0rc3`, not a final 3.14. `py314` stays in `env_list` and was creatable here.

### 3. Build verification — executable, not a nested pytest case

- Files: none new

1. After units 1–2 are green, run `uvx --with tox tox` from the worktree (or `tox` if on PATH) so each declared interpreter that is installed actually runs the suite.
2. Do not add a pytest case that invokes tox (recursion under the matrix).

## Technology Validation

Validated on this machine, 2026-08-19:

- `uvx --with tox tox` with `package = skip` and no `pyproject.toml` ran pytest using `pytest.ini` `testpaths = tests` (temp POC).
- Interpreters tox found: 3.11.11, 3.12.11, 3.13.7, 3.14.0rc3. `uv python install 3.14.0` still only offers rc3 on uv 0.8.22. Matrix stays 3.11–3.14; document the rc3 gap.
- tox-uv not required: vanilla tox resolved `python3.12`/`python3.13`/`python3.14` on PATH after `uv python install`. Do not add `requires = tox-uv` (that would make uv mandatory).
- pytest-testmon: skipped (not installed, not proven on this filesystem suite). Do not adopt rpytest. Do not write a cache library.

## Dependencies

- tox >= 4 (dev command; not a product dependency)
- pytest (already the suite runner; tox env `deps`)
- CPython 3.11–3.14 on PATH, or a subset plus `skip_missing_interpreters = true`

## Challenges & Mitigations

- Missing interpreters make `tox` fail: `skip_missing_interpreters = true` so the documented command still runs what is installed; the contract test keeps all four names declared.
- Runner tests that call tox recurse when the suite runs under tox: parse `tox.ini` / `pytest.ini` only.
- README/techContext tests would be change-detectors: no tests on those files.
- 3.14.0rc3 vs final 3.14: keep `py314`; document the rc3 gap in techContext. Not a product fork.

## Pre-Mortem

- We add `pyproject.toml` "because tox needs a package": already disproved; `package = skip` is the plan.
- We require tox-uv and break no-uv contributors: already covered — vanilla tox, optional `uvx --with tox`.
- We adopt testmon and skip a filesystem test that should run: already covered — skip the cache.
- Runner tests assert README wording and preflight strikes them: already covered — config contract only.
- We treat rc3 as a reason to drop 3.14 from the matrix: already covered — declare and document.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
