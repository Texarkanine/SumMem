# Tech Context

The first backend specified in `VISION.md` is a Python 3 shebang script at `.summem/summem` that writes ordinary files in git. A store is a `.summem/` directory (not `.mem/` — that name is already taken in this problem space). The driver is a sibling of store data inside that brand directory. Per-store knobs live in `.summem/config.toml`, read with stdlib [`tomllib`](https://docs.python.org/3/library/tomllib.html) (added in 3.11; parse only). Default config is a commented template written as text, not a TOML dump. Agents talk to a stable CLI (`wake`, `note`, `nap`, `recall`, `zoom`, `start`). The on-disk format may later change, including to sqlite; the CLI table in `VISION.md` must not.

This tree is not itself a SumMem store until a working driver is bound to an agentic hook. The committed product is `.summem/summem`. Generated store data in this repository is ignored.

## Environment Setup

The intended floor is Python 3.11 so `tomllib` is available without a backport. There is no project manifest and no hatchling package. Invoke the driver as `.summem/summem`. Tests must not use this machine's bare `python3` (3.10) or a `python3.11` pyenv shim; use `uv run --python 3.11`.

Hashing is SHA-256 from the language standard library (`hashlib` in Python 3). Do not call `sha256sum` or `openssl`. Do not use `git hash-object`.

## Build Tools

None. The product is one shebang file; there is no packaging step and no separate database to provision.

License: GNU AGPL v3, in `LICENSE`.

## Testing Process

Tests are pytest as configured in `pytest.ini`, run with `uv run --python 3.11 --with pytest pytest`. They load `.summem/summem` via `SourceFileLoader` (the path has no `.py` suffix). Executable behavior is TDD-governed by `.cursor/rules/shared/always-tdd.mdc`. The acceptance proofs the file backend must satisfy are listed in `VISION.md` under "First proof". Those are product tests, not a change-detector on the vision document.

## Canonical documents

- `VISION.md` — design contract: agent interface, store roles, invariants, change surfaces, first proofs
- `LICENSE` — AGPL-3.0
