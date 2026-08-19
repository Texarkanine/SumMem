# Progress

Make SumMem CLI help a memo-style ratchet, then require a repository for store commands.

**Complexity:** Level 1

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
