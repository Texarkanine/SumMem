# Progress

Give naps a five-part stem with a pair-bytes variant tag so concurrent same-block folds merge as distinct paths, then let the existing zipper drop all but one equal-leaf-set variant. Ship a migration script for four-part stores. Spec: [issue #61](https://github.com/Texarkanine/SumMem/issues/61).

**Complexity:** Level 3

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent from issue #61 plus the operator's migration-script requirement; operator approved.
    - Classified as Level 3 and wrote ephemeral memory-bank files.
* Decisions made
    - Level 3, not L2: disk-format change, shared stem constructor, dual-read, 14 merge/heal proofs, atlas invariants, and a migration script.
    - Level 3, not L4: one coherent breaking PR that completes the existing file-backend ingest contract; not a new subsystem or independently shippable milestone set.
* Insights
    - Product success criteria still say “same-block naps conflict only on the caption”; this task retires that line.
    - Issue #59's manual whole-pair recipe is superseded for new stems; it remains relevant only to pre-upgrade legacy conflicts.

## 2026-08-25 - CREATIVE - COMPLETE

* Work completed
    - Explored where the operator migration helper lives.
* Decisions made
    - Sibling `migrate.py` (surgery analogue): loads `summem`, hashes on-disk pair bytes, renames complete four-part stems. Not a CLI verb, not folded into `surgery.py`, not a shell reimplementation of the digest.
* Insights
    - The README command-table stability rule is what kills `summem migrate` as the shipped surface.

## 2026-08-25 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 3 plan: eight implementation units (seven executable TDD units, one prose/policy), process-level union/heal/squash proofs, `migrate.py` tests, atlas/product copy.
* Decisions made
    - `_parse_nap_stem` returns a five-tuple; legacy variant is `""`.
    - Heal production code changes only if unit 4 proves the existing `<=` + filename order wrong.
    - Invert `test_same_pair_two_captions_conflict_only_on_sum` in place; new proofs live in `tests/test_nap_variants.py`.
    - Dogfood migrate of this clone is part of unit 7 green, not its own untested executable unit.
* Insights
    - `surgery.py` already calls `_nap_stem`; rematerialize constructor reuse covers surgery without a surgery source change unless a test pins old dest names.

