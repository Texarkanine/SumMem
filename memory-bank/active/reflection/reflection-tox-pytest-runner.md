---
task_id: tox-pytest-runner
date: 2026-08-19
complexity_level: 2
---

# Reflection: tox-pytest-runner

## Summary

Shipped `tox` as the one pytest command for CPython 3.11–3.14 without a package manifest. QA passed first try. 211 tests × four interpreters.

## Requirements vs Outcome

#6 and #9 landed together. Cache skipped (not proven on this filesystem suite). No product CLI change. No hatchling/`pyproject.toml`. 3.14 stayed in `env_list`; this machine’s uv only offered 3.14.0rc3, which still ran the suite.

## Plan Accuracy

The plan’s file list and TDD sequence were right. `package = skip` validation held. No step reordering.

## Build & QA Observations

Red was three failures on the stub `tox.ini` plus a green `testpaths` assert on existing `pytest.ini`. Preflight (Gemini) and QA (GPT) both PASS with no rework.

## Insights

### Technical
- stdlib `configparser` interpolates `{posargs}` unless `interpolation=None`.
- A pytest case that subprocesses tox recurses once the suite runs under tox; parse the ini files instead.

### Process
- Nothing notable

### Million-Dollar Question

`tox.ini` + `package = skip` + existing `pytest.ini` is what you would have put here on day one. A package manifest would have been the wrong foundation for a shebang script.
