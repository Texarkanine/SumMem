# Active Context

- **Current Task:** read-once (PR #95 rework: one `.tree` read per command)
- **Phase:** PREFLIGHT - COMPLETE (FAIL (fixable))

## What Was Done

- Level 2 plan written to `tasks.md`, with measurements: dd16eac reads each `.tree` twice per `note` and about three times per `nap`. A path cache halves reads and digests (in-process `note` 63 → 42 ms, `nap` 97 → 42 ms at 4094 leaves).
- Design: `_as_child` caches parses only while `with_store_lock` holds the lock. Heal's `leaf_digests` goes through `_as_child`, and `_digests_of_dict` is deleted. Expected net `summem` delta is about −11 lines.

## Next Step

- Preflight (subagent), then build.
