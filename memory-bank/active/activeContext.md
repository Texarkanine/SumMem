# Active Context

- **Current Task:** read-once (PR #95 rework: one `.tree` read per command)
- **Phase:** REFLECT - COMPLETE

## Files Modified

- `/home/mobaxterm/worktrees/Texarkanine/SumMem/SumMem-feat/fold-grain-as-child/summem`:
    - Added `_CHILDREN`.
    - `with_store_lock` turns the cache on and off in `try` and `finally`, and its docstring states why.
    - `_replace_bytes` forgets each path it writes.
    - `_as_child` caches `(Tree, digests)` or `None`, keyed on `tree_path`, and builds `NapChild` from the current node.
    - `leaf_digests` reads through `_as_child`.
    - Deleted `_digests_of_dict`.
    - Net −8 lines from dd16eac (+36 −44).
- `/home/mobaxterm/worktrees/Texarkanine/SumMem/SumMem-feat/fold-grain-as-child/tests/test_zipper.py`:
    - Added `test_cli_note_reads_each_children_file_once` and `test_cli_nap_reads_each_children_file_once`, with helpers `_over_budget_naps` and `_count_tree_reads`.
    - Deleted `test_leaf_digests_nap_does_not_build_tree`.
- `/home/mobaxterm/worktrees/Texarkanine/SumMem/SumMem-feat/fold-grain-as-child/docs/architecture/index.md`: added one sentence in the Zipper lock paragraph.
- `.summem/`:
    - Two notes: the operator norm, and the cache-scope gotcha.
    - Two naps the driver requested; the Windows rows are compressed.

## Decisions During Build

- Docstring reason follows preflight run 2 advisory 1: only this process writes under the lock, and `_replace_bytes` forgets each write. It does not claim "fixed bytes".
- The nap test takes its pair from a `fold_request` `Run:` line (preflight run 2 advisory 2).
- Write-through cache (run 2 advisory 3) declined: it adds lines, and the benchmark has no heal split. Reading a file just written is still that path's first read.

## Deviations

- None from the amended plan.

## Next Step

- Operator: ponytail review and push; then `/niko-archive`.
