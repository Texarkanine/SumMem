# Progress

Fix middle orphans: replace the neighbors-only equal-grain fold picker with oldest-pair-first skip fold, narrow `nap` to same-grain nearest pairs, sort wake's opened rows by date, leave legacy non-power-of-two packs alone, and update the docs. Red regression tests already exist on this branch.

**Complexity:** Level 1 (rework of a Level 3 task; the Level 3 reflection stands and `/niko-archive` still follows)

## 2026-10-06 - RESEARCH (pre-Niko) - COMPLETE

* Work completed
    - Reproduced the stall on the real driver and named five ways a wall forms (unseen partner across a merge, late note, zipper reopen, surgery, non-power-of-two pack).
    - Committed red regression tests: `299c0fa`, `b9dc459` (`tests/test_middle_orphans.py`, `tests/test_nap_reject.py`).
    - Simulated six fold rules on the real driver with four writers and git-style merges. Harness, results, and the visual review are in `memory-bank/active/creative/fold-research/`.
    - Scanned the 22 local stores (11 repos): no non-power-of-two packs, no walls in the four stores that have folded.
    - Recorded findings in SumMem (`ded53bc`, `35fc79b`).
* Decisions made
    - Operator: never write a non-power-of-two pack.
    - Operator: skip fold; oldest pair first, chosen over the operator's pull-back rule on simulation evidence.
    - Operator: decision 2 = yes (`nap` takes same grain, nearest); decision 3 = yes (wake sorts opened rows by date); decision 4 = no (do not open legacy packs).
    - Operator: captions only through the normal fold cascade; opening legacy packs up front is dangerous.
* Insights
    - Today's rule only works while grains never rise from older to newer rows. Any merge can break that, and then the rows before the wall are dead lines.
    - Pure pull-back strands rows forever, for example a young `main` `[4, 1]` followed by a merged 8-pack. Misordering piles up while a wall stands.
    - Oldest-pair-first makes the same choice as today on a healthy listing, and keeps the one-writer shape after 87–97% of merges.

