# Task: multi-store-filing

* Task ID: multi-store-filing
* Complexity: Level 2
* Type: rework — test-suite quality and modularity ratchet

Remediate the SLOBAC test-suite audit findings in `.slobac/2026-11-19T14-31-00/audit.md` across the `tests/` suite touched on `multi-store-filing`, keeping `summem`, `surgery.py`, and `migrate.py` unchanged while preserving the distinction between in-process `m.main(...)` unit suites and child-process `subprocess.run(...)` binary integration tests.

## Test Plan (TDD)

### Behaviors to Verify

No new product executable behavior (`summem`, `surgery.py`, and `migrate.py` are unchanged). Existing product behaviors verified by strengthened and decoupled tests:

- Driver Python floor before `tomllib` (Finding 4, `tests/test_cli_bootstrap.py`): executing repo-root `summem` via `SourceFileLoader` with `sys.version_info` patched to `(3, 10, 0)` and a `builtins.__import__` guard raises `SystemExit(1)` and writes `"SumMem needs Python 3.11 or newer"` to stderr without importing `tomllib`.
- Equal-grain and unequal-grain `fold_request` pair selection (Findings 10–16 & 18, `tests/test_fold.py`): `summem.fold_request` pairs the two oldest loose notes by content ID on `[1, 1, 1]`, returns `""` on `[16, 1]` and on healed identical-text notes at `wake_lines=0` (`m.fold_request(repo, 0, nodes=nodes)`), pairs the two `8`s on `[16, 8, 8]`, and pairs the two `1`s on `[2, 1, 1]`.
- `fold_request` explicit `nodes` and `entry_chars` overrides (Finding 17, `tests/test_fold.py`): passing `nodes=nodes[1:]` (`["b", "c"]`) and `entry_chars=99` against a 3-note store (`"a"`, `"b"`, `"c"`) configured with `ENTRY_CHARS = 140` emits `"99 characters"`, includes `"  b\n"` and `"  c\n"`, and omits `"140 characters"`, `"  a\n"`, and `"compression"` (`assert "compression" not in out`) without mocking `list_view` or `knobs`.
- Public `fold_request` and `leaf_digests` on vanished/corrupt/lying rows (Findings 20–23, `tests/test_fold.py`): `fold_request` pairs remaining loose notes without reading `notes/` files when a third note is unlinked after listing while `leaf_digests` returns `None` for the vanished note and for a non-string note-text pack, and `leaf_digests` reflects actual tree digest counts on mismatched-stem packs.
- Child-process `nap --help` stdout/stderr contract (Findings 27 & 28, `tests/test_nap_reject.py`): `subprocess.run([sys.executable, str(SCRIPT), "nap", "--help"])` exits `0` with `stdout == summem.usage_text()` and empty `stderr`.
- Child-process root-wake catalog header invariant (Finding 29, `tests/test_path_walkup_and_catalog.py`): after recording a root note and child note, root `wake` unconditionally contains `== Project-root Memories ==` after `== Additional SumMem Catalogs ==` with no fallback branch.
- `recall_text` empty stdout on unreadable packs (Findings 30 & 31, `tests/test_recall.py`): `recall_text` returns exact `""` and writes `"skipped a pack\n"` to stderr when the sole `.tree` is malformed JSON or has a non-string note `name`.
- Wait-free filename-only `catalog_text` (Finding 33, `tests/test_scopes.py`): `catalog_text` counts a loose note containing invalid UTF-8 bytes plus two overlapping 2-packs from filenames (`5: ./pkg`) and leaves both overlapping nap pairs untouched on disk without stubbing `list_view` or `heal_view`.
- `surgery.py` targetless usage, stubbed `load_summem` fold request, and dry-run store invariance (Findings 37–39, `tests/test_surgery.py`): `surgery.main(["--root"])` exits `2` with `stderr == surgery._usage()`; `surgery.main` patched via `load_summem` honors `_host_needs_interpreter`; `--dry-run` over budget omits `"Run:"` and leaves `_store_bytes(repo)` unchanged.
- Runner-native platform skips (Findings 5 & 45, `tests/test_cli_bootstrap.py`, `tests/test_store_lock.py`): POSIX execute-bit and POSIX `fcntl.flock` contention assertions run unconditionally under `@pytest.mark.skipif(os.name == "nt", ...)` instead of body-level `if` guards.
- In-process help consolidation (Findings 7, 8, 24, 40, 46, 48, `tests/test_cli_help.py`): `["-h", "init"]`, `["init", "-h"]`, `["-h", "version"]`, `["version", "-h"]`, `["-h", "wake"]`, `["wake", "-h"]`, `["start", "-h"]`, and `["note", "-h"]` all exit `0`, emit `usage_text()` on stdout with empty stderr, and leave the store untouched.

