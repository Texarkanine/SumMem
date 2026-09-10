# Progress

Rework of PR #84: monotonic 30s `msvcrt` lock deadline, host-pinned invoke tests, timeout regression test.

**Complexity:** Level 1

## 2026-09-10 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified windows-compat-review as Level 1 (isolated review fixes on the existing Windows lock/invoke surface).
* Decisions made
    - Bug-fix tree, single component: `_with_runtime_lock` plus tests that already live on this branch. No creative/plan/preflight.
* Insights
    - QA already named the accumulator as a non-blocking OptMem-parity advisory; this rework treats the `30.0` vs elapsed-time mismatch as a defect.
