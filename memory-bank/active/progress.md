# Progress

Fix [issue #77](https://github.com/Texarkanine/SumMem/issues/77) under the operator vote: `L` is a set of facts. Trigger 1 is intended (shoebox). Trigger 2 is the remaining lie: two identical notes must not nap into grain 2 with one leaf.

**Complexity:** Level 3

## 2026-08-29 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated from issue #77 and confirmed
    - Classified as Level 3
    - Wrote ephemeral memory-bank files
* Decisions made
    - Level 3, not Level 1 or 2: the defect is a bug, but the issue names three non-equivalent layers (per-file identity, multiset heal, nap-reject-only). Option 1 changes every stored leaf-set id. L3 Creative exists for that fork.
* Insights
    - Atlas already says two notes with the same text share an id and remain two view nodes. That holds for two loose notes (note/note skip) and stops holding the moment one copy is inside a pack.
    - `leafset_id` keys on the leaf multiset; `leaf_digests` keys on the set. Grain counts duplicates; overlap does not.

## 2026-08-29 - CREATIVE - COMPLETE

* Work completed
    - Architecture creative on which layer to make honest (`memory-bank/active/creative/creative-leaf-identity.md`)
* Decisions made
    - Per-file identity: `note_digest(name, bytes)` is SHA-256 of `name + NUL + bytes`. Issue option 2 does not fix trigger 1. Nap-reject misses trigger 1 and can stick fold. Heal-by-filename keeps two overlap rules.
* Insights
    - `test_heal_note_covered_by_nap_dropped` is rematerialize of the same name, not the bug. It must stay green.
    - Every note id changes, not only duplicates, because the digest input grows.

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Four implementation units: digest+call sites, heal/nap tests, migrate.py, atlas/theory
    - Required test: a note written after its text was folded still exists after the next heal
* Decisions made
    - No new test files. Driver does not dual-read old content-only 16-hex stems.
* Insights
    - Fold of two identical notes becomes two prefixes on `Run:`, not one prefix twice.

## 2026-08-29 - CREATIVE - REVISED

* Work completed
    - Operator vote: `L` is a set of facts; same sentence is one leaf regardless of when noted
    - Rewrote `memory-bank/active/creative/creative-leaf-identity.md`
* Decisions made
    - Keep content identity. Trigger 1 is the shoebox, not a keep-the-file bug. Remove the note/note skip; `write_nap` rejects any digest overlap. No migrate. `Saved.` stays.
* Insights
    - The first pass treated the theory “leak” section as spec. The shoebox is the spec. The leak section was the issue talking.

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Retargeted four units: heal skip, nap overlap for notes, fold/CLI same-id tests, atlas/theory
    - Trigger 1 test now pins deletion, not survival
* Decisions made
    - Recency-by-renoting is out of scope
* Insights
    - After heal, `(id, id)` nap of two copies is gone because only one view node remains

## 2026-08-29 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the revised Level 3 plan against the current driver, test suite, atlas, and theory document
* Decisions made
    - Build is gated until the direct `write_nap` duplicate-note regression test is explicitly retargeted
* Insights
    - `test_write_nap_identical_text_notes_still_concat` still asserts the behavior that the planned overlap guard removes
    - The atlas contains duplicate-note behavior in both Identity and Zipper sections

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Named `test_write_nap_identical_text_notes_still_concat` in unit 2 with ValueError / no pack files / both notes remain
    - Unit 4 now rewrites Identity and Zipper, not Identity alone
* Decisions made
    - Did not add an `assert_unique_leaf_sets` helper; `gitutil.assert_unique_cover` already exists
* Insights
    - Direct `write_nap` is the path that still sees two files; CLI heal runs first

## 2026-08-29 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Re-validated the amended Level 3 plan against `summem`, the test suite, the atlas, and `docs/theory.md`
* Decisions made
    - Build stays gated: `tests/gitutil.py::assert_unique_cover` still hard-codes the note/note overlap skip Unit 1 removes in production, and no unit's Files list touches it
* Insights
    - The "`assert_unique_cover` already exists" premise from the prior planning pass is false once Unit 1 lands — the helper still permits exactly the case being fixed
    - Every existing call site of that helper runs after a `heal_view` on non-duplicate text, so nothing currently breaks; the gap is a blind regression-detector, not a red test

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Unit 1 Files now includes `tests/gitutil.py`; drop `assert_unique_cover`'s note/note skip and docstring
    - Unit 2 Files includes `tests/test_cli.py`
    - Unit 4 quotes the real `systemPatterns.md` sentence (“adjacency must keep both”)
* Decisions made
    - Do not make `assert_unique_cover` call `_first_overlap`; drop the skip in the helper instead
* Insights
    - `test_two_identical_notes_stay` never calls `heal_view`; leave it alone

## 2026-08-29 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Re-validated the amended Level 3 plan against the driver, existing tests, acceptance criteria, and documentation targets
* Decisions made
    - Build remains gated until the plan explicitly schedules the CLI `note` packed-duplicate regression test
* Insights
    - Naming `tests/test_cli.py` in Unit 2 only accounts for the same-id `nap` retarget; it does not cover acceptance criterion 1's `note` acknowledgement and post-heal behavior

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Unit 1 now numbers `test_cli_note_text_inside_nap_exits_0_no_loose_note`: exit 0, `Saved.\n`, no loose duplicate, zoom reaches
* Decisions made
    - Keep that test in `tests/test_zipper.py`; do not move it to `test_cli.py`
* Insights
    - The CLI case already exists; it was missing `Saved.` and zoom, not a missing file

## 2026-08-29 - PREFLIGHT - COMPLETE (PASS)

* Work completed
    - Fourth preflight run; re-validated the amended plan against `summem`, the full named test set, and documentation targets
* Decisions made
    - Build unblocked: the CLI `note` regression test gap is closed with all four required assertions in the right TDD order
* Insights
    - Confirmed against `summem` that `note`'s CLI path always heals before printing and `fold_request` returns `""` for a single-node view, so the plan's "stdout is exactly `Saved.\n`" claim is technically sound, not just plausible

## 2026-08-29 - BUILD - COMPLETE (PASS)

* Work completed
    - Removed the note/note skip in `_first_overlap`; heal keeps the later filename
    - `write_nap` rejects any intersecting digest sets
    - Retargeted same-id fold/CLI/nap tests; planted zoom/recall duplicate-date trees
    - Atlas Identity and Zipper, `systemPatterns.md`, and `docs/theory.md` (Duplicate receipts) match `L` as a set
    - py311 371 passed, 1 skipped; `tox run-parallel` py311+py314 OK, py312+py313 skipped
* Decisions made
    - Kept the existing `overlapping packs` error string (one family; tests already pinned it)
    - `fold_request` unchanged: mutating commands heal first
* Insights
    - Zoom and recall still list two same-text nested children when a children file is planted; `write_nap` can no longer create that pack

## 2026-08-29 - QA - COMPLETE (FAIL)

* Work completed
    - Semantic review of the build diff (`a6ffe93..HEAD`) against the brief, plan, and creative decision
    - Re-ran `tox -e py311` for context: 371 passed, 1 skipped, matching the build's claim
    - Wrote `memory-bank/active/.qa-validation-status` and QA findings into `tasks.md`
* Decisions made
    - FAIL routed to Build rework, not Plan: all three blocking findings are test-name/docstring/prose local, and the plan and the 4-line production diff are sound
    - `overlapping packs` for two loose notes accepted as advisory: the plan permitted one error family and the wording is unreachable from the CLI
* Insights
    - Retargeting a test updated its docstring but left its name asserting the removed contract in three places; the name is what `-k` and failure output show, so it is the contract a reader trusts
    - `docs/architecture/index.md:161` already stated the general overlap rule, so this fix removed a contradiction between Zipper and Identity rather than introducing one
    - Dropping the `leafset_id`/`leaf_digests` citations from `docs/theory.md` cost the paragraph its referent; the list-vs-set asymmetry is still true of the code and is the reason the refuse exists

## 2026-08-29 - BUILD - COMPLETE (QA rework)

* Work completed
    - Renamed three tests whose names still asserted the removed contract
    - Scoped the pre-heal digest pin (`test_leaf_digests_shared_for_identical_notes`)
    - Rewrote `docs/theory.md` Duplicate receipts closer; named `leafset_id` vs `leaf_digests`
    - Docstrings on planted zoom/recall duplicate-date tests now say they cover pre-change packs
* Decisions made
    - Did not change the `overlapping packs` error string (advisory; plan permitted one family)
* Insights
    - A retargeted docstring is not enough: `-k` and failure output still index the old name

## 2026-08-29 - QA - COMPLETE (PASS)

* Work completed
    - Re-reviewed the build and its QA rework against the brief, plan, and creative decision
    - Confirmed test names and docstrings now describe their assertions
    - Verified the Duplicate receipts explanation and planted compatibility-test rationale
    - Ran `uvx --with tox tox run-parallel`: py311 and py314 passed; py312 and py313 skipped because their interpreters are unavailable
* Decisions made
    - Accepted the implementation as-is; no Build or Plan rework is required
* Insights
    - The remaining `overlapping packs` wording is a non-blocking shared-error-family choice and CLI-unreachable for two loose duplicate notes

## 2026-08-29 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-heal-same-text.md`
    - Reconciled persistent files: no further edits
* Decisions made
    - Archive is the next operator step; this task is not an L4 sub-run
* Insights
    - Retarget is not done until the test name matches the body
    - A why-page “leak” section is not spec until the operator says so
