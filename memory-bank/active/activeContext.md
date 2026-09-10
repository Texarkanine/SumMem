# Active Context

## Current Task: windows-compat
**Phase:** PREFLIGHT - COMPLETE (FAIL (fixable))

## What Was Done
- Level 2 plan: CRLF `store_bytes` on reads; capability lock (directory flock else runtime-dir file); `agent_invoke()` + init warning above `---`; shebang bit gated; notes/atlas/memory-bank prose. No new deps. Symlink punt.

## Next Step
- Revise the plan to encode and test the `msvcrt` runtime-file locking branch before build.
