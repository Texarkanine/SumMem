# Progress

Equal-grain fold requests, carry-stable nap names, and in-memory wake expand so `WAKE_LINES` is a view-time projection while `nap` still unlinks.

**Complexity:** Level 3

## 2026-08-18 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Advanced L4 `file-backend`: marked single-store complete, deleted single-store `tasks.md` / `activeContext.md` / `progress.md` / `.qa-validation-status` / `.preflight-status`
    - Classified issue #1 (equal-grain fold) as Level 2
    - Wrote a new `projectbrief.md` scoped to the picker, catch-up chain, and proof 4 pack math
* Decisions made
    - Level 2, not Level 3: one policy in the existing nap-request path; the CLI does not grow; identity, wake, zoom, and `write_nap` stay; architecture is already in issue #1 and `VISION.md`'s year-later diagram
    - Level 2, not Level 1: production fold shape and proof 4 packing change; not a single-component bug
* Insights
    - `write_nap` may still fold any two adjacent nodes so a post-merge lazy cover remains an agent nap; only the request printer becomes equal-grain
    - Proof 4's 40/30/30 is a left-spine helper, unreachable under equal-grain; squash+zoom stays, pack sizes become powers of two

## 2026-08-18 - PLAN - COMPLETE

* Work completed
    - Wrote the L2 equal-grain plan in `tasks.md`: picker, catch-up print after `nap`, proof 4 helper packs 64/32/4, contract wording
    - Mapped red tests to `tests/test_fold.py`; proof 4 stays a green helper adaptation
* Decisions made
    - Sequential emit after each `nap`, not a pre-printed disjoint list
    - `write_nap` still accepts any adjacent pair; only the request printer is equal-grain
    - Delete `oldest_adjacent` so a second fold policy cannot linger
    - No creative phase: issue #1 and the year-later diagram are the design
* Insights
    - A long-stream test that only asserts powers of two is vacuous on a `None` stub (all 1s); it must also bound view length and require a real fold
    - Depth must fold via `equal_grain_pair`, not `fold_ids`, or a correct picker still sees a left spine

## 2026-08-18 - PREFLIGHT - COMPLETE (FAIL)

* Work completed
    - Validated the plan's TDD ordering, conventions, dependency impacts, existing implementations, requirements, and proof touchpoints
    - Reproduced same-second parent reordering: four notes can become grains `[1, 2, 1]` after one adjacent fold
    - Reproduced an over-budget equal-grain stall: 24 same-second notes at budget 8 stopped at 12 view nodes with no adjacent equal pair
    - Recorded the failed gate and required replanning in `tasks.md` and `.preflight-status`
* Decisions made
    - Block build because the planned policy does not guarantee a short bounded view for supported same-second notes
    - Require `/niko-plan` to design a carry-stable nap sequence key before implementation
    - Require the 16+1 CLI setup and depth assertion to be corrected during replanning
* Insights
    - Minimum child time is not enough to preserve a folded interval when note timestamps tie; the leaf-set hash can move the parent between surviving notes
    - `zoom_reaches` bounds breadth-first work, not hop depth, so it cannot prove the logarithmic-depth acceptance criterion

## 2026-08-18 - PLAN - COMPLETE (replan after preflight FAIL)

* Work completed
    - Rewrote the L2 plan: carry-stable nap names first, then equal-grain picker, catch-up, proof 4 packs, contract wording
    - Added same-second `[2, 1, 1]` and 24-note same-second stream as the regression that failed preflight
    - Updated `projectbrief.md` with the filename order-key requirement
* Decisions made
    - Stem is `{stamp}-{rand}-{leafset}-{leaves}`; `{stamp}-{rand}` copied from the left child's filename
    - Stay Level 2; no creative phase
    - Depth is max NoteChild depth in `.tree`; `zoom_reaches` stays a reachability check
* Insights
    - Tests that used `split("-")[1]` as leafset must move to `[-2]` in the same unit as the stem change
    - A mixed-time long stream would not catch the stall; the hard case is one UTC second

## 2026-08-18 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Revalidated TDD ordering, conventions, dependency impacts, conflicts, requirement coverage, and test quality against the current script and tests
    - Confirmed left-child `{stamp}-{rand}` inheritance preserves the folded interval under same-second notes and equal-grain requests bound sequential fold depth logarithmically
    - Amended unit 1 to update `list_view` for `_parse_nap_stem`'s new four-tuple
* Decisions made
    - Pass the build gate; the replan addresses all three blockers from the first preflight
    - Keep non-adjacent merge healing outside this milestone because it conflicts with the adjacent-only binary nap contract
* Insights
    - The stem migration affects both filename assertions and production tuple unpacking
    - The deterministic same-second stream is the load-bearing regression because mixed timestamps conceal interval reordering

## 2026-08-18 - CREATIVE - COMPLETE (wake-projection)

* Work completed
    - Explored how to keep `WAKE_LINES` as a view-time projection after the operator rejected burn-the-lens fold
    - Compared notes-stay + wake cover, unlink + explode `.tree`, and keep-nap-layers / unlink-notes
    - Wrote `memory-bank/active/creative/creative-wake-projection.md`
    - Revoked the equal-grain preflight PASS (`FAIL` in `.preflight-status`)
