# Active Context

## Current Task: fold-scan-rows
**Phase:** BUILD - COMPLETE

## What Was Done

- `_fold_grains` keeps a note at `node.leaves` and does not open the note file.
- `_digests_of_tree` raises `ValueError("unreadable pack")` when a note's text is not a string. The scan's existing `except ValueError` sets grain 0.
- py311: 425 passed, including the two new fold tests.

## Next Step

- Level 1 QA in a subagent.
