# Progress

Make SumMem CLI help a memo-style ratchet: bare invocation lists every command’s shape including `--path`; `-h <command>` opens that command’s help.

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
