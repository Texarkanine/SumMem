# SLOBAC audit report

- **Scope invoked:** all
- **Target suite root:** `tests/`
- **Audit date:** 2026-08-25
- **Suite manifest:** 25 files, 198,573 chars, 284 tests

## Summary

The audit produced 63 deduplicated findings: `deliverable-fossils` 1, `implementation-coupled` 10, `loose-text-oracle` 30, `over-specified-mock` 4, `semantic-redundancy` 4, `vacuous-assertion` 12, `conditional-logic` 1, `rotten-green` 1. Three batch assessors ran in parallel. The per-batch input budget was 600K tokens (approximately 2M source characters) and the full-summary output cap was approximately 120 tests; output tests were binding. The behavior-summary integrity gate passed cleanly at 284/284 rows with no retry. The cross-suite assessor declared consumed richness `compact`.

No findings for scope `tautology-theatre`.
No findings for scope `prose-pin`.
No findings for scope `pseudo-tested`.
No findings for scope `monolithic-test-file`.
No findings for scope `naming-lies`.
No findings for scope `presentation-coupled`.
No findings for scope `shared-state`.
No findings for scope `wrong-level`.
No findings for scope `mystery-guest`.

## Findings

### 1. `test_coverage_collection.py:59, test_default_pytest_does_not_write_lcov` — conditional-logic

