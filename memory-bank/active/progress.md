# Progress

Apply obviously wrong and fixable remediations from the 2026-08-25 SLOBAC audit of `tests/`. Leave the file-backend proof suite and other product-shaped findings.

**Complexity:** Level 2

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
