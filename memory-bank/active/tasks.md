# Task: codecov-upload

* Task ID: codecov-upload
* Complexity: Level 2
* Type: simple enhancement

Add opt-in Python coverage collection (`tox -e coverage`: `pytest-cov --cov=summem` → lcov) and upload it from a new CI job the way stockroom uploads engine coverage. Put a Codecov badge on the README. Default `tox` stays coverage-free.


## Test Plan (TDD)

### Behaviors to Verify

- [Coverage source]: `pytest --cov=summem --cov-report=lcov:DEST` on a narrow existing test → DEST exists and lcov `SF:` includes `summem`, not a tests-only report
- [Coverage tox env]: `tox.ini` `[testenv:coverage]` is the collection command: `--cov=summem`, an lcov report under `{env:COVERAGE_DIR:coverage}/`, and `{posargs}`
- [Default suite]: `tox.ini` `env_list` stays `py311`–`py314` (no `coverage`); `[testenv]` `commands` stay `pytest {posargs}` with no `--cov`
- [Edge — no required artifact]: the default suite does not require writing `coverage/lcov.info`

No tests for `.github/workflows/ci.yaml`, `codecov.yml`, or the README badge (consumer Actions YAML / Codecov config / prose; see projectbrief constraint 6).

### Test Infrastructure

- Framework: pytest (as configured in `pytest.ini`)
- Test location: `tests/`
- Conventions: `test_*.py`; contract locks on `tox.ini` live in `tests/test_tox_runner.py` (`ConfigParser(interpolation=None)`); tests load repo-root `summem` via `SourceFileLoader` in `tests/conftest.py`
- New test files: `tests/test_coverage_collection.py` (live lcov emit). Coverage-env contract cases may be added to `tests/test_tox_runner.py` (same ini reader) or the new file — one place, not both.

## Implementation Plan

### 1. Coverage collection — executable ✅

- Files: `tox.ini`, `tests/test_coverage_collection.py`, `tests/test_tox_runner.py`

1. Stub tests: empty cases in `tests/test_coverage_collection.py` (and/or `tests/test_tox_runner.py`) for the four behaviors above.
2. Stub interface: add `[testenv:coverage]` to `tox.ini` with empty/placeholder `deps` and `commands` (so the names exist, the assertions fail).
3. Write tests and run red: live nested `pytest --cov=summem --cov-report=lcov:{tmp_path}/lcov.info` on `tests/test_version.py::test_version_prints_script_version` asserts `SF:` contains `summem` and is not tests-only; ini contract asserts `[testenv:coverage]` flags, default `commands` / `env_list` unchanged. Default suite must install `pytest-cov` so the live case does not skip.
4. Write code and run green: `[testenv]` `deps` = `pytest` + `pytest-cov`; `[testenv:coverage]` overrides `commands` to `pytest --cov=summem --cov-report=lcov:{env:COVERAGE_DIR:coverage}/lcov.info {posargs}` (create the dest dir if the reporter will not). Do not put `--cov` in default `commands` or `coverage` in `env_list`.

### 2. Ignore coverage artifacts — prose/policy ✅

- Files: `.gitignore`
- No tests: prose/policy artifact

1. Ignore `.coverage`, `coverage/`, `htmlcov/`.

### 3. CI upload — prose/policy ✅

- Files: `.github/workflows/ci.yaml`, `codecov.yml`
- No tests: consumer GitHub Actions YAML and Codecov config; not product TDD (projectbrief constraint 6)

1. Add a CI workflow (PR + push to `main`) that checks out, sets up Python 3.11, installs `tox`, runs `tox -e coverage`, then `codecov/codecov-action@v7` with `files: coverage/lcov.info`, `token: ${{ secrets.CODECOV_TOKEN }}`, `fail_ci_if_error: false` (stockroom Python upload).
2. Add root `codecov.yml` (that filename, not `.yaml`): project/patch status `enabled: false` until a baseline exists.

### 4. README badge and Developing note — prose/policy ✅

