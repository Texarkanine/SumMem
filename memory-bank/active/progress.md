# Progress

Make SumMem CLI help a memo-style ratchet, then fold accepted PR #5 review fixes into the same task.

**Complexity:** Level 2

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent after scopes was already shipped: help discoverability, not a second scopes build
    - Classified as Level 2 (self-contained help/usage enhancement in one driver)
* Decisions made
    - Inspiration is bare `~/.optmem/memo` (catalog of copy-paste lines plus a footer for the cross-cutting flag)
    - `-h` is help, not an unknown command (unlike memo’s `No such command: -h`)
* Insights
    - `summem -h wake` reprints top-level help today because argparse consumes `-h` before the subcommand

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 plan: catalog + `-h <command>` dispatch in `.summem/summem`, tests in `tests/test_cli.py`
* Decisions made
    - Assert tokens and forbidden words, not the full catalog poem
    - Intercept argv before `parse_args`; `-h` is help, not an unknown command
    - Footer explains `--path` without mentioning git
* Insights
    - Bare `memo` is one page of copy-paste lines plus a cross-cutting-flag paragraph; SumMem still wants a last click (`<command> -h`) because argparse subcommands have more flags than memo

## 2026-08-19 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated the cli-help plan against `.summem/summem` argparse, `tests/test_cli.py`, and `tests/test_proof_reject.py`
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is acceptable as-is; TDD order is correct; no change-detector strike; no in-phase plan edits
    - Advisories are for the builder: `argv is None`, stdout vs stderr, footer/`--help` asserts, characterization tests already green, do not collide with `catalog_text`
* Insights
    - Today `main([])` is argparse’s `{wake,note,…}` usage on stderr (rc 2); `main(["-h", "wake"])` reprints top-level help; `main(["wake", "-h"])` already shows `--path`

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - `usage_text()` memo-style catalog; argv intercept; `--path` help on subparsers
    - 6 new tests in `tests/test_cli.py`; 183 pytest passed
* Decisions made
    - Missing command → catalog on stderr, rc 2; `-h` → catalog on stdout, rc 0
    - `-h <command>` rewritten to `[command, "--help"]` without mutating the caller’s list
* Insights
    - `parse_args(argv)` would have thrown away the rewrite; it has to be `parse_args(args_list)`

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the CLI-help implementation against the Level 2 plan, project brief, and system patterns
    - Checked KISS, DRY, YAGNI, completeness, regression, integrity, and documentation
    - Ran the complete pytest suite: 183 passed
* Decisions made
    - Accepted the implementation as-is with no blocking findings
    - Accepted `_cli_argv` as a necessary, small deviation that preserves normal `main()` invocation and caller input
* Insights
    - The handwritten catalog and pre-argparse dispatch remain narrow and aligned with the intended first-invocation help ratchet

## 2026-08-19 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-cli-help.md`
    - Surgical `systemPatterns.md`: top-level help is `usage_text()`, not argparse
* Decisions made
    - productContext skip: no new audience or use case
    - techContext skip: still one shebang and the same pytest runner
* Insights
    - `parse_args(argv)` discards a `-h <command>` rewrite; the copy has to reach parse
    - A flag that never appears on the first usage line is invisible, even when the code is shipped

## 2026-08-19 - REWORK INITIATED

* Work completed
    - Operator folded a follow-up into cli-help instead of archiving: require a repository, strip the cwd fallback
* Decisions made
    - Not in a repository is an error for store commands, not a silent store in `$PWD`
    - Help still works without a repository so the ratchet does not depend on being in one
    - Error text must not say “git”
* Insights
    - The no-repo path was one `return cur` plus a VISION parenthetical; it was not a second mode

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE (rework)

* Work completed
    - Classified the repository-required supplement as Level 1
* Decisions made
    - Store commands error when `find_store_parent` finds no `.git`; help does not
    - L1: skip plan and preflight; go to build

## 2026-08-19 - BUILD - COMPLETE (rework)

* Work completed
    - `find_store_parent` raises; start probes before mkdir; VISION fallback struck
    - 3 tests in `tests/test_cli.py`; 186 pytest passed
* Decisions made
    - Error text is `not in a repository` (no “git”)
    - Help remains wait-free of a repository so the ratchet still works from `/tmp`
