# SumMem

[![codecov](https://codecov.io/github/Texarkanine/SumMem/graph/badge.svg)](https://codecov.io/github/Texarkanine/SumMem)

**A committed, concurrent memory for agents working in a git repository.**

Drop the `summem` Python script into your repo and bootstrap a few lines in your `AGENTS.md`, and all the agents that work on your repo will start remembering what's going on with it.

## Why Memory?

Many agents may work on a repository. They'll make decisions, discover facts and gotchas, and... forget it all and leave no record, unless you do something about it.

### Why Repo Memory?

If *you* set up memory for *your* agent on *your* machine via an MCP, server (local or remote), or some other means, that doesn't help other contributors. *Your* agents may one-shot changes to the repository but you'll still receive low-quality contributions from the rest of the world. The memory of what's good and how things are done needs to come along with your code.

### Why SumMem?

- **Repo-local** — memories are stored in the repository, in git. No external dependencies or servers - once you've got the repository, you've got the memory.
- **Many writers, no lock** — two memories are two distinct file paths: git merges do not corrupt memory.
- **Bounded context** — recent facts stay verbatim; older compress into summaries so the initial "remembering" is a fixed size.
- **Perfect recall when needed** — original memories of compressed summaries persist and may be surfaced on-demand.
- **Hierarchical stores** — Got a monorepo or other situation where memories should be scoped to a subdirectory? No problem; just `start <dir>` and you've got a second store.
- **Universal** — drop the script in, update your `AGENTS.md`, and jsut about every agent, everywhere, will start recalling *and* contributing memories.

## Quick Start

### Prerequisites

- A git repository
- Python 3.11+ (`tomllib`)

### Onboard a repository

1. Copy [summem](./summem) into `.summem/summem` in your repository's root.
2. Run `.summem/summem init` and insert that print at the top of committed `AGENTS.md`.
3. Add `**/.summem/__pycache__/` to your `.gitignore`
4. The first `wake`, `note`, `nap`, `zoom`, or `recall` creates the root store. Until someone `start`s another path, every note in the tree rolls up there.
5. (optional): run `.summem/summem start <path>` now for any sub-packages (i.e. in a monorepo)

### Day to day

Root `wake` prints the current agent how-to under `== SumMem Usage ==`, then any catalog of other stores, then the memories. Copying a newer script updates that how-to.

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

Agents invoke `.summem/summem`. Sometimes recording a `note` will ask for a `nap` - a compression of two adjacent notes into one summary. Agents do that and then continue on with their work; thus the memories are intelligently compressed.

`--path` aims at a file in the repo. The script walks from that path up to the nearest started store in the repository.

## Documentation

- [Architecture](docs/architecture/index.md) — algorithm, store layout, invariants
- [Emergency surgery](docs/surgery.md) — zipper-excise one raw note at the branch tip (not a shipped command)
- [Notes](docs/notes.md) — what this backend is not yet
- [AGENTS.md](AGENTS.md) — this repository's activation plus extra agent context

## Developing

Tests load repo-root `summem` (the path has no `.py` suffix). The suite command is `tox`. It runs pytest on `tests/` for every declared non-EOL CPython from the 3.11 floor (3.11–3.14) that is installed. `tox -e py311` is the single-interpreter form. If tox is not on `PATH`, `uvx --with tox tox` is the same command without a global install. `tox -e coverage` is the opt-in lcov command (`coverage/lcov.info`); default `tox` does not pass `--cov`. The Codecov badge 404s until the `CODECOV_TOKEN` repository secret exists and CI has uploaded once.

There is no test-result cache. This suite is heavy on `tmp_path`, git worktrees, and a no-suffix script loaded via `SourceFileLoader`; coverage-based selection (pytest-testmon and the like) is not proven not to skip a test that should run.

## License

The program is licensed under the [GNU AGPL v3](LICENSE). 
The prompt that is recommended for insertion into `AGENTS.md` is separately licensed under the [0BSD license](https://opensource.org/licenses/0BSD).

Additional permissions for invocation and the 0BSD terms for the agent prompt template live in the comment block at the top of `summem`. **That block is the authoritative statement.**

Summarized,

> Put the bootstrap prompt anywhere you need, with no restrictions.
>
> Invoking the script does not make the caller or the containing repo a covered work. Using the script inside your org doesn't require making any source available.
>
> Making a modified version available outside your organization — by distributing it, or by offering remote interaction with it — remains AGPL.
