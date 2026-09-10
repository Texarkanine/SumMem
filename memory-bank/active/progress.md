# Progress

Make SumMem able to launch and run on native Windows with the smallest capability-based internals port: store lock, CRLF-on-read, host invoke strings, and an init warning above the fold. Spec: `memory-bank/archive/enhancements/20260909-windows-compat-audit.md`. Do not advertise Windows.

**Complexity:** Level 2

## 2026-09-09 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified windows-compat as Level 2
    - Wrote project brief from the approved restatement
* Decisions made
    - Level 2: self-contained enhancement against an already-decided audit spec; multiple surfaces in one driver, no architectural redesign
* Insights
    - Capability-vs-OS is a planning constraint, not a reason to raise complexity; OptMem already has the lock pattern

## 2026-09-09 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 TDD plan: store reads, lock fallback, host invoke + init warning, shebang gate, prose
* Decisions made
    - Lock: try directory flock, else runtime-dir file (`fcntl` then `msvcrt`); not `if windows` in the lock path
    - Invoke/init warning: single `os.name == "nt"` in `agent_invoke()`; `prompt_text()` stays Unix
    - CRLF: always canonicalize on read; no platform branch
* Insights
    - `init` cannot import `fcntl` to decide the warning; `os.name` is the allowed host check

## 2026-09-09 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the Level 2 plan against the driver, test suite, audit specification, and documented architecture
    - Confirmed conventions, downstream lock consumers, CRLF read surfaces, and non-advertisement constraints are otherwise covered
* Decisions made
    - Return the plan to planning before build so the new `msvcrt` branch has executable coverage
* Insights
    - A fallback-success test does not prove the `msvcrt` byte-range lock works; the runtime file must contain a defined byte before locking, and the lock/unlock path needs a fake-backend test

## 2026-09-09 - PLAN - COMPLETE

* Work completed
    - Added `msvcrt` oracle tests to unit 2 (append, one byte, lock/unlock, retry) and split `fcntl`-on-file fallback from the `msvcrt` path
* Decisions made
    - Fake `msvcrt` is the required test; native Windows CMD probe stays optional skip
    - Empty runtime lock file gets exactly one `b"\0"` before `LK_NBLCK`
* Insights
    - Directory-flock miss with `fcntl` still present is a different backend than `fcntl` missing (`msvcrt`)

## 2026-09-09 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Re-validated the re-planned Level 2 plan; confirmed the prior FAIL's `msvcrt` coverage gap is closed
    - Traced every raw content-addressed read site in the driver against the plan's canonicalization points; traced every `with_store_lock` and `AGENT_BIN` consumer
* Decisions made
    - Plan proceeds to Build; three non-blocking advisories recorded (dead `import fcntl` in `test_zipper.py` after the wake-test rewrite, a docstring update on `with_store_lock`, and a radical-innovation idea for a single read choke-point)
* Insights
    - `leaf_digests` bypasses `loads_tree` and parses `.tree` JSON directly; the plan already names this as a required canonicalization site, matching the Pre-Mortem's stated risk

## 2026-09-09 - BUILD - COMPLETE

* Work completed
    - Implemented CRLF canonicalize-on-read, capability lock, host invoke + init warning, shebang gate, and stance/docs updates
    - tox -e py311: 387 passed
    - Native Windows Python: version, init warning above ---, note Saved.
* Decisions made
    - Patch `_host_needs_interpreter` in tests, not `os.name`
    - Runtime lock file `"ab+"` with one `b"\0"` byte
* Insights
    - `os.name = "nt"` on Linux makes pathlib raise `cannot instantiate 'WindowsPath'`

## 2026-09-09 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of the build against the plan: all four executable units and both prose units verified in the diff; every raw store read traced to a canonicalization point; lock consumers (`note`, `nap`, `surgery.py`) confirmed to catch `ValueError("cannot lock")` without a traceback
    - Reran `tox -e py311`: 387 passed
    - Wrote `.qa-validation-status` (PASS, two advisories) and QA results in `tasks.md`
* Decisions made
    - Both plan deviations (patch `_host_needs_interpreter`, `"ab+"` lock file) accepted as justified and recorded
    - `msvcrt` retry-cap arithmetic (counter, not wall time; ~12 min effective bound) judged faithful to the plan's cited OptMem oracle — advisory, not a build defect
* Insights
    - The plan's "30s cap" language overstates the oracle's wall-clock bound; fixing it would be a plan-level change that also applies to OptMem upstream