* Insights
    - `start` never called `find_store_parent`; it had to probe the target (or its parent) before creating directories

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the repository-required rework against the project-brief Rework section, VISION, and system patterns
    - Checked KISS, DRY, YAGNI, completeness, regression, integrity, and documentation
    - Wrote `memory-bank/active/.qa-validation-status` with `PASS`
* Decisions made
    - Accepted the implementation as-is: raise in `find_store_parent`, `start` probe-before-mkdir, help still wait-free of a repository
    - Advisories only: `systemPatterns.md` does not yet restate the no-repo failure; wake/start/`-h` tests cover the distinct paths
* Insights
    - `start` could not ride `resolve_parent`; the repo check has to aim at the target (or its parent) or it would mkdir first

## 2026-08-19 - REWORK INITIATED

* Work completed
    - Operator folded PR #5 review items into cli-help instead of archiving
* Decisions made
    - Fix judge items 1, 2, 5, 6, 8, 9, 10, 11, 13, 14, 15, 17, 18, 19, and the item 21 comment
    - Driver stays at repo-root `summem`; `dogfood/` remains a toy store; root `.summem/` stays reserved
    - Unknown argv already fails argparse; `note` must still be an explicit branch so fallthrough cannot write a note
    - Deterministic tests (monkeypatch unreadable `.tree`); accurate test names; VISION must not mislead
* Insights
    - `./dogfood/.summem/summem "raw invocation of random stuff"` already prints argparse invalid choice; the 19 fear is leftover-cmd-as-note, not unknown-token-as-note

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE (rework)

* Work completed
    - Classified the PR #5 review punch list as Level 2
* Decisions made
    - Not L1: driver, tests, and VISION move together
    - Not L3: no design fork; each item names the change
* Insights
    - Item 19 is an explicit `note` arm so fallthrough cannot write a note; argparse already rejects unknown tokens

## 2026-08-19 - PLAN - COMPLETE (rework)

* Work completed
    - Wrote Level 2 plan: eight steps, TDD on executable items, VISION/comment as prose
* Decisions made
    - SCRIPT first so the suite can run
    - Recall prints `format_wake_line` over `list_view`, then tree children
    - Auto-create docs follow the code (any store command at root)
    - Item 17 stays in `test_proof_reject.py` even though `test_unknown_prefix_is_error` exists
* Insights
    - Unknown argv already cannot write a note; the `note` arm is leftover-cmd insurance

## 2026-08-19 - PREFLIGHT - FAIL (fixable)

* Work completed
    - Gemini preflight: missed printed `.summem/summem` strings, their tests, and persistent briefing
* Decisions made
    - Re-plan: printers say `summem`; reject `sys.argv[0]` (pytest)
    - VISION examples and systemPatterns/techContext move with the driver
* Insights
    - `ensure_store` still copies into `.summem/summem`; that is a store-local copy, not the committed source

## 2026-08-19 - PLAN - COMPLETE (rework, after preflight)

* Work completed
    - Added plan steps 2 and 10 for printed invocations and persistent briefing
* Decisions made
    - Hardcode printed name `summem`, not basename of argv
* Insights
    - Catalog tests already match `summem {name}` with or without the `.summem/` prefix

## 2026-08-19 - PREFLIGHT - FAIL (fixable)

* Work completed
    - GPT preflight: catalog prefix has no red test; zoom CLI cases incomplete
* Decisions made
    - Add `test_catalog_omits_store_driver_path`; add CLI zoom malformed + OSError cases
    - Accept `CLI_NAME = "summem"` as the one printed name
* Insights
    - `"summem wake" in catalog` is already true of `.summem/summem wake`

## 2026-08-19 - PLAN - COMPLETE (rework, after second preflight)

* Work completed
    - Tightened steps 2 and 4 so the catalog prefix and CLI zoom have reds
* Decisions made
    - One `CLI_NAME` constant feeds the three printers
* Insights
    - In-process `zoom_text` tests do not prove `main` sanitizes stderr; CLI cases do

## 2026-08-19 - PREFLIGHT - FAIL (fixable)

* Work completed
    - Opus preflight: malformed-JSON zoom already raises ValueError (JSONDecodeError subclass); second loads_tree site untested
