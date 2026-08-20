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

## 2026-08-19 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the plan against the tree; wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
    - Independently confirmed no executable behavior is at stake: `git grep -E 'VISION|ROADMAP'` outside `memory-bank/archive/` and the two files hits only memory-bank prose; `summem` (no `.py` suffix), `tests/`, `pytest.ini`, `AGENTS.md`, and `.cursor/` are clean
    - Inventoried the living citation surface: `productContext.md` ×2, `systemPatterns.md` ×1, `techContext.md` ×4
    - Spot-checked triage buckets against `summem`: hot margin and pack-size cap genuinely absent; baked prompt has no "do what it prints"
* Decisions made
    - PASS WITH ADVISORY: no plan edits made, no re-plan needed; two minor findings absorbed by build
    - Step 2.1's `.cursor/skills/ai-rizz/architecture-docs/SKILL.md` does not exist in this repo; build reads the user-level `~/.cursor/skills/ai-rizz/architecture-docs/SKILL.md`
    - Step 6.2's grep is to be executed as "any citation of either deleted file", not only contract citations, so `techContext.md` lines 3 and 21 get fixed
* Insights
    - `techContext.md` line 21 cites VISION's "First proof" as the acceptance bar; it needs the same redirect to `tests/test_proof_*.py` that step 5.1 gives `productContext.md`
    - The "8-character id" bucket item is true-of-tree, not built-else: VISION already says shortest unique hex, at least 8, and `short_id`/`unique_prefix` implement that
    - Advisory: naming the architecture page's invariants and citing them from `tests/test_proof_*.py` docstrings would make the page checkable without adding tests
