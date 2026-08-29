# Progress

Retarget SumMem ingest membership so `note` is lore plus tree-affecting in-flight work, in as few words as will carry it, without naming OptMem.

**Complexity:** Level 3

## 2026-08-28 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified Level 3
    - Wrote project brief from the approved intent plus the density constraint
* Decisions made
    - Not Level 2: the deliverable is choosing a membership test that already failed once as “eternal currency”; L2 has no creative phase
    - Not Level 4: no store, CLI, or architecture change
    - Task id `note-membership` (lineage of `prompt-membership`)
* Insights
    - Clone-portability answered whose fact; it did not answer when the fact is for
    - `(mandatory)` plus a stay-out list that only names personal/machine/preference fills the hole with process telemetry

## 2026-08-28 - CREATIVE - COMPLETE

* Work completed
    - Explored membership wording and placement (`creative-membership-wording.md`)
* Decisions made
    - Option A: “work in this clone” probe on bootstrap and how-to; how-to adds genre, denylist, skip-if-nothing; OptMem unchanged
    - Retarget `test_init.py` clone / another-machine pins; do not restore eternal-currency
* Insights
    - “Would still need” is the next agent on this PR; “work in this clone” is someone using the tree
    - “Decisions” in today’s how-to is how PR telemetry qualifies

## 2026-08-28 - PLAN - COMPLETE

* Work completed
    - One executable step: retarget `test_init.py` then rewrite `prompt_text` / `how_to_text` / `AGENTS.md` lockstep
    - Persistent docs and OptMem left alone
* Decisions made
    - Pin `work in this clone` on both surfaces; do not pin denylist examples
    - No new test files; `test_scopes.py` identity-compares `how_to_text()`
* Insights
    - `clone not in prompt_text` was protecting the bootstrap from a portability lecture, not from the word “clone”

## 2026-08-28 - PREFLIGHT - COMPLETE

* Work completed
    - Verified the plan's named test edits against the live `tests/test_init.py` lines 75-154; exact match
    - Hand-checked the proposed `prompt_text()` / `how_to_text()` bodies against every surviving assertion; all hold
    - Confirmed `test_scopes.py` compares by `how_to_text()` identity, not literal string; no other doc quotes the retargeted phrases
* Decisions made
    - `.preflight-status` first line: `PASS WITH ADVISORY`
* Insights
    - The new `work in this clone` pin is a product-contract assertion (same class as today's `contributor` pin), not a change-detector
    - Radical (advisory, not applied): hoist the shared probe phrase into one module constant both surfaces interpolate, so the two-surface pin can't silently drift like the `wake-usage-prompt` first-preflight FAIL did

## 2026-08-28 - BUILD - COMPLETE

* Work completed
    - Retargeted membership pins; rewrote `prompt_text` / `how_to_text` / `AGENTS.md` lockstep to Option A
    - Full matrix: 369 passed, 1 skipped
* Decisions made
    - Did not apply the preflight shared-constant advisory
* Insights
    - The old `clone not in prompt_text` pin was the only thing that made “this clone” look like a bootstrap break; once retargeted, lockstep was a copy

## 2026-08-28 - QA - COMPLETE (PASS)

* Work completed
    - Diffed the build commit against pre-build and confirmed it matches the plan and Option A creative decision verbatim across `prompt_text()`, `how_to_text()`, `AGENTS.md`, and `tests/test_init.py`
    - Re-ran `tox -e py311 -- tests/test_init.py` (11 passed) and `tox run-parallel` (py311/py314 OK, py312/py313 skip)
    - Grepped the repo for stale membership phrasing (`would still need`, `another machine`, `designs, decisions, invariants`) outside `memory-bank/`; none found in shipped docs
* Decisions made
    - PASS with the preflight's shared-constant advisory carried forward, not re-raised as a new finding
* Insights
    - Sentence-count parity (3 bootstrap, 4 how-to) held through Build exactly as Preflight verified by hand

## 2026-08-28 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-note-membership.md`
    - Reconciled persistent files (all skip)
* Decisions made
    - Shared-constant hoist stays a follow-up, not a silent build add
* Insights
    - Lockstep does not bind how-to to bootstrap; the two-surface probe can still drift
    - An advisory that names a drift class this repo has already failed should be adopted in the plan, not carried across three phases

## 2026-08-28 - CREATIVE - COMPLETE

* Work completed
    - Re-evaluated the membership probe after PR #74 feedback that contributors have separate clones
    - Compared repository, checkout, and generic need-to-know wording
* Decisions made
    - Use “another contributor needs to work on this repository” on both shipped surfaces
    - Retarget both invariant probes and remove the obsolete how-to `clone` requirement
* Insights
    - SumMem shares committed repository context, not a physical working copy
    - A generic “needs to know” test would again admit process telemetry

## 2026-08-28 - PLAN - COMPLETE

* Work completed
    - Revised the task brief, component analysis, test plan, implementation plan, challenges, and pre-mortem for repository-oriented wording
    - Confirmed no new test files, dependencies, or store mechanics are needed
* Decisions made
    - The targeted `clone` assertion is removed rather than retaining the word solely to satisfy a stale test
    - The earlier build and QA records remain historical; this revision must repeat Preflight, Build, and QA
* Insights
    - Two probe pins plus `AGENTS.md` lockstep cover both product surfaces and their committed bootstrap copy
