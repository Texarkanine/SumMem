# Progress

Emergency-only repo-root `surgery.py`: zipper-excise one whole raw note at the branch tip so HEAD no longer embeds the sentence in `notes/` or remaining `.tree` files. Spec: https://github.com/Texarkanine/SumMem/issues/28

**Complexity:** Level 2

## 2026-08-21 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent from issue #28 plus parent standing constraints (no CLI fold-in, no summem edits, heal_view is not targeted break-out, zip-again is heal not write_nap).
    - Classified Level 2: self-contained script + tests + operator docs.
* Decisions made
    - Standing consent substitutes for the intent-confirmation wait.
    - Optional `--contains` and `--dry-run` are in scope (operators know the sentence, rarely the UTC filename).
    - Do not extend `tox -e coverage` `--cov=` unless needed; default tox stays coverage-free.
* Insights
    - Sibling #27 owns `summem` / prompt / AGENTS.md; colliding those files would break the wave.

## 2026-08-21 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 TDD plan: locate, break-out/unlink/heal, CLI, operator docs.
* Decisions made
    - Break-out loops every view nap whose tree still contains the target name; `heal_view` only after the loose unlink.
    - `--contains` matches note text only, never nap captions as delete targets.
    - `surgery.py` loads sibling `summem` via `SourceFileLoader`.
* Insights
    - Calling `heal_view` mid-break-out can subset-drop the rematerialized note back into a larger overlapping pack.

## 2026-08-21 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated the Level 2 surgery plan against repo-root `summem` helpers, zipper tests, CLI/`--path` patterns, and issue #28.
    - Wrote `memory-bank/active/.preflight-status`; first line is `PASS WITH ADVISORY`.
* Decisions made
    - No in-phase plan edits (TDD order is already test-first; no change-detectors).
    - Build may proceed; advisories are implementer notes, not plan rewrites.
* Insights
    - `heal_view` subset-drop of a loose note still covered by a larger overlapping pack is real (`test_heal_note_covered_by_nap_dropped`); skipping `heal_view` during break-out is required.
    - `with_store_lock` is `with_store_lock(parent, fn)`, not a context manager; `_unlink_node` takes a `ViewNode`.

## 2026-08-21 - BUILD - COMPLETE

* Work completed
    - Added repo-root `surgery.py` and `tests/test_surgery.py` (16 tests).
    - Operator docs at `docs/surgery.md`; README and `docs/index.md` link it.
    - `uvx --with tox tox`: 252 passed on py311–py314.
* Decisions made
    - `NAME` wins when both `--contains` and a positional name are given; `--contains` must still appear in that note.
    - Mutate under `with_store_lock(parent, fn)`; dry-run skips the lock.
    - Break-out picks containing view naps in `list_view` filename order.
* Insights
    - Injected conftest `load_summem()` into locate/excise so the `write_nap` monkeypatch hits the same module; CLI loads a second copy.

## 2026-08-21 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of `surgery.py`, `tests/test_surgery.py`, and operator docs against the Level 2 plan, brief, and issue #28.
    - Wrote `memory-bank/active/.qa-validation-status`; first line is `PASS`.
* Decisions made
    - Accept as-is. Advisories are lockstep notes, not build defects.
* Insights
    - Dry-run and mutate are two walks by plan (`plan_break_out` vs `_naps_containing`); both depend on `list_view` filename order.
    - Forbidden files (`summem`, prompt, `AGENTS.md`) stayed out of the build commit.

## 2026-08-21 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-surgery.md`.
    - Reconciled persistent files: all three skipped.
* Decisions made
    - Standing-contract probe: zipper delete algorithm stays in `surgery.py` / `docs/surgery.md`; briefing files already say the script is the only writer.
* Insights
    - `heal_view` mid-break-out subset-drops a rematerialized target still covered by a larger pack.
* Persistent skip receipts
    - productContext: skip — agent use cases and “script is the only writer” still hold; surgery.py is an emergency script, not a new audience use case.
    - systemPatterns: skip — unrelated changes (wake, recall) are not damaged by not knowing `surgery.py`; later CLI fold-in is not this issue.
    - techContext: skip — shipped product is still the no-suffix shebang; tox/SourceFileLoader/`--cov=summem` unchanged.


