---
task_id: middle-orphans
date: 2026-10-07
complexity_level: 3
---

# Reflection: middle-orphans

## Summary

Skip fold, oldest pair first, is in. `nap` takes a nearest same-grain power-of-two pair, wake sorts opened rows by date, and legacy odd packs stay listed. QA passed. The suite is 417 tests, green on py311–py314.

## Requirements vs Outcome

The seven requirements in the brief shipped. The picker names the oldest power-of-two row that has a twin below it. `nap` accepts that pair and keeps the earlier refusals in order. Nothing writes a non-power-of-two pack. Wake sorts by the oldest note's sequence. Legacy odd packs are never requested and never opened on disk. Existing stores heal through ordinary fold requests. Help, README, architecture, theory, notes, and `systemPatterns.md` describe the new rule.

Nothing was dropped from the plan except advisory 7, the exhaustive two-writer model. The operator asked to build the planned fix, and active context had left that check as the operator's call. "No row strands forever" is what the five scenarios and two many-writer seeds check. It is not a proof.

## Plan Accuracy

The five-unit order held. Preflight run 1 found one unequal nap the plan had missed (`test_branch_pack_merge.py`); run 2's scratch build of Units 1–4 matched the named retargets (5 failed, 397 passed) and corrected the stranding count, the pair return type, the grain check, and the Unit 1 gate. Those corrections went in before production code.

Two surprises were outside the challenge list. Identical notes share a digest, so a successful `write_nap` of one id with itself cannot show the closest-pair rule; the test landed on `_pair_nodes`. The many-writers test was about 115 seconds a seed while each note restarted a zoom walk, and 3.17 seconds once one walk collected the reachable text. The assertion did not change.

The error-order challenge was the one that paid for itself: the four existing tests stayed green through the new checks.

## Creative Phase Review

Skip fold, oldest pair first, held. On a listing that never rises it chose the same pair as the neighbors-only rule at all 6,404 one-writer steps. The two many-writer seeds healed to the one-writer shape after 64 quiet notes.

Same-grain nearest `nap`, with grain and nearest checked after the children load and the overlap check, held. The pinned order is why the older refusals did not move.

Sorting opened rows by `{stamp}-{rand}` held. Listings that wake does not open are unchanged, which is why the existing wake tests stayed put.

Leaving legacy odd packs closed held. A lone 6-pack was already unrequested under the old picker, because it has no twin. Two 6-packs were the case that would have become a 12-pack. The architecture zipper walk that built those 6-packs had to be redrawn as two grain-8 packs, because `nap` now refuses the unequal nap the picture used to assume.

## Build & QA Observations

Units 1–4 went red for the reasons the plan named, then green. QA passed on the first review and re-ran py311 (417 passed). It left three advisories, none blocking: test names that still say adjacent, refusal text that states the problem only, and the overlapping leaves check and digest-count check. The plan asked for both checks and for problem-only messages.

The research scripts under `creative/fold-research/` still call `_adjacent_nodes`, which the product no longer has. They are not on the test path.

## Cross-Phase Analysis

The preflight scratch build is what kept the real build from discovering the missed fixture and the stale counts in the middle of TDD. The creative simulation is what made oldest-pair-first a decision instead of a guess, and the build's one-writer oracle is that same comparison moved into the suite.

Advisory 7 stayed out. If a later store strands under this rule, the pre-mortem says to re-enter the plan rather than special-case the picker.

## Insights

### Technical

- Two notes with the same text share an id and a digest. Once they are two rows, `write_nap` of that id twice is "overlapping packs". A closest-pair preference has to be tested on `_pair_nodes`.
- Neighbors-only fold and this picker are the same function on a listing whose grains never rise. The one-writer picture in the architecture doc can keep saying "neighbors" for that walk.

### Process

- A preflight that builds the plan in scratch, and reports the exact failing names, is cheaper than discovering those failures one red test at a time.
- A property test that restarts a tree walk per item can pass and still be unusable. One walk of the view was the same assertion at a fraction of the time.
