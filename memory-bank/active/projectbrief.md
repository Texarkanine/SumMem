# Project Brief

## User Story

As an agent waking a repository that has no nested stores, I want root `wake` to omit all catalog guidance so I am not taught how to deal with catalogs that are not there.

## Use-Case(s)

### Use-Case 1

Root `wake` in a repo with only the git-root store. Usage prints note/nap/recall/zoom mechanics. It does not mention catalogs, catalog lines, or `wake --path`. There is no `== Additional SumMem Catalogs ==` section (already true today).

### Use-Case 2

Root `wake` in a repo with nested stores. Usage still teaches catalog lines and `wake --path`. The catalog section still lists `./path` lines.

### Use-Case 3

Bare invocation and `-h` still document catalogs and `--path`. Those surfaces do not depend on whether any nested store exists.

## Requirements

1. When root `wake` has an empty catalog, print no information about catalogs.
2. When root `wake` has a non-empty catalog, keep teaching catalog paths and `wake --path` as today.
3. Operator help (bare invocation and `-h`) still documents catalogs.

## Constraints

1. Change only the agent-facing root-wake text. Do not change operator help, `prompt_text()`, or `AGENTS.md`.
2. Do not invite agents to `start` nested stores.
3. Nested-store teaching on wake is catalog-conditional, not permanently removed.

## Acceptance Criteria

1. Root `wake` with no other started stores contains neither `catalog` guidance nor `wake --path`.
2. Root `wake` with other started stores still includes catalog how-to and `== Additional SumMem Catalogs ==`.
3. `summem -h` and bare `summem` still mention `--path` / catalogs.
