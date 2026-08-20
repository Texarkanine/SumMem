# Project Brief

## User Story

As a contributor or agent, I want one reliable command that runs this repo's pytest suite on every non-EOL CPython from our 3.11 floor, so I do not have to remember `uv run --python 3.11 --with pytest pytest` or this machine's bare 3.10.

## Use-Case(s)

### Use-Case 1

A contributor (or agent) at the repo root runs the documented command. Pytest runs the suite under `tests/` on Python 3.11 through the current non-EOL CPython (3.14 as of 2026-08-19), without using this machine's bare `python3`.

### Use-Case 2

Someone reads README Developing and `memory-bank/techContext.md` Testing Process and finds the same command. They do not need a hatchling/PyPI package.

### Use-Case 3

A result cache is used only if an off-the-shelf maintained tool can be shown not to skip a test that should run on this tmp_path / git-worktree / filesystem-store suite. Otherwise the cache is skipped.

## Requirements

1. As described in https://github.com/Texarkanine/SumMem/issues/6 — test with tox against the Python floor through current non-EOL CPython.
2. As described in https://github.com/Texarkanine/SumMem/issues/9 — one simple command that reliably runs pytest; cache only if proven reliable.
3. Floor is Python 3.11 (`tomllib`). Matrix is 3.11, 3.12, 3.13, 3.14. Do not add 3.10. If 3.14 is impractical on this machine, document the gap and still test 3.11–3.13.
4. Prefer `tox.ini` plus the existing shebang script. Do not become a hatchling/PyPI package unless tox truly needs a tiny manifest.
5. Update README Developing and `memory-bank/techContext.md` Testing Process to the same command.
6. TDD the runner: it invokes pytest on `tests/`, and the declared Pythons are the intended set. No change-detectors on README prose.
7. One Niko task, one draft PR that closes #6 and #9.

## Constraints

1. Do not change `summem` product CLI semantics. Do not edit product code except a test helper if strictly required for the runner (prefer not).
2. Do not use this machine's bare `python3` (3.10).
3. Do not build a cache library. Do not adopt rpytest. Skip pytest-testmon unless reliability is proven against these filesystem tests.
4. Do not recreate VISION/ROADMAP. Living contract is README, `docs/architecture/index.md`, `docs/notes.md`, persistent `memory-bank/`.
5. Do not expand into sqlite, hooks, `cover(T)`, or leftover `docs/notes.md` items.
6. Ponytail is not auto-on.

## Acceptance Criteria

1. `tox` (or the one documented equivalent) runs pytest on `tests/` for each declared non-EOL CPython from 3.11.
2. Declared environments are 3.11–3.14, or 3.11–3.13 with the 3.14 gap documented.
3. README Developing and techContext Testing Process name that same command.
4. No hatchling/PyPI package unless tox cannot run without a tiny manifest.
5. Cache is off-the-shelf and proven, or omitted with the reason recorded.
6. Product CLI behavior is unchanged.
