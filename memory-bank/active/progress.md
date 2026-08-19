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
