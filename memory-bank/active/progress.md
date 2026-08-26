# Progress

Investigate whether pytest-xdist is safe inside each tox env, then apply it (with serial markers only where needed) so tests within an env can run in parallel. Specified by [issue #64](https://github.com/Texarkanine/SumMem/issues/64).

**Complexity:** Level 2

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated against issue #64 and approved
    - Classified as Level 2 (self-contained test-runner enhancement)
* Decisions made
    - Within-env xdist only; parallel tox envs stay #63's job
    - Empirical investigation before enabling by default
* Insights
    - Session-scoped `summem` fixture from #63 is already on the tree; xdist must live with that cache (`conftest._SUMMEM`)

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Technology validation: installed pytest-xdist 3.8.0 in `.tox/py311` and ran the suite
    - Wrote the Level 2 plan in `tasks.md`
* Decisions made
    - Safe with no serial markers (355 passed under `-n auto` and `-n 8`)
    - Default `[testenv]` command will be `pytest -n auto {posargs}`; do not put `-n` in `pytest.ini` or coverage commands
    - Do not bake `--maxprocesses` (16-wide was slower than 8-wide here but still beat serial; override via posargs)
* Insights
    - Flock/sys.modules/worktree risks in #64 did not fire: locks and git state are per `tmp_path`; each xdist worker is a process with its own session fixture
    - pytest-cov can combine xdist workers; we still keep `tox -e coverage` serial as the issue allowed

## 2026-08-25 - PREFLIGHT - COMPLETE

`.preflight-status` first line: `FAIL (fixable)`

* Work completed
    - Validated the plan against `tox.ini`, `tests/test_tox_runner.py`, README, CI workflows, and the Level 2 workflow references
    - TDD encoding passed; no change-detector strike and no test/code step swap, so `tasks.md` was not edited
    - Measured the `tox run-parallel` interaction: 4 concurrent envs at 53s serial-within-env vs 67s with `-n auto` each (355 passed per env both times, py311-py314)
    - Verified `-n 0` is legal and last-wins over `-n auto`, and that xdist 3.8.0 installs and passes on py312/py313/py314
* Decisions made
    - FAIL (fixable) on two grounds: the plan does not account for `-n auto` multiplying against #63's `tox run-parallel` (and its `--maxprocesses` prohibition rests on single-env data), and AC3's serial-marker justification has no owning step in any Level 2 phase
* Insights
    - The two parallelism dials compound: `-n auto` per env times 4 concurrent envs is ~64 workers on 16 cores, making the documented full-matrix command ~26% slower even though every env stays green
    - CI is unaffected in kind - `pr.yaml` and `ci.yaml` run one env per job, so oversubscription is a local-matrix-only concern

## 2026-08-25 - PLAN - COMPLETE (rework)

* Work completed
    - Measured `-n 4`: py311 19.55s (fastest single-env width); `tox run-parallel -- -n 4` 31.49s vs 53s serial-within-env and 67s unbounded auto
    - Rewrote `tasks.md`: cap `--maxprocesses=4`, owned AC3 via `gh issue comment` during Build, matrix step compares wall time to `-n0`
* Decisions made
    - Accepted trade-off: `pytest -n auto --maxprocesses=4 {posargs}` — not unbounded auto, not a `PYTEST_WORKERS` env var (forgettable unsafe default)
    - 4 is a suite cap (git-heavy tests + four tox envs), not this machine's nproc; CI 2-core still gets 2 workers
* Insights
    - The cap that saves the matrix is also the fastest iteration width here; those two constraints agreed rather than traded

## 2026-08-25 - PREFLIGHT - COMPLETE (rework)

`.preflight-status` first line: `PASS WITH ADVISORY`

* Work completed
    - Revalidated TDD ordering, conventions, dependency impact, conflicts, and requirement coverage against the revised plan and current tox/test/CI surfaces
    - Confirmed the worker cap resolves the local matrix regression and the issue-comment step owns the zero-marker justification
    - Confirmed pytest-xdist documents `--maxprocesses` as an upper bound on `-n auto` and `-n0` as serial execution
* Decisions made
    - Build may proceed with `pytest -n auto --maxprocesses=4 {posargs}`
    - No TDD step swap or change-detector strike was required; `tasks.md` was not edited
* Insights
    - The revised matrix verification protects performance as an acceptance condition, not merely test correctness
    - Advisory only: a future scheduled py311 soak at worker counts 2 and 4 could detect low-frequency races without burdening required PR checks

## 2026-08-25 - BUILD - IN-PROGRESS

* Work completed
    - TDD: three contracts in `tests/test_tox_runner.py`; `tox.ini` `[testenv]` is `pytest -n auto --maxprocesses=4 {posargs}` with `pytest-xdist` in deps
    - Docs: README, `techContext.md`, `.cursor/rules/SumMem-testing.mdc`
    - [Issue #64 comment](https://github.com/Texarkanine/SumMem/issues/64#issuecomment-5419816806): serial-marker count **0**; flock / session fixture / subprocess / worktree tests ran under xdist on `tmp_path` and per-worker processes; 358 passed on `tox -e py311` (4 workers, 19.96s)
* Decisions made
    - Coverage test `test_coverage_env_runs_serial` was already green before the tox.ini edit (asserting absence of `-n`); kept as a lock so coverage cannot pick up workers
* Insights
    - None yet; matrix vs `-n0` still to run

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - Shipped `[testenv] commands = pytest -n auto --maxprocesses=4 {posargs}` with `pytest-xdist` in deps
    - 358 passed on `tox -e py311` (4 workers, 19.96s); `tox run-parallel` 28.77s vs same-session `-n0` 38.78s; `tox -e coverage` 358 passed serial, `coverage/lcov.info` written, no xdist workers
    - Serial markers: **0**. Justification: [issue comment](https://github.com/Texarkanine/SumMem/issues/64#issuecomment-5419816806)
* Decisions made
    - Built to plan. One TDD quirk: `test_coverage_env_runs_serial` was green before the tox.ini change because it asserts `-n` stays absent
* Insights
    - The shipped matrix is faster than serial-within-env, not merely green
    - Coverage env installs xdist (inherited deps) but does not start workers without `-n`
