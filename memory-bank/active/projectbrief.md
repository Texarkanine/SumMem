# Project Brief

## User Story

As an agent using SumMem, I want `recall` and `zoom` to unique-prefix in linear time and parse each view `.tree` at most once per command, so a common-word search on a several-thousand-leaf store finishes in well under a second instead of tens of seconds.

Intent is [issue #50](https://github.com/Texarkanine/SumMem/issues/50). The issue body is the approved specification.

## Use-Case(s)

### Use-Case 1

An agent runs `recall` of a common word against a large store. Prefixes for every printed pack line come from one table built once (sort plus longest common prefix with neighbors). Each printed line is O(1).

### Use-Case 2

An agent runs `zoom` of a nested id. Each view `.tree` is parsed at most once. That pass yields nested ids, captions, leaf counts, and stamps. `named_ids` shares the pass instead of being a second full walk.

### Use-Case 3

An unreadable sibling pack still prints `skipped a pack` and does not fail the command if another pack answered. Wake listing and fold-request formatting may keep today's `short_id` and must not regress.

## Requirements

1. Compute unique prefixes once per command (sort plus longest common prefix with neighbors). Each printed line is O(1).
2. Parse each view `.tree` at most once per command. One walk yields nested ids, captions, leaf counts, and stamps together.
3. `named_ids` shares that walk with recall/zoom instead of being a second full walk.
4. Prefix uniqueness stays among distinct ids, not view-row count. A repeated id is still that one prefix.
5. Recall still matches note text and nap captions, not grain, day, or id prefix.
6. Zoom still walks children from the tree, not stdout tokens.
7. Unreadable sibling packs still print `skipped a pack` and do not fail if another pack answered.
8. Wake listing and fold-request formatting may keep today's `short_id` if they stay cheap; do not regress their output.

## Constraints

1. Stay in lane: `short_id` / a prefix table, `named_ids`, `recall_text`, `_recall_nested`, `zoom_text`, `_find_in_tree`, `_projected_child`, `_collect_ids`, and tests/atlas for those commands.
2. Do not change catalog (`catalog_text` / `_ignored_store`), heal (`heal_view` / `leaf_digests` / `_first_overlap`), dataclass definitions, skip-heal markers, or how `note`/`nap` call `heal_view`.
3. Proof walkers must keep enqueueing nap ids from `Tree.kids`, not zoom stdout.
4. No new dependencies.

## Acceptance Criteria

1. `recall` of a common word on a several-thousand-leaf store finishes in well under a second on this class of machine, not tens of seconds.
2. `zoom` of a nested id does not re-parse every pack to build `named_ids` and then parse them again to find the target.
3. Unique prefixes remain unique among distinct ids; a repeated id is still that one prefix.
4. Unreadable sibling packs still print `skipped a pack` and do not fail if another pack answered.
5. Wake listing and fold-request formatting do not regress.