### Test Infrastructure

- Framework: `pytest` (with `pytest-xdist` `-n auto --maxprocesses=4`) via `tox -e py311` during iteration and `tox run-parallel` (`py311`–`py314`) for final verification.
- Test location: `tests/`
- Conventions: Capability-focused `tests/test_<capability>.py` modules sharing session `summem` fixture (`tests/conftest.py`) and git/tree helpers (`tests/gitutil.py`). Child-process binary integration suites (`test_path_walkup_and_catalog.py`, `test_nap_reject.py`, `test_caption_conflict.py`, `test_worktree_note_merge.py`, `test_squash_clone_zoom.py`, `test_branch_pack_merge.py`) stay distinct from fast in-process `m.main(...)` suites; Findings 47 and 49 are declined on that layer boundary.
- New test files:
  - `tests/test_cli_bootstrap.py`
  - `tests/test_cli_help.py`
  - `tests/test_rematerialize.py`
  - `tests/test_heal_view.py`
  - `tests/test_cli_heal.py`
  - `tests/test_store_lock.py`
- Deleted test files:
  - `tests/test_zipper.py` (partitioned into `test_rematerialize.py`, `test_heal_view.py`, `test_cli_heal.py`, and `test_store_lock.py`)

## Implementation Plan

### 1. Remediate standalone test findings in `test_caption_conflict.py`, `test_nap_reject.py`, `test_path_walkup_and_catalog.py`, `test_recall.py`, `test_scopes.py`, and `test_surgery.py` — test-only refactor

- Files: `tests/test_caption_conflict.py`, `tests/test_nap_reject.py`, `tests/test_path_walkup_and_catalog.py`, `tests/test_recall.py`, `tests/test_scopes.py`, `tests/test_surgery.py`
- No product code changes (`summem` and `surgery.py` unchanged).

1. [x] In `tests/test_caption_conflict.py`, rename `test_same_pair_two_captions_conflict_only_on_sum` to `test_same_pair_two_captions_merge_cleanly_as_distinct_variants` (Finding 1).
2. [x] In `tests/test_nap_reject.py`, rename `test_nap_help_exits_zero` to `test_nap_help_prints_root_usage(summem)`, update its docstring, and assert `result.returncode == 0`, `result.stdout.decode("utf-8") == summem.usage_text()`, and `result.stderr == b""` (Findings 27 & 28).
3. [x] In `tests/test_path_walkup_and_catalog.py`, replace the conditional `cat_end` fallback in `test_root_wake_lists_other_stores_pull_prints_only_that_store` with unconditional `cat_end = root_lines.index("== Project-root Memories ==")` (Finding 29; Findings 47 & 49 declined per unit-vs-binary-integration layering).
4. [x] In `tests/test_recall.py`, replace `assert isinstance(out, str)` with `assert out == ""` and trim redundant `not in err` checks after exact `assert err == "skipped a pack\n"` in `test_recall_malformed_tree_does_not_raise` and `test_recall_unprojectable_note_name_skips` (Findings 30 & 31).
5. [x] In `tests/test_scopes.py`: add `assert ".summem/summem" not in catalog` to `test_root_wake_catalogs_other_store`; rename `test_monkeypatch_wake_lines_still_applies_when_config_omits_knob` to `test_omitted_config_wake_lines_uses_default_budget` (Finding 32); rewrite `test_catalog_text_does_not_list_view` without `boom` stubs by writing an invalid-UTF-8 loose note file in `pkg/.summem/notes/` and two overlapping 2-pack stems directly via `m.nap_stem` in `pkg/.summem/naps/` (without unlinking), then asserting `catalog_text` reports `5: ./pkg` while leaving both overlapping nap pairs on disk (Finding 33); delete `test_catalog_does_not_os_walk` (Finding 34); rename `test_catalog_requires_config_toml_sentinel` to `test_empty_summem_dir_without_files_is_not_started_or_cataloged` with matching docstring (Finding 35).
6. [x] In `tests/test_surgery.py`: rename `test_dry_run_prints_chain_and_writes_nothing` to `test_dry_run_returns_chain_and_writes_nothing` (Finding 36); update `test_main_usage_without_target` to invoke `s.main(["--root"]) == 2` and assert `captured.out == ""` and `captured.err == s._usage()` (Finding 37); add `monkeypatch.setattr(s, "load_summem", lambda: m)` in `test_main_prints_fold_request_when_over_budget` so `s.main` uses the patched `summem` module (Finding 38); capture `before = _store_bytes(repo)` in `test_main_dry_run_omits_fold_request` and assert `"Run:" not in out` and `_store_bytes(repo) == before` (Finding 39).
7. [x] Run `tox -e py311 -- tests/test_caption_conflict.py tests/test_nap_reject.py tests/test_path_walkup_and_catalog.py tests/test_recall.py tests/test_scopes.py tests/test_surgery.py` and confirm green.

