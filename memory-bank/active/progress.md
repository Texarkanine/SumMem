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

## 2026-08-26 - PREFLIGHT - PASS WITH ADVISORY

* Work completed
    - Third preflight verified the revised plan directly against live code (summem, migrate.py), live tests, live docs, and the fetched GitHub issue #67 body — not just against the plan's own prose.
    - Confirmed both defects from the second preflight are fixed: grain-8 two-depth fixture pins `_shorten_tree` recursion; unit 2 step 4 now writes via `_write_pair` then unlinks sources instead of `Path.replace`.
    - Independently re-derived the "leftover 64-hex fixture" grep across all of `tests/` and found no fixture the plan's enumeration missed.
* Decisions made
    - No plan changes required. Two advisories recorded, neither blocking: a declarative legacy-stem-upgrade table for `migrate.py` (future-proofing, not this issue), and a non-blocking docstring-precision nit in two unrelated tests.
* Insights
    - Live inspection of this clone's root store confirms nested 64-hex `NapChild.id` at depth up to 4 (grain-32), independently validating activeContext's correction of the prior preflight's "no nested id" claim.

## 2026-08-26 - BUILD - COMPLETE

* Work completed
    - Truncated `leafset_id` to 16 hex; `_parse_nap_stem` accepts only five-part-16.
    - Rewrote `migrate.py` for 4-part-64 and 5-part-64: recursive `_shorten_tree`, `_write_pair` then unlink.
    - Updated atlas, `systemPatterns.md`, and README walkthrough.
    - Migrated this clone's root and dogfood stores. `tox run-parallel` py311–py314 green (366 tests).
* Decisions made
    - Atlas Identity hash step 3 states the stored id is the first 16 hex of the join hash, not only the wake-prefix sentence.
* Insights
    - Grain-2 note-only pairs keep the same variant tag after migrate; grain-4+ recomputes it because nested ids change the tree bytes.

## 2026-08-26 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of driver width, migrate dual-source rewrite, atlas/systemPatterns/README, and this clone's stores against the plan. No product-code edits.
    - Confirmed root (3 view pairs) and dogfood (2 pairs) are five-part-16, nested nap `"id"` values are 16 hex, and each stem equals `nap_stem` of the on-disk pair bytes.
* Decisions made
    - PASS with two non-blocking advisories. Implementation is acceptable as-is.
* Insights
    - Truncation inside `leafset_id` plus `_as_child` copying `node.id` is why new folds cannot split stem width from nested JSON width without a separate write-path change.