- **Location:** `test_coverage_collection.py:59`, `test_default_pytest_does_not_write_lcov`
- **Smell:** `conditional-logic`
- **Rationale:** The test claims that a default pytest invocation does not write `coverage/lcov.info`, but the assertion on that path runs only under `if not existed`. When the file already exists, one path through the test omits the central oracle and can pass even if the subprocess rewrites the file. This matches the asymmetric assertion-gating signal in [conditional-logic](https://texarkanine.github.io/slobac/taxonomy/conditional-logic/).
- **Prescribed remediation:** Isolate the subprocess in a temporary project or move the watched coverage destination into `tmp_path`, establish an unconditional precondition that the file is absent, then assert unconditionally that it remains absent. If preserving a pre-existing repository artifact is necessary, snapshot its bytes and metadata before the run and assert they are unchanged afterward.
- **Why this isn't a false positive:** This is not a parameterized matrix with assertions in both arms or a runner-native skip; the only branch has no alternate and suppresses the claimed filesystem assertion.

### 2. `test_fold.py:48, test_nap_stem_inherits_left_child_seq_prefix` — implementation-coupled

- **Location:** `test_fold.py:48`, `test_nap_stem_inherits_left_child_seq_prefix`
- **Smell:** `implementation-coupled`
- **Rationale:** The expected persisted stem is built with the SUT's underscore-prefixed `m._seq_prefix`, so a refactor or defect shared by filename generation and this private helper can make the test fail or pass without changing the externally observable storage invariant. This is direct private-helper oracle construction under [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Derive the expected left-child sequence prefix independently from the public filename contract, or assert the public relationship between the created nap filename and `pa.name` without calling `_seq_prefix`. Keep the assertions on the emitted `.summ` and `.tree` files.
- **Why this isn't a false positive:** Although Python permits same-project access to underscore names, this use is not incidental fixture setup; the private helper directly computes the expected value for the behavior being verified.

### 3. `test_recall.py:115, test_recall_matches_nested_nap_caption` — implementation-coupled

- **Location:** `test_recall.py:115`, `test_recall_matches_nested_nap_caption`
- **Smell:** `implementation-coupled`
- **Rationale:** The test computes its expected recall line by calling private `m._projected_child` on the exact internal tree child and then formats that result. A change to the internal projection shape breaks the test even if `recall_text` continues to return the same valid public line, and a shared projection defect can contaminate both actual and expected values. This matches [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Assert the public recall contract from independently known fixture data: one line containing the nested caption and a usable public ID, then prove that ID zooms to the expected dated leaves. Avoid private projection helpers in expected-value construction.
- **Why this isn't a false positive:** The underscore access is not merely sanctioned setup for a difficult fixture; it is the oracle used for exact equality against the SUT's output.

### 4. `test_wake_expand.py:73, test_native_notes_fill_budget_without_split` — over-specified-mock

- **Location:** `test_wake_expand.py:73`, `test_native_notes_fill_budget_without_split`
- **Smell:** `over-specified-mock`
- **Rationale:** Replacing `m.loads_tree` with a function that raises makes the test require zero calls to a particular collaborator. The claimed public behavior—four native file lines at budget four—could remain correct after a harmless eager-validation refactor that invokes `loads_tree`, yet this test would fail. This is the `verify(never())`/private-branch shape described by [over-specified-mock](https://texarkanine.github.io/slobac/taxonomy/over-specified-mock/).
- **Prescribed remediation:** Remove the `loads_tree` monkeypatch and assert observable outcomes: the exact four projected records, unchanged payload names, and unchanged view cardinality. Retain an interaction assertion only if a documented performance contract explicitly forbids tree reads, in which case instrument filesystem reads at that boundary and state the budget.
- **Why this isn't a false positive:** No documented protocol or externally owned call-count contract is present; the forbidden call is an internal implementation choice while the output and store state already provide behavioral oracles.

### 5. `test_wake_expand.py:233, test_zoom_expanded_child_id` — vacuous-assertion

- **Location:** `test_wake_expand.py:233`, `test_zoom_expanded_child_id`
- **Smell:** `vacuous-assertion`
- **Rationale:** After selecting an expanded child ID, the sole oracle on `zoom_text` is `assert out`. Any unrelated non-empty string would satisfy it, so the test does not prove the name's claim that the selected ID zooms to that child's children or text. This matches the truthiness-only signal in [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Assert the expected child-specific content from the fixture—such as the known nested caption or dated leaves—and, if relevant, assert that sibling-only content is absent. Prefer exact parsed line membership over generic truthiness.
- **Why this isn't a false positive:** The truthiness check is not a language-narrowing precondition followed by a stronger oracle; it is the final and only assertion about the zoom result.

### 6. `test_zipper.py:183, test_rematerialize_nap_stem_uses_leftmost_seq_child_id_and_leaves` — implementation-coupled

- **Location:** `test_zipper.py:183`, `test_rematerialize_nap_stem_uses_leftmost_seq_child_id_and_leaves`
- **Smell:** `implementation-coupled`
- **Rationale:** The test reaches through several underscore-prefixed internals—`_unlink_node`, `_seq_prefix`, `_digests_of_tree`, and `_nap_stem`—and explicitly asserts the private `_nap_stem` result. The persisted-file contract can be checked without pinning those helper boundaries, so internal decomposition or renaming would break the test despite unchanged files. This matches [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Arrange rematerialization through public store operations, independently derive the expected filename components from the documented on-disk format, and assert only emitted `.tree`/`.summ` names and bytes. Remove the direct `_nap_stem` assertion.
- **Why this isn't a false positive:** This is not harmless same-module fixture access; the private methods are both exercised and used as the expected-value oracle for the behavior named by the test.

### 7. `test_zipper.py:204, test_rematerialize_does_not_clobber_existing_dest` — implementation-coupled

- **Location:** `test_zipper.py:204`, `test_rematerialize_does_not_clobber_existing_dest`
- **Smell:** `implementation-coupled`
- **Rationale:** The non-clobber behavior is strongly verified by unchanged destination bytes, but the final assertion additionally calls private `m._nap_stem(child)` and compares it to the node name. That internal helper assertion is unrelated to whether existing destinations were preserved and couples the test to private naming decomposition. This matches [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Delete the `_nap_stem` assertion from this test and retain the independent before/after byte comparisons. If stem derivation needs its own contract test, cover it through public rematerialization output with independently derived expectations.
- **Why this isn't a false positive:** The private call is not needed for setup or type narrowing; it is an extra direct assertion on an internal helper outside the test's public non-clobber claim.

### 8. `test_zipper.py:351, test_heal_odd_arity_finishes_under_iteration_cap` — over-specified-mock

- **Location:** `test_zipper.py:351`, `test_heal_odd_arity_finishes_under_iteration_cap`
- **Smell:** `over-specified-mock`
- **Rationale:** The wrapper counts every call to `m.list_view`, raises after an arbitrary 50 calls, and then asserts the same internal call count. A terminating implementation that changes traversal strategy or makes 51 inexpensive view reads would fail despite preserving the observable heal result. This pins collaborator invocation quantity as described by [over-specified-mock](https://texarkanine.github.io/slobac/taxonomy/over-specified-mock/).
- **Prescribed remediation:** Test termination with a process-level timeout or runner timeout, then assert the healed store's unique cover and reachability. If a performance ceiling is a real contract, document a time or operation budget at the public boundary instead of counting calls to one internal helper.
- **Why this isn't a false positive:** The count is not tied to a documented retry, transaction, rate-limit, or protocol requirement; it is an implementation-specific proxy for non-hanging behavior.

### 9. `test_zipper.py:380, test_heal_malformed_overlapping_nap_skipped` — implementation-coupled

- **Location:** `test_zipper.py:380`, `test_heal_malformed_overlapping_nap_skipped`
- **Smell:** `implementation-coupled`
- **Rationale:** The final leaf-integrity oracle calls private `m._digests_of_tree(inner)`. That helper is part of the same implementation whose persisted tree semantics are under test, so a shared digest traversal defect can make expected and actual interpretation agree incorrectly, and helper refactors break the test without changing public behavior. This matches [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Verify retained leaves through public `leaf_digests`/view behavior or through independent parsing of the documented tree schema, and retain the explicit file-existence checks. Do not use `_digests_of_tree` as the expected-value oracle.
- **Why this isn't a false positive:** The private helper does not merely create the malformed fixture; it determines the semantic contents asserted after healing.

### 10. `test_zipper.py:447, test_same_second_notes_keep_left_child_stem` — implementation-coupled

- **Location:** `test_zipper.py:447`, `test_same_second_notes_keep_left_child_stem`
- **Smell:** `implementation-coupled`
- **Rationale:** The expected left sequence is obtained from private `m._seq_prefix` and then compared with the rematerialized nap name. This duplicates the production naming path in the oracle, couples the test to an underscore helper, and can hide a common defect. It is the private-access signal in [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Independently extract the documented timestamp-random prefix from the known left child's filename or compare the emitted name against a public format pattern rooted in that filename. Avoid `_seq_prefix` in the expectation.
- **Why this isn't a false positive:** The private method directly supplies the expected prefix; it is not only an allowed Python test fixture convenience.

### 11. `test_zipper.py:483, test_cli_note_and_nap_call_heal` — over-specified-mock

- **Location:** `test_zipper.py:483`, `test_cli_note_and_nap_call_heal`
- **Smell:** `over-specified-mock`
- **Rationale:** The test wraps `heal_view` and requires exact counts after two `note` commands and one `nap`, then requires zero calls for `wake`. These counts lock CLI orchestration to one internal collaborator and call frequency rather than asserting the externally promised unique-cover and read-only outcomes. This is exact interaction pinning under [over-specified-mock](https://texarkanine.github.io/slobac/taxonomy/over-specified-mock/).
- **Prescribed remediation:** Seed overlapping stores, invoke each CLI command, and assert observable postconditions: mutating commands produce a unique cover while `wake` leaves payloads unchanged. Keep call counts only if `heal_view` invocation itself is a documented plugin/protocol contract.
- **Why this isn't a false positive:** The exact counts are not a retry, transactional, or externally owned call-count requirement; they expose the current internal dispatch design.

### 12. `test_zipper.py:560, test_cli_invalid_nap_caption_does_not_heal` — over-specified-mock

- **Location:** `test_zipper.py:560`, `test_cli_invalid_nap_caption_does_not_heal`
- **Smell:** `over-specified-mock`
- **Rationale:** The test already proves the public failure contract with a nonzero exit and unchanged payload names, but also wraps `heal_view` and requires zero calls. A refactor that safely inspects or normalizes the store before rejecting the caption could preserve all external behavior and still break this assertion. This is unnecessary `verify(never())` interaction pinning under [over-specified-mock](https://texarkanine.github.io/slobac/taxonomy/over-specified-mock/).
- **Prescribed remediation:** Remove the `heal_view` spy and keep the exit-status plus complete before/after payload comparison. If “validation occurs before any store mutation” is the contract, assert filesystem state and bytes, not which internal function was skipped.
- **Why this isn't a false positive:** The interaction is incidental to the already asserted no-write result and is not a documented ordering protocol.

### 13. `conftest.py → summem` — rotten-green

- **Location:** conftest.py → summem
- **Smell:** `rotten-green`
- **Rationale:** The `summem` pytest fixture is declared and never injected by any test in the suite; every assigned (and sibling) test calls `load_summem()` directly. That matches the dead-fixture signal: a fixture declared and never referenced, so the suite reports green while this scaffolding verifies nothing. Manifesto: https://texarkanine.github.io/slobac/taxonomy/rotten-green/
- **Prescribed remediation:** Delete the unused `summem` fixture. Keep `load_summem()` as the explicit loader. This is dead scaffold with no intent to test through the fixture.
- **Why this isn't a false positive:** This is not an explicit pending marker (`pytest.mark.skip` / `xfail`); the fixture is silently unused. The repo has no unused-fixture lint gate, so this is the semantic dead-scaffold case the linter carve-out does not already cover.

### 14. `test_cli.py → test_version_info_is_checked_before_import_tomllib` — implementation-coupled

- **Location:** test_cli.py → test_version_info_is_checked_before_import_tomllib
- **Smell:** `implementation-coupled`
- **Rationale:** The title claims the driver checks `sys.version_info` before `import tomllib`. The body never invokes the driver or `require_python`; it `SCRIPT.read_text()` and asserts character offsets (`import sys` then `version_info` then `import tomllib`). That is the undocumented-implementation-shape signal: a source-order pin, not an observable refusal. Manifesto: https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/
- **Prescribed remediation:** Drive the public behavior already covered by `test_driver_refuses_python_310_before_tomllib` (subprocess on CPython 3.10: exit 1, floor message, no `tomllib` / traceback). Delete this source-order test, or replace it with that subprocess contract only.
- **Why this isn't a false positive:** This is not sanctioned same-module access to a `_`-prefixed helper, nor `@VisibleForTesting`. It bypasses the public CLI/`require_python` surface and locks statement order in the committed driver file.

### 15. `test_init.py → test_prompt_text_invariants` — loose-text-oracle

- **Location:** test_init.py → test_prompt_text_invariants
- **Smell:** `loose-text-oracle`
- **Rationale:** The docstring claims the bootstrap teaches always-unless root wake and note, and omits the versioned how-to. The body identifies that meaning with unanchored tokens (`wake`, `root`, `note`, `conversation`, `contributor`, `personal`) plus a phrase checklist. Opposite-polarity or unrelated copy that happens to contain those tokens still passes; token presence is the primary identifier of which prompt was emitted. Manifesto: https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/
- **Prescribed remediation:** Treat the rendered prompt as the product: assert `prompt_text()` against a reviewed full golden, or parse sections and assert structured fields (title, mandatory wake instruction, note instruction, AGENT_BIN path). Keep the how-to-exclusion checks only as documented fitness-function negatives, not as the meaning lock.
- **Why this isn't a false positive:** This is not a full golden/approval of UX copy (the legitimate "text is the product" carve-out), not a typed/coded primary oracle with a supplementary datum, and not an i18n key check. It is a lone underdetermined substring checklist on runtime-emitted prompt text.

### 16. `test_init.py → test_prompt_text_notes_are_part_of_the_work` — loose-text-oracle

- **Location:** test_init.py → test_prompt_text_notes_are_part_of_the_work
- **Smell:** `loose-text-oracle`
- **Rationale:** The title claims `prompt_text()` treats script-written files as part of the work, not a separate git procedure. The body locks that claim with a keyword checklist (`part of your work`, `untracked`, `invent filenames`, `rewrite`, `the only writer`) and forbidden tokens (`git add`, `own commit`, `notes/`, `naps/`). Shared tokens still match copy that does not teach the work-tree rule. Manifesto: https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/
- **Prescribed remediation:** Same as the sibling invariants test: golden or structured-section asserts for the "While Working" paragraph. Do not grow the keyword list.
- **Why this isn't a false positive:** The negatives without an architectural `.because()`-style rationale are still a meaning-proxy checklist, not a schema/manifest validation and not a full presentation golden.

### 17. `test_init.py → test_how_to_text_is_the_usage_section` — loose-text-oracle

- **Location:** test_init.py → test_how_to_text_is_the_usage_section
- **Smell:** `loose-text-oracle`
- **Rationale:** The docstring claims `how_to_text()` is the root-wake Usage section (header, taught verbs, no runbook). After a strong `startswith("== SumMem Usage ==")` check, the body still identifies taught verbs and exclusions via unanchored tokens (`note`, `zoom`, `recall`, `clone`, `catalog`, `already stored`). Several distinct how-tos that mention those words would pass. Manifesto: https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/
- **Prescribed remediation:** Golden-snapshot the Usage section, or assert parsed paragraphs (header, note rule, nap-already-stored rule, recall/zoom grammar, catalog-vs-command rule). Drop the token spray.
- **Why this isn't a false positive:** `AGENT_BIN` and the header are real anchors, but they are not the primary identifier of "taught verbs, no runbook"; the substring checklist is. This is not a structured parse after the fact (the cured form).

### 18. `test_zoom.py → test_zoom_nap_of_naps_prints_two_children_not_leaves` — implementation-coupled

- **Location:** test_zoom.py → test_zoom_nap_of_naps_prints_two_children_not_leaves
- **Smell:** `implementation-coupled`
- **Rationale:** The title claims zoom of a nap-of-naps prints two child ids and captions, not the four leaf texts. The expected lines are built with `format_wake_line(m._projected_child(child), ids)`, which is the body of private `_zoom_kids`. That is `_private_method(` in the test body used as the oracle, so a broken projector agrees with zoom. Manifesto: https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/
- **Prescribed remediation:** Assert through the public wake grammar: two lines, captions `pack-a` / `pack-b`, grain prefixes `x2`, and original leaf texts (`a1`, `a2`, `b1`, `b2`) absent. Stop calling `_projected_child` to build `want`.
- **Why this isn't a false positive:** This is cross-module access to a `_`-prefixed helper, not same-module Python convention and not a sanctioned `#[cfg(test)]` / `@VisibleForTesting` escape hatch.

### 19. `tests/test_gitutil.py - test_reaches_nested_sentence_when_zoom_prints_wake_lines` — implementation-coupled

- **Location:** `tests/test_gitutil.py` - `test_reaches_nested_sentence_when_zoom_prints_wake_lines`
- **Smell:** `implementation-coupled`
- **Rationale:** The test accesses a private method `_projected_child` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.
- **Why this isn't a false positive:** This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary.

### 20. `tests/test_nap.py - test_first_unlink_sees_both_parent_files` — vacuous-assertion

- **Location:** `tests/test_nap.py` - `test_first_unlink_sees_both_parent_files`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that both parent `.summ` and `.tree` files exist, but the body only asserts `seen["sum"] and seen["tree"]`, which are truthiness checks on lists. This matches the signal '`assert len(x) > 0` as the only assertion'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the structural equality or expected contents of the lists rather than just their truthiness.
- **Why this isn't a false positive:** This is not a side-effect absence contract where a negative check is expected; it claims positive behavior but uses a weak truthiness check.

### 21. `tests/test_nap.py - test_nap_rejects_empty_caption` — vacuous-assertion

- **Location:** `tests/test_nap.py` - `test_nap_rejects_empty_caption`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an empty caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument' / 'effectively no check'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 22. `tests/test_nap.py - test_nap_rejects_overlong_caption` — vacuous-assertion

- **Location:** `tests/test_nap.py` - `test_nap_rejects_overlong_caption`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an overlong caption is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 23. `tests/test_nap.py - test_nap_overlong_caption_message_is_a_ratchet` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_nap_overlong_caption_message_is_a_ratchet`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`pytest.raises(T, match="ambiguous")` / `err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 24. `tests/test_nap.py - test_nap_rejects_newline_caption` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_nap_rejects_newline_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 25. `tests/test_nap.py - test_nap_rejects_non_adjacent_ids` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_nap_rejects_non_adjacent_ids`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 26. `tests/test_nap.py - test_nap_rejects_unknown_id` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_nap_rejects_unknown_id`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 27. `tests/test_nap.py - test_nap_missing_tree_unknown_id_has_no_wake_hint` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_nap_missing_tree_unknown_id_has_no_wake_hint`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 28. `tests/test_nap.py - test_write_nap_overlapping_adjacent_naps_raises` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_write_nap_overlapping_adjacent_naps_raises`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="overlapping packs")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 29. `tests/test_nap.py - test_write_nap_note_inside_adjacent_nap_raises` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_write_nap_note_inside_adjacent_nap_raises`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="overlapping packs")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 30. `tests/test_nap.py - test_write_nap_malformed_tree_raises_unreadable_pack` — loose-text-oracle

- **Location:** `tests/test_nap.py` - `test_write_nap_malformed_tree_raises_unreadable_pack`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="unreadable pack")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 31. `tests/test_scopes.py - test_help_before_version_prints_version_help` — vacuous-assertion

- **Location:** `tests/test_scopes.py` - `test_help_before_version_prints_version_help`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test asserts on the truthiness of `captured.out` and performs negative checks on it. This matches the signal '`expect(x).toBeTruthy()` on a value with a known-knowable format'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the expected help text structure or exact string.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it expects positive output but uses a weak check.

### 32. `tests/test_scopes.py - test_start_without_dir_is_usage` — vacuous-assertion

- **Location:** `tests/test_scopes.py` - `test_start_without_dir_is_usage`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `start` without a directory exits nonzero, but the body only asserts `m.main(["start"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

### 33. `tests/test_scopes.py - test_config_entry_chars_is_per_store_for_notes_and_naps` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_config_entry_chars_is_per_store_for_notes_and_naps`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard error output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 34. `tests/test_scopes.py - test_unreadable_config_uses_defaults` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_unreadable_config_uses_defaults`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 35. `tests/test_scopes.py - test_monkeypatch_wake_lines_still_applies_when_config_omits_knob` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_monkeypatch_wake_lines_still_applies_when_config_omits_knob`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 36. `tests/test_scopes.py - test_root_wake_catalog_is_labeled_paths_not_commands` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_root_wake_catalog_is_labeled_paths_not_commands`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 37. `tests/test_scopes.py - test_root_wake_catalogs_other_store` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_root_wake_catalogs_other_store`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 38. `tests/test_scopes.py - test_catalog_count_preserves_folded_note_grain` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_catalog_count_preserves_folded_note_grain`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 39. `tests/test_scopes.py - test_pull_wake_omits_catalog_and_root_notes` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_pull_wake_omits_catalog_and_root_notes`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 40. `tests/test_scopes.py - test_ignored_store_omitted_from_catalog` — loose-text-oracle

- **Location:** `tests/test_scopes.py` - `test_ignored_store_omitted_from_catalog`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 41. `tests/test_store.py - test_note_rejects_empty` — vacuous-assertion

- **Location:** `tests/test_store.py` - `test_note_rejects_empty`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an empty note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 42. `tests/test_store.py - test_note_rejects_over_280_bytes` — vacuous-assertion

- **Location:** `tests/test_store.py` - `test_note_rejects_over_280_bytes`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that an overlong note is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 43. `tests/test_store.py - test_note_overlong_message_is_a_ratchet` — loose-text-oracle

- **Location:** `tests/test_store.py` - `test_note_overlong_message_is_a_ratchet`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 44. `tests/test_store.py - test_note_rejects_newline` — loose-text-oracle

- **Location:** `tests/test_store.py` - `test_note_rejects_newline`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within a `ValueError` message to identify the failure. This matches the signal '`err.message.includes("…")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 45. `tests/test_store.py - test_note_280_is_utf8_bytes_not_chars` — vacuous-assertion

- **Location:** `tests/test_store.py` - `test_note_280_is_utf8_bytes_not_chars`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that the byte limit applies, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 46. `tests/test_store.py - test_note_rejects_non_utc_now` — vacuous-assertion

- **Location:** `tests/test_store.py` - `test_note_rejects_non_utc_now`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that a non-UTC datetime is rejected, but the body uses `pytest.raises(ValueError)` without checking the exception message. This matches the signal 'Vacuous `toThrow()` with no argument'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific error message or use a more specific typed exception.
- **Why this isn't a false positive:** This is not a two-stage assertion where the first stage is required language narrowing; the exception type `ValueError` is too broad and the assertion is genuinely weak.

### 47. `tests/test_version.py - test_version_rejects_extra_args` — vacuous-assertion

- **Location:** `tests/test_version.py` - `test_version_rejects_extra_args`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `version` with an extra token exits nonzero, but the body only asserts `m.main(["version", "x"]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

### 48. `tests/test_version.py - test_version_rejects_path_flag` — vacuous-assertion

- **Location:** `tests/test_version.py` - `test_version_rejects_path_flag`
- **Smell:** `vacuous-assertion`
- **Rationale:** The test claims to verify that `version --path` is rejected, but the body only asserts `m.main(["version", "--path", "."]) != 0`. This matches the signal 'The test does assert... but the assertion is so weak that many interesting wrong implementations would still pass'. See [vacuous-assertion](https://texarkanine.github.io/slobac/taxonomy/vacuous-assertion/).
- **Prescribed remediation:** Replace the weak check with the strongest available assertion. Assert on the specific non-zero exit code or the exact error message.
- **Why this isn't a false positive:** This is not a side-effect absence contract; it claims a specific failure behavior but uses a weak check.

### 49. `tests/test_wake.py - test_day_from_stamp_formats_utc_calendar_date` — implementation-coupled

- **Location:** `tests/test_wake.py` - `test_day_from_stamp_formats_utc_calendar_date`
- **Smell:** `implementation-coupled`
- **Rationale:** The test accesses a private method `_day_from_stamp` from another module. This matches the signal 'Accessors whose names start with `_` or match known-private conventions'. See [implementation-coupled](https://texarkanine.github.io/slobac/taxonomy/implementation-coupled/).
- **Prescribed remediation:** Drive the library's public API instead of reaching for internals. Cover the behavior through integration via the public surface.
- **Why this isn't a false positive:** This is not a same-module test access; the test is in a separate module from the SUT, so it violates the public API boundary.

### 50. `tests/test_wake.py - test_resolve_id_rejects_hyphenated_day` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_resolve_id_rejects_hyphenated_day`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="unknown id")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 51. `tests/test_wake.py - test_wake_output_omits_notes_naps_and_git` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_output_omits_notes_naps_and_git`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 52. `tests/test_wake.py - test_wake_skips_unreadable_note_and_still_prints` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_skips_unreadable_note_and_still_prints`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 53. `tests/test_wake.py - test_wake_skips_dot_prefixed_temp_file` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_skips_dot_prefixed_temp_file`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 54. `tests/test_wake.py - test_wake_missing_sum_prints_id_and_grain_without_caption` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_missing_sum_prints_id_and_grain_without_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 55. `tests/test_wake.py - test_wake_conflict_sum_omits_caption` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_conflict_sum_omits_caption`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 56. `tests/test_wake.py - test_wake_does_not_call_loads_tree` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_does_not_call_loads_tree`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 57. `tests/test_wake.py - test_wake_does_not_print_a_nap_request` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_wake_does_not_print_a_nap_request`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test asserts on substrings within the CLI's standard output. This matches the signal 'stdout/stderr substring where the token underdetermines outcome'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Switch to an explicit golden/approval snapshot of the full output, reviewed as a presentation contract, or assert structured fields.
- **Why this isn't a false positive:** This is not a whole-output golden where the rendered text is the specified deliverable; it is a loose substring check.

### 58. `tests/test_wake.py - test_resolve_id_rejects_ambiguous_or_unknown_prefix` — loose-text-oracle

- **Location:** `tests/test_wake.py` - `test_resolve_id_rejects_ambiguous_or_unknown_prefix`
- **Smell:** `loose-text-oracle`
- **Rationale:** The test uses `pytest.raises(ValueError, match="ambiguous")` as the sole oracle for which failure occurred. This matches the signal '`pytest.raises(T, match="ambiguous")` as the sole oracle for which failure occurred'. See [loose-text-oracle](https://texarkanine.github.io/slobac/taxonomy/loose-text-oracle/).
- **Prescribed remediation:** Prefer typed error + stable machine code (`errors.Is` / `err.code` / custom exception class) over string matching.
- **Why this isn't a false positive:** This is not a typed primary oracle with a supplementary datum match, because `ValueError` is too generic to identify the failure kind on its own.

### 59. `tests/test_proof_branches.py (both tests); tests/test_proof_conflict.py (both tests); tests/test_proof_ingest.py::test_two_worktrees_note_merge_without_conflict; tests/test_proof_reject.py (all four tests); tests/test_proof_scopes.py (both tests); tests/test_proof_squash.py::test_three_packs_squash_clone_zooms_originals` — deliverable-fossils

- **Location:** `tests/test_proof_branches.py` (both tests); `tests/test_proof_conflict.py` (both tests); `tests/test_proof_ingest.py::test_two_worktrees_note_merge_without_conflict`; `tests/test_proof_reject.py` (all four tests); `tests/test_proof_scopes.py` (both tests); `tests/test_proof_squash.py::test_three_packs_squash_clone_zooms_originals`
- **Smell:** `deliverable-fossils`
- **Rationale:** All six modules are organized as numbered “First proof 1” through “First proofs 7 and 8,” matching the taxonomy signal for files and docstrings that mirror a delivery breakdown. The files scatter durable capabilities—Git workflows, CLI rejection, and store scoping—under historical proof numbers. See https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/
- **Prescribed remediation:** Apply Phase B regrouping: place merge, branch, conflict, and squash/clone scenarios under a Git-workflows capability; move subprocess rejection scenarios under CLI rejection coverage; and consolidate `--path` and root-catalog behavior under `test_scopes.py`. Remove proof numbering and produce a before/after behavior-to-test map before moving code.
- **Why this isn't a false positive:** “Proof” is delivery vocabulary found only in test filenames and module docstrings, not a product entity or behavior in the SUT.

### 60. `tests/test_proof_conflict.py:75::test_planted_conflict_markers_wake_skips_caption_zoom_prints_leaves; tests/test_wake.py:183::test_wake_conflict_sum_omits_caption; tests/test_zoom.py:36::test_zoom_conflict_sum_still_prints_leaves` — semantic-redundancy

- **Location:** `tests/test_proof_conflict.py:75::test_planted_conflict_markers_wake_skips_caption_zoom_prints_leaves`; `tests/test_wake.py:183::test_wake_conflict_sum_omits_caption`; `tests/test_zoom.py:36::test_zoom_conflict_sum_still_prints_leaves`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test recreates the same conflict-marked `.summ` fixture and combines the two observables already protected separately: wake omits the conflicted caption while zoom still returns both leaves. It adds no distinct assertion beyond the focused tests. This matches the cross-file equivalent-behavior signal in https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep the focused canonical tests in `test_wake.py` and `test_zoom.py`; delete the composite proof test after confirming its mutation kill-set is fully absorbed.
- **Why this isn't a false positive:** These are not different business concepts or mirrored products—the same pack corruption state and the same two public outcomes are asserted.

### 61. `tests/test_proof_reject.py:79::test_nap_unknown_ids_rejected_without_writing; tests/test_cli.py:271::test_unknown_prefix_is_error` — semantic-redundancy

- **Location:** `tests/test_proof_reject.py:79::test_nap_unknown_ids_rejected_without_writing`; `tests/test_cli.py:271::test_unknown_prefix_is_error`
- **Smell:** `semantic-redundancy`
- **Rationale:** Both invoke `nap deadbeef cafebabe`, require failure, require the same `unknown id` and wake-copy guidance, and verify that no nap is written. The subprocess fixture changes execution style but not the protected observable. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep one functional CLI test in the canonical CLI-rejection location, using the subprocess boundary plus the seeded-store no-nap assertion; delete the duplicate in-process case.
- **Why this isn't a false positive:** The tests protect the same command and rejection rule, not independent implementations or different error concepts.

### 62. `tests/test_proof_scopes.py:29::test_note_path_lands_in_started_store_else_ancestor; tests/test_scopes.py:104::test_note_path_writes_started_store; tests/test_scopes.py:120::test_note_path_rolls_up_when_unstarted` — semantic-redundancy

- **Location:** `tests/test_proof_scopes.py:29::test_note_path_lands_in_started_store_else_ancestor`; `tests/test_scopes.py:104::test_note_path_writes_started_store`; `tests/test_scopes.py:120::test_note_path_rolls_up_when_unstarted`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test combines exactly the two already-isolated scope outcomes: a path inside a started store writes there, while an unstarted sibling rolls up to the Git-root store without creating an intermediate store. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep the two focused tests in canonical `test_scopes.py`; delete the composite proof test after mutation-equivalence verification.
- **Why this isn't a false positive:** The subprocess fixture does not introduce a separate business rule; its assertions are the union of the two focused scope tests.

### 63. `tests/test_proof_scopes.py:50::test_root_wake_lists_other_stores_pull_prints_only_that_store; tests/test_scopes.py:278::test_root_wake_catalog_is_labeled_paths_not_commands; tests/test_scopes.py:325::test_pull_wake_omits_usage; tests/test_scopes.py:340::test_root_wake_catalogs_other_store; tests/test_scopes.py:385::test_pull_wake_omits_catalog_and_root_notes` — semantic-redundancy

- **Location:** `tests/test_proof_scopes.py:50::test_root_wake_lists_other_stores_pull_prints_only_that_store`; `tests/test_scopes.py:278::test_root_wake_catalog_is_labeled_paths_not_commands`; `tests/test_scopes.py:325::test_pull_wake_omits_usage`; `tests/test_scopes.py:340::test_root_wake_catalogs_other_store`; `tests/test_scopes.py:385::test_pull_wake_omits_catalog_and_root_notes`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test aggregates observables already covered by focused scope tests: root wake lists `./pkg` under the catalog without command syntax, while `wake --path pkg` displays only child-store content and omits usage, catalog, and root memories. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Retain the focused tests in `test_scopes.py` as the canonical capability coverage and delete the composite proof test once its mutation kill-set is shown to be absorbed.
- **Why this isn't a false positive:** The tests use the same root/child-store scenario and protect the same presentation and isolation rules, rather than distinct concepts.

## Tests considered but not flagged

None.

## Out-of-scope requests

None.