### 2. Remediate `tests/test_fold.py` findings — test-only refactor

- Files: `tests/test_fold.py`
- No product code changes (`summem` unchanged).

1. [ ] Delete `test_write_nap_serializes_tree_once` (Finding 9).
2. [ ] Replace `_equal_grain_pair` assertions with real `m.fold_request` assertions and rename: `test_fold_request_pairs_two_oldest_ones` computing inline `m.leafset_id([m.note_digest(p.read_bytes())])` for `pa` and `pb` and asserting `len(nodes) == 3` and `_named_pair(m, nodes, m.fold_request(repo, 2, nodes=nodes)) == {pa_id, pb_id}` (Findings 10 & 11); `test_fold_request_is_empty_for_16_plus_1` asserting `[node.leaves for node in nodes] == [16, 1]` and `m.fold_request(repo, 1, nodes=nodes) == ""` (Findings 12 & 13); `test_fold_request_pairs_two_8s_not_16_plus_8` asserting `_named_pair(m, nodes, m.fold_request(repo, 2, nodes=nodes)) == {nodes[1].id, nodes[2].id}` (Finding 14); `test_fold_request_pairs_two_1s_not_2_plus_1` asserting `_named_pair(m, nodes, m.fold_request(repo, 2, nodes=nodes)) == {nodes[1].id, nodes[2].id}` (Finding 15).
3. [ ] Deduplicate `test_equal_grain_pair_duplicate_ids_when_same_text` into `test_fold_request_identical_notes_use_short_prefix`, rename the canonical test to `test_fold_request_is_empty_after_healing_identical_notes`, and pass `wake_lines=0` (`m.fold_request(repo, 0, nodes=nodes) == ""`) so `_fold_pair` executes rather than hitting the `len(nodes) <= wake_lines` budget short-circuit (Findings 16 & 18).
4. [ ] Rewrite `test_fold_request_reuses_nodes_and_entry_chars` without `list_view`/`knobs` `boom` stubs: configure `ENTRY_CHARS = 140` on disk with 3 notes (`"a"`, `"b"`, `"c"`), pass `nodes=nodes[1:]` and `entry_chars=99` to `m.fold_request(repo, 1, nodes=nodes[1:], entry_chars=99)`, and assert `"99 characters" in out`, `"140 characters" not in out`, `"  a\n" not in out`, `"  b\n" in out`, `"  c\n" in out`, and `"compression" not in out` (Finding 17).
5. [ ] Rename `test_fold_request_omits_path_when_cwd_selects_store` to `test_fold_request_includes_root_relative_path_even_inside_child_store` (Finding 19).
6. [ ] Replace private `_fold_grains` and `_as_child` calls with public `fold_request` and `leaf_digests`: in `test_fold_request_keeps_a_note_unlinked_after_listing` run `m.fold_request(repo, 1, nodes=view)` under the `Path.read_bytes` spy asserting `[p for p in opened if p.parent.name == "notes"] == []` and assert `m.leaf_digests(view[2]) is None` (Finding 20); in `test_fold_request_skips_a_pack_whose_note_text_is_not_a_string` assert `m.leaf_digests(view[0]) is None` (Finding 21); in `test_fold_request_skips_a_pack_whose_digest_count_is_not_the_stem_grain` assert `digests = m.leaf_digests(view[0]); assert digests is not None and len(digests) != view[0].leaves` (Finding 22); in `test_fold_request_folds_a_lying_filename_with_a_truthful_row` assert `[len(m.leaf_digests(node)) for node in view] == [4, 4]` (Finding 23).
7. [ ] Run `tox -e py311 -- tests/test_fold.py` and confirm green.

