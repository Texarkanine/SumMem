---
task_id: wake-never-cut
complexity_level: 1
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: wake-never-cut

## SUMMARY

Wake was dropping oldest view nodes when the listing exceeded `WAKE_LINES`. `expand_frontier` sliced `nodes[-budget:]` and, after expand, `frontier[-budget:]`. Packed history vanished from the document even though the atlas already said an at-or-over-budget wake lists view nodes. Both slices are gone. A `WAKE_LINES = 0` early return that printed nothing is gone too. Over-budget (including 0) lists every view node, oldest first. Under-budget expand is unchanged. `note`/`nap` still fold the count back to spec.

Landed on `feat/wake-never-cut`. Draft [PR #60](https://github.com/Texarkanine/SumMem/pull/60).

## REQUIREMENTS

- Wake never drops oldest view lines when the store is over `WAKE_LINES`.
- The printed document is the full current view (decaying captions are “back to the beginning”).
- Over-budget is allowed; `note`/`nap` remain the path that returns the count to spec.
- Do not change fold-request selection or make wake heal or demand a nap.
- Under-budget in-memory expand stays as it is.
- Work on a feature branch.

## IMPLEMENTATION

`expand_frontier` now builds a frontier from every view node and expands naps only while `len(frontier) < budget`. No newest-N slice. No `budget <= 0 → []`.

Atlas settings paragraph: wake budget is the fold threshold and the expand-when-short target, not a print cap. `productContext.md` and `systemPatterns.md` state that wake does not drop nodes to fit the budget.

First QA asked to commit leftover local store files (`55a93401` nap + Parallel-naps note). Rejected: those AGPL sentences already live in the committed 32-pack (nested `55a93401`); the untracked pair is a subset leftover from local `main`. Parked in `stash@{0}` on this machine.

## TESTING

- `test_wake_over_budget_prints_every_view_node` — eleven notes at budget 4 print all eleven.
- `test_wake_over_budget_keeps_oldest_pack` — oldest pack stays when later notes overflow.
- `test_wake_zero_budget_prints_every_view_node` — committed `WAKE_LINES = 0` lists the pack and the later note, no expand.
- Retargeted `test_recall_matches_loose_note_when_over_budget` and the 8-2-1 zipper wake-count assertion (3 lines at budget 2, not 2).
- `uvx --with tox tox`: 314 passed on py311–py314 after the zero-budget fix.
- Live `./summem wake` on the dirty local tree printed 34 lines including the oldest `x32` pack (that extra count was leftover untracked files, later stashed).

QA: FAIL (stale settings definition + integrity finding) → FAIL (`WAKE_LINES = 0` empty document) → PASS.

## LESSONS LEARNED

- The atlas behavior paragraph and the settings definition can disagree. Fixing one is not enough.
- `frontier[-budget:]` after expand was dead for binary naps (loop grows by one and stops at budget) but would still cut if the first slice were removed and the start listing was already over budget.
- An empty document at `WAKE_LINES = 0` is a cut, not an advisory.
- A live wake that shows `x2 55a93401` can be untracked leftovers, not a missing payload at HEAD.

## PROCESS IMPROVEMENTS

L1 still has no archive phase. This archive exists because the operator invoked `/niko-archive` after wrap-up.

## TECHNICAL IMPROVEMENTS

None beyond the never-cut contract already recorded in the atlas and persistent memory-bank files.

## NEXT STEPS

- Merge [PR #60](https://github.com/Texarkanine/SumMem/pull/60).
- Local `stash@{0}` still holds the leftover `55a93401` pair and Parallel-naps note. Do not commit them onto this branch.
