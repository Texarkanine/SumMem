# Active Context

## Current Task: recall-zoom-prefix
**Phase:** BUILD - COMPLETE

## What Was Done
- `unique_prefixes` builds one table via sort plus neighbor LCP. `short_id` is a lookup. `format_wake_line` accepts a prefix `dict` for O(1) lines.
- `_index_tree` / `_view_packs` parse each view `.tree` once. `named_ids`, `recall_text`, and `zoom_text` share that walk.
- Dropped `_collect_ids`, `_recall_nested`, and `_find_in_tree`. Left `_projected_child` for wake expand. Left wake/fold `short_id` list call sites.
- Atlas Zoom and recall section updated. Catalog, heal, and dataclass definitions untouched.

## Files modified
- `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem/summem`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem/tests/test_wake.py`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem/tests/test_recall.py`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem/tests/test_zoom.py`
- `/home/mobaxterm/.cursor/worktrees/summem-issue-50/SumMem/docs/architecture/index.md`

## Key decisions
- Prefix map is a `dict` passed into `format_wake_line`; a list still calls `short_id`.
- `_view_packs` records `ok` / `missing` / `unreadable` only. Commands decide warn vs raise.
- No process-global parse cache.

## Deviations from Plan
- None that change the contract. `_collect_ids` was removed in the shared-walk unit once `named_ids` no longer called it, rather than waiting for the zoom unit.

## Next Step
- QA review of the build.
