# Progress

Split the baked SumMem note prompt so the mandatory-note workflow and the clone-portability membership test are separate sentences. No store or CLI change.

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent from the standalone creative; operator approved.
    - Classified Level 2 (self-contained enhancement to `prompt_text()` / `AGENTS.md`).
* Decisions made
    - Task id: prompt-membership.
    - Creative doc `creative-note-membership.md` is the design record; plan should not reopen store/CLI/OptMem/redact.
* Insights
    - The leaked note stays; this task does not flatten or rewrite it.

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - One executable step: substring/structure tests in `tests/test_init.py`, then `prompt_text()` split and `AGENTS.md` lockstep.
* Decisions made
    - New invariants: `clone` in `prompt_text()`; the `Call it whenever` sentence must not contain `personal` / `machine-local`.
    - No full-prompt snapshot. No #14 / git-add work on this branch.
* Insights
    - Existing `personal` / `contributor` checks are already policy-as-contract; clone-portability fits that pattern.
