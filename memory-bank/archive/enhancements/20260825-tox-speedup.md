---
task_id: tox-speedup
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: tox-speedup

## SUMMARY

Local full tox is `tox run-parallel` (py311–py314, `-p auto`). Iteration is `tox -e py311`. Tests load repo-root `summem` once per session via a pytest fixture. After reflect, CI split: [`.github/workflows/pr.yaml`](../../../.github/workflows/pr.yaml) runs the matrix on pull requests; [`.github/workflows/ci.yaml`](../../../.github/workflows/ci.yaml) runs the matrix plus coverage upload on pushes to `main`. Product CLI unchanged. Draft [PR #65](https://github.com/Texarkanine/SumMem/pull/65) closes #63.

## REQUIREMENTS

- One tox invocation for the full py311–py314 matrix (`tox run-parallel`, not `-j`).
- `.cursor/rules/SumMem-testing.mdc`: iterate on py311; full matrix at end-of-work; no overlapping tox on the same env in one checkout.
- Session-scoped `summem` fixture replacing per-test `load_summem()`.
- README / `techContext.md` Testing Process match the commands.
- TDD for fixture and tox.ini contracts. Suite green on py311–py314.
- Do not change product behavior; no pytest-xdist, testmon, or proof deletion.
- Original brief kept CI at coverage-on-3.11; operator later required the matrix on PRs/`main` and coverage upload only from `main`.

## IMPLEMENTATION

Level 2. Session fixture in [`tests/conftest.py`](../../../tests/conftest.py); cache is `conftest._SUMMEM` (not `sys.modules["summem"]` — migrate.py/surgery.py overwrite that). ~200 call sites in 21 test modules. [`tests/test_summem_fixture.py`](../../../tests/test_summem_fixture.py) locks cache identity, impostor `sys.modules` replace, monkeypatch undo, and no `load_summem` in other `test_*.py`. [`tox.ini`](../../../tox.ini) stays `pytest {posargs}` (no `--basetemp`). [`.cursor/rules/SumMem-testing.mdc`](../../../.cursor/rules/SumMem-testing.mdc). Separate worktrees can run tox concurrently (each has its own `.tox/`).

Post-reflect: PR workflow is matrix only; main CI is matrix plus `tox -e coverage` and Codecov.

## TESTING

TDD for fixture and tox.ini locks. First QA FAIL (`--basetemp` clobber; pytest-private fixture marker). Rework then QA PASS. `uvx --with tox tox run-parallel`: 355 tests, py311–py314 OK in ~48s.

## LESSONS LEARNED

- Pytest's default basetemp under tox is already outside the worktree and numbers concurrent runs (`pytest-0`…). An explicit `--basetemp` `rm_rf`s a fixed path with no numbering — a cross-checkout clobber. tox FAQ `{env_tmp_dir}` is inside the clone; this suite's outside-repo tests `chdir` to `tmp_path` and would wake the real store.
- `sys.modules["summem"]` is not a stable test cache while migrate.py/surgery.py reload the driver into that name.
- Asserting pytest private fixture markers is a change-detector when `deps = pytest` is unpinned.

## PROCESS IMPROVEMENTS

- Probe FAQ patterns against this suite (outside-repo `chdir`, two checkouts sharing `/tmp`) before locking them in tox.ini.
- Split PR vs main into two workflow files when the check sets differ, so PRs do not show a skipped coverage job.

## TECHNICAL IMPROVEMENTS

`m = summem` remains at 318 plan-sanctioned sites. `conftest.load_summem` and `tests/gitutil.py::_load_driver` still share a cache-then-load shape under different module keys.

## NEXT STEPS

- [PR #65](https://github.com/Texarkanine/SumMem/pull/65) on `feat/tox-speedup`. Review, then squash-merge when ready. pytest-xdist is still a separate issue.
