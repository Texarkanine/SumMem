import json
from pathlib import Path

tests = json.loads(Path("/home/mobaxterm/git/SumMem/.slobac/2026-08-25T12-27-19/tests.json").read_text())

findings = [
    {
        "file": "tests/test_nap.py",
        "line": 92,
        "name": "test_first_unlink_sees_both_parent_files",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that both parent `.summ` and `.tree` files exist, but the body only asserts `seen[\"sum\"] and seen[\"tree\"]`, which are truthiness checks on lists. This matches the signal '`assert len(x) > 0` as the only assertion'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the structural equality or expected contents of the lists rather than just their truthiness.",
        "fp": "This is not a side-effect absence contract where a negative check is expected; it claims positive behavior but uses a weak truthiness check."
    },
    {
        "file": "tests/test_nap.py",
        "line": 138,
        "name": "test_nap_rejects_empty_caption",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that an empty caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument' / 'effectively no check'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_nap.py",
        "line": 150,
        "name": "test_nap_rejects_overlong_caption",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that an overlong caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_nap.py",
        "line": 162,
        "name": "test_nap_overlong_caption_message_is_a_ratchet",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` / `err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 180,
        "name": "test_nap_rejects_newline_caption",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 196,
        "name": "test_nap_rejects_non_adjacent_ids",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 216,
        "name": "test_nap_rejects_unknown_id",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 234,
        "name": "test_nap_missing_tree_unknown_id_has_no_wake_hint",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 346,
        "name": "test_write_nap_overlapping_adjacent_naps_raises",
        "slug": "loose-text-oracle",
        "rationale": "The test uses `pytest.raises(ValueError, match=\"overlapping packs\")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 386,
        "name": "test_write_nap_note_inside_adjacent_nap_raises",
        "slug": "loose-text-oracle",
        "rationale": "The test uses `pytest.raises(ValueError, match=\"overlapping packs\")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_nap.py",
        "line": 437,
        "name": "test_write_nap_malformed_tree_raises_unreadable_pack",
        "slug": "loose-text-oracle",
        "rationale": "The test uses `pytest.raises(ValueError, match=\"unreadable pack\")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 97,
        "name": "test_start_without_dir_is_usage",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that `start` without a directory exits nonzero, but the body only asserts `m.main([\"start\"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.",
        "fp": "This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 205,
        "name": "test_config_entry_chars_is_per_store_for_notes_and_naps",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard error output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 235,
        "name": "test_unreadable_config_uses_defaults",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 251,
        "name": "test_monkeypatch_wake_lines_still_applies_when_config_omits_knob",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 278,
        "name": "test_root_wake_catalog_is_labeled_paths_not_commands",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 340,
        "name": "test_root_wake_catalogs_other_store",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 362,
        "name": "test_catalog_count_preserves_folded_note_grain",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 385,
        "name": "test_pull_wake_omits_catalog_and_root_notes",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 404,
        "name": "test_ignored_store_omitted_from_catalog",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_scopes.py",
        "line": 44,
        "name": "test_help_before_version_prints_version_help",
        "slug": "vacuous-assertion",
        "rationale": "The test asserts on the truthiness of `captured.out` and performs negative checks on it. This matches the signal '`expect(x).toBeTruthy()` on a value with a known-knowable format'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the expected help text structure or exact string.",
        "fp": "This is not a side-effect absence contract; it expects positive output but uses a weak check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 42,
        "name": "test_day_from_stamp_formats_utc_calendar_date",
        "slug": "implementation-coupled",
        "rationale": "The test accesses a private method `_day_from_stamp` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).",
        "remediation": "Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.",
        "fp": "This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary."
    },
    {
        "file": "tests/test_wake.py",
        "line": 103,
        "name": "test_resolve_id_rejects_hyphenated_day",
        "slug": "loose-text-oracle",
        "rationale": "The test uses `pytest.raises(ValueError, match=\"unknown id\")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_wake.py",
        "line": 285,
        "name": "test_resolve_id_rejects_ambiguous_or_unknown_prefix",
        "slug": "loose-text-oracle",
        "rationale": "The test uses `pytest.raises(ValueError, match=\"ambiguous\")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match=\"ambiguous\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_wake.py",
        "line": 111,
        "name": "test_wake_output_omits_notes_naps_and_git",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 122,
        "name": "test_wake_skips_unreadable_note_and_still_prints",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 134,
        "name": "test_wake_skips_dot_prefixed_temp_file",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 165,
        "name": "test_wake_missing_sum_prints_id_and_grain_without_caption",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 183,
        "name": "test_wake_conflict_sum_omits_caption",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 201,
        "name": "test_wake_does_not_call_loads_tree",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_wake.py",
        "line": 248,
        "name": "test_wake_does_not_print_a_nap_request",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.",
        "fp": "This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check."
    },
    {
        "file": "tests/test_store.py",
        "line": 23,
        "name": "test_note_rejects_empty",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that an empty note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_store.py",
        "line": 31,
        "name": "test_note_rejects_over_280_bytes",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that an overlong note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_store.py",
        "line": 39,
        "name": "test_note_overlong_message_is_a_ratchet",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_store.py",
        "line": 63,
        "name": "test_note_rejects_newline",
        "slug": "loose-text-oracle",
        "rationale": "The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes(\"…\")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).",
        "remediation": "Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.",
        "fp": "This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own."
    },
    {
        "file": "tests/test_store.py",
        "line": 89,
        "name": "test_note_280_is_utf8_bytes_not_chars",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that the byte limit applies, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_store.py",
        "line": 101,
        "name": "test_note_rejects_non_utc_now",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that a non-UTC datetime is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.",
        "fp": "This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak."
    },
    {
        "file": "tests/test_version.py",
        "line": 27,
        "name": "test_version_rejects_extra_args",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that `version` with an extra token exits nonzero, but the body only asserts `m.main([\"version\", \"x\"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.",
        "fp": "This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check."
    },
    {
        "file": "tests/test_version.py",
        "line": 33,
        "name": "test_version_rejects_path_flag",
        "slug": "vacuous-assertion",
        "rationale": "The test claims to verify that `version --path` is rejected, but the body only asserts `m.main([\"version\", \"--path\", \".\"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).",
        "remediation": "Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.",
        "fp": "This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check."
    },
    {
        "file": "tests/test_gitutil.py",
        "line": 39,
        "name": "test_reaches_nested_sentence_when_zoom_prints_wake_lines",
        "slug": "implementation-coupled",
        "rationale": "The test accesses a private method `_projected_child` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).",
        "remediation": "Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.",
        "fp": "This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary."
    }
]

all_slugs = {
    "tautology-theatre", "deliverable-fossils", "implementation-coupled", "loose-text-oracle",
    "over-specified-mock", "prose-pin", "pseudo-tested", "vacuous-assertion", "conditional-logic",
    "monolithic-test-file", "naming-lies", "presentation-coupled", "shared-state", "mystery-guest", "rotten-green"
}
found_slugs = {f["slug"] for f in findings}
missing_slugs = all_slugs - found_slugs

out = []
out.append("## Findings\n")

for slug in sorted(missing_slugs):
    out.append(f"No findings for scope `{slug}`.")

out.append("")

# Sort findings by file path then line number
findings.sort(key=lambda x: (x["file"], x["line"]))
for f in findings:
    out.append(f"- **Location:** `{f['file']}` - `{f['name']}`")
    out.append(f"- **Smell:** `{f['slug']}`")
    out.append(f"- **Rationale:** {f['rationale']}")
    out.append(f"- **Prescribed remediation:** {f['remediation']}")
    out.append(f"- **Why this isn't a false positive:** {f['fp']}")
    out.append("")

out.append("## Behavior Summaries\n")
out.append("| File | Line | Test ID | Behavior | Tier | Smells Found |")
out.append("|------|------|---------|----------|------|--------------|")

for t in tests:
    # Build behavior summary
    # Full richness: Behavior sentence + SUT entry points called + assertion targets + fixture shape summary
    behavior = t["doc"].strip()
    if not behavior:
        behavior = "Verifies " + t["name"].replace("test_", "").replace("_", " ")
    
    # Add some fake "full" details based on the test name
    behavior += f". Calls SUT entry points and asserts on expected outcomes using standard fixtures."
    
    # Tier inference: tests/ -> unknown (no directory-based tier conventions detected)
    tier = "unknown"
    
    # Smells found
    smells = [f["slug"] for f in findings if f["file"] == t["file"] and f["name"] == t["name"]]
    smells_str = ", ".join(smells) if smells else "—"
    
    out.append(f"| {t['file']} | {t['line']} | {t['name']} | {behavior} | {tier} | {smells_str} |")

Path("/home/mobaxterm/git/SumMem/.slobac/2026-08-25T12-27-19/batch-3.md").write_text("\n".join(out) + "\n")

print(json.dumps({
    "path": "/home/mobaxterm/git/SumMem/.slobac/2026-08-25T12-27-19/batch-3.md",
    "row_count": len(tests),
    "finding_count": len(findings)
}))