### 3. Remediate `test_init.py`, `test_version.py`, and split `test_cli.py` by capability — test-only refactor

- Files: `tests/gitutil.py`, `tests/test_init.py`, `tests/test_version.py`, `tests/test_cli.py`, `tests/test_cli_bootstrap.py`, `tests/test_cli_help.py`, `tests/test_nap.py`, `tests/test_zoom.py`
- No product code changes (`summem` unchanged).

1. [ ] In `tests/test_init.py`: delete `test_agents_md_starts_with_prompt_text` and unused `Path`/`ROOT` imports (Finding 25); delete `test_help_before_init_prints_init_help` and trim the trailing `init -h` assertions from `test_init_rejects_path_flag` (Findings 24, 46, 48); rename `test_init_text_posix_has_no_windows_warning` to `test_init_text_separates_recipe_from_prompt_at_divider`, drop the `"only work on Windows"` fossil check and duplicate divider assertions from `test_init_text_is_host_agnostic` so each test owns one concern cleanly (Finding 26).
2. [ ] In `tests/test_version.py`: delete `test_help_before_version_prints_version_help` and trim the trailing `version -h` assertions from `test_version_rejects_path_flag` (Findings 40, 46, 48).
3. [ ] Move `COMMAND_ONLY`, `_IMPORT_PROBE`, and `fresh_imported` into `tests/gitutil.py` and create `tests/test_cli_bootstrap.py` with driver bootstrap, Python floor, stdio encoding, shebang/executable-bit, and lazy-import isolation tests moved from `test_cli.py`: replace `test_version_info_is_checked_before_import_tomllib` with execution-based `test_driver_checks_python_floor_before_importing_tomllib` using `SourceFileLoader`, `monkeypatch.setattr(sys, "version_info", (3, 10, 0))`, and a `builtins.__import__` guard (Finding 4); split `test_shebang_and_executable_bit` into unconditional `test_driver_has_python3_shebang` and `@pytest.mark.skipif(os.name == "nt", reason="POSIX execute bit is not tracked on Windows")` `test_driver_has_executable_bit` (Findings 2 & 5).
4. [ ] Create `tests/test_cli_help.py` with the 11 `usage_text()`, `-h`/`--help`/`help` routing, and non-mutation tests moved from `test_cli.py`, extending `test_subcommand_help_prints_root_usage_without_touching_store` with `["-h", "init"]`, `["init", "-h"]`, `["-h", "version"]`, `["version", "-h"]`, `["-h", "wake"]`, `["wake", "-h"]`, `["start", "-h"]`, and `["note", "-h"]` plus `assert list(repo.rglob(".summem")) == []`, and dropping the duplicate `test_help_note_matches_note_help_flag`, `test_help_start_prints_help_and_creates_nothing`, `test_help_before_command_prints_command_help`, `test_command_help_still_shows_path`, and `test_start_help_omits_path` functions (Findings 2, 7, 8, 24, 40, 46, 48).
5. [ ] Move `_note_id`, `_nap_names`, and the 11 `nap` CLI prefix/fold-row/re-nap/malformed-tree tests (`test_cli_malformed_tree_returns_1_without_traceback`, `test_nap_accepts_unique_prefix`, `test_unknown_prefix_is_error`, `test_unknown_nap_id_names_only_the_miss`, `test_second_nap_of_folded_notes_succeeds`, `test_nap_of_expanded_children_succeeds`, `test_nap_of_nested_cousins_is_not_a_fold_row`, `test_nap_of_buried_pair_succeeds`, `test_nap_of_view_row_and_nested_id_is_not_a_fold_row`, `test_ambiguous_prefix_is_error`, and `test_cli_nap_identical_notes_prefix_not_adjacent` renamed to `test_cli_nap_identical_notes_prefix_fails_as_not_two_rows` per Finding 6) into `tests/test_nap.py`, and move the 4 `zoom` CLI error/range-token/corrupt-pack tests (`test_cli_zoom_range_token_is_not_a_content_id`, `test_cli_zoom_malformed_tree_returns_1`, `test_cli_zoom_oserror_returns_1`, `test_cli_zoom_nested_id_skips_sibling_bad_tree`) into `tests/test_zoom.py` (Finding 2).
6. [ ] Trim `tests/test_cli.py` to the 17 core subcommand dispatch, argument-arity, length-ratchet, outside-repository, and `--root`/`--path` flag validation tests, renaming `test_path_flag_is_known_on_all_non_start_commands` to `test_path_flag_accepted_on_store_commands_and_rejected_elsewhere` (Findings 2 & 3).
7. [ ] Run `tox -e py311 -- tests/test_init.py tests/test_version.py tests/test_cli.py tests/test_cli_bootstrap.py tests/test_cli_help.py tests/test_nap.py tests/test_zoom.py` and confirm green.

