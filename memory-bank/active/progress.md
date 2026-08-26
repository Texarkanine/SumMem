# Progress

Shorten stored nap leaf-set ids to 16 hex; grow `migrate.py` so one pass rewrites four-part and five-part-64 pairs (including nested `.tree` ids) to five-part-16; rewrite this clone's root and dogfood stores; update atlas and systemPatterns. Spec: [SumMem #67](https://github.com/Texarkanine/SumMem/issues/67).

**Complexity:** Level 3

## 2026-08-26 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Intent restated from #67; operator confirmed, including breaking change and post-reflect non-draft PR with a copyable `BREAKING CHANGE:` footer.
    - Classified Level 3: multiple components (driver, migrate, stores, docs), not a new architecture.
* Decisions made
    - Level 3, not Level 2: dual-source migrate plus nested-id rewrite is the same class as #61, not a suffix rename.
    - Level 3, not Level 4: on-disk width change inside the existing file backend; no milestone decomposition.
* Insights
    - Filename-only truncate is rejected in the issue because `resolve_id` would see a 16-hex view id that is a prefix of a 64-hex nested id.

## 2026-08-26 - PLAN - COMPLETE

* Work completed
    - Component analysis: `leafset_id`, `_parse_nap_stem`, write path, migrate, this clone's stores, atlas/systemPatterns.
    - Four implementation units (driver width, migrate rewrite, docs, clone stores). No creative phase.
* Decisions made
    - Truncation lives inside `leafset_id`, not at call sites, so `named_ids` is one width.
    - Migrate re-`dumps_tree` after shortening nested `NapChild.id`; unreadable `.tree` is incomplete, not filename-only.
    - Legacy test fixtures use `hashlib` full digests; do not round-trip the new writer.
* Insights
    - Grain-2 note-only trees have no nested nap `id`; the load-bearing rewrite is grain-4+.
    - Heal overlap still hashes note file bytes; that 64-hex layer is not this issue.

## 2026-08-26 - PREFLIGHT - FAIL (fixable)

* Work completed
    - First preflight (Claude Opus) recorded three fixable defects and four advisories in `memory-bank/active/.preflight-status`.
* Decisions made
    - Replan rather than build: README is a canonical document this change falsifies; the #61 “do not shorten” sentence is not in-tree; unit 1 must name `tests/test_migrate.py` as expected-red.
    - Keep truncate-stored-ids migrate (issue spec). Content-rebuild migrate stays advisory.
* Insights
    - Same failure class as #61 preflight: tests scheduled on the wrong side of a red-making change must be named, not omitted from the green list.

## 2026-08-26 - PLAN - COMPLETE

* Work completed
    - Unit 3 gains `README.md` (truncate walkthrough leaf-set to `cfbf987aa25d8492`; variant unchanged).
    - Brief req 8 / AC 6 restated to real sentences (atlas “full id”, systemPatterns, README). Phantom #61 clause struck.
    - Unit 1 step 4: `tests/test_migrate.py` stays red until unit 2; do not patch it in unit 1.
    - `_shorten_tree` recurses with `m._replace`; unit 4 is data migration plus `tox run-parallel`.
* Decisions made
    - Advisories 4–7 folded into the plan because they would fail a second preflight or ship a vacuous test. Advisory 8 (rebuild identity from content) not adopted.
* Insights
    - Grain-32 in this clone is why recursion is load-bearing, not only the grain-4 migrate test.

## 2026-08-26 - PREFLIGHT - FAIL (fixable)

* Work completed
    - Second preflight verified that the revised plan resolves every defect and advisory folded in from the first run.
    - Found two remaining migration-unit defects: recursion lacks a depth-two red test, and the implementation step computes rewritten tree bytes without persisting them before `Path.replace`.
* Decisions made
    - Replan unit 2 before build: add a grain-8-or-deeper legacy fixture and name the atomic rewritten-tree write before the rename sequence.
    - Keep content-derived identity rebuild as advisory only; #67 remains a stored-id truncation migration.
* Insights
    - The current root store's trees contain no nested `"id"` fields; dogfood exercises only one nested level, so applying migration to this clone cannot validate recursion.
    - `Path.replace` moves the original file bytes; computing a new buffer and hashing it into the destination stem does not write that buffer.

## 2026-08-26 - PLAN - COMPLETE

* Work completed
    - Unit 2 tests: add grain-8 five-part-64 fixture with nap ids at two nested depths; dest variant hashes fully rewritten bytes.
    - Unit 2 code: `_write_pair(dest, rewritten_tree_bytes, caption_bytes)` then unlink sources. Never `Path.replace` source `.tree` onto dest.
    - Unit 4 inventory corrected: root grain-32/16/8 trees nest 64-hex ids; dogfood grain-4 is one level. Recursion is still pinned by the grain-8 test.
* Decisions made
    - Keep content-rebuild migrate advisory. Truncate stored ids as specified.
    - Did not copy the second preflight’s “root has no nested id fields” — that is false of the current trees.
* Insights
    - Grain-4 is one nested nap `id` level. Recursion needs a grandchild.
