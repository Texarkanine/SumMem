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
