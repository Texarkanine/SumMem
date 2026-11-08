# Task: start, help, and nap replies

* Task ID: start-help-nap
* Complexity: Level 2
* Type: simple enhancement

Three CLI replies in `summem`. `start` names the store in one sentence and refuses a missing directory. `help` reuses the existing `-h` rewrite. A `nap` of a pair that is already some nap's two children succeeds through the normal `Saved.` path. Any other miss stays a short refusal and does not mention `wake`.

## Test Plan (TDD)

### Behaviors to Verify

- `start pkg` on an existing directory with no store → exit 0, stdout `There is a store in ./pkg.\n`, `pkg/.summem/` has `notes/`, `naps/`, and a comment-led `config.toml`, and no driver file
- `start pkg` again → the same stdout line, exit 0, and the same `config.toml` bytes
- `start missing` when `missing` does not exist → exit 1, stderr `not a directory: ./missing\n`, and no `missing/` directory
- `start foo/packages/baz` when none of those directories exist → exit 1, stderr `not a directory: ./foo/packages/baz\n`, and no `foo/`
- `start` on a file → exit 1, stderr `not a directory: ./file\n`, and no store directory beside that file
- `start pkg` outside a repository, after `pkg` exists → exit 1, stderr contains `repository`, and `pkg/.summem` does not exist
- `start` with no path → exit 2
- `start` success and the missing-directory error contain neither `notes/`, `naps/`, nor `git`
- `main(["help"])` → exit 0, stdout equals `usage_text()`, stderr empty
- `main(["help", "note"])` → exit 0, stdout equals `main(["note", "-h"])`
- `main(["help", "start"])` → exit 0, stdout equals `main(["start", "-h"])`, and no directory named `help` is created
- `main([])` → exit 2, catalog on stderr, stdout empty
- `main(["note", "help"])` in a repository → exit 0, the note text is `help`
- `main(["note", "--", "--help"])` → exit 0, the note text is `--help`
- Second `main(["nap", prefix_a, prefix_b, caption])` after that pair was folded → exit 0, stdout is `Saved.\n\nNothing left to compress.\n` when no other pair remains, and the nap directory is unchanged
- `nap` of the two direct child ids of an expanded nap (the ids `wake` would print under budget) → exit 0, `Saved.`, nap file set unchanged
- `nap` of two nested ids that are not one nap's two direct children → exit 1, stderr `not a fold row\n`, nap file set unchanged, stderr does not contain `wake`
- `nap` of one current view id and one id that exists only under a nap → exit 1, stderr `not a fold row\n`, store unchanged
- `nap` of `deadbeef` and `cafebabe` → exit 1, stderr `unknown id\n`, no `wake`, no new files
- `write_nap` of an unknown id → `unknown id`, and the text does not contain `wake`
- `zoom` of an unknown id still contains `Copy an id from wake`

### Test Infrastructure

- Framework: pytest, run with `tox -e py311`
- Test location: `tests/`
- Conventions: one behavior per test, docstring states the behavior, CLI through `summem` fixture `main()`, store setup with `init_repo` and `write_note` / `write_nap`. Process-level nap refusals live in `tests/test_nap_reject.py`.
- New test files: none

## Implementation Plan

### 1. start — executable

- Files: `summem` (`main` start arm), `tests/test_scopes.py`, `tests/test_cli.py`, `tests/test_surgery.py`, `tests/test_path_walkup_and_catalog.py`

1. Stub tests: add empty tests in `tests/test_scopes.py` for the success sentence, the second start, the missing path, the missing nested path, and start on a file. Adjust the docstring of `test_start_creates_store_in_dir` so it no longer claims `start` creates the directory.
2. Stub interface: none. `main` already has the start arm.
3. Write tests and run red: assert the strings and exit codes above. In existing tests that call `start` on a path the test did not create, create that directory before `start`. That includes `tests/test_scopes.py`, `tests/test_cli.py` `test_start_without_repository_errors`, `tests/test_surgery.py`, and `tests/test_path_walkup_and_catalog.py` (`foo/packages/baz` and `pkg`, which those tests start through a subprocess). `test_start_does_not_create_ancestor_stores` still asserts that ancestor directories get no `.summem`. `test_path_flag_is_known_on_all_non_start_commands` rejects `--path` on `start` in argparse and does not need a directory. Run `tox -e py311 -- tests/test_scopes.py tests/test_cli.py tests/test_surgery.py tests/test_path_walkup_and_catalog.py -n0` and see the new assertions fail.
4. Write code and run green: in the start arm, resolve the path as today. If it is not an existing directory, write `not a directory: ./<path>\n` to stderr and return 1. Do not call `mkdir`. Then keep the repository check and `ensure_store`. On success write `There is a store in ./<path>.\n` to stdout and return 0. `<path>` is the relative posix path the caller passed, prefixed with `./` when it has no `./`. Run the same tox command green.

### 2. help — executable

- Files: `summem` (`main`, `usage_text`), `tests/test_cli.py`

1. Stub tests: empty tests for `help`, `help note`, `help start` creating nothing, bare stderr, `note help`, and `note -- --help`.
2. Stub interface: none. `_HELP_FLAGS` and the `-h <command>` rewrite already exist.
3. Write tests and run red: the assertions in the behavior list. `help note` compares stdout to a fresh `main(["note", "-h"])`. Run `tox -e py311 -- tests/test_cli.py -n0 -k "help or bare or note"`.
4. Write code and run green: if `args_list[0] == "help"`, replace it with `["-h", *args_list[1:]]` before the existing help-flag branch. Add one `usage_text` row, `summem help [command]`, pointing at that same text. Do not add an argparse subparser. Run the same tests green.

