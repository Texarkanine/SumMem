# Progress

Fix [issue #77](https://github.com/Texarkanine/SumMem/issues/77): heal must not delete a loose note whose text already sits inside a pack, and napping two identical notes must not produce a pack whose grain disagrees with its leaf set.

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
