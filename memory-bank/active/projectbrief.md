# Project Brief

## User Story

As a contributor iterating on SumMem locally, I want a faster full tox matrix, a cheaper default test command, and a session-scoped `summem` fixture so that local verification is not four serial Python passes plus ~200 repeated `SourceFileLoader` loads.

## Use-Case(s)

### Full-matrix verification

An agent or operator runs one tox invocation that exercises py311–py314 concurrently and finishes in about one environment's wall time, without two overlapping tox processes stomping the same `.tox/` env.

### Cheap iteration

An agent iterating on a change runs `tox -e py311` (or a single test/file under that env) by default, and runs the full declared matrix only at end-of-work verification.

### Shared driver load

Tests obtain the loaded `summem` module from a session- or module-scoped pytest fixture instead of calling `load_summem()` per test. Tests that monkeypatch the loaded module keep isolation.

## Requirements

1. Parallelize tox environments via a single orchestrator invocation (e.g. `tox run-parallel -j auto`), documented as the full-suite command and/or wired in `tox.ini` if there is a clean config hook.
2. Add `.cursor/rules/SumMem-testing.mdc` matching project rule conventions: default iteration `tox -e py311` (or a single test/file); full tox only at end-of-work; do not overlap tox on the same env in one checkout.
3. Replace per-test `load_summem()` calls with a session- or module-scoped pytest fixture in `tests/conftest.py`. Tests that monkeypatch the loaded module need explicit handling.
4. Update README and/or `memory-bank/techContext.md` Testing Process so the documented full-suite command matches.
5. TDD for any test-infra contract changes (fixture behavior; tox parallel docs contract if tested).
6. Suite stays green on py311–py314.

## Constraints

1. Do not change product behavior.
2. Do not add `pytest-xdist` within an env (separate issue).
3. Do not add `pytest-testmon` or other coverage-based selection (explicitly rejected).
4. Do not delete or merge process-level git/worktree proofs.
5. Do not expand CI to all four Pythons (optional follow-up).
6. Two concurrent `tox -e py311` in the same repo stomp; the orchestrator must be a single invocation.

## Acceptance Criteria

1. Parallel env execution is the documented full-suite command (or wired in `tox.ini` if there is a clean config hook); README and/or `memory-bank/techContext.md` Testing Process updated.
2. `.cursor/rules/SumMem-testing.mdc` exists and matches project conventions (glob/paths as other SumMem rules use).
3. Session fixture lands; suite stays green on py311–py314.
4. TDD for any test-infra contract changes.

Spec: [issue #63](https://github.com/Texarkanine/SumMem/issues/63).
