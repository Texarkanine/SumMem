# Progress

`start` reports a store in one sentence and refuses a missing directory. `help` reuses the existing help text. A `nap` of an already-folded pair succeeds, and any other bad id gets a short refusal that does not point at `wake`.

**Complexity:** Level 2

## 2026-11-07 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the three open issues as one Level 2 enhancement of the CLI
* Decisions made
    - Level 2: one script, contained behavior changes, wording still to try during build
* Insights
    - Bare `summem` is an intentional usage error (stderr, exit 2) from the first CLI. `-h` is already stdout and exit 0. The blog post's stdout rule covers help probes, which this path already is.

## 2026-11-07 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan for start, help, and nap replies
* Decisions made
    - One start sentence: `There is a store in ./path.`
    - Missing path: `not a directory: ./path`, and no `mkdir`
    - `help` rewrites to the existing `-h` path, including `help <command>`
    - An already-folded pair succeeds with `Saved.` and the real next fold or the idle line
    - Other nap misses are `not a fold row` or `unknown id`, with no wake hint
* Insights
    - Napping the two children `wake` expanded is the nap that already exists, so it is the success path, not a second error

## 2026-11-07 - PREFLIGHT - FAIL (fixable)

* Work completed
    - Preflight of the first plan returned three fixable findings and no plan edits
* Decisions made
    - Revise the plan and preflight again
* Insights
    - A note's view id is `leafset_id` of its digest, 16 hex. The raw digest does not match a wake prefix.
    - `tests/test_path_walkup_and_catalog.py` also starts directories it does not create.

## 2026-11-07 - PLAN - COMPLETE

* Work completed
    - Revised the plan for the three preflight findings and the commands-table advisory
* Decisions made
    - `_nap_miss` reuses `_projected_child` and `_index_tree`. No new child-id helper.
    - Known ids are view rows plus nested tree ids. One of each, when not a direct pair, is `not a fold row`.
* Insights
    - The id formula was already in two places. A third copy of the raw digest would not match wake.

## 2026-11-07 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Validated the implementation plan against the codebase, test suite, and documentation
    - Wrote `memory-bank/active/.preflight-status` with first line `FAIL (fixable)`
* Decisions made
    - Flagged three fixable plan issues before Build: `tests/test_path_walkup_and_catalog.py` calling `start` on uncreated directories, `_nap_miss` using `note_digest` instead of `leafset_id([note_digest(...)])` for `NoteChild` ids, and `_nap_miss` checking only nap trees rather than `view_ids | nested_ids` when classifying `not a fold row`
* Insights
    - A `NoteChild`'s 16-hex content id is `leafset_id([note_digest(note_file_bytes(text))])`, not the raw 64-hex `note_digest`

## 2026-11-07 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated revised implementation plan against codebase, test suites, and documentation
    - Verified all three previous fixable findings and the commands table advisory were resolved in the plan
    - Overwrote `memory-bank/active/.preflight-status` with `PASS WITH ADVISORY`
* Decisions made
    - Approved plan for build transition with one advisory finding on structuring `_nap_miss`
* Insights
    - Single-pass inspection of view naps with `_as_child` and `_index_tree` provides both direct-pair detection and complete known-id cataloging for `not a fold row` vs `unknown id` determination

## 2026-11-07 - BUILD - COMPLETE

* Work completed
    - Implemented start, help, and nap replies with tests first
    - py311 suite: 441 passed
* Decisions made
    - One start sentence for a new store and an existing store
    - `help` is a rewrite onto `-h`, not a new parser
    - An already-folded pair skips `write_nap` and still prints `Saved.`
* Insights
    - Note ids inside a nap are `leafset_id` of the digest. Matching the raw digest misses them.

## 2026-11-07 - QA - COMPLETE (PASS)

* Work completed
    - Performed post-implementation semantic review against the implementation plan, project brief, and system patterns
    - Verified all 441 tests pass under `py311`
    - Wrote `PASS` status to `memory-bank/active/.qa-validation-status`
* Decisions made
    - Approved implementation with one non-blocking documentation advisory (`docs/user-guide/commands.md:142`)
* Insights
    - Reusing `_as_child`, `_projected_child`, and `_index_tree` in `_nap_miss` kept the already-folded and `not a fold row` checks within a single pass over view naps without duplicating tree traversal or id computation

## 2026-11-07 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-start-help-nap.md`
    - Recorded that `start` requires an existing directory in `systemPatterns.md`
* Decisions made
    - Left the outside-a-repository sentence as QA found it
    - Did not add a store note. View ids as `leafset_id` are already remembered
* Insights
    - A note id on wake is `leafset_id` of the digest. The raw digest matches nothing in the view.

## 2026-11-07 - SAVE

* Work completed
    - Opened draft PR 101
    - Slimmed `_nap_miss` onto `resolve_id` and `root_kids`, and dropped a redundant path join in `start` (`fix: ponytail` on the PR branch)
    - py311: 441 passed after the slim
* Decisions made
    - Did not fold the two nap refusals into one string, and did not walk trees on a nap that already resolves
* Insights
    - The pair check can use `root_kids` from the walk `_nap_miss` already runs

## 2026-11-07 - REWORK - INITIATED

* Work completed
    - Operator chose rework of start-help-nap over archive, from PR 101 review
* Decisions made
    - The help printout names one way to do each thing. `help` keeps working and is not listed
    - A nap of some nap's two direct children succeeds even when that nap is nested inside a larger one
    - The sentences that already describe that success stay. No added sentence whose only job is to mention the nested case
* Insights
    - On main, both the one-level retry and the nested retry already failed with `unknown id`. The nested miss is a hole in this branch's new success path, which only checks `root_kids`

## 2026-11-07 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework as Level 2
* Decisions made
    - Level 2: one script, the catalog mirror in the user guide, and no architectural choice
* Insights
    - Item 1 is a product rule about what the catalog prints. Item 2 is a hole in the success path this branch added. Together they stay inside the CLI that already owns both.

## 2026-11-07 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan for the help-catalog omission and the buried-pair nap
* Decisions made
    - `usage_text` loses the `help` row. The argv rewrite stays
    - The commands table returns to naming only `-h` and `<command> -h`
    - `_nap_miss` pair-matches `root_kids` and every list in `index["kids"]`
    - The four sentences that already describe that success are not edited
* Insights
    - `kids` does not include the view nap's own pair. Both lists are required