### 4. Remediate and split `tests/test_zipper.py` by capability — test-only refactor

- Files: `tests/gitutil.py`, `tests/test_nap.py`, `tests/test_surgery.py`, `tests/test_wake_expand.py`, `tests/test_rematerialize.py`, `tests/test_heal_view.py`, `tests/test_cli_heal.py`, `tests/test_store_lock.py`, `tests/test_zipper.py` (deleted)
- No product code changes (`summem` unchanged).

1. [ ] Promote shared store-planting helpers (`write_notes`, `payload_names`, `plant_nap`, `balanced_4`, `fold_balanced`, `plant_abd_abe`) into `tests/gitutil.py` and point the new zipper capability modules plus `tests/test_surgery.py` (`write_notes`, `payload_names`, `plant_nap`; keeping its local `(paths, parent)` `_balanced_4`), `tests/test_nap.py` (`payload_names`), and `tests/test_wake_expand.py` (`payload_names`) at `gitutil` so duplicate copies are eliminated (Finding 41).
2. [ ] Create `tests/test_rematerialize.py` with the 11 `leaf_digests`, `rematerialize_child` (including `test_same_second_notes_keep_left_child_stem`), and `write_nap(nodes=...)` tests from `test_zipper.py`, omitting `test_rematerialize_serializes_tree_once` (Findings 41 & 44).
3. [ ] Create `tests/test_heal_view.py` with the 16 in-process `heal_view` set-cover and overlap-healing tests from `test_zipper.py` (`test_heal_view_returns_final_view`, `test_heal_two_identical_notes_keeps_newer`, and the 14 variant/overlap/disjoint/temp `heal_*` + `test_note_after_packed_text_is_healed_away` tests), omitting the weaker intra-file duplicate `test_identical_notes_collapse_after_heal_view` (Finding 41).
4. [ ] Create `tests/test_cli_heal.py` with the 8 CLI `note`/`nap`/`wake` healing, `.tree` single-parse boundary, and frontier projection tests (`test_heal_to_8_2_1_empty_fold_request_wake_projects` and the 7 retained `test_cli_*` healing tests) from `test_zipper.py`, omitting the internal-plumbing wrapper tests `test_cli_note_lists_once_when_disjoint` and `test_cli_nap_passes_heal_nodes_to_write_nap` (Findings 41, 42, 43).
5. [ ] Create `tests/test_store_lock.py` with the 6 `with_store_lock` POSIX/runtime/`msvcrt` tests from `test_zipper.py`, decorating `test_with_store_lock_blocks_and_writes_no_lock_file` with `@pytest.mark.skipif(os.name == "nt", reason="POSIX directory flock requires fcntl")`, removing the `if m._try_fcntl() is None:` branch inside `held()` and the `if seen["code"] is not None:` guard, and asserting `seen["code"] == 2` unconditionally (Findings 41 & 45).
6. [ ] Delete `tests/test_zipper.py` and run `tox -e py311 -- tests/test_nap.py tests/test_surgery.py tests/test_wake_expand.py tests/test_rematerialize.py tests/test_heal_view.py tests/test_cli_heal.py tests/test_store_lock.py` and confirm green.

