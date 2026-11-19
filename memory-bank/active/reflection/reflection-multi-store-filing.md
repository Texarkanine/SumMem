---
task_id: multi-store-filing
date: 2026-11-19
complexity_level: 2
---

# Reflection: Multi-Store Filing (`--root` / `--path`)

## Summary

Implemented [Texarkanine/SumMem#103](https://github.com/Texarkanine/SumMem/issues/103) across `summem`, `surgery.py`, `AGENTS.md`, `tests/`, and `docs/`, then completed a SLOBAC test-suite rework addressing 47 of 49 audit findings (declining Findings 47 and 49 to preserve child-process binary integration tests alongside in-process unit suites) and splitting `tests/test_cli.py` and `tests/test_zipper.py` into focused capability modules. Full `properdocs build --strict` and `tox run-parallel` (`py311`–`py314`, 445 passed per environment) succeeded with zero product-code regressions, and QA passed.

## Requirements vs Outcome

Every functional, non-functional, constraint, and acceptance requirement in #103 shipped cleanly, and the rework resolved every accepted SLOBAC finding without altering `summem`, `surgery.py`, or `migrate.py`. During rework, the operator ruled that this repository's `AGENTS.md` is operator-owned rather than bound to `prompt_text()`, superseding the initial pass's AC 15 lockstep test (`test_agents_md_starts_with_prompt_text` deleted, `docs/contributing/index.md` and `memory-bank/techContext.md` updated). Findings 47 and 49 were declined because `test_path_walkup_and_catalog.py` invokes the `summem` binary in a child process while `test_scopes.py` calls `m.main(...)` in-process—walking the same path across two distinct execution layers.

## Plan Accuracy

In the initial build, two callers outside Unit 2's file list surfaced (`tests/test_branch_pack_merge.py` in Preflight and `tests/test_middle_orphans.py` / `tests/test_fold_many_writers.py` during test runs). In the rework, two Preflight passes caught real defects before build: (1) `"compression" not in out.splitlines()[-2]` was vacuous because `splitlines()[-2]` is never the remaining-compressions line (`assert "compression" not in out` fixed it), and (2) deleting `test_agents_md_starts_with_prompt_text` invalidated a bullet in `docs/contributing/index.md` that said `"in step with"` rather than `"lockstep"`. Reconciling exact collected test counts in planning (`459 → 445`) prevented any silent drop across the two file splits.

## Build & QA Observations

In the initial build, handling `ValueError` in `_fold_store_flag` kept store-layer functions usable on non-git `tmp_path` directories (`test_fold_many_writers.py`). In the rework build, full-suite verification caught `tests/test_summem_fixture.py::test_test_modules_do_not_reference_load_summem`, which forbids the string `"load_summem"` in any `tests/test_*.py` module; switching Finding 38 in `tests/test_surgery.py` to the audit's first option (removing the unread `_host_needs_interpreter` monkeypatch and asserting `f"Run: {m.agent_invoke()} nap " in out`) fixed all four Python environments immediately. QA passed with three minor non-blocking advisories.

## Insights

### Technical
- Pure store-layer helpers (`write_note`, `write_nap`, `heal_view`, `fold_request`) run on bare non-git `tmp_path` directories in simulation tests (`test_fold_many_writers.py`), so repository-root lookups inside them must tolerate `find_store_parent` raising `ValueError`.
- `tests/test_summem_fixture.py` scans every `tests/test_*.py` file as raw text and fails if the substring `"load_summem"` appears anywhere in it.
- In-process `m.main(...)` unit suites and child-process `subprocess.run(...)` binary tests exercise distinct layers and are not redundant when one binary test guards the OS entrypoint and the in-process suite covers the branch matrix.

### Process
- When retiring a cross-file sync test, search docs for plain-English phrasing (`"in step"`, `"A test checks this"`) in addition to codebase jargon (`"lockstep"`).
- Reconciling exact `pytest --collect-only` counts (`459 − 14 = 445`) before splitting large test files catches accidental drops or duplicate carry-overs mechanically.

### Million-Dollar Question

Separating store selection (`_select_store` returning `(parent, root)`) from pure `parent`-scoped store operations, formatting every user-visible path through `_root_path(path, root)`, and organizing `tests/` from the outset into small capability modules (`test_cli_bootstrap.py`, `test_cli_help.py`, `test_rematerialize.py`, `test_heal_view.py`, `test_cli_heal.py`, `test_store_lock.py`) paired with thin child-process binary smoke files is the exact structure that would have emerged if multi-store filing and SLOBAC hygiene had been foundational from day one.
