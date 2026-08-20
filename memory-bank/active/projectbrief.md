# Project Brief

## User Story

As a contributor, I want CI to collect Python coverage and upload it to Codecov, and a README badge for that report, so coverage is visible the same way it is on stockroom.

## Use-Case(s)

### Use-Case 1

A push or pull request runs the test suite with coverage, then uploads the report to Codecov.

### Use-Case 2

A reader of the README sees a Codecov badge that links to this repository's coverage graph.

## Requirements

1. Collect Python coverage in the stockroom style (`pytest-cov` → lcov).
2. Upload that report to Codecov from CI (`codecov/codecov-action`).
3. Add a Codecov badge on the README.
4. Do the work on a feature branch.

## Constraints

1. Follow stockroom's Python coverage-upload path (`pytest-cov` → lcov → `codecov/codecov-action`), not its dashboard-JS / dual-root setup.
2. This repository currently has no test CI job (only Release Please).
3. The product is a shebang script with no `.py` suffix.
4. Work stays on a feature branch.
5. `tox` remains the suite command. Do not add Make or a project package just to copy stockroom.
6. TDD does not govern GitHub Actions YAML that only invokes a third-party action; SumMem is not an Action. Same class as `release-please.yaml` and [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116). `codecov.yml` is Codecov config, not a product schema. The README badge is prose.
7. `CODECOV_TOKEN` is operator-provisioned. A 404 badge until the first successful upload is expected.

## Acceptance Criteria

1. `tox -e coverage` collects Python coverage for repo-root `summem` and writes a Codecov-ready lcov report.
2. Default `tox` pytest stays coverage-free (`--cov` is not in the default commands; `coverage` is not in `env_list`).
3. CI uploads that lcov report with `codecov/codecov-action`.
4. The README shows a Codecov badge for Texarkanine/SumMem.
5. The work lives on a feature branch, not `main`.
