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

## 2026-09-10 - BUILD - COMPLETE

* Work completed
    - `_with_runtime_lock` msvcrt loop: monotonic 30s deadline, sleep clamped to remainder.
    - Regression test `test_with_store_lock_msvcrt_retry_deadline_is_elapsed`.
    - Host pin `_host_needs_interpreter` on POSIX invoke/`Run:`/catalog asserts.
    - `tox -e py311`: 388 passed.
* Decisions made
    - Keep the 0.01 spin increment for backoff; elapsed time is only the deadline.
    - Pin the host check, not `os.name`.
* Insights
    - The red test saw `sum(sleeps) == 735.48` before the deadline fix.

## 2026-09-10 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the lock-deadline fix and host-pinned output assertions against the project brief.
    - Verified `uvx --with tox tox -e py311`: 388 passed.
* Decisions made
    - Accepted the rework as-is; no Build or Plan rerun is required.
* Insights
    - The fake monotonic-clock test exercises the exact elapsed-time boundary without relying on a Windows host.