### 3. nap replies — executable

- Files: `summem` (`main` nap arm, new helper, `_pair_nodes`), `tests/test_cli.py`, `tests/test_nap.py`, `tests/test_nap_reject.py`, `tests/test_zoom.py` only if a zoom assertion must stay put

1. Stub tests: empty CLI tests in `tests/test_cli.py` for the repeated nap, the expanded direct-child nap, the nested non-pair, the mixed view-row-plus-nested-id nap, and the garbage ids. Point the existing unknown-id tests at the new words in the "write tests" step rather than adding a second oracle.
2. Stub interface: add `def _nap_miss(nodes, token_a, token_b) -> str | None` with a docstring and `raise NotImplementedError`. A note's id is the view id `leafset_id([note_digest(note_file_bytes(text))])`, the value `list_view` and `_projected_child` already use. A nap child's id is `NapChild.id`. Do not compare a token to the raw 64-hex `note_digest`. Return `None` when some nap's two direct children are exactly these two ids (each token a unique prefix of a different child, via `_projected_child`). Known ids are the view row ids plus every id `_index_tree` reports under those naps. Load each tree with `_as_child` so the lock cache is reused. Return `not a fold row` when both tokens match a known id and are not that direct pair, including one view row and one nested id. Return `unknown id` when either token matches nothing known. No new `_child_id` helper.
3. Write tests and run red: the five CLI cases, and change `test_nap_rejects_unknown_id`, `test_unknown_prefix_is_error`, and `test_nap_unknown_ids_rejected_without_writing` so they require `unknown id` and forbid `wake`. Leave `test_nap_missing_tree_unknown_id_has_no_wake_hint` and the zoom unknown-id test as they are. Run those tests and see the new CLI cases fail.
4. Write code and run green: implement `_nap_miss` with one walk, using `_as_child`. In the nap arm, resolve ids as today. On `ValueError` whose text starts with `unknown id`, call `_nap_miss` on the healed view and the raw tokens. `None` means skip `write_nap` and fall through to the existing `Saved.` / `fold_request` / idle output. Otherwise write that string plus a newline to stderr and return 1. Change `_pair_nodes` to raise `unknown id` with no wake hint. Do not change `resolve_id`. Run the nap CLI tests, `tests/test_nap.py`, `tests/test_nap_reject.py`, and `tests/test_zoom.py`.

### 4. Docs and the ratchet sentence — prose/policy

- Files: `docs/user-guide/commands.md`, `docs/user-guide/stores.md`, `docs/user-guide/troubleshooting.md`, `docs/architecture/wake.md`, `docs/architecture/merges-and-healing.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. `commands.md` and `stores.md`: `start` requires an existing directory, prints `There is a store in ./path.`, and does not rewrite an existing config. Remove "prints nothing" and "creates the directory". Update the printed `-h` table at the top of `commands.md` so it matches `usage_text()`, including the `help` row.
2. `troubleshooting.md`: remove the "`start` printed nothing" row. Point the `unknown id. Copy an id from wake.` row at `zoom`. Describe nap's `unknown id` and `not a fold row` without a wake hint.
3. `wake.md` Expand: a `nap` of the two children just expanded is the nap that already exists, so it succeeds and writes nothing. A pair that is not some nap's two children is refused with `not a fold row`.
4. `merges-and-healing.md`: a stale fold request succeeds. The memories stay in the nap that won. The command still prints `Saved.` and then whatever fold is actually left.
5. `systemPatterns.md`: nap's identity miss does not say to copy an id from `wake`. Zoom's identity miss still does.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest suite and `tox -e py311`
- `usage_text`, the `-h` rewrite, `ensure_store`, `resolve_id`, `_as_child`, `fold_request`

## Challenges & Mitigations

- Prefix collision: a short token can match both children. `_nap_miss` returns success only when each token matches a different child of one two-child nap.
- `start` today creates missing directories, and many tests rely on that. Those tests create the directory first. The new refusal tests are what lock the behavior.
- `resolve_id` is shared with `zoom`. The nap arm catches the unknown-id error and does not change `resolve_id`, so zoom still says to copy an id from `wake`.
- The already-folded check runs only after view resolution fails, so a normal nap of two current rows does not walk nap trees.
- One success sentence cannot say "created" versus "already there". The second-start test locks "config bytes unchanged" instead of a second sentence.
- A note's wake id is `leafset_id([note_digest(...)])`, 16 hex, not the 64-hex digest. Matching the digest would miss every folded note. `_nap_miss` takes ids from `_projected_child` and `_index_tree`.
- One current row plus one nested id is still not a fold. Both tokens are known, so the message is `not a fold row`, not `unknown id`.

## Pre-Mortem

- Treating `nap` of an expanded nap's two children as success is the wrong product call. The operator asked for that: a nap that already happened succeeds. The expanded-child test locks it. A pair that is only nested stays `not a fold row`.
- A large `start` test edit could drop the ancestor-store assertion. That assertion stays in `test_start_does_not_create_ancestor_stores`.
- Rewriting every argv that contains `help` would make `note help` record nothing. The rewrite checks `argv[0]` only, and a test records the note `help`.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

## QA Results

- **Status**: PASS
- **Advisory (`docs/user-guide/commands.md:142`)**: "Outside a repository" mentions "`init`, `version`, and `-h` work anywhere"; `help` works outside a repository as well via the `-h` rewrite, though omitting it does not conflict with the rest of the guide.
- **Verification**: All KISS, DRY, YAGNI, Completeness, Regression, Integrity, and Documentation checks passed; `tox -e py311` passed (`441 passed`).
