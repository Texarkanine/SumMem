# Contributing

Issues and pull requests are welcome at [Texarkanine/SumMem](https://github.com/Texarkanine/SumMem).

## The repository

| Path | What it is |
|---|---|
| `summem` | The product: one script with no `.py` suffix. Tests load this file. |
| `.summem/summem` | A symlink to `summem`, so this repository can use its own memory. Consumer repositories hold a copy instead. |
| `.summem/notes/`, `.summem/naps/` | This repository's own memory. |
| `dogfood/` | A small example store, used on [How SumMem Works](../how-it-works/index.md). |
| `surgery.py`, `migrate.py` | Repair tools run from a clone. Not part of an install. |
| `tests/` | The pytest suite. |
| `docs/` | This site. See [Docs Site](docs.md). |
| `memory-bank/` | Task notes for agents developing SumMem, kept by the [Niko](https://github.com/Texarkanine/.cursor-rules/tree/main/rulesets/niko) workflow. |
| `AGENTS.md` | Instructions for agents working on this repository, starting with the SumMem activation block. |

## Rules for changes

- **Read [Architecture](../architecture/index.md) before you change how SumMem behaves.** It names the constraints that look optional and are not.
- **Behavior changes start with a failing test.** This applies to the script, its output, and anything else it runs. The full rule is in [`always-tdd.md`](https://github.com/Texarkanine/SumMem/blob/main/.claude/rules/shared/always-tdd.md). It does not apply to prose such as these docs. Do not write tests that only check the wording of a document.
- **Keep the script short.** `summem` is copied into every repository that uses it, people read it there, and it runs inside agent turns. Use the fewest lines that do the job, and do no work the result does not need. Trade lines for speed only when you have measured the gain.
- **Keep `AGENTS.md` in step with `init`.** This repository's activation block must match what `init` prints. A test checks this.
- **Run the full test matrix before you open a pull request.** See [Testing](testing.md).

## Pull requests and releases

Title each pull request as a [conventional commit](https://www.conventionalcommits.org/): `feat`, `fix`, or `chore`, with an optional scope such as `fix(cli):`. Pull requests are squash-merged, so the title becomes the commit message on `main`.

Releases come from [Release Please](https://github.com/googleapis/release-please), configured in [`release-please-config.json`](https://github.com/Texarkanine/SumMem/blob/main/release-please-config.json):

- `feat` and `fix` cut a release. A breaking change, marked with `!` as in `feat!:`, also cuts one.
- `chore` does not cut a release.
- A release bumps `__version__` in `summem` and `surgery.py` together.

The docs site is published when a release is published. A docs change titled `chore(docs):` goes live with the next release. A docs change that should go live now can be titled `fix(docs):`, or a maintainer can run the Docs workflow by hand.

## Agents working on this repository

This repository uses SumMem for its own memory, and the Niko memory bank for task work. `AGENTS.md` tells agents how to use both. Agents should wake SumMem first, as the block at the top says.
