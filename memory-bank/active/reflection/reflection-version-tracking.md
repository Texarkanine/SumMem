---
task_id: version-tracking
date: 2026-08-20
complexity_level: 2
---

# Reflection: version-tracking

## Summary

[SumMem#20](https://github.com/Texarkanine/SumMem/issues/20) is implemented: `summem version` prints in-script `__version__`, and Release Please (`simple` + generic extra-files on repo-root `summem`) can tag semver releases. Second QA passed.

## Requirements vs Outcome

Delivered as planned. CLI is the `version` subcommand, not `--version`. No Dependabot. Helper-bot names are `HELPER_APP_ID` / `HELPER_APP_PRIVATE_KEY` (operator sets them after merge). No extra command surface.

## Plan Accuracy

Sequence and files were right. The first preflight was wrong: it treated consumer GitHub Actions YAML as product TDD. The operator ruled that TDD applies if SumMem *were* an Action; we only invoke Release Please. Unit 4 named README, architecture, systemPatterns, and techContext, but not the closed CLI list inside techContext’s first paragraph or the outside-repository line in productContext — first QA failed on those.

## Build & QA Observations

Build was linear TDD. Catalog footer advisory was absorbed in Unit 1. First QA was a closed-list miss, not a behavior miss. Full tox stayed 229 passed plus the pre-existing `AGENTS.md` / `prompt_text()` space typos on this SHA.

## Insights

### Technical

- Adding one store-free command touches three in-script lists (`usage_text`, `_COMMANDS`, argparse) and several briefing sentences that repeat the same inventory. A registry would only pay if more commands keep arriving; this task correctly did not add one.

### Process

- In this repo, GitHub Actions that only invoke a third-party action are not TDD-governed product behavior. Preflight should not fail a plan for omitting tests on that YAML.
- When a new command is store-free, search persistent briefing for “init and help” and for parenthetical CLI inventories, not only the README table.

### Million-Dollar Question

The same shape: one `__version__` in the one file, generic extra-files, `version` next to `init`. That is what we built.
