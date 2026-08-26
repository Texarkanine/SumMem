# Task: tox-speedup

* Task ID: tox-speedup
* Complexity: Level 2
* Type: simple enhancement

Speed up local tox without changing product behavior: document `tox run-parallel` as the full matrix, isolate pytest temps so parallel envs do not stomp, add an agent iteration rule, and load the driver once per session via a pytest fixture.

Spec: [issue #63](https://github.com/Texarkanine/SumMem/issues/63).

## Test Plan (TDD)

### Behaviors to Verify

- Session fixture: requesting `summem` → the object is the SourceFileLoader module for repo-root `summem`, and the fixture scope is `session`.
- Monkeypatch restore: `monkeypatch.setattr(summem, "WAKE_LINES", 1)` then `monkeypatch.undo()` → `summem.WAKE_LINES` is the original default (32).
- Call-site contract: every `tests/test_*.py` except `test_summem_fixture.py` → source text does not contain `load_summem` (`conftest.py` still defines the loader; the contract test may mention the name).
- Parallel-safe pytest: `tox.ini` `[testenv]` commands → `pytest --basetemp="{env:TMPDIR:/tmp}/summem-{env_name}" {posargs}` (coverage env pytest line includes the same `--basetemp`; not `{env_tmp_dir}`, which is inside the git worktree).
- Unchanged tox contract: env_list stays py311–py314; `package = skip`; coverage stays out of env_list; default commands still have no `--cov`.
- Existing suite: any test that used `load_summem()` → same assertions via the `summem` fixture; process-level git/worktree proofs unchanged.

No tests for README, `techContext.md`, or `.cursor/rules/SumMem-testing.mdc` (prose/policy; a content lock would be a change-detector).

### Test Infrastructure

- Framework: pytest via tox (`pytest.ini` `testpaths = tests`; `tox.ini` `package = skip`)
- Test location: `tests/`
- Conventions: `test_*.py`, helpers in `tests/conftest.py` (`ROOT`, `SCRIPT`, `dated_leaf`, `load_summem`); tox.ini locked with stdlib `ConfigParser(interpolation=None)` in `tests/test_tox_runner.py`; do not subprocess tox from pytest
- New test files: `tests/test_summem_fixture.py`

## Implementation Plan

### 1. Session-scoped summem fixture — executable

- Files: `tests/conftest.py`, `tests/test_summem_fixture.py`

1. Stub tests: `tests/test_summem_fixture.py` empty cases `test_summem_fixture_is_session_scoped`, `test_summem_is_repo_root_driver`, `test_monkeypatch_on_summem_restores_after_undo`.
2. Stub interface: in `tests/conftest.py`, `@pytest.fixture(scope="session")` `summem()` with empty body; keep `load_summem()` as the loader.
3. Write tests and run red: fixture scope is `session` via the pytest fixture marker; `summem.__file__` equals `SCRIPT`; after setattr+undo, `WAKE_LINES == 32`.
4. Write code and run green: `summem` fixture returns `load_summem()`. Cache the loaded module in `load_summem()` (return `sys.modules["summem"]` when that module's `__file__` is `SCRIPT`) so an accidental extra call cannot replace the session object.

- [x] Done

### 2. Replace per-test load_summem call sites — executable

- Files: `tests/test_summem_fixture.py`; every `tests/test_*.py` that currently does `from conftest import load_summem` / `m = load_summem()` (21 files: `test_branch_pack_merge`, `test_caption_conflict`, `test_cli`, `test_codec`, `test_fold`, `test_gitutil`, `test_init`, `test_migrate`, `test_nap`, `test_nap_variants`, `test_recall`, `test_scopes`, `test_squash_clone_zoom`, `test_store`, `test_surgery`, `test_version`, `test_view`, `test_wake`, `test_wake_expand`, `test_zoom`, `test_zipper`)

1. Stub tests: add `test_test_modules_do_not_reference_load_summem` (empty) to `tests/test_summem_fixture.py`.
2. Stub interface: none.
3. Write tests and run red: no `tests/test_*.py` other than `test_summem_fixture.py` contains the substring `load_summem`. Red while ~200 call sites remain.
4. Write code and run green: drop `load_summem` from imports; add `summem` to each affected test signature; replace `m = load_summem()` with `m = summem` (or use `summem` directly). Keep `dated_leaf`, `ROOT`, `SCRIPT` imports. Leave `surgery.py` / `migrate.py` loaders alone. `tox -e py311`.

- [x] Done

### 3. Isolate pytest temps for parallel envs — executable

- Files: `tox.ini`, `tests/test_tox_runner.py`

1. Stub tests: empty `test_tox_pytest_basetemp_is_env_tmp_dir` in `tests/test_tox_runner.py`.
2. Stub interface: none (ini keys already exist).
3. Write tests and run red: `[testenv] commands` contains `--basetemp="{env:TMPDIR:/tmp}/summem-{env_name}"` (not `{env_tmp_dir}`, which is inside the git worktree) and still starts with `pytest` and includes `{posargs}`; `[testenv:coverage]` pytest line contains the same `--basetemp`. Do not subprocess tox.
4. Write code and run green: `[testenv] commands = pytest --basetemp="{env:TMPDIR:/tmp}/summem-{env_name}" {posargs}`; add the same `--basetemp` to the coverage pytest line. Parallel pytest needs isolated temps ([tox FAQ](https://tox.wiki/en/latest/faq.html)); this suite's outside-repo tests `chdir` to `tmp_path`, so temps must not live under `{toxinidir}`. There is no ini key that turns default `tox` into parallel; that remains the CLI subcommand.

- [x] Done

### 4. Document the full-suite command — prose/policy

- Files: `README.md` Developing, `memory-bank/techContext.md` Testing Process
- No tests: prose/policy artifact

1. Name `tox run-parallel` as the full local matrix (`-p auto` is tox’s default; do not document `-j`, which is not tox).
2. Keep `tox -e py311` as the single-interpreter form; `uvx --with tox tox …` when tox is not on PATH; `tox -e coverage` unchanged; CI unchanged.
3. State that two concurrent tox invocations on the same env in one checkout stomp; one orchestrator process only.

- [x] Done

### 5. Agent iteration rule — prose/policy

- Files: `.cursor/rules/SumMem-testing.mdc`
- No tests: prose/policy artifact

1. Frontmatter matches sibling rules (`alwaysApply: true` like `.cursor/rules/shared/test-running-practices.mdc`; fill `description`).
2. Body: default iteration is `tox -e py311` or a single test/file under that env; full declared matrix is `tox run-parallel` only at end-of-work; do not overlap tox on the same env in one checkout.

- [x] Done

## Technology Validation

No new technology - validation not required. tox 4 already declares `min_version = 4.0`; `run-parallel` / `-p auto` is that CLI. pytest fixtures and `monkeypatch.undo()` are already in the suite.

## Dependencies

- Existing `tests/conftest.py` `load_summem` / `SCRIPT`
- Existing `tests/test_tox_runner.py` ini locks
- tox 4 `run-parallel` and `{env_tmp_dir}` ([tox parallel mode](https://tox.wiki/en/latest/user_guide.html#parallel-mode))
- pytest session-scoped fixtures and monkeypatch undo

## Challenges & Mitigations

- Leaked module mutation under a session fixture: grep found no `m.ATTR =` assignments; tests already `monkeypatch.setattr` on the loaded module. Pytest restores patches at test teardown; the undo test pins that. Cache `load_summem` so a stray reload cannot swap `sys.modules["summem"]`.
- Parallel envs sharing pytest temps: isolate with `--basetemp` per env under `TMPDIR`, not `{env_tmp_dir}` (that path is inside the clone; outside-repo tests `chdir` to `tmp_path`). `.pyc` files are version-tagged.
- Issue example `-j auto` is not tox’s flag: document `tox run-parallel` (`-p auto` default).
- Do not subprocess tox from pytest (recursion under the suite): prove parallel-safety with ini locks; Build runs `tox run-parallel` live.
- Mechanical miss of a call site: the substring contract test stays red until none remain outside `conftest.py`.

## Pre-Mortem

- Agents keep running sequential `tox` as “the suite” because README still leads with `tox`: plan already updates README and techContext to name `run-parallel` as the full matrix, plus the agent rule. If those three disagree, the docs step is incomplete.
- Session fixture flakes from order-dependent `WAKE_LINES`: already covered by Challenge 1; if Build sees it, convert the offender to monkeypatch rather than widening fixture scope to function.
- We invent a live `tox run-parallel` pytest and recurse: already covered by Challenge 4; do not add that test.
- We TDD the cursor rule or README wording: do not; those steps stay prose/policy.

## QA Results

FAIL. Full findings in `memory-bank/active/.qa-validation-status`. Build must rerun; the plan itself is sound.

### Blocking

1. **`tox.ini` `--basetemp` (step 3) is a regression and is not needed.** An explicit basetemp is `rm_rf`'d at first use with no numbering, lock, or ownership check, so two concurrent runs on `/tmp/summem-{env_name}` from different checkouts share and clobber the same `tmp_path`. Proven by probe: two concurrent runs on one explicit basetemp both got `.../test_a0`. Also proven unnecessary: pytest's default basetemp already isolates concurrent runs (`pytest-0`..`pytest-3`) and already lands outside the worktree, because inside a tox env `TMPDIR` is unset and `gettempdir()` is `/tmp`. Fix: drop `--basetemp` from `[testenv]` and `[testenv:coverage]`; drop or invert `test_tox_pytest_basetemp_is_per_env_system_tmp`; re-check the "in one checkout" wording in README / `techContext.md` / `.cursor/rules/SumMem-testing.mdc` once the flag is gone.
2. **`test_summem_fixture_is_session_scoped` asserts pytest's private `_fixture_function_marker`.** That attribute already renamed once (Build's own deviation note) and `deps = pytest` is unpinned, so a future pytest reddens the suite for a non-SumMem reason. The scope it locks is also unobservable, since `load_summem()` returns the cached module regardless of fixture scope — a change-detector by `always-tdd.mdc`. The cache that actually delivers "load once" is untested. Fix: assert the behavior (`load_summem() is load_summem()`, and the fixture is that object) instead of the marker.

### Advisory

- `m = summem` at 318 sites (plan-sanctioned minimal diff).
- `conftest.load_summem` duplicates `tests/gitutil.py::_load_driver`'s cache-then-load body.
- `test_test_modules_do_not_reference_load_summem` now guards style, not behavior, since a stray `load_summem()` call is a cache hit.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA (FAIL - Build must rerun)