* Decisions made
    - Assert `unreadable pack`, not merely ValueError
    - Add nested-id + sibling-bad-tree CLI case; put CLI zoom tests in `test_cli.py`
* Insights
    - A local untracked `.summem/summem` can make collection succeed; SCRIPT equality is still red

## 2026-08-19 - PLAN - COMPLETE (rework, after third preflight)

* Work completed
    - Tightened step 4 so the JSON wrap and the nested walk have real reds
* Decisions made
    - Sibling bad tree continues; target bad tree is `unreadable pack`
* Insights
    - Leaked parser text is why “raises ValueError” is not a red

## 2026-08-19 - PREFLIGHT - COMPLETE (FAIL)

* Work completed
    - Validated the rework plan (PR #5 review items) against `summem`, `tests/`, `VISION.md`, and memory bank files
    - Wrote `memory-bank/active/.preflight-status` with first line `FAIL (fixable)`
* Decisions made
    - Found missing updates for hardcoded `.summem/summem` paths in the driver script (`usage_text`, catalog, prompts), tests, and `VISION.md`
    - Found missing updates for `systemPatterns.md` and `techContext.md` to reflect the new `summem` repo-root convention
* Insights
    - Relying on static hardcoded driver paths (`.summem/summem`) throughout the codebase creates brittle tests and output; using `os.path.basename(sys.argv[0])` dynamically solves this.

## 2026-08-19 - PREFLIGHT - COMPLETE (FAIL)

* Work completed
    - Re-validated the revised PR #5 rework plan against the driver, affected tests, VISION, and persistent briefing
    - Wrote `memory-bank/active/.preflight-status` with first line `FAIL (fixable)`
* Decisions made
    - Prior driver-path, downstream-test, VISION, and persistent-briefing findings are resolved by the revised plan
    - Build remains gated on explicit red coverage for the `usage_text()` executable-name change and CLI zoom handling of both malformed and unreadable trees
* Insights
    - Existing `"summem wake"` catalog coverage also matches `.summem/summem wake`, so it cannot drive the planned prefix change
    - A direct malformed-tree `zoom_text()` test does not prove CLI rc/stderr behavior or the separate `OSError` path

## 2026-08-19 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-validated the revised PR #5 rework plan against the driver, affected tests, VISION, and persistent briefing
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is acceptable as-is; TDD order is correct; no change-detector strike; no in-phase plan edits
    - Added an advisory regarding silently skipping unreadable trees in `zoom` and `recall`
* Insights
    - The revised plan successfully corrects previous missing tests and executable steps for printed driver locations and tree unreadable handling.

## 2026-08-19 - BUILD - COMPLETE (rework)

* Work completed
    - SCRIPT, `CLI_NAME`, recall/zoom degrade, `ENTRY_CHARS` prompt, test accuracy, explicit `note` arm, VISION + persistent briefing
    - 197 pytest passed
* Decisions made
    - Keep operator wake footer `You are up to speed.`
    - Skip stderr warnings on unreadable sibling trees (wake-style silent degrade)
* Insights
    - CLI wake line-count proofs must include the footer; `wake_text` tests do not

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Semantic QA on the review punch list; 197 pytest
    - Wrote `memory-bank/active/.qa-validation-status` with `PASS`
* Decisions made
    - Accepted the implementation; advisory only on a leftover config-command sentence
* Insights
    - `systemPatterns.md` still named an explicit config command after VISION dropped it

## 2026-08-19 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-cli-help.md`
    - Struck the leftover config-command sentence in `systemPatterns.md`
* Decisions made
    - productContext and techContext already matched the driver move from build
* Insights
    - Asserting `ValueError` is not a red when `JSONDecodeError` already is one

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the PR #5 rework against the Level 2 plan, project brief, system patterns, and canonical VISION
    - Checked KISS, DRY, YAGNI, completeness, regression, integrity, and documentation
    - Ran the complete pytest suite: 197 passed
* Decisions made
    - Accepted the implementation as-is with no blocking semantic findings
    - Recorded the stale “explicit config command” sentence in `systemPatterns.md` as a nonblocking documentation advisory
* Insights
    - Full-view recall and selective bad-tree degradation preserve useful results without making unrelated corruption fatal

