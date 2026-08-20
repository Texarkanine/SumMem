# Progress

Wire Python coverage collection and Codecov upload (stockroom-style) plus a README badge, on a feature branch.

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed: add Python coverage collection and Codecov upload, following stockroom's Python path, plus a README badge, on a feature branch
    - Determined Level 2
* Decisions made
    - Level 2: small self-contained enhancement (CI/tooling + badge), not a product-architecture change
* Insights
    - The only GitHub workflow today is Release Please; coverage mentions in README/techContext are about not using coverage-based test selection, not reporting

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 plan: tox coverage env, live lcov test, CI upload, README badge
    - Validated `pytest-cov --cov=summem` on the shebang script
    - Put the consumer-Actions TDD ruling in the brief before preflight
* Decisions made
    - `--cov=summem` (not `--cov=.`); `coverage` stays out of default `env_list`
    - Do not subprocess `tox` from pytest; lock the env in `tox.ini` and prove measurement with nested pytest
    - Follow stockroom's Python upload (`codecov-action@v7`, status checks off, `fail_ci_if_error: false`), not Make/uv
* Insights
    - Adding test CI is in scope only because upload needs a job; no multi-version matrix in this task

## 2026-08-20 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated the Level 2 plan against tox.ini, tests, CI, README, stockroom’s Python upload path, and always-tdd
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is acceptable as-is; no TDD swap or change-detector strike
    - Consumer Actions YAML / codecov.yml / README badge remain out of product TDD (brief constraint 6)
* Insights
    - Live nested `--cov` will also run under CI `tox -e coverage`; isolate `COVERAGE_FILE` so the child cannot collide with the outer session
    - Lcov parent dir should be created in the coverage env; the live test’s `tmp_path` will not catch a missing `coverage/`

## 2026-08-20 - BUILD - COMPLETE

* Work completed
    - TDD for coverage collection (stub → red → green); 4 new tests
    - `tox -e coverage` emits `coverage/lcov.info`; CI uploads it; README badge added
    - tox 236 passed on py311–py314
* Decisions made
    - Live emit in `tests/test_coverage_collection.py`; ini locks in `tests/test_tox_runner.py`
    - Isolate nested `--cov` with `COVERAGE_FILE` under `tmp_path`; mkdir via `Path.mkdir`; pin `base_python = py311`
    - Did not drive the live test from the tox command string (preflight radical, not applied)
* Insights
    - `--cov=summem` works on the no-suffix shebang; nested `--cov` under `tox -e coverage` needs a clean child env
