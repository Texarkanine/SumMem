# Active Context

## Current Task: cli-help
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Memo-style `usage_text()` catalog; `main` intercepts empty / `-h` / `-h <command>` before argparse via `_cli_argv` (copy; `None` → `sys.argv[1:]`); `parse_args(args_list)`.
- `--path` help string: "aim at this file or directory".
- Six tests in `tests/test_cli.py`. Full suite 183 passed.

## Files
- `/home/mobaxterm/git/SumMem/.summem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_cli.py`

## Deviations
- Added `_cli_argv` (not named in the plan) so `argv is None` cannot catalog every `__main__` invocation, per preflight advisory 1.

## Next Step
- Reflect
