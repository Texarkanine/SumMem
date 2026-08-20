# Progress

Instrument Release Please for semantically versioned tags, keep `summem` one file, and report the in-script version from the CLI. No Dependabot.

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified version-tracking ([SumMem#20](https://github.com/Texarkanine/SumMem/issues/20)) as Level 2
    - Wrote ephemeral memory-bank files
* Decisions made
    - Level 2: small self-contained enhancement (Release Please + CLI version report). Sibling repos already fix the config and helper-bot pattern
    - Dependabot is out of scope
* Insights
    - Stockroom is the closest match: `release-type: simple`, generic extra-files, helper-bot token, no publish job

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan: version subcommand, extra-files lockstep, workflow, living docs
* Decisions made
    - CLI surface is `summem version`, not `--version` (`init` is the analog)
    - `__version__ = "0.1.0"` with `x-release-please-version`; `release-type: simple`
    - Extra-files target repo-root `summem` only
    - No Dependabot, no CHANGELOG stub, no publish job
* Insights
    - Existing catalog and `--path` tests list a closed command set and must be extended in Unit 1

## 2026-08-20 - PREFLIGHT - COMPLETE

* Result
    - `FAIL (blocking)`
* Findings
    - The Release Please workflow is executable configuration, not prose/policy; its implementation unit has no test-first steps and violates the blocking TDD plan-encoding gate
    - CLI and Release Please lockstep units otherwise match existing code, test, and sibling-repository conventions
    - Advisory: consider deriving parser registration, `_COMMANDS`, and catalog rows from one declarative command registry

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Re-planned after the blocking preflight: unit 3 stays prose/policy
* Decisions made
    - Operator ruling: GitHub Actions that only invoke a third-party action are not executable product behavior for TDD in this repo. TDD would apply if the product were an Action
    - Did not take the command-registry advisory
* Insights
    - always-tdd’s “workflow the product runs” means product-owned executable config, not a consumer YAML for someone else’s Action

## 2026-08-20 - PREFLIGHT - COMPLETE

* Result
    - `PASS WITH ADVISORY`
* Findings
    - TDD ordering passes for CLI and Release Please lockstep units; workflow unit correctly stays prose/policy after the operator ruling
    - Advisory: schedule updating the `usage_text()` `--path` footer to exclude `version`, and consider a declarative command registry for future commands

## 2026-08-20 - BUILD - COMPLETE

* Work completed
    - `summem version` prints `__version__`
    - Release Please config, manifest, and helper-bot workflow
    - Docs: README, architecture, systemPatterns, techContext
    - `tox` 229 passed; 1 pre-existing AGENTS.md lockstep fail left alone
* Decisions made
    - Took the catalog-footer advisory; left the command-registry advisory
* Insights
    - `AGENTS.md` on this SHA already drifted from `prompt_text()` (`cloneon`, `napbefore`)

## 2026-08-20 - QA - COMPLETE

* Result
    - `FAIL (blocking)`
* Findings
    - `memory-bank/techContext.md` omits `version` from its stable CLI inventory, contradicting its own Release Please paragraph and the implementation
    - `memory-bank/productContext.md` omits repository-independent `version` behavior from its outside-repository invariant
    - The implementation otherwise matches the plan; all 8 version tests pass on Python 3.11–3.14
    - Full tox remains at 229 passed and 1 pre-existing `AGENTS.md` lockstep failure per environment
* Next step
    - Build must rerun to correct the two persistent documentation statements

## 2026-08-20 - BUILD - COMPLETE

* Work completed
    - Persistent docs now name `version` in the CLI inventory and the outside-repository invariant
* Decisions made
    - Also updated the matching sentence in `systemPatterns.md` so the next QA cannot trip on the same stale line
* Insights
    - One command added three “closed lists” in persistent briefing, not only the README table
