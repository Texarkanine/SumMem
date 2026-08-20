---
task_id: docs-sunset
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: docs-sunset

## SUMMARY

Retired `VISION.md` and `ROADMAP.md`. Living docs are a sibling-genre README, mkdocs-shaped `docs/` (architecture atlas, leftovers, landing), and a memory-bank that no longer treats VISION as the contract. Draft [PR #11](https://github.com/Texarkanine/SumMem/pull/11). pytest 207. QA failed once on inherited VISION sentences, then passed. Operator rework after reflect: concepts-first atlas, `A`–`H` fold pictures, letter/number zipper snapshots.

## REQUIREMENTS

- Drop what is now true of the tree and what we built differently.
- Keep leftovers in `docs/notes.md`.
- Write a README in the vein of stockroom, ai-rizz, slobac.
- Reconcile persistent memory-bank with the README. VISION is not the design contract.
- Identify leftover architecture or other relevant information for `docs/` (mkdocs-shaped markdown, not a site). An algorithm and store-layout page was expected.
- No executable behavior change. No mkdocs site. Issue-wave fan-out stayed on hold.

## IMPLEMENTATION

Triage: leftovers were sqlite/second backend, harness hooks, aligned `cover(T)`, pack-size cap, and hot margin. ROADMAP phases 1–3 and wake-as-a-script were built-else, not leftover.

Shipped: `README.md`; `docs/index.md`; `docs/notes.md`; `docs/architecture/index.md`; surgical edits to `productContext.md`, `systemPatterns.md`, `techContext.md`; one `AGENTS.md` When-to-load pointer after the baked prompt. Deleted `VISION.md` and `ROADMAP.md`. Archives were not rewritten.

Post-reflect atlas rewrite (pushed on the same PR): talk in concepts; introduce a name before using it; no OptMem “it’s like this”; no unintroduced code identifiers. Fold pictured as eight letters. Zipper pictured as shared `A B C D` plus writer-1 letters `E F` and writer-2 numbers `1 2`, with rematerialize as its own snapshot. A 2048-nap is eleven binary levels and one fat children file, not unbounded nesting.

## TESTING

No new tests (prose/policy). Full suite `uv run --python 3.11 --with pytest pytest`: 207 passed. Preflight PASS WITH ADVISORY (skill path, grep scope, 8-char id bucket). `/niko-qa` FAIL then PASS after narrowing view-node budget, `.tree` bytes per tree not per leaf set, and heal-dropped id → `nap` exit 1.

## LESSONS LEARNED

- Nested captions live inside the children file. Leaf-set identity never implied identical payload bytes except for the same tree (same grouping, same nested wording).
- When sunsetting a design doc, the sentences most worth keeping are the ones to verify against the code. “Still sounds right” is how a retired contract becomes VISION 2.0.
- The merge chart that skipped rematerialize was the confusing one; showing letters inside each pack made the overlap obvious.

## PROCESS IMPROVEMENTS

Triage “true of the tree” needed a code check on the strongest claims, not a vibe check against the retired prose. Preflight’s test-docstring invariant anchoring was left undone (no operator direction).

## TECHNICAL IMPROVEMENTS

None. This task did not change the product.

## NEXT STEPS

- Draft PR #11 is open; merge when ready.
- Issue-wave fan-out (`#6`–`#9`) was on hold for this sunset; it can resume after `/niko`.
- Pack-size cap, `cover(T)`, sqlite, and hooks remain in `docs/notes.md` — not a backlog contract.
