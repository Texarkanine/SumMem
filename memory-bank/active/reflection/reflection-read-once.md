---
task_id: read-once
date: 2026-10-31
complexity_level: 2
---

# Reflection: read-once

## Summary

Reworked PR #95 so that `note` and `nap` each read and digest every nap children file at most once. Heal, the fold scan, and `nap` share `_as_child`'s parse through a cache that lives only while the store lock is held. It worked:
- At 4094 leaves, `.tree` reads went from 22 to 11 for `note` and from 34 to 12 for `nap`.
- In-process `nap` time is roughly halved.
- `summem` is 8 lines shorter than at dd16eac.

## Requirements vs Outcome

Every requirement was met:
- The baseline was measured first.
- The change is smaller than before (net −8 lines) and adds no dependency or import.
- There is one parse, so #88's refusal parity holds by construction.
- Behavior is unchanged, and py311–py314 all pass.
- The operator's norm is recorded as a SumMem note.

Two additions came out of review:
- A superseding SumMem note says heal no longer walks raw JSON, reversing #51.
- The operator norm was added to `productContext.md`, and the cache-write coupling to `systemPatterns.md`.

## Plan Accuracy

The design came from a prototype run against the full suite before planning. Ten failures showed that a process-wide cache is unusable: tests edit store files in place between direct calls. That moved the cache scope to the lock window. The plan's premise that "a path names fixed bytes under the lock" was wrong. Heal can write a missing `.summ` or repair a `.tree` during the command, which preflight caught. The fix was to never cache captions and to have `_replace_bytes` drop what it writes.

## Build & QA Observations

The build went to plan, and both read-count tests were red for the right reason (3 reads per file). QA run 1 failed on memory, not code. SumMem still said "heal raw JSON", and a future agent could reintroduce the second parser for speed. QA also flagged that the tests pinned the number of files read rather than "at most once". Both were fixed in one small rework.

## Insights

### Technical

- In this driver, "content-addressed path ⇒ fixed bytes" holds across commands but not inside one. Heal rematerializes a missing half of a pair. A per-command cache must be invalidated at the single writer (`_replace_bytes`), not justified by content addressing.
- The repo's tests treat the module as a library and edit store files between direct calls. Any memoization must be scoped to a CLI-command window, or tests go stale even though production processes are one command each.

### Process

- On this WSL machine, subprocess timing drifts by tens of ms between back-to-back blocks. Interleave drivers round-robin and also time `main()` in-process, or a real 30–50% gain can look like noise.
- When a change reverses an earlier recorded decision (here #51's raw-JSON heal), record the superseding note in the same change. Otherwise wake keeps advertising the old design.

### Million-Dollar Question

If one-parse-per-command had been foundational, a mutating command would load the view once into memory, with each row owning its parsed children lazily. Heal and `nap` would then update that in-memory view as they write files, instead of re-listing the directory after every mutation. The re-list after mutation is the root cause of the repeated reads. The lock-scoped path cache is the smallest retrofit of that model. It gets the same read count without changing `heal_view`, `write_nap`, or `fold_request` signatures, so in today's codebase it is close to the elegant answer.
