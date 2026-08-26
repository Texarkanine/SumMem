---
task_id: 16-hex-leafset
date: 2026-08-26
complexity_level: 3
---

# Reflection: 16-hex-leafset

## Summary

Stored public leaf-set ids are the first 16 hex of the existing SHA-256. The driver lists only five-part-16 stems; `migrate.py` rewrites 4-part-64 and 5-part-64 (including nested `.tree` ids) in one pass. QA passed. This clone's root and dogfood stores match the driver.

## Requirements vs Outcome

Every brief requirement landed: truncation inside `leafset_id`, five-part-16 only in the driver, dual-source migrate with recursive nested-id rewrite, atlas / `systemPatterns.md` / README, and this clone's stores in the same change. `tox run-parallel` py311–py314 was green (366 tests). Nothing was descoped. Two small additions: atlas Identity step 3 now names `[:16]` on the join hash, and `test_nap_stem_is_five_part` also asserts a 64-hex `nap_stem` is not a view name.

## Plan Accuracy

Four units were the right split. Leaving `tests/test_migrate.py` red through unit 1 was load-bearing: after `leafset_id` truncates, `write_nap` cannot plant 64-hex fixtures. The planned challenges were the ones that showed up — planting old stems with `hashlib`, re-`dumps_tree` so the variant matches rewritten bytes, and not `Path.replace`ing source `.tree` onto dest. The surprise was inventory, not mechanism: build notes said four root pairs; the view has three, with grain-8 nested inside those trees. QA recorded that as an advisory. Stores were still migrated correctly.

## Creative Phase Review

No creative phase. Width change plus a second migrate source did not need a design fork. Leftover `memory-bank/active/creative/` files are from prior tasks and were unused.

## Build & QA Observations

Build followed TDD. Unit 1 went red for the right reasons (64-hex still returned / still parsed), then green except migrate. Unit 2's grain-8 fixture is what pins `_shorten_tree` recursion after this clone's files are already 16-hex. Grain-2 note-only pairs keep the same variant tag; grain-4+ recomputes it. QA passed with two non-blocking advisories: the nested-fold test does not assert `len(NapChild.id) == 16` (write path copies the 16-hex view id), and the four-vs-three root-pair count.

## Cross-Phase Analysis

Two preflight FAIL (fixable) rounds prevented the expensive mistakes. The first caught README still showing a 64-hex basename, a phantom in-tree “do not shorten” sentence, and migrate tests that would have been planted 16-hex after unit 1. The second caught a grain-4 test that cannot prove recursion and `Path.replace` of old `.tree` bytes under a dest stem hashed from rewritten buffers. Live inspection also corrected a false “root has no nested id fields” claim. Those defects would have shipped mixed widths or a dest name that disagreed with dest bytes. QA did not have to rediscover them.

## Insights

### Technical
- Mixing 16-hex view ids with leftover 64-hex nested `.tree` ids makes `resolve_id` treat the short id as a prefix of the long one. Truncation has to live in `leafset_id` (so notes and naps share a width) and in every nested `NapChild.id`, not only the filename.
- `_as_child` copies `node.id` from the stem. After `leafset_id` returns 16 hex, new folds cannot emit a 64-hex nested id without a separate write-path change. That is why the missing nested-length assert is an advisory, not a hole.
- Grain-2 note-only trees round-trip under shorten; grain-4+ must recompute `variant_tag` because `dumps_tree` bytes change.

### Process
- Preflight on a width-changing migrate needs a test that a one-level walk cannot satisfy, and an implementation step that persists rewritten bytes before any rename. Grain-4 is one nested id; recursion needs a grandchild.
- Store inventory from memory is cheaper than opening the trees. It was also wrong once. Count view pairs from `list_view`, and nested ids from `.tree`, separately.
