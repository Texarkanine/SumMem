---
task_id: tox-pytest-runner
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: tox-pytest-runner

## SUMMARY

`tox` is the one documented pytest command. `tox.ini` declares `py311`–`py314`, skips packaging the shebang script, and runs `pytest {posargs}` on `tests/`. No hatchling/`pyproject.toml`. No test-result cache. Closes #6 and #9.

## REQUIREMENTS

- Test every non-EOL CPython from the 3.11 floor (no 3.10).
- One reliable command for contributors and agents; uv not required.
- Cache only if off-the-shelf and proven not to skip a test that should run.
- TDD the runner contract; no README change-detectors; no product CLI change.

## IMPLEMENTATION

Added [`tox.ini`](../../../tox.ini) (`package = skip`, `skip_missing_interpreters = true`) and [`tests/test_tox_runner.py`](../../../tests/test_tox_runner.py) (stdlib `configparser`, `interpolation=None`). Ignored `.tox/`. README Developing and `memory-bank/techContext.md` Testing Process name `tox`; `uvx --with tox tox` is the no-global-install form. Did not add tox-uv as a `requires`.

## TESTING

TDD red on a stub `tox.ini` (3 failed, existing `testpaths` already green). `uvx --with tox tox`: 211 passed on 3.11.11, 3.12.11, 3.13.7, and 3.14.0rc3. Preflight PASS (Gemini). QA PASS (GPT), no rework.

## LESSONS LEARNED

- `{posargs}` needs `ConfigParser(interpolation=None)` or the braces are interpolation.
- Do not subprocess tox from pytest: the suite will run under tox and recurse.
- This machine’s uv 0.8.22 only offered CPython 3.14.0rc3; `py314` stayed in `env_list` and ran.

## PROCESS IMPROVEMENTS

Nothing notable. Plan, preflight, build, and QA were linear.

## TECHNICAL IMPROVEMENTS

None. A package manifest would have been the wrong foundation for a shebang script.

## NEXT STEPS

None. Draft PR should close #6 and #9.
