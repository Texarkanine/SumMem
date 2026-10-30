# Project Brief

## User Story

As a reviewer of draft PR #90, I want the root-excision fold request pinned again and the docs to match the printed verb and the serial test command, so that the branch fixes the real coverage hole and the two doc defects without locking prompt wording.

## Use-Case(s)

### Use-Case 1

A real root-store excision that leaves the view over budget prints a `Run:` line naming the two oldest remaining short ids, and the excised id is absent from stdout.

### Use-Case 2

A reader of the README sample note output and `docs/surgery.md` Aftercare sees `Summarize these two`, the line `fold_request` prints.

### Use-Case 3

A reader who copies the serial py311 example runs that one test with `-n0`, not the whole suite.

## Requirements

1. Restore the root-excision checks that `test_main_prints_fold_request_when_over_budget` provided: `Run:` names the two oldest remaining short ids, and the excised id is absent.
2. Point the README sample note output and the `docs/surgery.md` Aftercare quote at `Summarize these two`.
3. Keep `tests/test_foo.py::test_bar` on the serial command: `uvx --with tox tox -e py311 -- -n0 tests/test_foo.py::test_bar`.

## Constraints

1. Leave the fold-prompt verb unpinned. Do not assert `Summarize these two` or `Compress these two` in tests.
2. Prompt and write-rule wording stay unpinned, per the root-wake memory and `memory-bank/techContext.md`.

## Acceptance Criteria

1. A root-store excision of one note from four loose notes at `WAKE_LINES = 2` prints a `Run:` line whose nap ids are the short ids of the two oldest remaining notes, and the excised id is not in stdout.
2. README sample output and surgery Aftercare quote `Summarize these two`.
3. The serial Developing command includes `-n0` and `tests/test_foo.py::test_bar`.
