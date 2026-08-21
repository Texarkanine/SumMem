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