## 2026-10-06 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified as Level 3.
* Decisions made
    - Level 3, not Level 2. The change is in the core fold contract described in `docs/architecture/index.md`. It spans the fold picker, the `nap` pair rule, wake expansion, test fixtures, and five docs. It needed a design exploration (six algorithms) before planning. Comparable earlier changes (equal-grain #1, zipper-heal #3) were Level 3.

## 2026-10-06 - CREATIVE - COMPLETE

* Work completed
    - Recorded four resolved creative decisions in `memory-bank/active/creative/`: fold picker, nap pair rule, wake expand order, legacy odd packs.
    - Saved the research harness, prototype patch, raw results, and the visual review under `memory-bank/active/creative/fold-research/`.
* Decisions made
    - Fold picker: skip fold, oldest pair first (high confidence; simulation evidence).
    - Nap pair rule: same grain, nearest; grain and nearest checks run after child loading and the overlap check (operator decision 2).
    - Wake expand order: sort rows by oldest note's `{stamp}-{rand}` after each split (operator decision 3).
    - Legacy odd packs: never opened; picker skips them (operator decision 4).
* Insights
    - Checking grain before loading children would flip four error-order tests (`unknown id`, `unreadable pack`, `overlapping packs`).

## 2026-10-06 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 3 plan in `tasks.md`: component analysis, invariants, 18 behaviors (B1–B18) mapped to test files, five ordered units with always-tdd substeps, challenges, and pre-mortem.
    - Checked the plan against the code. A balanced `fold_ids` breaks only `test_zoom_expanded_child_id`. `ProjectedNode` constructions in tests use keywords, so a defaulted `seq` slot is safe. `surgery.py` only consumes `fold_request`.
* Decisions made
    - Unit order: fixtures, then `nap`, then picker, then wake, then docs. `nap` must accept skip pairs before the picker requests them.
    - `nap` check order: resolve → load children → overlap → equal grain → power of two → nearest.
    - Seeded multi-writer property test (B18) as the ratchet for "no row strands forever".
* Insights
    - Two legacy packs of the same odd grain would satisfy "same grain"; the power-of-two guard has to live in both the picker and `nap`.

## 2026-10-06 - PREFLIGHT - COMPLETE

* Work completed
    - Checked the plan against the code. Ran a scratch prototype of Units 1–4 (outside the worktree) through the full suite, plus a model of B18 and a check of the B5 legacy-pack cases.
    - `.preflight-status` first line: `FAIL (fixable)`.
* Decisions made
    - FAIL (fixable): `tests/test_branch_pack_merge.py::test_two_branch_overlapping_packs_heal_on_next_mutate` naps a 2-pack with a note at lines 74 and 84. Unit 2 breaks it, and the plan does not name it. Fix: use `plant_pack` there in Unit 1 and list the file.
    - The TDD plan encoding passes. No step swaps or change-detector strikes were needed.
* Insights
    - Baseline is 7 red and 395 green. With Units 1–4 applied, every stranding test and the unequal-nap test pass. The only failures outside the plan's named retargets come from that one fixture.
    - B18 needs "doubled grain" to count only grains ≥ 2 (as `sim4.py` does). B5's "returns to budget" holds only at note counts whose power-of-two remainder fits in the rows left over (32 works).

## 2026-10-06 - PLAN (rework after Preflight FAIL (fixable)) - COMPLETE

* Work completed
    - Unit 1 now also replaces the two direct 2-pack + note naps in `tests/test_branch_pack_merge.py::test_two_branch_overlapping_packs_heal_on_next_mutate` (lines 74, 84) with `plant_pack`.
    - Adopted advisories:
        - B5 asserts the budget at 32 notes.
        - B18 counts doubled grains ≥ 2 only, and merges every writer before checking that no note is lost.
        - The docs sweep is case-insensitive (`adjacen|neighbo`) and names `systemPatterns.md:72` and `architecture/index.md:185`.
        - Brief Requirement 1 now says "no two power-of-two rows".
        - Test counts are stated consistently.
    - Partly adopted the advisory "one shared pure pair function":
        - pure `_fold_pair(grains)` drives `fold_request`;
        - `_nearest_twin` and `_is_pow2` are shared by the picker and `write_nap`, so the requested pair is accepted by construction;
        - new pure tests: B19 (one writer: `_fold_pair` equals the old neighbors-only oracle `_equal_grain_pair` for budgets 1–32) and B20 (non-power-of-two rows are skipped).
* Decisions made
    - `nap` keeps decision 2: any nearest same-grain power-of-two pair. It is not narrowed to the picker's single pair; that would override the operator's decision.
* Insights
    - My earlier fallout count lumped the branch-merge test in with the `fold_ids` failures. The real breakdown is 11 through `fold_ids`, 1 direct nap in `test_branch_pack_merge.py`, and 4 zipper tests.

## 2026-10-06 - PREFLIGHT (run 2) - COMPLETE

* Work completed
    - Checked the reworked plan against the code. Built Units 1–4 exactly as written in scratch copies outside the worktree and ran the full suite.
    - Also checked B2–B5, B14, B15, B19, and B20 on the prototype, and ran a B18 model: 3 writers, budget 6, six seeds, three merge rates.
    - `.preflight-status` first line: `PASS WITH ADVISORY`.
* Decisions made
    - PASS WITH ADVISORY. Run 1's blocking finding is fixed. With Unit 1's `plant_pack` change, `test_branch_pack_merge.py` stays green under the new `nap` rule.
    - TDD plan encoding passes. No step swaps or change-detector strikes were needed.
    - Advisories:
        - the stranding-test count is still "six"; it is five;
        - `_pair_nodes` should return indices;
        - name which grain `write_nap` compares, and check that the digest count is a power of two;
        - keep the node form of `_equal_grain_pair` for its six callers;
        - Unit 1's "393 passed" is out of date (395 is correct);
        - Requirement 5 should say "never opened on disk".
    - Radical innovation (advisory): a bounded, exhaustive pure-model check of the fold rule next to B18.
* Insights
    - Unchanged code: 7 failed, 395 passed. Unit 1 alone: the same 7 failed and 395 passed. Units 1–4: 5 failed, 397 passed, and every failure is a retarget the plan names.
    - For one writer, the new picker chose the same pair as the neighbors-only rule at all 6,404 fold steps (budgets 1–32, up to 200 notes).
    - B18 model: no stall while a pair was available, no notes lost, and the one-writer shape at 64 quiet notes, in 1.5–2.6 s per run. On the unchanged driver the same model stalls, so B18's red step works.

## 2026-10-07 - BUILD - COMPLETE

* Work completed
    - Units 1–5, in order, with tests before production code on the executable units.
    - Fixtures: `fold_ids` only builds balanced packs; `plant_pack` writes a legacy shape with no pairing policy.
    - `nap` accepts a nearest same-grain power-of-two pair and refuses the rest in the pinned check order. `_adjacent_nodes` is gone.
    - `fold_request` uses `_fold_pair`: oldest power-of-two row with a same-grain row below it, paired with the nearest such row.
    - Wake sets `ProjectedNode.seq` and sorts opened rows by it after each split.
    - Docs, help, and `systemPatterns.md` describe that rule. The one-writer walk in the architecture doc stays, because on a listing that never rises the pair is still the oldest neighbors.
* Decisions made
    - Advisories 1–6 applied. Advisory 7 not built.
    - Closest-pair preference is pinned on `_pair_nodes`, not by a successful nap of identical text.
* Insights
    - `tox run-parallel`: py311, py312, py313, and py314 all OK. py311 reported 417 passed in 19.27 s.
    - Seed 7 of the many-writers test was 3.17 s after reachability became one walk of the view.

## 2026-10-07 - QA - COMPLETE

* Work completed
    - Reviewed the `main...HEAD` diff of `summem`, tests, and docs against the plan and brief for KISS, DRY, YAGNI, completeness, regression, integrity, and documentation.
    - Confirmed every planned test (B2, B3, B5, B7–B10, B12, B14–B16, B18–B20) exists. Re-ran `tox -e py311`: 417 passed.
    - Searched docs, README, help text, and `systemPatterns.md` for "adjacent" and "neighbor": the remaining hits are the single-writer walk, the wall definition, and the retained test oracle.
* Decisions made
    - PASS with three non-blocking advisories (stale "adjacent" test names, problem-only refusal text, overlapping leaves and digest-count checks in `write_nap`). Details in `.qa-validation-status`.
* Insights
    - No debris, TODOs, or print statements in the diff. `surgery.py` and `migrate.py` are untouched, as planned.

## 2026-10-07 - REFLECT - COMPLETE

* Work completed
    - Compared the brief's seven requirements to the build. All shipped. Advisory 7 stayed out, as left for the operator.
    - Wrote `memory-bank/active/reflection/reflection-middle-orphans.md`.
    - Persistent files: productContext, systemPatterns, and techContext needed no further edit. systemPatterns already states the fold and wake-sort contract from the docs unit.
* Decisions made
    - The "stranded forever" claim stays a tested rule, not a proof.
* Insights
    - Identical text shares a digest, so closest-pair is not observable through a successful nap.
    - The many-writers test's cost was the per-note walk, not the fold rule.

## 2026-10-07 - HANDOFF

* Work completed
    - Pushed `middle-orphans` and opened draft PR https://github.com/Texarkanine/SumMem/pull/87 (`fix: fold the oldest same-grain pair across a wall`).
* Decisions made
    - Archive waits. The operator is smoke-testing first.

## 2026-10-11 - REWORK - INITIATED

* Work completed
    - Operator requested rework from PR #87 review feedback.
* Decisions made
    - Fix cursor[bot]'s finding (https://github.com/Texarkanine/SumMem/pull/87#discussion_r4242528865): a nap whose children file is missing or unreadable still counts by its filename grain. The fold picker names it, `nap` fails (`unknown id` / `unreadable pack`), and every later `note` asks for the same pair. Folding stops for good. `main` had the same stall only when the broken nap was in the oldest adjacent pair; oldest-pair-first makes it near-certain.
    - Dismissed LlamaPReview's `_replace` / `seq` question: `_replace` rebuilds from `__slots__`.

## 2026-10-11 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework as Level 1.
* Decisions made
    - Level 1: one component, one rule, no design choice. The picker already skips non-power-of-two rows; a nap with a missing or unreadable children file gets the same treatment.

## 2026-10-11 - BUILD - COMPLETE

* Work completed
    - Four red tests first (fold request skips a broken pack; `nap` pairs across a broken same-grain row; each for a missing and an unreadable children file), then `_fold_grains` in `summem`, used by `fold_request` and `write_nap`. One sentence in `docs/architecture/index.md`.
    - `tox run-parallel`: py311–py314 OK.
* Insights
    - The picker and the nearest-twin check must agree on which rows count. One helper feeds both, so a row the picker skips can never block a pair in `nap`.
