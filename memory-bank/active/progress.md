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
