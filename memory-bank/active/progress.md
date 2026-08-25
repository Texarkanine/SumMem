# Progress

Apply obviously wrong and fixable remediations from the 2026-08-25 SLOBAC audit of `tests/`. Leave the file-backend proof suite and other product-shaped findings. Rework: pin `test_zoom_expanded_child_id` to this child's public wake lines so `zoom_text` cannot ignore `child.id`.

**Complexity:** Level 1

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent confirmed: audit is a ratchet; models acceptable; judge-and-fix, not 100%.
    - Findings 59–63 inspected against the proof files and the overlapping focused tests.
    - Classified Level 2.
* Decisions made
    - Leave 59–63. `test_proof_*.py` is the acceptance surface in product/tech context. "First proof N" is leftover VISION numbering, not a reason to regroup or delete.
    - The 60–63 "redundancies" are subprocess proofs sitting next to in-process units of the same rule. That is layering, not dead weight.
* Insights
    - Several other findings pair `vacuous-assertion` (no `match=`) with `loose-text-oracle` (has `match=`). Those cancel: the product ratchet is `ValueError` plus a stable message.

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Level 2 plan written: 20 accepted findings, 43 rejected with reasons.
    - No new product behavior; tests are the change.
* Decisions made
    - Do not golden `prompt_text` / `how_to_text`.
    - Do not add typed exceptions.
    - Do not remove heal/wake call-count spies (they are the wait-free contract).
    - Derive nap `{stamp}-{rand}` from the public filename, not `_seq_prefix`.
* Insights
    - Leftover `memory-bank/active/creative/` files are from archived tasks and are not this design.

## 2026-08-25 - PREFLIGHT - COMPLETE

* Work completed
    - `.preflight-status` first line: `FAIL (fixable)`.
    - Verified baseline before judging: `tox -e py311` → 284 passed.
    - Checked every named test exists, every `match=` string against `require_entry` / `require_utc`, both exit-code claims against `main`'s argparse handling, and the `_two_eights` / `_two_notes` fixtures behind the new oracles.
    - Confirmed all 20 accepted findings map to a concrete substep, and the `summem` fixture is unused (no signature, no `getfixturevalue`).
* Decisions made
    - TDD Plan Encoding passes; no in-phase plan edits made.
    - Fail on unit 2: deleting `test_version_info_is_checked_before_import_tomllib` leaves the 3.11-floor ordering unenforced in CI, because the replacement subprocess test skips where no CPython 3.10 exists and `ci.yaml` provisions only 3.11 with no `uv`.
* Insights
    - `_seq_prefix` is the first two hyphen fields, and a note filename has exactly two — so `pa.name` is the exact public expected value and no test-local helper is needed.
    - `ProjectedNode` is public, so exact wake-line equality is reachable without `_projected_child`; the plan's substring oracles are weaker than achievable.

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Re-planned after FAIL (fixable): 19 accepted findings, finding 14 rejected.
* Decisions made
    - Keep `test_version_info_is_checked_before_import_tomllib`. CI has no 3.10, so the source-order pin is the floor guard that actually runs there.
    - Coverage oracle is one before/after byte snapshot (`None` if absent).
    - Note seq prefix is the public filename; exact wake lines from `short_id` + caption.

## 2026-08-25 - PREFLIGHT - COMPLETE

* Work completed
    - `.preflight-status` first line: `PASS WITH ADVISORY`.
    - Revalidated all 19 accepted findings, rejected-finding coverage, TDD ordering, file locations, public-oracle construction, and downstream test impact.
    - Verified the baseline with `uvx --with tox tox -e py311`: 284 passed.
* Decisions made
    - The revised plan resolves the prior blocker by retaining the CI-effective Python 3.11 import-order guard.
    - Proceed to build without replanning.
* Insights
    - Removing the unused fixture also leaves an unused `pytest` import in `tests/conftest.py`; remove both together during build.
    - A test-owned pack-line helper could independently encode shared wake grammar, but it remains optional extra scope.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - 19 accepted findings applied in existing tests. Unused `summem` fixture and `pytest` import removed.
    - `tox` py311–py314: 284 passed.
* Decisions made
    - Expand-child zoom oracle is `bN` / `eight-b-N` because expand walks the right 8-pack.
    - No product file changed.
* Insights
    - Finding 14 stays: CI still has no CPython 3.10, so the source-order pin is the floor guard that runs there.

## 2026-08-25 - QA - COMPLETE

* Work completed
    - Reviewed test oracle changes and dead scaffold removal against the TDD plan.
    - Verified `test_coverage_collection.py` branchless snapshot implementation.
    - Confirmed public wake lines were constructed properly without private test helpers.
    - Verified that no product files were changed.
* Decisions made
    - Assessed as PASS. The implementation matches the preflight and plan strictly, avoiding both regressions and YAGNI.

## 2026-08-25 - REFLECT - COMPLETE

* Work completed
    - Reflection at `memory-bank/active/reflection/reflection-slobac-audit-ratchet.md`.
    - Persistent files scanned; none updated.
* Decisions made
    - Standalone task: next operator step is `/niko-archive`.
* Insights
    - Note filename is already the seq prefix. The 3.10 subprocess proof is not CI coverage.

## 2026-08-25 - REWORK - Phase A fossils

* Work completed
    - Operator corrected finding 59: leftover VISION numbering is the smell. Phase A applied.
    - Renamed `test_proof_*.py` to capability files; stripped `First proof N` from module lines.
    - `productContext.md` / `techContext.md` no longer glob `test_proof_*`.
* Decisions made
    - Findings 60–63 still left: same rule, different harness. No Phase B regroup.

## 2026-08-25 - PR #48

* Work completed
    - Pushed `initial-slobac` and opened non-draft https://github.com/Texarkanine/SumMem/pull/48 so automated reviewers run.

## 2026-08-25 - REWORK INITIATED - PR #48 zoom oracle

* Work completed
    - Operator chose rework, not archive.
    - Feedback: [discussion_r3856003101](https://github.com/Texarkanine/SumMem/pull/48#discussion_r3856003101) on `tests/test_wake_expand.py`. The nap-branch `any(b{i} or eight-b-{i})` oracle stays green if `zoom_text` ignores `child.id` (fake `x2 00b0aaaa: eight-a-0`, or this fixture's `wake_text`).
* Decisions made
    - Pin exact public wake lines: `x5 …: eight-b-3` plus dated `b5`. Same style as `test_zoom_nap_of_naps_prints_two_children_not_leaves`.
    - Do not add substring-absent `b6`/`b7` checks; those bigrams can appear in a hex prefix.

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Rework classified Level 1: one test oracle in `tests/test_wake_expand.py`.
* Decisions made
    - Bug fix, single component. L1 skips plan, creative, and preflight; go to build.
* Insights
    - The first non-file frontier child is the `eight-b-4` nap; its zoom is `x5 …: eight-b-3` plus dated `b5`.
