---
task_id: codecov-upload
date: 2026-08-20
complexity_level: 2
---

# Reflection: codecov-upload

## Summary

CI now collects Python coverage with `tox -e coverage` (`pytest-cov --cov=summem` → `coverage/lcov.info`) and uploads it; the README has a Codecov badge. The work succeeded on `feat/codecov-upload`. Default `tox` stays coverage-free.

## Requirements vs Outcome

Delivered as asked: stockroom’s Python upload path, not Make/uv/dual-root. Added the first test CI job because upload needs one; no multi-version matrix. `CODECOV_TOKEN` remains operator-provisioned; badge 404 until the first successful upload is expected.

## Plan Accuracy

The file list and TDD split (live emit vs tox.ini contract) were right. Preflight advisories were the real plan refinement: isolate nested `--cov`, mkdir the lcov parent, pin `base_python = py311`. The feared empty report (`--cov=.` / `--cov=`) did not happen; the PoC already picked `--cov=summem`.

## Build & QA Observations

Build was clean: stub → red (no pytest-cov / empty coverage commands) → green. tox 236 on py311–py314. QA passed with two non-blocking advisories: live `--cov` argv is still a second surface, and `test_default_pytest_does_not_write_lcov` is weaker than the ini lock.

## Insights

### Technical

- `pytest-cov --cov=summem` measures the no-suffix shebang; lcov `SF:` is `summem`. Nested `--cov` under `tox -e coverage` must get its own `COVERAGE_FILE` or it shares the outer session.

### Process

- Put the consumer-Actions TDD ruling in the brief before the first preflight when the plan adds YAML that only invokes a third-party action. That is the version-tracking FAIL class (`.cursor-rules#116`).

### Million-Dollar Question

If coverage upload had been assumed from the start, the suite command would still be `tox`, with one opt-in coverage env and the first CI job running that env. That is what we built. Parsing the tox command line in the live test (preflight radical) would collapse the two argv surfaces; it was not worth a rebuild.
