# Task: help catalog and nested nap retry

* Task ID: start-help-nap
* Complexity: Level 2
* Type: simple enhancement

The printed catalog names one way to do each thing. `help` and `help <command>` keep working and are not listed. A `nap` of two ids that are already some nap's two direct children succeeds even when that nap sits inside a larger nap.


## Test Plan (TDD)

### Behaviors to Verify

- `usage_text()` → the text has no `summem help` line, and it still contains `<command> -h`
- Notes `a` `b` `c` `d` folded into two naps, then those naps folded into one → `nap` of the ids of `a` and `b` exits 0, stdout is `Saved.\n\nNothing left to compress.\n`, stderr is empty, and the nap filenames are unchanged
- Existing: `help`, `help note`, and `help start` still print the same text as `-h` and `<command> -h`; `note help` still records `help`
- Existing: a second nap of a pair that is still a view nap's two children succeeds; `a` with `c` inside the outer nap is `not a fold row`; a view row plus a nested id is `not a fold row`; `deadbeef` with `cafebabe` is `unknown id`

### Test Infrastructure

- Framework: pytest, run with `tox -e py311`
- Test location: `tests/test_cli.py`
- Conventions: one behavior per test, docstring states the behavior, CLI through the `summem` fixture `main()`, store setup with `init_repo` and `write_note`. Nap filenames compared with `_nap_names`. A note's id is `_note_id`.
- New test files: none

## Implementation Plan

### 1. Catalog omits the help alias — executable

- Files: `summem` (`usage_text`), `tests/test_cli.py`

1. Stub tests: an empty test in `tests/test_cli.py` whose docstring says the printed catalog does not offer `help` as a command.
2. Stub interface: none. `usage_text` already returns the catalog.
3. Write tests and run red: assert `"summem help" not in usage_text()` and `"<command> -h" in usage_text()`. Run `tox -e py311 -- tests/test_cli.py::test_catalog_does_not_list_the_help_command -n0` and see it fail. Existing tests already bind `-h`, `--help`, bare `summem`, and `help` to that same string.
4. Write code and run green: delete the `help    [command]` row from `usage_text`. Leave the `help` argv rewrite in place. Run the same test green.

### 2. User-guide table matches the printout — prose/policy

- Files: `docs/user-guide/commands.md`
- No tests: prose/policy artifact

1. Remove the `summem help    [command]` row from the table.
2. Restore the following sentence to the one-way form: the table is what `.summem/summem -h` prints, and one command's options are `.summem/summem <command> -h`.

### 3. Buried pair succeeds — executable

- Files: `summem` (`_nap_miss`), `tests/test_cli.py`

1. Stub tests: an empty test beside `test_nap_of_nested_cousins_is_not_a_fold_row` whose docstring says napping the two children of a nap that was folded further prints `Saved.` and writes nothing.
2. Stub interface: none. `_nap_miss` already exists.
3. Write tests and run red: the four-note fold in the behavior list, then `nap` of `_note_id` for `a` and `b`. Assert exit 0, the Saved and idle stdout, empty stderr, and `_nap_names` unchanged. Run `tox -e py311 -- tests/test_cli.py::test_nap_of_buried_pair_succeeds -n0` and see it fail with `not a fold row`.
4. Write code and run green: in `_nap_miss`, pair-match `index["root_kids"]` and every list in `index["kids"].values()` with the check that is already there. `kids` holds each nested nap's own children and does not include the root pair, so both stay. Return `None` on the first match, which skips `write_nap` on the existing path. No new helper. Run that test, `tests/test_cli.py` nap cases, `tests/test_nap.py`, `tests/test_nap_reject.py`, and `tests/test_zoom.py` under `tox -e py311 -- … -n0`.

`docs/user-guide/troubleshooting.md`, `docs/architecture/wake.md`, `docs/architecture/merges-and-healing.md`, and `memory-bank/systemPatterns.md` already say this pair succeeds. They stay as written.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest suite and `tox -e py311`
- `usage_text`, the `help` argv rewrite, `_nap_miss`, `_one_id`, `_index_tree`, `_as_child`

## Challenges & Mitigations

- A ban on the word `help` would reject a real catalog line later. The assertion is the command spelling `summem help`.
- `index["kids"]` does not include the view nap's own pair. Dropping `root_kids` would reject a retry of two notes whose nap is still a view row. The code step keeps both.
- A projected child can be `None`. The existing `None` skip stays on every list.
- Calling `write_nap` for the buried ids would try to fold rows that are not in the view. `None` from `_nap_miss` already skips that call. The test locks unchanged filenames.
- A documentation pass can grow a sentence that only restates the nested case. Those four files have no edit step.

## Pre-Mortem

- The catalog test passes while the user guide still teaches `help <command>`. The prose step restores the sentence that names only `<command> -h`, in the wording the page used before the alias row.
- The pair check walks one extra level by hand and misses a nap `_index_tree` already recorded. The code step uses `kids`, which that walk fills for every nested nap, rather than a depth limit.
- The four existing sentences get a bolted-on clause so the nested case is "documented." Already covered by the last Challenge. No edit step for those files.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

### QA Review Findings

- **KISS**: Pass. `_nap_miss` iterates over `(index["root_kids"], *index["kids"].values())` reusing existing child-pair matching logic without added abstractions.
- **DRY**: Pass. Reuses `kids` populated by `_index_tree` and the existing `_one_id` resolver.
- **YAGNI**: Pass. No unused parameters, speculative logic, or extraneous helper methods added.
- **Completeness**: Pass. Catalog omits `help` command, user guide matches catalog, buried nap pairs succeed, and invalid folds continue to fail with appropriate errors (`not a fold row` / `unknown id`).
- **Regression**: Pass. All 443 tests pass under `py311`. CLI dispatch for `help` and `help <command>` remains fully functional.
- **Integrity**: Pass. No scaffolding remnants, magic numbers, or debug artifacts.
- **Documentation**: Pass. User-guide commands table and description updated cleanly; troubleshooting and architecture docs already match the implemented contract.
