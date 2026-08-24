# Project Brief

## User Story

As an operator who dogfoods SumMem in several repositories, I want a small `AGENTS.md` bootstrap that stays put and a root `wake` that prints the versioned how-to, so upgrading a consumer is copying the script and not also editing `AGENTS.md`.

## Use-Case(s)

### Session start

An agent reads the committed bootstrap, runs one repository-root `wake`, and receives the current how-to plus the decaying memory document.

### Script upgrade

The operator copies a newer `summem` into `.summem/summem`. `AGENTS.md` is left alone. The next root `wake` prints the new note/nap/zoom/recall grammar and catalog-pull recipe.

### Compaction recovery

An agent can no longer see this conversation's root-wake usage block. The bootstrap tells it to run root `wake` again.

## Requirements

1. A small `AGENTS.md` bootstrap that does not change when the script's usage details change.
2. The initial repository-root `wake` prints the versioned how-to: note, nap, zoom/recall grammar, catalog pull.
3. A consumer upgrade does not require editing `AGENTS.md`.
4. Do this work on a feature branch, not `main`.

## Constraints

1. Activation remains the `AGENTS.md` block. Presence of the driver is not activation.
2. `init` does not write `AGENTS.md`.
3. Wake is a document. Do not print an executable command list that a cheap agent will run as a script.
4. A pull (`wake --path`) does not reprint the root usage document or the full catalog.
5. Do not add a `summem upgrade` command. Copying the script remains the upgrade path.
6. The insertable onboarding file stays lockstep with whatever bootstrap `init` prints. This repository's `AGENTS.md` may keep extra sections after that prefix.
7. The prompt template stays 0BSD. The program stays AGPL. `surgery.py` is out of scope.

## Acceptance Criteria

1. A consumer that already has the bootstrap can take a new script without editing `AGENTS.md` and receive updated how-to from root `wake`.
2. An agent that cannot see this conversation's root-wake usage block runs root `wake`.
3. Note, nap, zoom/recall grammar, and the catalog-pull recipe appear in root `wake`, not in the bootstrap.
4. Store, fold, note, nap, zoom, and recall behavior stay the same except for the root-wake document.
