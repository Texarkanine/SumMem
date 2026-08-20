# Progress

Sunset `VISION.md` and `ROADMAP.md`: drop what is true of the tree or what we built differently; keep leftovers under `docs/`; write a sibling-quality README; reconcile the memory-bank so it no longer treats VISION as the contract.

**Complexity:** Level 2

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed intent: leftovers are any relevant leftover; architecture page for algorithm + store layout is expected unless triage finds none
    - Classified as Level 2
* Decisions made
    - Level 2: contained docs enhancement, not a product-architecture change; mkdocs site is out of scope
* Insights
    - Persistent memory-bank still cites VISION as the design contract; that citation is the reconciliation target

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 plan: six prose/policy steps, no new tests
    - Surveyed sibling READMEs and stockroom `docs/` shape; no `VISION`/`ROADMAP` references in `*.py`
* Decisions made
    - Architecture page is a required deliverable (`docs/architecture/index.md`), not contingent on leftover triage
    - Leftovers (Later items, unbuilt knobs) go to `docs/notes.md`; mkdocs landing is `docs/index.md` only
    - Archives keep historical VISION mentions
* Insights
    - `summem` has `WAKE_LINES` / `ENTRY_CHARS` only; VISION’s hot margin and pack-size cap are leftovers
    - Sibling READMEs are why + quickstart + doc pointers, not design contracts