- Files: `README.md`
- No tests: prose/policy artifact

1. Add the stockroom-style badge: `[![codecov](https://codecov.io/github/Texarkanine/SumMem/graph/badge.svg)](https://codecov.io/github/Texarkanine/SumMem)`.
2. In Developing, document `tox -e coverage` as the opt-in lcov command and that the badge 404s until `CODECOV_TOKEN` plus a successful upload.

### 5. Tech context — prose/policy ✅

- Files: `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. Update Testing Process: coverage is opt-in via `tox -e coverage`; default `tox` stays coverage-free; CI uploads lcov.

## Technology Validation

New Python dependency: `pytest-cov` (tox `deps` only; no project package).

PoC (2026-08-20, `uvx --with pytest --with pytest-cov --python 3.11`): `pytest tests/test_version.py::test_version_prints_script_version --cov=summem --cov-report=lcov:DEST` writes lcov whose only `SF:` is `summem` (777 statements). `--cov=.` also lists tests; `--cov=` collects nothing. Use `--cov=summem`.

`codecov/codecov-action@v7` is CI-only (stockroom), not a Python dependency.

## Dependencies

- `pytest-cov` (already proven against this shebang)
- `codecov/codecov-action@v7` and repository secret `CODECOV_TOKEN` (operator; upload may no-op until provisioned)
- New `.github/workflows/ci.yaml` (first test CI job in this repo)

## Challenges & Mitigations

- Nested `tox -e coverage` from inside `tox -e py311` would recurse and needs host `tox`: do not subprocess `tox` from pytest. Live test invokes `pytest --cov=summem` with `tmp_path`; the tox env is locked by ini contract (same style as `tests/test_tox_runner.py`).
- `CODECOV_TOKEN` missing: `fail_ci_if_error: false`; badge 404 is expected until the operator adds the secret and CI uploads once (stockroom).
- Preflight treats consumer Actions YAML as product TDD: the brief and this plan record the existing ruling before preflight runs.
- lcov parent directory missing: create `{env:COVERAGE_DIR:coverage}` in the coverage env if the reporter does not.

## Pre-Mortem

- Collection measured tests only or nothing, so Codecov looked empty: already covered by the live `SF: summem` assertion and `--cov=summem` (validated).
- We copied stockroom's Make/uv lock and over-scoped: plan forbids Make and a project package; `tox` stays the suite command.
- Preflight blocked on CI YAML TDD: already covered by constraint 6 / Challenge.
- `--cov` landed on every local `tox` run: already covered by the default-suite behavior and `env_list` lock.

## QA Results

PASS. Implementation matches the plan and acceptance criteria. Advisories do not block.

- Completeness: all five plan units are present (`tox -e coverage` → `coverage/lcov.info`, default suite coverage-free, CI upload, README badge, work on `feat/codecov-upload`). No stubs or TODOs.
- KISS / DRY: dest-dir `Path.mkdir`, nested `--cov` isolation, and split live-emit vs ini-lock tests match the plan and preflight advisories; no extra runner or product-package layer.
- YAGNI: `workflow_dispatch`, `permissions`, concurrency, and codecov.yml `comment` are stockroom copies (and preflight hygiene), not speculative product features. Make/uv/dual-root flags correctly omitted.
- Regression / Integrity: default `env_list` and `[testenv] commands` unchanged; `pytest-cov` in default deps as planned; public CLI untouched; `checkout@v7` / `codecov-action@v7` are current majors.
- Documentation: README badge + Developing note and techContext Testing Process updated; systemPatterns correctly left alone.
- Advisory (non-blocking): live emit hardcodes `--cov=summem` rather than parsing `[testenv:coverage] commands` (preflight radical, not applied). The ini lock still owns the tox surface.
- Advisory (non-blocking): `test_default_pytest_does_not_write_lcov` is a weak complement (tmp_path dest is never used by default pytest; ROOT lcov assert is skipped if a leftover file exists). `test_default_tox_commands_have_no_cov` is the real default-suite contract.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA
