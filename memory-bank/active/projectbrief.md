# Project Brief

## User Story

As a concurrent writer, I want same-block naps whose pair bytes differ to land at different paths so git merge is a clean union and the existing zipper drops all but one equal-leaf-set variant, so I never hand-resolve `.tree`/`.summ` add/add conflicts or risk a mismatched pair.

## Use-Case(s)

### Use-Case 1

Two worktrees fold the same grain-2 notes with different captions. Git merge has zero conflicted `.summem/` paths. Wake may briefly print two same-id rows. The next `note` or `nap` zipper-collapses them to one complete pair; original notes remain zoomable.

### Use-Case 2

Three workers fold 1→2→4 from a shared four-note base with different intermediate and parent captions. Branch tips contain distinct five-part stems. Merge is set union. The next mutation keeps one internally consistent grain-4 pack.

### Use-Case 3

An operator upgrades a repository that still has four-part nap stems. They run the PR's migration script; the store is rewritten to five-part stems and a current driver can read it.

## Requirements

1. Implement [issue #61](https://github.com/Texarkanine/SumMem/issues/61) as specified: five-part nap stem `{seq-prefix}-{leaf-set id}-{grain}-{variant tag}`, variant tag = first 16 hex of SHA-256 over domain tag + length-prefixed tree bytes + caption bytes.
2. `write_nap` and `rematerialize_child` share one stem constructor. Bytes hashed are bytes written.
3. `_parse_nap_stem` accepts five-part stems only. `migrate.py` is the only four-part reader. New folds and rematerialized nested naps always use five-part stems.
4. Public commands (`note`, `wake`, `nap`, `zoom`, `recall`) and leaf-set identity are unchanged. Variant tag is not shown to agents and is not accepted by `nap` or `zoom`.
5. Sequence prefix stays the inherited leftmost-note `{timestamp}-{random}` byte-for-byte. Variant tag is a same-block arbitrary tie-break, not preference.
6. After merge, `heal_view` drops equal-leaf-set variants by existing overlap (`<=`); survivor is the lexicographically greatest complete stem. Wake stays read-only.
7. The PR includes a shell or Python script that rewrites an existing store from four-part stems to the new five-part shape.
8. Update the atlas, `systemPatterns.md`, and product success criteria. Retire “caption is the only honest conflict.” Close #59 as superseded.

## Constraints

1. Pre-1.0 clean-break disk format: driver and store land together. A legacy driver is not a supported concurrent writer once five-part stems exist.
2. Do not add a merge driver, `.gitattributes` rule, user-facing dedupe command, or wake-time heal.
3. Do not preserve every competing summary wording. Original note text is never lost.
4. Do not change leaf-set/content identity or public ids.
5. Keep `.tree` and `.summ` one atomic variant pair. Never mismatch a stem.
6. File count returns to O(view) after heal; duplicate variants are transient.

## Acceptance Criteria

1. Different captions, same grain-2 leaves: two worktrees merge with zero conflicted paths; wake initially prints two same-id rows.
2. Identical pair bytes: variant tags and paths match; git merges to one pair.
3. Atomic identity: same tree/different caption and same caption/different tree produce different complete stems.
4. Next `note` and next `nap` each collapse equal variants to one complete pair; all original notes zoom.
5. Reversing branch merge order retains the same (lexicographically greatest) variant tag.
6. Three or more equal-set variants reduce to the same single survivor regardless of insertion/merge order.
7. Triple-worker 1→2→4: zero `.summem/` conflicts; next mutation heals to one internally consistent pack; all four notes remain zoomable.
8. Distinct chronological positions keep inherited sequence-prefix order; variants of one logical block are adjacent and ordered only by variant tag.
9. Splitting and re-emitting a nested new-format nap reconstructs byte-identical paths; repeat is idempotent.
10. Unmigrated four-part stems are not view nodes (wake/zoom/recall do not see them). Rematerialized children still use five-part stems. `migrate.py` rewrites complete four-part pairs.
11. Strict-subset, partial-overlap, odd-arity, and crash-recovery zipper tests remain green.
12. After merge, heal, commit, and squash, a fresh clone can zoom every original note from the surviving tree.
13. After the merge scenario, no conflict markers and no `.tree`/`.summ` cross-variant mismatch.
14. `tox` passes on py311–py314.
15. The migration script rewrites a legacy four-part store to five-part stems that the new driver accepts.
