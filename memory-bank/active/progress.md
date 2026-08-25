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
