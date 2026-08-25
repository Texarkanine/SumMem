# Project Brief

## User Story

As an agent invoking SumMem, I want each command to skip unused stdlib imports and dataclass construction so that `version`, `init`, and help stay near the interpreter floor instead of paying a ~120 ms script-side tax.

## Use-Case(s)

### Use-Case 1

An agent runs `.summem/summem version` (or `init`, or `-h`). The process must not import `tomllib`, `fcntl`, or `subprocess`, and must not import `dataclasses`.

### Use-Case 2

Store commands (`wake`, `note`, `nap`, `zoom`, `recall`, `start`) still resolve a store, fold, heal, and print the same CLI. Tests still load repo-root `summem` via `SourceFileLoader`.

### Use-Case 3

Python 3.10 still prints `SumMem needs Python 3.11 or newer` and exits 1 before any `tomllib` import. The `sys.version_info` check stays immediately after `import sys`.

## Requirements

1. Replace the five frozen dataclasses (`NoteChild`, `Tree`, `NapChild`, `ViewNode`, `ProjectedNode`) with plain `__slots__` classes (or equivalent). Keep the public field names tests already use.
2. Provide a `_replace` helper or method equivalent to `dataclasses.replace` for `ProjectedNode` in `_prepare_nap`. Do not keep `from dataclasses import replace`.
3. Import `subprocess`, `fcntl`, `random`, and `tomllib` only on the commands that need them.
4. `import dataclasses` is gone from the driver.
5. Hand-rolled dispatch instead of `argparse` is optional, and only if (1) and (2) still leave argparse as the leftover. `usage_text` is already handwritten; do not drift command `-h`.
6. Stay in class definitions, module imports, and `main` dispatch. Do not rewrite `catalog_text`, `named_ids` / `short_id` / `recall_text` / `zoom_text`, or `heal_view` / `leaf_digests` except as required to construct the new slot types.

## Constraints

1. Work only in `/home/mobaxterm/.cursor/worktrees/summem-issue-52/SumMem` on `feat/drop-dataclasses`, branched from `main` (`ddc239e`). Never edit `/home/mobaxterm/git/SumMem`.
2. Do not add a marshal / `.pyc` cache for the no-suffix driver.
3. Not this issue: catalog walk (#49), heal skip-marker (#53), recall prefix table (#50), changing the shebang, telling operators to drop pyenv shims.
4. Sibling PRs #54 / #55 / #56 also edit `summem`. Three-way merge later is expected.
5. Tests via `uv` / `tox` py311–py314. Never bare `python3` (3.10). Prove 3.10 still prints the floor message (`/usr/bin/python3.10` if present).
6. Intent is [issue #52](https://github.com/Texarkanine/SumMem/issues/52) (already-approved).

## Acceptance Criteria

1. `version` / `init` / help do not import `tomllib`, `fcntl`, or `subprocess`.
2. `import dataclasses` is gone from the driver.
3. Store commands still behave; pytest via `SourceFileLoader` still loads repo-root `summem`.
4. Python 3.10 still dies with `SumMem needs Python 3.11 or newer` before `tomllib`. The `sys.version_info` check remains immediately after `import sys`.
