# Active Context

## Current Task: codecov-upload
**Phase:** PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

## What Was Done
- Planned opt-in `tox -e coverage` (`pytest-cov --cov=summem` → `coverage/lcov.info`), a CI job that uploads it, and a README Codecov badge.
- Tech validation: `--cov=summem` measures the no-suffix shebang; lcov `SF:` is `summem`.
- Recorded the TDD boundary: consumer Actions YAML / `codecov.yml` / badge are not product TDD; the collection command is.
- Preflight: PASS WITH ADVISORY (plan acceptable as-is; isolate nested `--cov` under CI; mkdir the lcov parent in the coverage env).

## Next Step
- Build (preflight gate: PASS WITH ADVISORY).
