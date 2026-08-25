## Findings

No findings for scope `conditional-logic`.
No findings for scope `deliverable-fossils`.
No findings for scope `monolithic-test-file`.
No findings for scope `mystery-guest`.
No findings for scope `naming-lies`.
No findings for scope `over-specified-mock`.
No findings for scope `presentation-coupled`.
No findings for scope `prose-pin`.
No findings for scope `pseudo-tested`.
No findings for scope `rotten-green`.
No findings for scope `shared-state`.
No findings for scope `tautology-theatre`.

- **Location:** `tests/test_gitutil.py` - `test_reaches_nested_sentence_when_zoom_prints_wake_lines`
- **Smell:** `implementation-coupled`
- **Rationale:** The test accesses a private method `_projected_child` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.
- **Why this isn't a false positive:** This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary.

- **Location:** `tests/test_nap.py` - `test_first_unlink_sees_both_parent_files`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that both parent `.summ` and `.tree` files exist, but the body only asserts `seen["sum"] and seen["tree"]`, which are truthiness checks on lists. This matches the signal '`assert len(x) > 0` as the only assertion'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the structural equality or expected contents of the lists rather than just their truthiness.
- **Why this isn't a false positive:** This is not a side-effect absence contract where a negative check is expected; it claims positive behavior but uses a weak truthiness check.

- **Location:** `tests/test_nap.py` - `test_nap_rejects_empty_caption`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an empty caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument' / 'effectively no check'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_nap.py` - `test_nap_rejects_overlong_caption`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an overlong caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_nap.py` - `test_nap_overlong_caption_message_is_a_ratchet`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`pytest.raises(T, match="ambiguous")` / `err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_nap_rejects_newline_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_nap_rejects_non_adjacent_ids`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_nap_rejects_unknown_id`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_nap_missing_tree_unknown_id_has_no_wake_hint`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_write_nap_overlapping_adjacent_naps_raises`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="overlapping packs")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_write_nap_note_inside_adjacent_nap_raises`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="overlapping packs")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_nap.py` - `test_write_nap_malformed_tree_raises_unreadable_pack`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="unreadable pack")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_scopes.py` - `test_help_before_version_prints_version_help`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test asserts on the truthiness of `captured.out` and performs negative checks on it. This matches the signal '`expect(x).toBeTruthy()` on a value with a known-knowable format'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the expected help text structure or exact string.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it expects positive output but uses a weak check.

- **Location:** `tests/test_scopes.py` - `test_start_without_dir_is_usage`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `start` without a directory exits nonzero, but the body only asserts `m.main(["start"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

- **Location:** `tests/test_scopes.py` - `test_config_entry_chars_is_per_store_for_notes_and_naps`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard error output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_unreadable_config_uses_defaults`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_monkeypatch_wake_lines_still_applies_when_config_omits_knob`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_root_wake_catalog_is_labeled_paths_not_commands`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_root_wake_catalogs_other_store`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_catalog_count_preserves_folded_note_grain`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_pull_wake_omits_catalog_and_root_notes`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_scopes.py` - `test_ignored_store_omitted_from_catalog`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_store.py` - `test_note_rejects_empty`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an empty note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_store.py` - `test_note_rejects_over_280_bytes`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an overlong note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_store.py` - `test_note_overlong_message_is_a_ratchet`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_store.py` - `test_note_rejects_newline`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_store.py` - `test_note_280_is_utf8_bytes_not_chars`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that the byte limit applies, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_store.py` - `test_note_rejects_non_utc_now`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that a non-UTC datetime is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

- **Location:** `tests/test_version.py` - `test_version_rejects_extra_args`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `version` with an extra token exits nonzero, but the body only asserts `m.main(["version", "x"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

- **Location:** `tests/test_version.py` - `test_version_rejects_path_flag`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `version --path` is rejected, but the body only asserts `m.main(["version", "--path", "."]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

- **Location:** `tests/test_wake.py` - `test_day_from_stamp_formats_utc_calendar_date`
- **Smell:** `implementation-coupled`
- **Rationale:** The test accesses a private method `_day_from_stamp` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.
- **Why this isn't a false positive:** This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary.

- **Location:** `tests/test_wake.py` - `test_resolve_id_rejects_hyphenated_day`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="unknown id")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

