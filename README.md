# SumMem

[![codecov](https://codecov.io/github/Texarkanine/SumMem/graph/badge.svg)](https://codecov.io/github/Texarkanine/SumMem)

**A committed, concurrent memory for agents working in a git repository.**

SumMem is one Python script. Put it in your repository and add a short block to `AGENTS.md`. From then on, each agent that works in the repository starts its session with what earlier agents learned, and records what it learns. The memories are small files in git, so they travel with every clone and pull request. Many agents can write at once, and git merges never conflict on them.

## Documentation

**<https://texarkanine.github.io/SumMem/>**

- [How SumMem works](https://texarkanine.github.io/SumMem/how-it-works/) and [why writers never conflict](https://texarkanine.github.io/SumMem/how-it-works/no-conflicts/)
- [Quickstart](https://texarkanine.github.io/SumMem/user-guide/quickstart/) and the [User Guide](https://texarkanine.github.io/SumMem/user-guide/)
- [Architecture](https://texarkanine.github.io/SumMem/architecture/) and [Contributing](https://texarkanine.github.io/SumMem/contributing/)

## Quick start

You need a git repository, and everyone who works in it needs Python 3.11 or newer.

1. Copy [`summem`](summem) to `.summem/summem` in your repository's root, and make it executable.
2. Run `.summem/summem init`, and put the block it prints at the top of `AGENTS.md`.
3. Add `**/.summem/__pycache__/` to `.gitignore`, and commit.

The [Quickstart](https://texarkanine.github.io/SumMem/user-guide/quickstart/) has the details.

## What is in this repository

| Path | What it is |
|---|---|
| [`summem`](summem) | The script. This one file is the whole product. |
| [`surgery.py`](surgery.py) | Removes one note from a store, after a mistake. Not part of an install. |
| [`migrate.py`](migrate.py) | Rewrites nap files from older formats. Not part of an install. |
| [`docs/`](docs/) | The documentation site. |
| [`tests/`](tests/) | The test suite. |
| [`dogfood/`](dogfood/) | A small example store, used in the documentation. |
| [`.summem/`](.summem/) | This repository's own memory. |
| [`memory-bank/`](memory-bank/) | Task notes for agents developing SumMem. |
| [`AGENTS.md`](AGENTS.md) | Instructions for agents working on this repository. |

## Contributing

See [Contributing](https://texarkanine.github.io/SumMem/contributing/).

## License

The program is licensed under the [GNU AGPL v3](LICENSE). The block that `init` prints for `AGENTS.md` is also available under [0BSD](https://opensource.org/licenses/0BSD). Running the script, including by an agent, does not make your repository a covered work.

The comment block at the top of [`summem`](summem) is the authoritative statement. [Licensing](https://texarkanine.github.io/SumMem/user-guide/licensing/) explains it in plain words.
