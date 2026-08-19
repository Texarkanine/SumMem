---
task_id: wake-listing
complexity_level: 2
date: 2026-08-19
status: completed
---

# TASK ARCHIVE: wake-listing

## SUMMARY

Wake is a recency budget, not a dump of 64-hex ids. `wake` prints at most `WAKE_LINES` dated lines. `note` and `nap` print an OptMem-style `Run:` prompt with unique prefixes when the view is still over budget. SHA-256 stays on disk and in `.tree` identity.

## REQUIREMENTS

- `wake` ≤ `WAKE_LINES` lines; never a nap request; over budget: newest files, no `.tree` open.
- Note line `YYYY-MM-DD: text`. Pack line `YYYY-MM-DD xN <prefix>: caption` (`xN` only when leaves > 1).
- Prefix: 8 hex, or shortest unique longer prefix among **distinct** content ids. Ambiguous prefix is an error.
- `note`/`nap` over budget: child bodies, invent-nothing, `Run: .summem/summem nap <p> <p> "<your line>"`.
- Stored hashes stay 64 hex. No positional ranges.
- Proofs 1–8 still hold with the new line format.

## IMPLEMENTATION

`.summem/summem`: `short_id` / `resolve_id` (uniqueness via `dict.fromkeys`), `format_wake_line`, `expand_frontier` slices newest when at/over budget, `fold_request` is the prompt string. `nap`/`zoom` resolve prefixes among view ids (zoom also nested tree ids). Identical adjacent notes share an id; `write_nap` already folded that pair; prefixes now treat it as one identity.

`VISION.md` and `systemPatterns.md` updated to dated lines and prefix-among-distinct-ids.

## TESTING

pytest via `uv run --python 3.11 --with pytest pytest`: 173 passed after the twin-id re-run (169 before the three regressions). First `/niko-qa` failed: two identical notes produced 64-hex prompt ids that `resolve_id` then rejected. Second QA passed. Proofs inverted off the old `64hex (N notes, from …)` strings.

## LESSONS LEARNED

A content id names leaves, not a view row. Prefix uniqueness is the set of ids, not the list of rows. The plan’s “two matches is an error” meant two *distinct* ids; applying it to duplicate rows made twins un-nappable. Tests that assert `short_id()`’s own output hide this; assert length 8 on a duplicated id list.

## PROCESS IMPROVEMENTS

CLI round-trip for identical notes belongs in the first test plan for any prefix resolver, not only as a QA find.

## TECHNICAL IMPROVEMENTS

No further shape. Treat the namable set as a set of ids from the first unit — that is what the re-run built.

## NEXT STEPS

None for this task. Related later work (not part of this archive): GitHub issue #4 (drop unused `.tree` `v` field); live-store trial after compressions finish; aligned `cover(T)` remains Later.
