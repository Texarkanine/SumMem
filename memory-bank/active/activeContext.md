# Active Context

## Current Task: codecov-upload
**Phase:** PLAN - COMPLETE

## What Was Done
- Planned opt-in `tox -e coverage` (`pytest-cov --cov=summem` → `coverage/lcov.info`), a CI job that uploads it, and a README Codecov badge.
- Tech validation: `--cov=summem` measures the no-suffix shebang; lcov `SF:` is `summem`.
- Recorded the TDD boundary: consumer Actions YAML / `codecov.yml` / badge are not product TDD; the collection command is.

## Next Step
- Preflight validation.
