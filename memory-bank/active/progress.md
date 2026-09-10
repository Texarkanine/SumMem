# Progress

Rework of PR #84: `init` always says `python .summem/summem wake`; wake Usage/`Run:` are host-specific (`python ` on Windows, bare on *nix).

**Complexity:** Level 2

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

## 2026-09-10 - REWORK - INITIATED

* Work completed
    - Operator feedback from native Windows PowerShell and CMD: the driver technically works; refine invoke recipes.
* Decisions made
    - `init` always tells agents to run `python .summem/summem wake` (python on PATH; Windows and *nix).
    - Root `wake` Usage/`Run:` stay host-specific: bare `.summem/summem` on *nix, `python ` prefixed on Windows.
    - Drop the Windows-only `init` warning and quoted `sys.executable` recipes.

## 2026-09-10 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified this rework as Level 2 (invoke-recipe enhancement; bootstrap contract change).
* Decisions made
    - Enhancement tree, self-contained: `prompt_text` / `init_text` / `agent_invoke` / lockstep `AGENTS.md`. Not a bug fix.
* Insights
    - Operator specified both recipes; remaining work is lockstep and dropping `sys.executable`, not exploring hosts.

## 2026-09-10 - PLAN - COMPLETE

* Work completed
    - Test plan: bootstrap wake, host-agnostic init, POSIX vs Windows `agent_invoke`, fold `Run:`, AGENTS.md lockstep.
    - Implementation: retarget `tests/test_init.py` / `tests/test_fold.py`, then `summem` + `AGENTS.md`, then briefing/notes.
* Decisions made
    - Wake handoff in `prompt_text` is always `python .summem/summem wake`. Intro may still name `{AGENT_BIN}`.
    - Windows Usage/`Run:` use unquoted `python .summem/summem`, not `sys.executable`.
* Insights
    - `python .summem/summem note` contains `.summem/summem note`; Windows tests cannot forbid that substring.

## 2026-09-10 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Verified TDD ordering, convention compliance, dependency impact (checked `test_scopes.py`, `test_surgery.py`, `test_fold.py`, README for hidden touchpoints beyond the plan's file list), conflict detection, and completeness against `projectbrief.md`.
* Decisions made
    - No plan edits required beyond the already-scheduled TDD ordering; no change-detector strikes needed.
* Insights
    - Requirement 4 (push the branch) has no scheduled step; tracked as advisory, not a blocking gap.
    - Radical-innovation advisory: a `cmd`/POSIX polyglot launcher would remove the need for `agent_invoke()`'s host branch entirely; recorded, not applied.

## 2026-09-10 - BUILD - COMPLETE

* Work completed
    - `agent_invoke()`: `python {AGENT_BIN}` on nt; `prompt_text` wake always that command; `init_text` host-agnostic.
    - Retargeted init/fold tests; lockstep `AGENTS.md`; briefing and `docs/notes.md`.
    - `tox -e py311`: 389 passed.
* Decisions made
    - Intro still names `{AGENT_BIN}`; only the wake line is `python …`.
    - Windows tests forbid backtick-bare recipes, not the substring `.summem/summem note`.
* Insights
    - Quoted `sys.executable` is gone from agent-facing output.

## 2026-09-10 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the invoke-recipe rework against `projectbrief.md`'s final Rework requirements and `tasks.md`'s plan.
    - Re-ran `tox -e py311 tests/test_init.py tests/test_fold.py -n0` (45 passed) and the full `tox -e py311` (389 passed).
    - Repo-wide search confirmed no stale `sys.executable` / Windows-warning references outside the correctly-untouched archive files.
* Decisions made
    - Accepted the rework as-is; no Build or Plan rerun required.
* Insights
    - `test_init_text_posix_has_no_windows_warning` is now fully subsumed by `test_init_text_is_host_agnostic` (which proves `windows == posix`); flagged as a non-blocking, pre-existing DRY advisory rather than a defect.
    - Requirement 4 (push `windows-support`) is still open — a delivery action, not a code gap.

## 2026-09-10 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-windows-compat-review.md`.
* Decisions made
    - Persistent files were already reconciled in Build; no further briefing edits.
* Insights
    - `python` on PATH is clone-portable; `sys.executable` is not.
