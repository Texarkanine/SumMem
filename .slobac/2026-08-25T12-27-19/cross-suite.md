Consumed richness: compact

## Findings

### `deliverable-fossils`

- **Location:** `tests/test_proof_branches.py` (both tests); `tests/test_proof_conflict.py` (both tests); `tests/test_proof_ingest.py::test_two_worktrees_note_merge_without_conflict`; `tests/test_proof_reject.py` (all four tests); `tests/test_proof_scopes.py` (both tests); `tests/test_proof_squash.py::test_three_packs_squash_clone_zooms_originals`
- **Smell:** `deliverable-fossils`
- **Rationale:** All six modules are organized as numbered “First proof 1” through “First proofs 7 and 8,” matching the taxonomy signal for files and docstrings that mirror a delivery breakdown. The files scatter durable capabilities—Git workflows, CLI rejection, and store scoping—under historical proof numbers. See https://texarkanine.github.io/slobac/taxonomy/deliverable-fossils/
- **Prescribed remediation:** Apply Phase B regrouping: place merge, branch, conflict, and squash/clone scenarios under a Git-workflows capability; move subprocess rejection scenarios under CLI rejection coverage; and consolidate `--path` and root-catalog behavior under `test_scopes.py`. Remove proof numbering and produce a before/after behavior-to-test map before moving code.
- **Why this isn't a false positive:** “Proof” is delivery vocabulary found only in test filenames and module docstrings, not a product entity or behavior in the SUT.

### `semantic-redundancy`

- **Location:** `tests/test_proof_conflict.py:75::test_planted_conflict_markers_wake_skips_caption_zoom_prints_leaves`; `tests/test_wake.py:183::test_wake_conflict_sum_omits_caption`; `tests/test_zoom.py:36::test_zoom_conflict_sum_still_prints_leaves`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test recreates the same conflict-marked `.summ` fixture and combines the two observables already protected separately: wake omits the conflicted caption while zoom still returns both leaves. It adds no distinct assertion beyond the focused tests. This matches the cross-file equivalent-behavior signal in https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep the focused canonical tests in `test_wake.py` and `test_zoom.py`; delete the composite proof test after confirming its mutation kill-set is fully absorbed.
- **Why this isn't a false positive:** These are not different business concepts or mirrored products—the same pack corruption state and the same two public outcomes are asserted.

- **Location:** `tests/test_proof_reject.py:79::test_nap_unknown_ids_rejected_without_writing`; `tests/test_cli.py:271::test_unknown_prefix_is_error`
- **Smell:** `semantic-redundancy`
- **Rationale:** Both invoke `nap deadbeef cafebabe`, require failure, require the same `unknown id` and wake-copy guidance, and verify that no nap is written. The subprocess fixture changes execution style but not the protected observable. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep one functional CLI test in the canonical CLI-rejection location, using the subprocess boundary plus the seeded-store no-nap assertion; delete the duplicate in-process case.
- **Why this isn't a false positive:** The tests protect the same command and rejection rule, not independent implementations or different error concepts.

- **Location:** `tests/test_proof_scopes.py:29::test_note_path_lands_in_started_store_else_ancestor`; `tests/test_scopes.py:104::test_note_path_writes_started_store`; `tests/test_scopes.py:120::test_note_path_rolls_up_when_unstarted`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test combines exactly the two already-isolated scope outcomes: a path inside a started store writes there, while an unstarted sibling rolls up to the Git-root store without creating an intermediate store. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Keep the two focused tests in canonical `test_scopes.py`; delete the composite proof test after mutation-equivalence verification.
- **Why this isn't a false positive:** The subprocess fixture does not introduce a separate business rule; its assertions are the union of the two focused scope tests.

- **Location:** `tests/test_proof_scopes.py:50::test_root_wake_lists_other_stores_pull_prints_only_that_store`; `tests/test_scopes.py:278::test_root_wake_catalog_is_labeled_paths_not_commands`; `tests/test_scopes.py:325::test_pull_wake_omits_usage`; `tests/test_scopes.py:340::test_root_wake_catalogs_other_store`; `tests/test_scopes.py:385::test_pull_wake_omits_catalog_and_root_notes`
- **Smell:** `semantic-redundancy`
- **Rationale:** The proof test aggregates observables already covered by focused scope tests: root wake lists `./pkg` under the catalog without command syntax, while `wake --path pkg` displays only child-store content and omits usage, catalog, and root memories. See https://texarkanine.github.io/slobac/taxonomy/semantic-redundancy/
- **Prescribed remediation:** Retain the focused tests in `test_scopes.py` as the canonical capability coverage and delete the composite proof test once its mutation kill-set is shown to be absorbed.
- **Why this isn't a false positive:** The tests use the same root/child-store scenario and protect the same presentation and isolation rules, rather than distinct concepts.

No cross-suite findings for scope `wrong-level`.
