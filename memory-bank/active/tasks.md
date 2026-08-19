# Task: cli-help

* Task ID: cli-help
* Complexity: Level 2
* Type: bug fix / review punch list

Fold accepted PR #5 review items into the driver, tests, and VISION. Driver stays at repo-root `summem`. `dogfood/` stays a toy store. Root `.summem/` stays reserved.

## Test Plan (TDD)

### Behaviors to Verify

- SCRIPT path: `tests/conftest.py` / `tests/gitutil.py` `SCRIPT` → repo-root `summem` exists and loads
- Recall of a loose note older than `WAKE_LINES` → that sentence is found
- Recall of a nap caption / tree leaf → still found (no wake-window regression)
- Recall when a nap `.tree` is malformed → empty or partial result, no exception
- CLI `zoom` of a nap whose `.tree` raises `OSError`/`JSONDecodeError` → rc 1, no traceback
- `fold_request` / over-budget `note` with `ENTRY_CHARS = 140` in config → prompt says 140, not 280
- `write_nap` overlapping-note case → rematerialized `pa` is still on disk (tight assert)
- `chmod`-independent unreadable `.tree` → wake prints one pack line
- CLI `nap` of two syntactically valid unknown ids on an initialized store → nonzero, no new payloads
- CLI leftover: `note` still writes; an unknown token still does not write a note (argparse invalid choice)
- Printed invocations (`usage_text`, `catalog_text`, `fold_request`) name `summem`, not `.summem/summem`
- Bare/`-h` catalog does not contain `.summem/summem`
- CLI `zoom` of a nap whose `.tree` is malformed JSON → rc 1, no traceback, no store paths
- CLI `zoom` of a nap whose `.tree` read raises `OSError` → rc 1, no traceback, no store paths

### Test Infrastructure

- Framework: pytest via `uv run --python 3.11 --with pytest pytest`
- Test location: `tests/`
- Conventions: `test_*.py`, `load_summem()` + `init_repo`, monkeypatch cwd/`WAKE_LINES`
- New test files: none

## Implementation Plan

### 1. SCRIPT points at repo-root `summem` — executable

- Files: `tests/conftest.py`, `tests/gitutil.py`, `tests/test_cli.py`

1. Stub tests: add `test_script_is_repo_root_driver` in `tests/test_cli.py` (empty)
2. Stub interface: none (path constant only)
3. Write tests and run red: `SCRIPT == ROOT / "summem"` (a local untracked `.summem/summem` may exist, so collection can succeed today; the equality is the red)
4. Write code and run green: both `SCRIPT` assignments and their docstrings

### 2. Printed invocations say `summem` — executable

- Files: `summem` (`usage_text`, `catalog_text`, `fold_request`), `tests/test_fold.py`, `tests/test_scopes.py`, `tests/test_proof_scopes.py`

1. Stub tests: add `test_catalog_omits_store_driver_path` in `tests/test_cli.py`; edit fold/scope path asserts
2. Stub interface: add `CLI_NAME = "summem"` next to `_COMMANDS`
3. Write tests and run red: `usage_text()` has no `.summem/summem` and catalog lines start with `  summem `; `Run: summem nap `; `summem wake --path pkg`
4. Write code and run green: `usage_text`, `catalog_text`, and `fold_request` compose from `CLI_NAME`. Do **not** use `sys.argv[0]`. `ensure_store` still copies the driver to each store's `.summem/summem`

### 3. Recall searches the store, degrades on bad trees — executable

- Files: `summem` (`recall_text`), `tests/test_recall.py`

1. Stub tests: `test_recall_matches_loose_note_outside_wake_window`, `test_recall_malformed_tree_does_not_raise`
2. Stub interface: none (`recall_text` exists)
3. Write tests and run red: `WAKE_LINES=4` and 11 loose notes, `recall n0` nonempty; planted `{not json` `.tree` + `recall_text` returns without raising
4. Write code and run green: iterate `list_view` + `format_wake_line`, then tree children; wrap `loads_tree` in `_TREE_PARSE_ERRORS` and skip

### 4. Zoom degrades on unreadable trees — executable

- Files: `summem` (`zoom_text`), `tests/test_zoom.py`

1. Stub tests: `test_zoom_unreadable_tree_is_unreadable_pack` in `tests/test_zoom.py`; `test_cli_zoom_malformed_tree_returns_1`, `test_cli_zoom_oserror_returns_1`, `test_cli_zoom_nested_id_skips_sibling_bad_tree` in `tests/test_cli.py` (CLI arms live there)
2. Stub interface: none
3. Write tests and run red: `{not json` → `zoom_text` raises `ValueError` matching `unreadable pack` (today it leaks the JSON parser message because `JSONDecodeError` is a `ValueError`); CLI same message, rc 1, no traceback/store paths; `read_bytes` → `OSError` same CLI asserts; zoom a nested id while another view nap has a bad tree → still prints the child (today the second `loads_tree` raises first)
4. Write code and run green: both `loads_tree` sites in `zoom_text` use `try/except _TREE_PARSE_ERRORS` → `ValueError("unreadable pack")` on the target pack, `continue` on a sibling pack in the nested walk. CLI already maps `ValueError` to rc 1