- **Location:** `tests/test_wake.py` - `test_wake_output_omits_notes_naps_and_git`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_skips_unreadable_note_and_still_prints`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_skips_dot_prefixed_temp_file`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_missing_sum_prints_id_and_grain_without_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_conflict_sum_omits_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_does_not_call_loads_tree`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_wake_does_not_print_a_nap_request`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

- **Location:** `tests/test_wake.py` - `test_resolve_id_rejects_ambiguous_or_unknown_prefix`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="ambiguous")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

## Behavior Summaries

| File | Line | Test ID | Behavior | Tier | Smells Found |
|------|------|---------|----------|------|--------------|
| tests/test_nap.py | 37 | test_nap_two_adjacent_notes_writes_pair_and_unlinks | Two adjacent notes become one nap pair; both notes are gone.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 68 | test_same_children_same_tree_bytes_and_paths | Same two notes and different captions share .tree bytes and dest paths.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 92 | test_first_unlink_sees_both_parent_files | At the first child unlink, both parent .summ and .tree already exist.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_nap.py | 113 | test_tree_replace_failure_leaves_children | If parent .tree replace fails, both notes remain and no nap pair is left.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 138 | test_nap_rejects_empty_caption | An empty caption is rejected and the store is unchanged.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_nap.py | 150 | test_nap_rejects_overlong_caption | A caption over ENTRY_CHARS is rejected and the store is unchanged.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_nap.py | 162 | test_nap_overlong_caption_message_is_a_ratchet | An over-long nap caption names actual UTF-8 bytes, the limit, and the compress hint.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 180 | test_nap_rejects_newline_caption | A caption with a newline is rejected and the store is unchanged.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 196 | test_nap_rejects_non_adjacent_ids | Non-adjacent ids are rejected without mentioning store paths or git.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 216 | test_nap_rejects_unknown_id | An unknown id is rejected without mentioning store paths or git.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 234 | test_nap_missing_tree_unknown_id_has_no_wake_hint | A view nap with no .tree raises unknown id and does not say to copy from wake.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 252 | test_nap_of_two_naps_nests_napchild_and_unions_digests | A nap of two naps stores NapChild nodes and the union of original digests.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 279 | test_napchild_sum_empty_when_child_sum_missing | Napping a child whose .summ is missing stores an empty NapChild.sum.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 300 | test_napchild_sum_empty_when_child_sum_conflict | Napping a child whose .summ is conflict-marked stores an empty NapChild.sum.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 321 | test_nap_two_identical_notes_by_repeated_id | Two adjacent notes with the same text share an id and can still be napped.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 346 | test_write_nap_overlapping_adjacent_naps_raises | Adjacent naps whose leaf-sets intersect raise before writing a parent.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 386 | test_write_nap_note_inside_adjacent_nap_raises | A note whose digest sits in the adjacent nap is overlapping packs.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_nap.py | 405 | test_write_nap_disjoint_adjacent_naps_still_concat | Disjoint adjacent naps still unlink and concat.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 423 | test_write_nap_identical_text_notes_still_concat | Two identical-text notes still concat; the overlap guard requires a nap.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_nap.py | 437 | test_write_nap_malformed_tree_raises_unreadable_pack | A selected nap whose .tree is malformed raises ValueError without store paths.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 12 | test_resolve_subdir_without_store_is_git_root | A subdirectory with no nested store resolves to the git root.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 22 | test_resolve_inside_started_dir_is_that_store | Resolve from inside a started directory returns that directory.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 35 | test_resolve_path_file_walks_from_parent | An existing file path walks from the file's parent directory.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 47 | test_resolve_missing_file_walks_from_parent | A missing file path walks from its parent directory.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 57 | test_resolve_omitted_path_uses_cwd | Omitting path_arg walks from cwd.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 71 | test_start_creates_store_in_dir | start <dir> creates a store in that directory.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 86 | test_start_does_not_create_ancestor_stores | start does not create .summem on ancestor directories.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 97 | test_start_without_dir_is_usage | start without a directory exits nonzero.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_scopes.py | 104 | test_note_path_writes_started_store | note --path into a started package writes there, not at git root.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 120 | test_note_path_rolls_up_when_unstarted | note --path under an unstarted sibling writes to the git-root store.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 134 | test_nap_zoom_recall_path_use_started_store | nap, zoom, and recall --path operate on the child store only.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 162 | test_note_path_fold_request_is_copy_paste_safe | A fold request after note --path is a command that naps that store from $PWD.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 183 | test_config_wake_lines_is_per_store | WAKE_LINES in one store's config does not change another store's budget.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 205 | test_config_entry_chars_is_per_store_for_notes_and_naps | ENTRY_CHARS applies per store to notes and nap captions, including above 280.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 235 | test_unreadable_config_uses_defaults | Unreadable config.toml uses defaults and is not rewritten.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 251 | test_monkeypatch_wake_lines_still_applies_when_config_omits_knob | Omitted WAKE_LINES still follows the module constant, including a monkeypatch.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 278 | test_root_wake_catalog_is_labeled_paths_not_commands | Root wake labels extra stores as ./paths, not as wake --path commands.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 299 | test_empty_root_omits_project_root_header | A cataloged repo with no root notes omits == Project-root Memories ==.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 312 | test_root_wake_starts_with_usage | Empty root wake is how_to_text() plus the footer; no other sections.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 325 | test_pull_wake_omits_usage | wake --path omits the Usage section.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_scopes.py | 340 | test_root_wake_catalogs_other_store | Root wake lists another started store under a catalog header.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 362 | test_catalog_count_preserves_folded_note_grain | Catalog note count keeps encoded nap grain after a fold.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 385 | test_pull_wake_omits_catalog_and_root_notes | wake --path on a child store omits the catalog and root notes.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 404 | test_ignored_store_omitted_from_catalog | A gitignored store is omitted from the catalog.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_scopes.py | 423 | test_root_only_wake_labels_nonempty_document | A repo with only the git-root store labels a non-empty document.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 18 | test_wake_without_store_creates_and_prints_nothing | First wake in a git repo with no store creates the store and prints nothing.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 28 | test_wake_lists_two_notes_sorted_by_filename | Wake prints two notes sorted by filename.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 42 | test_day_from_stamp_formats_utc_calendar_date | _day_from_stamp maps a 16-char UTC filename stamp to YYYY-MM-DD.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | implementation-coupled |
| tests/test_wake.py | 48 | test_wake_line_is_dated_grain_for_a_note | A note wake line is x1 YYYY-MM-DD: text from the filename stamp.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 61 | test_wake_pack_line_has_no_date | A pack wake line has grain and prefix and contains no YYYY-MM-DD.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 77 | test_format_wake_line_grain1_pack_is_undated_caption | A grain-1 pack (kind nap, leaves 1) prints the caption only.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 90 | test_format_wake_line_empty_note_caption_keeps_trailing_colon | A note with an empty caption prints x1 day: with no extra space.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 103 | test_resolve_id_rejects_hyphenated_day | A YYYY-MM-DD token is not a content-id prefix.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 111 | test_wake_output_omits_notes_naps_and_git | Wake output does not mention notes/, naps/, or git.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 122 | test_wake_skips_unreadable_note_and_still_prints | An unreadable note is skipped; readable notes still print.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 134 | test_wake_skips_dot_prefixed_temp_file | A leftover dot-prefixed temp file in notes/ is not listed.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 148 | test_wake_mixed_view_sorts_by_filename | A nap and a later loose note sort by filename; grain comes from the name.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 165 | test_wake_missing_sum_prints_id_and_grain_without_caption | Missing .summ: wake prints id and grain, not a caption, and does not refuse.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 183 | test_wake_conflict_sum_omits_caption | A .summ containing <<<<<<< omits the caption and still prints id and grain.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 201 | test_wake_does_not_call_loads_tree | At-budget wake lists files and does not open .tree.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 219 | test_wake_pack_line_is_grain_prefix_caption | A pack wake line is xN prefix: caption.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 233 | test_wake_prints_at_most_wake_lines_newest | Eleven notes at WAKE_LINES=4 print the newest four texts, no hashes.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 248 | test_wake_does_not_print_a_nap_request | Wake never prints Run: or a nap invocation, even when over budget.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 260 | test_short_id_is_8_hex_when_unique | short_id is 8 hex when that prefix is unique among the given ids.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 268 | test_short_id_lengthens_until_unique | short_id grows past 8 hex when two ids share the floor prefix.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 277 | test_resolve_id_returns_full_id_for_unique_prefix | resolve_id maps a unique prefix to the full id.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 285 | test_resolve_id_rejects_ambiguous_or_unknown_prefix | resolve_id raises ValueError when the prefix matches none or many ids.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_wake.py | 298 | test_short_id_is_8_hex_when_id_repeats | A repeated content id still shortens to 8 hex; uniqueness is among distinct ids.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_wake.py | 306 | test_resolve_id_accepts_prefix_when_id_repeats | resolve_id treats a repeated content id as one identity, not an ambiguous clash.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 23 | test_note_rejects_empty | Empty note text is rejected.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_store.py | 31 | test_note_rejects_over_280_bytes | A note longer than 280 UTF-8 bytes is rejected.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_store.py | 39 | test_note_overlong_message_is_a_ratchet | An over-long note names actual UTF-8 bytes, the limit, and the compress hint.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_store.py | 63 | test_note_rejects_newline | A note containing a newline or carriage return is rejected.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | loose-text-oracle |
| tests/test_store.py | 80 | test_note_accepts_280_bytes | A note of exactly 280 UTF-8 bytes is accepted.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 89 | test_note_280_is_utf8_bytes_not_chars | The 280 limit is UTF-8 bytes, not characters.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_store.py | 101 | test_note_rejects_non_utc_now | A naive or non-UTC now is rejected.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_store.py | 112 | test_first_note_creates_config_and_notes | First note creates commented config and a notes file, not a driver.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 127 | test_ensure_store_does_not_create_driver | ensure_store does not place .summem/summem.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 137 | test_existing_driver_is_not_overwritten | An existing .summem/summem is left unchanged.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 148 | test_ensure_store_creates_naps_dir | ensure_store creates naps/ and does not overwrite an existing driver.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 161 | test_note_name_uses_injected_utc_clock_and_rand | Note names use the injected UTC clock and rng bytes.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_store.py | 170 | test_same_second_notes_are_two_paths | Two notes in the same UTC second still produce two paths.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 11 | test_version_prints_script_version | main(['version']) exits 0 and prints __version__ plus a newline.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 18 | test_version_outside_repository_writes_nothing | version outside a repository exits 0 and creates no store.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 27 | test_version_rejects_extra_args | version with an extra token exits nonzero.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_version.py | 33 | test_version_rejects_path_flag | version --path is rejected; version -h does not list --path.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | vacuous-assertion |
| tests/test_version.py | 44 | test_help_before_version_prints_version_help | -h version prints version help, not top-level-only usage.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 56 | test_version_line_has_release_please_marker | Repo-root summem __version__ carries x-release-please-version.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 66 | test_version_matches_release_please_manifest | summem.__version__ equals the Release Please manifest root version.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 73 | test_release_config_generic_extra_file_is_summem | release-please generic extra-files targets repo-root summem.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 82 | test_surgery_version_matches_summem | surgery.py and summem print the same in-script version (lockstep, not enforced at runtime).. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 89 | test_surgery_version_line_has_release_please_marker | Repo-root surgery.py __version__ carries x-release-please-version.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_version.py | 99 | test_release_config_generic_extra_files_include_surgery | release-please generic extra-files also bump repo-root surgery.py.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_proof_conflict.py | 25 | test_same_pair_two_captions_conflict_only_on_sum | Two nappers of the same pair conflict on .summ only; both resolutions wake and zoom.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_proof_conflict.py | 75 | test_planted_conflict_markers_wake_skips_caption_zoom_prints_leaves | Planted <<<<<<< in a .summ: wake omits the caption; zoom still prints the leaves.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_view.py | 22 | test_view_includes_nap_stem_when_sum_is_missing | A .tree without a .summ is still one view node.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_view.py | 38 | test_view_ignores_leftover_sum_caption | A leftover .sum beside a .tree does not supply the caption.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_view.py | 55 | test_view_includes_nap_stem_when_sum_has_conflict_markers | A .summ containing <<<<<<< is still one view node.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_view.py | 69 | test_view_sorts_notes_and_naps_by_filename | Mixed notes and naps sort by filename, not by kind.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | — |
| tests/test_gitutil.py | 39 | test_reaches_nested_sentence_when_zoom_prints_wake_lines | reaches finds a nested original when zoom_text prints wake grammar, not 64-hex ids.. Calls SUT entry points and asserts on expected outcomes using standard fixtures. | unknown | implementation-coupled |
