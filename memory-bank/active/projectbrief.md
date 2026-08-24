# Project Brief

## User Story

As an operator or agent invoking `summem` (or `surgery.py`) on Python 3.10, I want the process to print `SumMem needs Python 3.11 or newer` and exit 1 instead of dying on `import tomllib`, so the documented floor is the first thing I see.

## Use-Case(s)

### Use-Case 1

A user whose `python3` is 3.10 runs `summem version` (or any other command). The process exits 1 with the floor message on stderr and does not mention `tomllib`.

### Use-Case 2

`surgery.py` loads repo-root `summem` via `SourceFileLoader`. On Python 3.10 that load must hit the same floor message rather than `ModuleNotFoundError: No module named 'tomllib'`.

## Requirements

1. As described in https://github.com/Texarkanine/SumMem/issues/38
2. Check `sys.version_info` immediately after `import sys` and before `import tomllib`
3. Leave any docs-toolchain Python pin alone
4. Do not reformat `summem`; surgical edit only

## Constraints

1. TDD for executable behavior
2. Suite is `tox` (or `uvx --with tox tox`); do not run the suite on this machine's bare `/usr/bin/python3` (3.10)
3. Sibling workers are editing other regions of `summem`

## Acceptance Criteria

1. `/usr/bin/python3.10 summem version` prints `SumMem needs Python 3.11 or newer` on stderr, exits 1, and does not raise `ModuleNotFoundError` for `tomllib`
2. Existing `require_python` behavior on an injected version tuple is unchanged
3. Full `tox` suite passes