* Decisions made
    - Notes stay. `nap` writes captions only. Wake covers the note sequence. `WAKE_LINES` is not an argument to unlink
    - Year-later compactness is printed-line count, not inode count
    - Equal-grain film plan is not a build; next is `/niko-plan`
* Insights
    - `VISION.md` already required missing summaries to degrade to finer grain; unlink made that impossible
    - Cheap wake and deleted children cannot both serve an arbitrary later budget

## 2026-08-18 - PLAN - COMPLETE (wake expand)

* Work completed
    - Re-leveled to L3: wake projection plus equal-grain is multiple components
    - Operator locked unlink + in-memory right-edge expand (not notes-stay)
    - Rewrote `projectbrief.md` and `tasks.md`; amended the creative doc
* Decisions made
    - `fold_request` uses file count; `wake_text` uses `expand_frontier` when files `<` budget
    - Split the rightmost expandable nap until the budget fills, not one split
    - `nap` stays file-ids only; `zoom` already resolves expanded ids
    - Proof 4/6 pin `WAKE_LINES` when they assert pack-grain listings
* Insights
    - Tests that harvest ids from `wake_text` become wrong the moment wake expands; they must use `list_view` or a pinned budget
    - New 1s are what turn expand back off — the directory meets the knob again

## 2026-08-18 - PREFLIGHT - COMPLETE (PASS)

* Work completed
    - Validated the L3 wake-expand plan against the script, every affected wake consumer, proof tests, architectural conventions, requirements, and TDD ordering
    - Moved Proof 4 adaptation into the test-first expansion unit and added the omitted caption-conflict proof adaptations
    - Added missing, malformed, and unreadable tree fallback coverage to preserve wait-free wake
    - Added an immutable projection-row boundary so virtual expanded ids cannot leak into storage-facing nap lookup
* Decisions made
    - Pass the build gate after incorporating all blocking findings into `tasks.md`
    - Keep file-grain proof assertions explicit by pinning `WAKE_LINES`; wake behavior tests exercise expansion separately
* Insights
    - Proofs 2 and 3 inspect post-nap captions and would otherwise expand to leaves under the default budget
    - Tree expansion needs a representation distinct from `ViewNode` because virtual children are printable and zoomable but deliberately not nappable

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - Carry-stable nap stems `{stamp}-{rand}-{leafset}-{leaves}` inherit the left child's sequence prefix
    - Equal-grain fold requests replace oldest-adjacent; catch-up prints after a successful `nap`; `oldest_adjacent` is gone
    - In-memory right-edge wake expand via `ProjectedNode` / `expand_frontier`; `write_nap` still unlinks files only
    - Proof 4 packs are 64/32/4; proofs 2/3/6 pin file-grain `WAKE_LINES`
    - Contract wording in `VISION.md`, `ROADMAP.md`, and `systemPatterns.md`
    - Full suite: 99 passed
* Decisions made
    - `ProjectedNode` carries optional `tree_path` so a file-backed nap can load `.tree` once without leaking into `write_nap`
    - Proof wakes that must see captions use the loaded module plus a pinned budget; subprocess cannot monkeypatch `WAKE_LINES`
    - Unreadable `.tree` is its own wait-free case next to missing and malformed
* Insights
    - Same-second `[1, 2, 1]` reproduced on the old stem and disappeared once the parent kept the left child's `{stamp}-{rand}`
    - Tests that harvested nap ids from `wake_text` would have gone red for expand, not for the writer; `list_view` is the file oracle

## 2026-08-19 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the implementation against the L3 plan, project brief, creative amendment, system patterns, and contract documents
    - Ran the full suite successfully: 99 passed
    - Reproduced a wait-free wake failure with a valid-JSON but semantically malformed nested tree
* Decisions made
    - Fail QA because malformed nested tree shapes can escape expansion fallback and raise from `wake_text`
    - Require Build to cache failed file-backed expansion attempts so each `.tree` is loaded at most once per wake
    - Require Build to reconcile `VISION.md`'s aligned-cover claim with the implemented right-edge projection and deferred roadmap work
* Insights
    - Decode-level malformed coverage is insufficient; projection must validate semantic tree invariants before replacing the file row
    - The immutable projected row boundary is sound, but it needs an explicit attempted/unsplittable state to preserve the one-load contract

## 2026-08-19 - BUILD - COMPLETE (rework after QA FAIL)

* Work completed
    - Nested nap children with no notes no longer raise from `wake_text`; the parent file line prints
    - Failed file-backed `.tree` loads are recorded on `ProjectedNode.tree_attempted` so each payload is parsed at most once per wake
    - `VISION.md` temporal bias now names aligned cover as later and equal-grain plus right-edge expand as this milestone
    - Creative implementation notes labeled as the rejected first pass
    - Full suite: 101 passed
* Decisions made
    - `_split_kids` must project both children before replacing a row; a None child means unsplittable, not a crash
    - Cache attempts on the projected row rather than a side map, so the one-load contract lives with the frontier
* Insights
    - Decode-level `loads_tree` exceptions never saw a valid JSON tree whose nested nap had zero notes