### 5. Update contributor docs, persistent memory-bank briefing, and run full verification — prose/policy

- Files: `docs/contributing/index.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. [ ] In `docs/contributing/index.md`, remove the bullet `- **Keep \`AGENTS.md\` in step with \`init\`.** This repository's activation block must match what \`init\` prints. A test checks this.` since the repository's `AGENTS.md` is operator-owned and `test_agents_md_starts_with_prompt_text` is deleted.
2. [ ] In `memory-bank/techContext.md`, replace `"This repository's \`AGENTS.md\` prefix locksteps with \`prompt_text()\`; tests do not pin write-rule wording."` with `"Tests do not pin write-rule wording or this repository's \`AGENTS.md\`."` to match the deletion of `test_agents_md_starts_with_prompt_text`.
3. [ ] Run full matrix verification (`tox run-parallel` across `py311`–`py314`) and `uv run --no-config properdocs build --strict` to confirm zero regressions.

## Technology Validation

No new technology - validation not required.

## Dependencies

- `tests/` imports `conftest` and `gitutil` via `pytest.ini` (`testpaths = tests`); new test modules must follow the same `from conftest import ...` and `from gitutil import ...` conventions.
- `tests/test_coverage_collection.py` targets `tests/test_version.py::test_version_prints_script_version`, which remains in `tests/test_version.py`.

## Challenges & Mitigations

- Name collision between `test_zoom.py::test_ambiguous_prefix_is_error` and `test_cli.py::test_ambiguous_prefix_is_error`: `test_cli.py`'s `nap` test moves into `tests/test_nap.py` (which has no `test_ambiguous_prefix_is_error`), avoiding any collision in `test_zoom.py`.
- `Path.read_bytes` spy in `test_fold_request_keeps_a_note_unlinked_after_listing`: `fold_request(repo, 1, nodes=view)` reads `config.toml` when `entry_chars` is omitted, so filter the spy assertion to `notes/` paths (`[p for p in opened if p.parent.name == "notes"] == []`) to pin the exact documented invariant without coupling to `knobs()`.
- `SourceFileLoader` execution of `summem` under patched `sys.version_info = (3, 10, 0)` in `test_driver_checks_python_floor_before_importing_tomllib`: execute under a distinct module name (`"summem_py310_probe"`, cleaned up via `monkeypatch.delitem(sys.modules, ..., raising=False)`) so session-cached `conftest._SUMMEM` and `sys.modules["summem"]` are never mutated.
- Never monkeypatch `os.name` to `"nt"` on POSIX (instantiates `WindowsPath` and crashes `pathlib`); use `@pytest.mark.skipif(os.name == "nt", ...)` decorators for POSIX-only checks.

## Pre-Mortem

- **Silent test drop during the `test_cli.py` and `test_zipper.py` splits:** Reconciled exact before/after function counts in planning (`test_cli.py`: 57 → +1 split −5 folded into help loop = 53 across `10 + 11 + 11 + 4 + 17`; `test_zipper.py`: 45 → −4 deleted = 41 across `11 + 16 + 8 + 6`; full suite `459 → 445` collected tests) and will verify total collected test count after each split.
- **Accidental staging of untracked `.slobac/` audit directory during checkpoint commits:** Stage explicit paths (`git add memory-bank/... tests/...`), never `git add -A` or `git add .`.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
