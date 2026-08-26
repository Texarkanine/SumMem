# Tech Context

The file backend is a Python 3 shebang script. A store is a `.summem/` directory (not `.mem/` — that name is already taken in this problem space). Nap captions are `.summ` (not `.sum` — that suffix is checksums). Agents invoke `.summem/summem`. This development repo’s record is repo-root `summem`; store-local `.summem/summem` is a symlink to it. `ensure_store` creates `notes/`, `naps/`, and default `config.toml` when missing. It does not copy the driver. Per-store settings live in `.summem/config.toml`, read with stdlib [`tomllib`](https://docs.python.org/3/library/tomllib.html) (added in 3.11; parse only). Default config is a commented template written as text, not a TOML dump. Agents talk to a stable CLI (`wake`, `note`, `nap`, `recall`, `zoom`, `start`, `init`, `version`). The on-disk format may later change, including to sqlite; the command table in the README must not.

Activation is the SumMem block at the top of committed `AGENTS.md`. Presence of the driver is not. `init` prints that bootstrap (`prompt_text()`). Tests load repo-root `summem`. This repository commits `.summem/notes/` (and naps when written). `.gitignore` does not ignore them.

## Environment Setup

The intended floor is Python 3.11 so `tomllib` is available without a backport. The script checks `sys.version_info` immediately after `import sys` and before any `import tomllib`, so Python 3.10 prints `SumMem needs Python 3.11 or newer` instead of dying on the import. `tomllib`, `fcntl`, `subprocess`, and `random` load inside the functions that need them; `version`, `init`, and bare help do not import them. View types are `__slots__` classes, not dataclasses. There is no project manifest and no hatchling package. Invoke the driver as `summem`. Tests must not use this machine's bare `python3` (3.10). The suite command is `tox` (or `uvx --with tox tox` if tox is not on `PATH`).

Hashing is SHA-256 from the language standard library (`hashlib` in Python 3). Do not call `sha256sum` or `openssl`. Do not use `git hash-object`.

## Build Tools

None. The product is one shebang file; there is no packaging step and no separate database to provision.

License: GNU AGPL v3, in `LICENSE`. Additional permission for running (including by an AI agent) and 0BSD terms for the agent prompt template are in the `summem` header (authoritative). `surgery.py` and `migrate.py` stay stock AGPL; they do not echo those terms.

Semver tags come from Release Please (`release-type: simple`) on `main`. Generic extra-files bump `__version__` in repo-root `summem` and `surgery.py` (`x-release-please-version`). `summem version` and `surgery.py version` print that string. `migrate.py` has no `__version__` and is not an extra-file: it is a one-shot store rewrite, not a versioned product surface. Helper-bot auth is repository variable `HELPER_APP_ID` and repository secret `HELPER_APP_PRIVATE_KEY`, provisioned after merge. GitHub Actions YAML that only invokes that third-party action is not product TDD in this repo.

## Testing Process

Tests are pytest as configured in `pytest.ini` (`testpaths = tests`). The one command is `tox`: `tox.ini` declares `py311`–`py314`, skips packaging the shebang script, and runs `pytest {posargs}`. Missing interpreters are skipped (`skip_missing_interpreters = true`); `tox -e py311` runs one version. If tox is not on `PATH`, `uvx --with tox tox` is the same command. Do not use this machine's bare `python3` (3.10). Coverage is opt-in via `tox -e coverage` (`pytest-cov --cov=summem` → `coverage/lcov.info`); default `tox` stays coverage-free. CI uploads that lcov report. They load repo-root `summem` via `SourceFileLoader` (the path has no `.py` suffix). There is no test-result cache: this suite is heavy on `tmp_path`, git worktrees, and a no-suffix script, and coverage-based selection is not proven safe here. Executable behavior is TDD-governed by `.cursor/rules/shared/always-tdd.mdc`. The process-level git, nap-rejection, and scope tests named in `productContext.md` Success Criteria are product tests, not a change-detector on a document.

## Canonical documents

- `README.md` — what it is, why, quickstart, command table
- `docs/architecture/index.md` — algorithm, store layout, invariants, change surfaces
- `LICENSE` — AGPL-3.0
