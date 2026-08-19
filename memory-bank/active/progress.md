# Progress

Zipper-heal overlapping nap leaf-sets after merge so the next `note` or `nap` rematerializes a cover of unique leaves without concatenating shared prefixes.

**Complexity:** Level 3

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Advanced L4 `file-backend`: marked issue #1 complete; deleted equal-grain ephemeral files (preserved `milestones.md`, `projectbrief.md`, `reflection/`)
    - Classified issue #3 (zipper-heal) as Level 3
    - Wrote a new `projectbrief.md` scoped to zipper on `note`/`nap`, rematerialize-from-`.tree`, local flock, and the no-unequal-grain fail-fast
* Decisions made
    - Level 3, not Level 2: heal is a new algorithm with crash order, local flock, overlap refusal in `write_nap`, and fold-request silence when the spine cannot equal-grain — not a single-component policy tweak
    - Level 3, not Level 1: the merge hole is real, but the work is a complete feature across `note`, `nap`, and `write_nap`
    - Level 3, not Level 4: identity, wait-free wake, and binary `nap` stay; aligned cover and flatten-as-normal stay Later; a milestone must not itself be L4
* Insights
    - Proof 6 assumed disjoint packs; equal-grain made the overlapping-prefix case the compaction hole rather than a flatten-to-leaves escape
    - Operator already locked remainder grain, local flock, and "do not zipper inside wake" in the issue; plan still owns crash-file choreography and how overlap is detected
