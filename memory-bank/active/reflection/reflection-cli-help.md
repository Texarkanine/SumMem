---
task_id: cli-help
date: 2026-08-19
complexity_level: 2
---

# Reflection: cli-help

## Summary

Bare `summem` and `-h` now print a memo-style command catalog with `--path` on every command except `start`. `summem -h wake` opens wake help. 183 pytest. QA passed first try.

## Requirements vs Outcome

Delivered as asked. Scopes behavior unchanged. `-h` is help, not memo’s “No such command.” Last click remains argparse subcommand help.

## Plan Accuracy

Sequence and files were right. The only extra helper was `_cli_argv`, from a preflight advisory: `argv is None` must become `sys.argv[1:]` before the empty check, and `parse_args` must see the rewritten list or `-h wake` is thrown away.

## Build & QA Observations

TDD red was real on the catalog and on `-h wake`; `wake -h` / `start -h` were already green. QA found nothing blocking.

## Insights

### Technical
- Intercepting argv is incomplete unless `parse_args` receives the copy. `parse_args(argv)` discards the `-h <command>` rewrite.

### Process
- A shipped `--path` that never appears on the first usage line is invisible. That is how this repo looked like it had not built scopes.

### Million-Dollar Question

If the first invocation had always been a catalog, argparse would never have been the top-level UI. The still-more-elegant version is to format those lines from the same subparser table that parses, so a new command cannot make help lie. This task handwritten `usage_text()` instead; that is the drift surface.
