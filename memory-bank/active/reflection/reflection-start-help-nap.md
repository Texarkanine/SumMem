---
task_id: start-help-nap
date: 2026-11-07
complexity_level: 2
---

# Reflection: start, help, and nap replies

## Summary

`start`, `help`, and `nap` now answer in the short lines the operator asked for. The py311 suite passed (441), and QA passed.

## Requirements vs Outcome

All ten requirements shipped. One start sentence covers a new store and an existing one. A missing path is refused and nothing is created. `help` is the existing `-h` text, including `help <command>`. Bare `summem` stays stderr and exit 2. An already-folded pair prints `Saved.` and writes nothing. Other nap misses are `not a fold row` or `unknown id`, with no wake hint. Zoom still names wake.

`help` was added to the command lists in `systemPatterns.md` and `techContext.md`. No `_child_id` helper. QA's advisory is still open: `docs/user-guide/commands.md` says `init`, `version`, and `-h` work outside a repository, and does not name `help`.

## Plan Accuracy

The sequence held. Preflight caught three plan errors before build: subprocess `start` calls the plan had not listed, a note id described as the raw digest, and a known-id set that omitted view rows. During build, a mechanical insert then skipped five `start` sites whose previous line already mentioned `repo`.

## Build & QA Observations

Each slice went red, then green: start, help, then nap. QA passed with the one documentation advisory above. It was left as written.

## Insights

### Technical

- A note id on wake is `leafset_id` of that note's digest, 16 hex. The raw digest matches nothing in the view.
- An already-folded nap is that nap's two direct children. Two ids nested under it, but not that pair, are `not a fold row`.

### Process

- When a command's contract changes, the plan has to name every caller, including subprocess tests outside the unit file the new tests live in.

### Million-Dollar Question

The small shape is the one that fits. `help` is the `-h` catalog, `start` says a store is there and will not create a path, and a nap that already exists is the same `Saved.` as a note. A new id helper would not have been clearer. The projection already returns the id wake prints.
