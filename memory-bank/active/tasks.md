# Task: slobac-audit-ratchet

* Task ID: slobac-audit-ratchet
* Complexity: Level 2
* Type: simple enhancement (test-suite hygiene)

Apply the obviously wrong and fixable remediations from `.slobac/2026-08-25T12-27-19/audit.md`. Leave the file-backend proof suite and other product-shaped findings. No product CLI change.

## Test Plan (TDD)

No new product behavior. The tests are the change. Each accepted finding gets a stronger oracle or less coupling in an existing case. There is no red-then-green product cycle: current `summem` already satisfies the stronger claims. Verification is the named test plus `tox -e py311` after each cluster.

### Behaviors to Verify

- Default pytest without `--cov` → `coverage/lcov.info` is unchanged if it already existed (same bytes) and still absent if it did not; no `lcov.info` is written under `tmp_path`.
- Suite load → every test still calls `load_summem()`; the unused `summem` fixture is gone.
- Zoom of an expand-frontier child id → output contains that child's known fixture text (not merely truthy).
- First child unlink during `write_nap` → exactly one `*.summ` and one `*.tree` already exist in `naps/`.
- Nap filename → stem starts with the left child's public `{stamp}-{rand}` from its note filename, without calling `_seq_prefix`.
- Recall of nested caption `pack-a` → exactly `x2 {short_id}: pack-a`; that id zooms to `a1`; `_projected_child` is not the oracle.
- Zoom of a nap-of-naps → exactly two `x2 {short_id}: pack-a` / `pack-b` lines; leaf texts absent; eight-hex prefixes; `_projected_child` is not the oracle.
- Rematerialize → destination names and bytes match the public `{left-stamp-rand}-{id}-{leaves}` shape; no `_nap_stem` equality assert.
- `reaches` with a fake `zoom_text` → finds `a1` when the fake returns hand-built wake lines (no `_projected_child`).
- Empty / over-long note or nap caption → `ValueError` matching the existing ratchet string; store unchanged.
- Note of 94 × `你` → `ValueError` matching the over-long ratchet; a 280-byte mix still writes.
- Non-UTC `now` → `ValueError` matching `clock must be UTC`.
- `main(["start"])` and `main(["version", "x"])` → exit `2` (argparse usage).

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini`, `pytest.ini`, `testpaths = tests`)
- Test location: `tests/`
- Conventions: `load_summem()` from `conftest.py`; `init_repo` from `gitutil.py`; no-suffix driver; no new runner
- New test files: none

## Implementation Plan

### 1. Disposition table — prose/policy

- Files: `memory-bank/active/progress.md` (reject reasons live there after build; this step is the plan's lock)
- No tests: prose/policy artifact

1. Treat these findings as **in**: 1, 2, 3, 5, 6, 7, 10, 13, 18, 19, 20, 21, 22, 32, 41, 42, 45, 46, 47.
2. Treat these findings as **out**, with the reason in the table below. Do not implement their prescribed remediations.

Rejected findings:

| # | Reason |
| --- | --- |
| 14 | The source-order pin is the only CI-effective guard on the 3.11 floor. The subprocess replacement skips unless CPython 3.10 is on the host; CI provisions only 3.11 and no `uv`. Deleting it trades implementation-coupled for rotten-green. |
| 4, 8, 11, 12 | Call-count spies are the wait-free / heal-on-mutate contract. A timeout is a worse oracle. |
| 9 | Leaf-integrity via `_digests_of_tree` after a planted malformed tree is same-module diagnosis, not a public CLI claim. |
| 15–17 | Prompt/how-to text is the product. Token checklists plus documented negatives are the current fitness function. A full golden is a change-detector. |
| 23–30, 43, 44, 50, 58 | `ValueError` plus a stable message is the ratchet. Typed exception classes are a product change. |
| 31, 48 | Already have structural asserts; truthiness is a narrowing precondition. |
| 33–40, 51–57 | CLI tokens are the contract; several already parse catalog sections. Whole-output goldens are change-detectors. |
| 49 | Public wake already pins dated leaves via `dated_leaf`. The helper unit is not a hole. |
| 59–63 | File-backend acceptance surface. "First proof N" is leftover VISION numbering. Overlaps are subprocess proofs next to in-process units. |

### 2. Dead scaffold — executable

- Files: `tests/conftest.py`

1. Stub tests: none. Existing suite already calls `load_summem()`.
2. Stub interface: none.
3. Write tests and run red: not applicable — deletion of a fixture no test injects. Delete `summem` in `conftest.py`. Leave `test_version_info_is_checked_before_import_tomllib` in place (finding 14 rejected).
4. Write code and run green: no product change. Run `tox -e py311 -- tests/test_version.py tests/test_cli.py tests/test_init.py`.

### 3. Coverage lcov isolation — executable

- Files: `tests/test_coverage_collection.py`

1. Stub tests: none. Keep `test_default_pytest_does_not_write_lcov`.
2. Stub interface: none.
3. Write tests and run red: one branchless oracle. Snapshot `before = watched.read_bytes() if watched.exists() else None` before the subprocess; after it, snapshot again the same way and `assert after == before`. Keep the `tmp_path / "lcov.info"` absence check.
4. Write code and run green: no product change. Run `tox -e py311 -- tests/test_coverage_collection.py::test_default_pytest_does_not_write_lcov`.

### 4. Vacuous oracles — executable

- Files: `tests/test_wake_expand.py`, `tests/test_nap.py`, `tests/test_store.py`, `tests/test_scopes.py`, `tests/test_version.py`

1. Stub tests: none. Strengthen existing cases listed below.
2. Stub interface: none.
3. Write tests and run red: apply these oracles (current product already satisfies them):
    - `test_zoom_expanded_child_id`: after `zoom_text`, assert fixture content from `_two_eights` (a known nested caption or dated leaf), not `assert out`.
    - `test_first_unlink_sees_both_parent_files`: `len(seen["sum"]) == 1` and `len(seen["tree"]) == 1`.
    - `test_nap_rejects_empty_caption`: `pytest.raises(ValueError, match="note is empty")`.
    - `test_nap_rejects_overlong_caption`: `match="Too long"`.
    - `test_note_rejects_empty`: `match="note is empty"`.
    - `test_note_rejects_over_280_bytes` and `test_note_280_is_utf8_bytes_not_chars`: `match="Too long"`.
    - `test_note_rejects_non_utc_now`: `match="clock must be UTC"`.
    - `test_start_without_dir_is_usage` and `test_version_rejects_extra_args`: `== 2`.
4. Write code and run green: no product change. Run the named tests under `tox -e py311`.

### 5. Private-helper oracles — executable

- Files: `tests/test_fold.py`, `tests/test_zipper.py`, `tests/test_recall.py`, `tests/test_zoom.py`, `tests/test_gitutil.py`

1. Stub tests: none. Same test names; new expected-value construction.
2. Stub interface: none. Do not add a product helper and do not copy `_seq_prefix`. A note filename is already `{stamp}-{rand}`; use `pa.name` / `nodes[0].name` / `paths[0].name` as the public prefix.
3. Write tests and run red:
    - `test_nap_stem_inherits_left_child_seq_prefix`: expected stem `f"{pa.name}-{leafset}-2"`.
    - `test_same_second_notes_keep_left_child_stem`: `left_seq = nodes[0].name`.
    - `test_rematerialize_nap_stem_uses_leftmost_seq_child_id_and_leaves`: leftmost `paths[0].name`; leaves `2`; drop `assert m._nap_stem(child) == stem`.
    - `test_rematerialize_does_not_clobber_existing_dest`: drop `assert m._nap_stem(child) == node.name`.
    - `test_recall_matches_nested_nap_caption`: exact line `f"x2 {m.short_id(kid.id, ids)}: pack-a"` from the public tree child; keep zoom-to-`a1` and `"both" not in out`; stop calling `_projected_child`.
    - `test_zoom_nap_of_naps_prints_two_children_not_leaves`: exact two lines `x2 {short_id}: pack-a` / `pack-b`; leaf texts absent; keep `all(len(m.short_id(child.id, ids)) == 8 …)`; stop calling `_projected_child`.
    - `test_reaches_nested_sentence_when_zoom_prints_wake_lines`: fake `zoom_text` returns those same hand-built pack lines (or dated leaves for `a1`/`a2`); no `_projected_child`.
4. Write code and run green: no product change. Run `tox -e py311 -- tests/test_fold.py tests/test_zipper.py tests/test_recall.py tests/test_zoom.py tests/test_gitutil.py`.

### 6. Full suite — executable

- Files: none new

1. Stub tests: none.
2. Stub interface: none.
3. Write tests and run red: none.
4. Write code and run green: `tox` (all configured envs). Fix only failures caused by this task.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest / tox / `load_summem` / `init_repo`
- Audit file `.slobac/2026-08-25T12-27-19/audit.md` (read-only punch list)

## Challenges & Mitigations

- Strengthening `match=` will look like loose-text-oracle to a later audit: already rejected as the product ratchet; do not add exception classes.
- Expand-frontier child content is not obvious from `_two_eights`: the helper plants `eight-a-5` next to leaf `a7`; assert one of those.

## Pre-Mortem

- The build treats the audit as a mandatory punch list and goldens prompts or deletes proofs: already locked out by step 1 and the brief.
- A "stronger" oracle is actually weaker (substring instead of exact line): prefer exact membership / counts; do not replace an exact `==` with `in` except where the old oracle was a private helper dump.
- Argparse exit-code assumption is wrong: preflight already confirmed `main(["start"])` and `main(["version", "x"])` return `2`.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
