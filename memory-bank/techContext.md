# Tech Context

The first backend specified in `VISION.md` is a Python 3 script that writes ordinary files in git. A store is a `.summem/` directory (not `.mem/` — that name is already taken in this problem space). Per-store knobs live in `.summem/config.toml`, read with stdlib [`tomllib`](https://docs.python.org/3/library/tomllib.html) (added in 3.11; parse only). Default config is a commented template written as text, not a TOML dump. Agents talk to a stable CLI (`wake`, `note`, `nap`, `recall`, `zoom`, `start`). The on-disk format may later change, including to sqlite; the CLI table in `VISION.md` must not.

If you cannot find the CLI, a store implementation, or a test harness, you are looking at an unfinished tree, not a different product.

## Environment Setup

No runtime pin or install path exists until a project manifest or version file is added. When one appears, it is the source of truth for how to run the script. The intended floor is Python 3.11 so `tomllib` is available without a backport.

Hashing is SHA-256 from the language standard library (`hashlib` in Python 3). Do not call `sha256sum` or `openssl`. Do not use `git hash-object`.

## Build Tools

None yet. The first store is files in the git tree; there is no separate database to provision. When build or packaging files appear, link them here instead of listing commands.

License: GNU AGPL v3, in `LICENSE`.

## Testing Process

No test runner is configured yet. Executable behavior is TDD-governed by `.cursor/rules/shared/always-tdd.mdc`. The acceptance proofs the file backend must satisfy are listed in `VISION.md` under "First proof". Those are product tests, not a change-detector on the vision document.

When a runner and layout exist, point to their config here.

## Canonical documents

- `VISION.md` — design contract: agent interface, store roles, invariants, change surfaces, first proofs
- `LICENSE` — AGPL-3.0
