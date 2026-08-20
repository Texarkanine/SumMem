# Project Brief

## User Story

As the Niko operator, I want two parallel worktree agents to close the open SumMem issues so each slice lands as its own draft PR without colliding on `main`.

## Use-Case(s)

### Use-Case 1

A product worker implements recall of nested nap captions (#8) and stderr warnings when zoom/recall skip an unreadable sibling pack (#7).

### Use-Case 2

An infra worker adds a tox matrix for non-EOL Pythons from the 3.11 floor (#6) and a reliable one-command pytest runner (#9), using an off-the-shelf test cache only if it is solid.

## Requirements

1. Workers start from `185c686` (docs-sunset #11). `VISION.md` and `ROADMAP.md` are gone; do not recreate them.
2. Each worker runs `/niko` and `/worktree` on its own branch, uses OptMem (`memo`), and opens a draft PR after reflect (or L1 end).
3. Product order: #8 then #7. Infra order: #6 then #9.
4. Python floor is 3.11 through current non-EOL (3.14 as of 2026-08-19). Not 3.10.
5. Test-result cache: choose a maintained off-the-shelf tool if it is reliable for this suite; otherwise skip. Do not build a cache library.
6. Parent decides remaining forks; workers stop only for a real un-decided fork.

## Constraints

1. Do not implement on `main`. Detached worktrees must get a named branch before commits.
2. Agent-facing CLI still omits store paths, hashes-as-paths, and git. Wake stays wait-free (no sibling-pack warning on wake).
3. `ensure_store` does not place the driver. Repo-root `summem` is the record.
4. Do not sunset leftover notes in `docs/notes.md`. Do not expand into sqlite, hooks, or `cover(T)`.
5. Product does not invent the test runner. Infra does not change recall/zoom semantics.
6. Parallel PRs must not both ship `memory-bank/active/` — archive before opening the PR.

## Acceptance Criteria

1. Two draft PRs exist, each from a worktree branch, targeting `main`.
2. Product PR closes #8 and #7 with tests; recall matches nested captions; zoom/recall warn on skipped sibling packs without failing if another pack answered.
3. Infra PR closes #6 and #9: tox covers 3.11–current non-EOL; there is a documented reliable test command; cache is either a chosen off-the-shelf tool or an explicit skip.
