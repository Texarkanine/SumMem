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
