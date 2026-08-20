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

1. Follow stockroom's Python coverage-upload path, not its dashboard-JS / dual-root setup.
2. This repository currently has no test CI job (only Release Please).
3. The product is a shebang script with no `.py` suffix.
4. Work stays on a feature branch.

## Acceptance Criteria

1. CI produces a Codecov-ready Python coverage artifact and uploads it.
2. The README shows a Codecov badge for this repository.
3. The work lives on a feature branch, not `main`.
