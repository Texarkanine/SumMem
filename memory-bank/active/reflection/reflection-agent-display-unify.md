---
task_id: agent-display-unify
date: 2026-08-24
complexity_level: 2
---

# Reflection: agent-display-unify

## Summary

Recall and zoom now print the same `format_wake_line` grammar as wake. Recall matches sentences, not formatted fields. Proof walkers enqueue `NapChild` ids from the children tree. The Register Memories clause is clone-portability, not eternal currency. QA PASS.

## Requirements vs Outcome

Delivered as specified. No requirements dropped. Preflight FAIL (fixable) added walker retarget and leftover `{id}  text` tests to the plan; that was missing scope, not a new product requirement. QA advisories (`zoom_reaches` has no dedicated wake-grammar unit test; prompt still says `<hash>`; test-local tree helpers duplicate gitutil) were left as follow-ups.

## Plan Accuracy

The first plan missed that `reaches` / `zoom_reaches` treat `line.split()[0]` as a content id, and that zoom/nap success tests still asserted `{id}  text`. Re-plan put walkers first and retargeted those tests. After that, file list and sequence were right. The surprise was not the printer — it was stdout-as-id in test infra.

## Build & QA Observations

Build was the known change plus the walker fix. Uncommitted product files were restored to HEAD more than once while plan/preflight overlapped; the green slice only stuck after a commit. QA PASS with advisories; no rework. First QA spawn on gpt-5.6 hit Other Models quota and had to be retried on grok.

## Insights

### Technical
- When agent stdout grammar changes, any helper that takes `line.split()[0]` as an id will enqueue grain (`x1` / `xN`). Walk `Tree.kids` for nested pack ids; use zoom stdout only as the sentence check.
- Wake-listing already used `format_wake_line`; zoom/recall still had `_zoom_note_line` / `{id}  text`. One printer is the invariant. Match haystack (caption/text) stays separate from print.

### Process
- Overlapping Niko phases in one workspace restored uncommitted product files to HEAD. Stage and commit as soon as a slice is green; do not leave the implementation sitting unstaged across a preflight spawn.
- Other Models quota was already spent; niko-qa/preflight on gpt fails immediately. Use a Cursor-native model until that quota recovers.

### Million-Dollar Question

If wake-listing had been the listing from the start, `_zoom_note_line` never existed: one `format_wake_line` for wake, recall hits, and zoom children; walkers never parsed stdout. That is what this task built. Not a redesign.