### 5. Fold prompt uses `ENTRY_CHARS` — executable

- Files: `summem` (`fold_request`), `tests/test_fold.py`

1. Stub tests: `test_fold_request_uses_config_entry_chars`
2. Stub interface: none
3. Write tests and run red: config `ENTRY_CHARS = 140`, over-budget pair, prompt contains `140` and not `280`
4. Write code and run green: `fold_request` formats `knobs(parent)["ENTRY_CHARS"]`; keep existing 280 asserts (default)

### 6. Test accuracy — executable

- Files: `tests/test_nap.py`, `tests/test_wake_expand.py`, `tests/test_zipper.py`, `tests/test_proof_reject.py`

1. Stub tests: `test_nap_unknown_ids_rejected_without_writing` in `test_proof_reject.py`; tighten/rename/monkeypatch are edits of existing cases
2. Stub interface: none
3. Write tests and run red: initialized store, `nap deadbeef cafebabe "x"` via `_run_nap`, nonzero, `_payload_files` empty. Existing `test_unknown_prefix_is_error` already covers a non-empty store; this one is the proof-file empty-payload case
4. Write code and run green:
    - `test_write_nap_note_inside_adjacent_nap_raises`: `assert pa.name in _payload_names(repo)`; drop unused `pb`
    - `test_unreadable_tree_does_not_split`: monkeypatch `Path.read_bytes` to `PermissionError` for that tree only
    - rename `test_cli_nap_overlapping_ids_exits_0_without_concat` → `…_exits_1_…`
    - implement the new reject test (behavior already in `resolve_id`; test is the change)

### 7. Explicit `note` arm; drop dead `present` guard — executable

- Files: `summem` (`main`), `tests/test_cli.py`

1. Stub tests: `test_unknown_token_does_not_write_a_note` (documents the argparse gate the operator already saw)
2. Stub interface: none
3. Write tests and run red: `main(["raw invocation of random stuff"])` nonzero, `notes/` empty if a repo exists; `main(["note", "ok"])` still writes
4. Write code and run green: `if args.cmd == "note":` wraps the write path; any other leftover `cmd` writes usage and returns 2. Remove `present` check; `write_nap` after `resolve_id`

### 8. Same-children comment — prose/policy

- Files: `tests/test_nap.py`
- No tests: prose/policy artifact

1. One comment above the cross-repo `write_nap`: ids match because both repos wrote the same text at the same timestamps

### 9. VISION wording — prose/policy

- Files: `VISION.md`
- No tests: prose/policy artifact

1. Scopes: outside a repository every store command fails, including `start`. `start <dir>` is the no-walk-up exception **inside** a repository
2. Drop “or an explicit config command”
3. One root auto-create rule: git root on first `wake`, `note`, `nap`, `zoom`, or `recall`; other paths only via `start`. Align the Onboarding sentence and the Empty-packages invariant
4. Example invocations use `summem`, not `.summem/summem`. Keep the fact that `ensure_store` copies the driver into a store's `.summem/summem`

### 10. Persistent briefing — prose/policy

- Files: `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. Committed driver is repo-root `summem`. Tests load that path. Each store may hold a copy at `.summem/summem`
2. Do not rewrite archives or ROADMAP in this task

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest suite
- `uv run --python 3.11 --with pytest pytest`

## Challenges & Mitigations

- SCRIPT change unblocks the whole suite; do step 1 first or later reds cannot run
- `test_over_budget_note_requests_equal_grain_ones` hardcodes 280; keep it as the default-knob case
- `fold_request(repo, n)` tests do not pass `ENTRY_CHARS`; read `knobs(parent)` inside `fold_request`
- Recall output shape: print `format_wake_line` for every matching view row so caption tests still see `folded pair`
- Item 19: unknown tokens already die in argparse; the new arm is so a future leftover `cmd` cannot fall through to `args.text`
- Printed help still says `.summem/summem` after the driver move: change those three printers in step 2; catalog tests already match `summem {name}` either way

## Pre-Mortem

- Plan treats item 17 as uncovered CLI reject, but `test_unknown_prefix_is_error` already exists: keep the proof-file case anyway (empty initialized store, `_payload_files`); do not delete the cli test
- Aligning auto-create docs to “any store command” contradicts older “wake or note only” in `productContext.md`: VISION follows the code (honest); persistent reconcile after QA
- Monkeypatching `Path.read_bytes` is too wide and breaks unrelated reads: patch only when `self` equals the target tree path
- Using `sys.argv[0]` for the printed name (preflight advisory) would make in-process tests print `pytest`: already rejected in step 2

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
