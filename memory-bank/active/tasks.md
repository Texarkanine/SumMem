# Task: cli-help

* Task ID: cli-help
* Complexity: Level 2
* Type: simple enhancement

Replace argparse’s top-level `{wake,note,…} ...` dead end with a memo-style catalog so `--path` is visible on the first invocation. Intercept `-h <command>` before argparse consumes `-h`. Command help stays the last click. Store behavior is unchanged.

## Test Plan (TDD)

### Behaviors to Verify

- Bare missing command: `main([])` → nonzero; output names `wake`, `note`, `nap`, `zoom`, `recall`, `start`; `--path` appears on every command except `start`
- Top-level help: `main(["-h"])` and `main(["--help"])` → 0; same catalog; `--path` visible on the commands that take it
- Help flag before command: `main(["-h", "wake"])` → 0; wake help includes `--path`; not a reprint of `{wake,note,…} ...` as the only usage line
- Help flag after command: `main(["wake", "-h"])` → 0; wake help includes `--path`
- Start help: `main(["start", "-h"])` → 0; `--path` absent
- Interface constraint: catalog and top-level help mention neither `notes/`, `naps/`, nor `git`
- Footer: catalog explains that `--path` is optional and aims at a file or directory (omit → `$PWD`)
- No regression: `--path` still accepted on wake/note/nap/zoom/recall and rejected on `start`

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`, run with `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `test_*.py`; tests load the driver via `SourceFileLoader` (`conftest.load_summem`); CLI tests live in `tests/test_cli.py` and assert `main(...)` plus `capsys`; help tests do not need a git repo
- New test files: none

## Implementation Plan

### 1. CLI help catalog and dispatch — executable

- Files: `tests/test_cli.py`, `.summem/summem`

1. Stub tests: in `tests/test_cli.py`, empty cases `test_bare_invocation_prints_command_catalog`, `test_help_flag_prints_catalog`, `test_help_before_command_prints_command_help`, `test_command_help_still_shows_path`, `test_start_help_omits_path`, `test_catalog_omits_store_paths_and_git`
2. Stub interface: `usage_text() -> str` in `.summem/summem`; keep `main` signature unchanged
3. Write tests and run red: assert command names and `--path` placement; `main(["-h"])` returns 0; `main([])` nonzero; `main(["-h", "wake"])` includes `--path` and does not equal the old top-level-only usage; catalog has no `notes/`, `naps/`, or `git`; assert tokens and structure, not the full catalog poem
4. Write code and run green: `usage_text()` returns a memo-style catalog (`.summem/summem <cmd> [args]`, one line each, `--path` in brackets on every command except `start`, footer for `--path` like memo’s `--global` paragraph). `main` inspects argv **before** `parse_args`: empty → catalog, nonzero; `-h`/`--help` alone → catalog, 0; `-h`/`--help` plus a known command → rewrite to `[command, "--help", ...]`; subparser `--path` gets a one-line help string. Do not treat `-h` as an unknown command.

**Build:** done. `_cli_argv` copies argv (`None` → `sys.argv[1:]`); `parse_args(args_list)` so `-h wake` rewrite is not discarded.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing argparse in `.summem/summem`
- Existing `tests/test_cli.py` path-flag coverage

## Challenges & Mitigations

- Argparse still owns `-h` if intercept runs after `parse_args`: rewrite and catalog short-circuit must be the first argv handling in `main`
- Exact-string catalog tests become change-detectors: assert required tokens (`wake`, `--path`, footer idea) and forbidden ones (`notes/`, `naps/`, `git`), not byte-for-byte prose
- VISION forbids mentioning git in the agent interface: footer says walk-up / nearest store / `$PWD`, not git root
- `summem -h wake` must not become memo’s `No such command: -h`: `-h` is help even when a command follows

## Pre-Mortem

- Catalog copies memo so closely that `-h` is an unknown command and the ratchet dies on the first `-h`: already covered by Challenge 4 and constraint “`-h` is help”
- Help tests lock the poem and fail on wording tweaks while missing a real regression (`-h wake` still broken): already covered by Challenge 2
- Intercept is added but `required=True` empty argv still hits argparse first: already covered by Challenge 1; build step 4 states intercept-before-parse as the order that cannot be reordered

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
