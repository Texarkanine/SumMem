# SumMem

[![codecov](https://codecov.io/github/Texarkanine/SumMem/graph/badge.svg)](https://codecov.io/github/Texarkanine/SumMem)

**A committed, concurrent memory for agents working in a git repository.**

Agents never touch the store. They run a script. The script owns every file. Wake prints a decaying view of what the repository has learned: recent notes verbatim, older notes as one-line summaries. Zoom can still open those summaries down to the original sentences after a squash merge.

The first consumer in mind is a monorepo — repo root plus many packages — but the model is any git tree. A scope is a directory that has opted in, not a `package.json` and not an actor.

## Why SumMem?

- **Many writers, no lock** — two `note`s are two paths. Git merge keeps both. There is no next-id and no cross-clone actor.
- **The view stays bounded** — recent facts stay verbatim; older facts collapse to one-line captions. Wake never refuses to print.
- **Squash does not erase sentences** — originals live in files at `HEAD`, so a fresh clone of `main` can still zoom.
- **Scopes are opt-in** — the git root auto-creates; every other store is `start <dir>`. Empty packages stay empty.
- **The script is the product** — one shebang file. The on-disk backend can change; the commands must not.

This is not a single-actor local diary ([OptMem](https://github.com/VictorTaelin/OptMem), including its machine-global store). It is not task-scoped working documentation (Niko’s `memory-bank/`).

## Quick Start

### Prerequisites

- A git repository
- Python 3.11+ (`tomllib`)

### Onboard a repository

1. Copy [summem](./summem) into `.summem/summem` in your repository's root.
2. Insert [docs/agents-prompt.md](docs/agents-prompt.md) from this repository at the top of committed `AGENTS.md`.
3. Add `**/.summem/__pycache__/` to your `.gitignore`
4. The first `wake`, `note`, `nap`, `zoom`, or `recall` creates the root store. Until someone `start`s another path, every note in the tree rolls up there.
5. (optional): run `.summem/summem start <path>` now for any sub-packages (i.e. in a monorepo)

Presence of the driver is not activation. The `AGENTS.md` block is.

### Day to day

```text
summem wake    [--path PATH]                    print this store's view
summem note    [--path PATH] TEXT               record one line
summem nap     [--path PATH] ID-A ID-B CAPTION  fold two adjacent ids
summem zoom    [--path PATH] ID                 open a nap to its children
summem recall  [--path PATH] PATTERN            search remembered text
summem start <path>                             create a store in that directory
summem init                                     print the agent prompt
summem version                                  print this script's version
```

Agents invoke `.summem/summem`. Bare `summem` is the printed name of this invocation. If `note` asks for a nap, the note is already stored; do that nap before the next action. Never edit store files by hand.

`--path` aims at work in the tree. The script walks from that path (or from `$PWD`) to the nearest started store.

## Documentation

- [Architecture](docs/architecture/index.md) — algorithm, store layout, invariants
- [Notes](docs/notes.md) — what this backend is not yet
- [docs/agents-prompt.md](docs/agents-prompt.md) — the baked session-start prompt (also printed by `init`)
- [AGENTS.md](AGENTS.md) — this repository's activation plus extra agent context

## Developing

Tests load repo-root `summem` (the path has no `.py` suffix). The suite command is `tox`. It runs pytest on `tests/` for every declared non-EOL CPython from the 3.11 floor (3.11–3.14) that is installed. `tox -e py311` is the single-interpreter form. If tox is not on `PATH`, `uvx --with tox tox` is the same command without a global install. `tox -e coverage` is the opt-in lcov command (`coverage/lcov.info`); default `tox` does not pass `--cov`. The Codecov badge 404s until the `CODECOV_TOKEN` repository secret exists and CI has uploaded once.

There is no test-result cache. This suite is heavy on `tmp_path`, git worktrees, and a no-suffix script loaded via `SourceFileLoader`; coverage-based selection (pytest-testmon and the like) is not proven not to skip a test that should run.

## License

[GNU Affero General Public License v3.0](LICENSE)
