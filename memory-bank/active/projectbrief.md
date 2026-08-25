# Project Brief

## User Story

As an agent waking a repository, I want the wake document to include every current view node so that the oldest packed history stays visible even when the view is over `WAKE_LINES`.

## Use-Case(s)

### Over-budget wake after a messy merge

A merge (or leftover overlapping packs) leaves more view nodes than `WAKE_LINES`. Wake still prints the full view, oldest first. The next `note` heals and/or asks for folds until the count is back in spec.

### Bounded wake when at or under budget

At or under budget, wake is unchanged: list the view, and expand the newest nap in memory only while the printed frontier is shorter than `WAKE_LINES`.

## Requirements

1. Wake never drops oldest view lines when the store is over `WAKE_LINES`.
2. The printed document is the full current view (decaying captions are “back to the beginning”).
3. Over-budget is allowed; `note`/`nap` remain the path that returns the count to spec.
4. Work lands on a feature branch.

## Constraints

1. Do not change how fold requests are chosen or when they print.
2. Do not make wake heal or demand a nap.
3. Under-budget in-memory expand stays as it is.

## Acceptance Criteria

1. An over-budget store’s wake includes the oldest view node, not only the newest `WAKE_LINES` rows.
2. Wake still does not print a fold request.
3. `note` on an over-budget store still prints the fold request that brings the view back toward spec.
