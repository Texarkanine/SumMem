# Project Brief

## User Story

As a contributor running the SumMem test matrix, I want each tox env to run pytest with `pytest-xdist` (if that is safe) so that the ~346 tests inside an env are not forced to run one at a time.

## Use-Case(s)

### Investigate within-env parallelism

Run the suite under `pytest-xdist` and record whether flock tests, the session `summem` fixture / `sys.modules["summem"]`, subprocess CLI proofs, git worktree/merge proofs, and `tox -e coverage` stay correct.

### Apply xdist if the investigation passes

Add `pytest-xdist` to tox testenv deps, pass parallel worker args by default, mark only the tests that must stay serial, and update README / `techContext.md` / `.cursor/rules/SumMem-testing.mdc` if the default iteration command changes.

## Requirements

1. Investigate whether `pytest-xdist` (`-n auto` or similar) is safe for this suite, as specified in [issue #64](https://github.com/Texarkanine/SumMem/issues/64).
2. If safe (or safe with markers): add `pytest-xdist` to tox deps; default testenv passes parallel worker args; full `tox` py311–py314 is green with xdist enabled.
3. Tests that must run serially are explicitly marked; the count is justified in the PR or issue comment.
4. If unsafe: document why and close or narrow the issue; do not turn xdist on by default.

## Constraints

1. This is within-env parallelism, not parallel tox environments (#63).
2. Coordinate with #63's session-scoped `summem` fixture (already landed) so xdist and that fixture do not fight.
3. Do not remove process-level proofs for speed. Do not add `pytest-testmon` or coverage-based test selection.
4. `tox -e coverage` may need different xdist settings or stay serial.

## Acceptance Criteria

1. Written outcome of the investigation (safe / unsafe / safe with markers); if unsafe, document why and close or narrow scope.
2. If applied: `pytest-xdist` in tox deps; default testenv passes parallel worker args; full `tox` py311–py314 green with xdist enabled.
3. Any tests that must run serially are explicitly marked; count is justified in the PR/issue comment.
4. README, `techContext.md`, and `.cursor/rules/SumMem-testing.mdc` updated if the default iteration command changes.
