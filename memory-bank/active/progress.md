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
