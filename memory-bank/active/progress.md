# Progress

Stop wake from dropping oldest view nodes when the listing is over `WAKE_LINES`. Over-budget prints stay complete; `note`/`nap` fold the count back to spec.

**Complexity:** Level 1

## 2026-08-25 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator approved
    - Classified Level 1 (single-component bug in `expand_frontier`)
    - Wrote ephemeral brief, context, tasks stub, and this file
* Decisions made
    - Level 1: remove the newest-N slice; do not redesign fold or expand-under-budget
    - Work on a feature branch off `origin/main`
* Insights
    - The atlas already says an at-or-over-budget wake lists view nodes and does not zipper. The cut is `nodes[-budget:]` in `expand_frontier`, pinned by `test_wake_prints_at_most_wake_lines_newest`.

## 2026-08-25 - BUILD - COMPLETE

* Work completed
    - Removed both newest-N slices in `expand_frontier`
    - Inverted the newest-four wake oracle; added oldest-pack keep; retargeted recall and 8-2-1 zipper tests
    - Surgical atlas / product / patterns updates
* Decisions made
    - `WAKE_LINES` stays a fold budget and an expand-when-short target, not a print cap
    - Expand overshoot (if a nap ever splits by more than +1) stays visible rather than re-slicing
* Insights
    - A second `frontier[-budget:]` after expand would have kept cutting even after the first slice was gone
    - The 8-2-1 zipper case already documented “lists three files at budget 2”; the test had drifted to a cap

## 2026-08-25 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the `expand_frontier` change, the four retargeted test oracles, and the atlas / patterns / product edits against the brief
    - Full suite on `.tox/py311`: 313 passed
    - Live check: `./summem wake` prints 34 view lines at `WAKE_LINES=32`, oldest `x32` pack included
    - Swept `README.md`, `how_to_text`, `prompt_text`, `usage_text`, and `docs/` for other statements of the removed cap
* Decisions made
    - FAIL on two findings: the stale wake-budget definition at `docs/architecture/index.md:75`, and three untracked script-written store files
    - The code change itself passes: both slices gone, nothing added, and the post-expand slice was unreachable dead code rather than live behavior
    - `budget <= 0` returning `[]` stays an advisory - pre-existing, degenerate config, out of this task's scope
* Insights
    - The build fixed the atlas's behavior paragraph (line 169) but not the setting's definition (line 75), so the atlas contradicted itself on the very setting under change
    - The untracked `x2 55a93401` pair is not just hygiene: its child notes were deleted on `main` and the pack never landed there, so at HEAD those two sentences live in no file at all. Committing the pair on this branch repairs a pre-existing loss

## 2026-08-25 - BUILD - COMPLETE (QA rework)

* Work completed
    - Rewrote the wake-budget definition at `docs/architecture/index.md` (settings paragraph): fold trigger + expand-when-short, not a print cap
    - Checked the QA integrity finding against HEAD: both AGPL sentences already live in the committed 32-pack (nested `55a93401` node). The untracked pair is a leftover subset nap from local `main`, not a missing payload
    - The untracked Parallel-naps note is an earlier wording of the `#59` sentence already on HEAD (`65041798`)
    - Parked the three leftover store files in `stash@{0}` so this branch does not add an overlapping pack
* Decisions made
    - Do not commit the leftover `55a93401` pair on this branch: it would overlap the 32-pack and is the zipper's job to drop
    - Do not commit the Parallel-naps note here: redundant with HEAD, not this task's output
* Insights
    - QA saw the live wake print `x2 55a93401` because those untracked files were in the worktree, not because HEAD lacked the sentences

## 2026-08-25 - BUILD - COMPLETE (QA rework 2)

* Work completed
    - Added `test_wake_zero_budget_prints_every_view_node` (red: empty listing)
    - Removed `expand_frontier`'s `budget <= 0 → []` early return so a zero/negative budget still lists every view node and does not expand
* Decisions made
    - Keep accepting non-positive `WAKE_LINES` rather than reject it: over-budget means print all, never cut
* Insights
    - The first QA called this advisory; the second correctly treated an empty document as a cut

## 2026-08-25 - QA - COMPLETE (FAIL, re-review)

* Work completed
    - Re-reviewed the implementation, tests, documentation, clean worktree, and parked store leftovers against the brief
    - Ran the full suite: 313 tests passed on each of py311, py312, py313, and py314
    - Probed the accepted `WAKE_LINES = 0` configuration; a non-empty wake returned an empty document
* Decisions made
    - PASS the two first-QA rework items: the settings definition is consistent, and the unrelated store files are outside the worktree
    - FAIL on the non-positive budget path: Build must rerun before acceptance
* Insights
    - `knobs` accepts zero and negative integer budgets, while `expand_frontier` returns `[]` for `budget <= 0`
    - That pre-existing branch now directly contradicts the task's unconditional full-view requirement and the new “return every view node” contract
