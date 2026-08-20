---
task_id: version-tracking
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: version-tracking

## SUMMARY

[SumMem#20](https://github.com/Texarkanine/SumMem/issues/20): `summem version` prints in-script `__version__`. Release Please (`simple` + generic extra-files on repo-root `summem`) can cut semver tags while `main` stays copyable. Draft [PR #22](https://github.com/Texarkanine/SumMem/pull/22). Rebased onto [#21](https://github.com/Texarkanine/SumMem/pull/21). `tox` 232 passed. Second QA passed.

## REQUIREMENTS

- Keep `summem` one file. Extra-files bump a variable inside that script (`x-release-please-version`).
- Report the version as `summem version` or `summem --version`, whichever fits the CLI. Chosen: `version` next to `init`.
- Sibling Release Please header and helper-bot names (`HELPER_APP_ID` / `HELPER_APP_PRIVATE_KEY`). Operator provisions after merge.
- No Dependabot.
- GitHub Actions YAML that only invokes a third-party action is not product TDD here.

## IMPLEMENTATION

`__version__ = "0.1.0"` beside `PROMPT_DOC`. `usage_text`, `_COMMANDS`, and argparse all name `version`. Catalog footer excludes it from `--path`. `main` writes the version and returns 0 before `resolve_parent`.

Release Please: `release-please-config.json` (`simple`, generic extra-files path `summem`, service-dog PR header), `.release-please-manifest.json` `0.1.0`, stockroom helper-bot workflow. No publish job. No CHANGELOG stub.

Living docs: README command table, architecture outside-repo sentence, persistent briefing command lists. Rebase kept main’s shorter `init` line (“print the agent prompt”) and `#21`’s `docs/agents-prompt.md` lockstep.

## TESTING

TDD in `tests/test_version.py` (print, outside-repo, extra args, `--path`, help routing, marker, manifest lockstep, extra-files path). Extended `tests/test_cli.py` catalog and `--path` reject set. First QA failed on stale CLI inventories in `techContext.md` / `productContext.md`; rework also fixed `systemPatterns.md`. Second QA PASS. After rebase: `uvx --with tox tox` 232 passed on py311–py314.

## LESSONS LEARNED

- A store-free command has three in-script lists and several briefing sentences that repeat the same inventory. Search “init and help” and parenthetical CLI lists, not only the README table.
- `x-release-please-version` is how the generic updater finds the assignment in a one-file script. Python does not use the comment.
- A command registry would only pay if more commands keep arriving. Not taken.

## PROCESS IMPROVEMENTS

First preflight FAIL (blocking) treated consumer `release-please.yaml` as TDD-governed product workflow. Same class as [Texarkanine/.cursor-rules#116](https://github.com/Texarkanine/.cursor-rules/issues/116). Operator ruling: TDD applies if SumMem *were* an Action. Write that into the brief before the first preflight when the plan adds CI that only invokes a third-party action.

## TECHNICAL IMPROVEMENTS

Nothing further. The shape if versioning had been present from the start is what shipped: one `__version__`, generic extra-files, `version` beside `init`.

## NEXT STEPS

- After merge: set repository variable `HELPER_APP_ID` and secret `HELPER_APP_PRIVATE_KEY`.
- Draft [PR #22](https://github.com/Texarkanine/SumMem/pull/22) is open on `feat/version-tracking`.
