# Project Brief

## User Story

As an agent working from repo root against a started child store, I want the fold request's `Run:` line to include `--path` when copy-paste from `$PWD` would hit a different store, so that I nap the ids that just overflowed instead of failing with `unknown id`.

## Use-Case(s)

### Nested store from repo root

An agent (or operator) runs `note --path pkg` / `nap --path pkg` from outside that store. When the child view is over budget, the printed `Run:` line is a command that still targets `pkg` if pasted from the same `$PWD`.

### Surgery after excision

`surgery.py` prints `fold_request()` after an excision that leaves the store over budget. The same `Run:` line must be copy-paste safe from the directory where surgery was invoked.

### Walk-up already correct

If `$PWD` is already under the started store, a bare `Run:` line is fine. Do not add `--path` when omitting it would still resolve to the store that produced the ids.

## Requirements

1. Investigate [issue #34](https://github.com/Texarkanine/SumMem/issues/34) and confirm the report against `fold_request()` and its callers.
2. Fix the `Run:` line when omitting `--path` would target a different store than the one that produced the ids.
3. Apply the same consideration to `surgery.py` if it has the same gap.
4. Cover the nested-store fold-request case in tests (today: `tests/test_scopes.py` and `tests/test_fold.py` leave it unasserted).

## Constraints

1. Agents never write the store; the script remains the only writer.
2. CLI output does not mention store files, hashes as paths, or git.
3. `usage_text` keeps `CLI_NAME`; the `Run:` line keeps `AGENT_BIN` (`.summem/summem`).
4. Do not change nap id resolution, walk-up, or store selection — only the fold prompt.

## Acceptance Criteria

1. From repo root, a fold request after `note --path <child>` (or `nap --path <child>`) includes `--path` such that pasting the `Run:` line from that `$PWD` targets the child store.
2. A fold request for the store walk-up from `$PWD` would already select omits `--path`.
3. Crossed-store copy-paste of a correctly hinted `Run:` line does not fail with `unknown id` for those ids.
4. Tests fail if the nested-store `Run:` line drops the path hint.
