---
task_id: codecov-upload
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: codecov-upload

## SUMMARY

CI collects Python coverage with `tox -e coverage` (`pytest-cov --cov=summem` → `coverage/lcov.info`) and uploads it with `codecov/codecov-action@v7`. The README has a Codecov badge. Default `tox` stays coverage-free. Shipped on `feat/codecov-upload` via draft [PR #23](https://github.com/Texarkanine/SumMem/pull/23). tox 236 passed on py311–py314. QA PASS.

## REQUIREMENTS

- Collect Python coverage the stockroom way (`pytest-cov` → lcov), not Make/uv/dual-root.
- Upload from CI. This repo had no test CI job (only Release Please).
- README Codecov badge for Texarkanine/SumMem.
- Work on a feature branch.
- `tox` remains the suite command. The product is a no-suffix shebang.
- Consumer Actions YAML / `codecov.yml` / the badge are not product TDD (same class as [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116)).
- `CODECOV_TOKEN` is operator-provisioned; badge 404 until the first successful upload is expected.

## IMPLEMENTATION

[`tox.ini`](../../../tox.ini): `pytest-cov` in default `[testenv]` deps; `[testenv:coverage]` pins `base_python = py311`, `Path.mkdir`s `{env:COVERAGE_DIR:coverage}`, then `pytest --cov=summem --cov-report=lcov:… {posargs}`. `coverage` stays out of `env_list`. Default commands stay `pytest {posargs}`.

Live emit in [`tests/test_coverage_collection.py`](../../../tests/test_coverage_collection.py) (nested `--cov` with `COVERAGE_FILE` under `tmp_path`; parent `COV_*` stripped). Ini locks in [`tests/test_tox_runner.py`](../../../tests/test_tox_runner.py).

CI: [`.github/workflows/ci.yaml`](../../../.github/workflows/ci.yaml) (`permissions: contents: read`, concurrency, upload `coverage/lcov.info`, `fail_ci_if_error: false`). Root [`codecov.yml`](../../../codecov.yml) has project/patch status off. [`.gitignore`](../../../.gitignore) ignores `.coverage`, `coverage/`, `htmlcov/`. README badge + Developing note; `techContext.md` Testing Process updated.

Did not parse `[testenv:coverage] commands` in the live test (preflight radical, not applied).

## TESTING

TDD: stub → red (no pytest-cov / empty coverage commands) → green. `tox -e coverage` wrote `coverage/lcov.info` with `SF: summem`. `uvx --with tox tox` 236 passed on py311–py314. Preflight PASS WITH ADVISORY. QA PASS (two non-blocking advisories: live `--cov` argv is a second surface; `test_default_pytest_does_not_write_lcov` is weaker than the ini lock).

## LESSONS LEARNED

- `pytest-cov --cov=summem` measures the no-suffix shebang; lcov `SF:` is `summem`. Nested `--cov` under `tox -e coverage` must get its own `COVERAGE_FILE` or it shares the outer session.
- Do not subprocess `tox` from pytest (recursion). Lock the coverage env in `tox.ini`; prove measurement with nested pytest.

## PROCESS IMPROVEMENTS

Put the consumer-Actions TDD ruling in the brief before the first preflight when the plan adds YAML that only invokes a third-party action. That is the version-tracking FAIL class.

## TECHNICAL IMPROVEMENTS

If coverage upload had been assumed from the start, the suite command would still be `tox`, with one opt-in coverage env and the first CI job running that env. That is what shipped.

## NEXT STEPS

- After merge: add repository secret `CODECOV_TOKEN`. The badge 404s until that exists and CI uploads once.
- Draft [PR #23](https://github.com/Texarkanine/SumMem/pull/23) is open on `feat/codecov-upload`.
