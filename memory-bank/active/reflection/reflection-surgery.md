---
task_id: surgery
date: 2026-08-21
complexity_level: 2
---

# Reflection: surgery

## Summary

Repo-root `surgery.py` zipper-excises one raw note at the branch tip. tox 252 passed on py311–py314. QA PASS. Spec https://github.com/Texarkanine/SumMem/issues/28.

## Requirements vs Outcome

Delivered as specified: not a `summem` subcommand; break out until the named `notes/` file is loose; unlink that `NoteChild`; `heal_view` for a unique cover; no `write_nap`; no history rewrite; `--contains` / filename / `--dry-run`; operator docs for tip-then-rewrite and agent aftercare. Sibling files (`summem`, prompt, `AGENTS.md`) untouched.

## Plan Accuracy

The plan's "no `heal_view` during break-out" was the load-bearing constraint and matched `test_heal_note_covered_by_nap_dropped`. Sequence (locate → excise → CLI → docs) did not need reordering. Preflight advisories (lock is a callback, inject conftest's module for the `write_nap` monkeypatch, filename-order split) were followed, not plan rewrites.

## Build & QA Observations

TDD red/green per unit was uneventful. Full `tox` 252 on four CPythons. QA PASS with advisories only (dual dry-run/mutate walks, skipped unreadable trees, no `fold_request` print). Other Models quota blocked Gemini/GPT for preflight and QA; both ran on Grok.

## Insights

### Technical
- Calling `heal_view` while the target is a rematerialized loose note still covered by a larger overlapping pack subset-drops that note and leaves the sentence in a `.tree`. Targeted break-out must split every containing view nap first, unlink the loose file, and only then heal.

### Process
- Cursor Other Models quota was still exhausted 2026-08-21; mix-family preflight/QA was not possible. Fallback `cursor-grok-4.6-xhigh` worked.

### Million-Dollar Question

If whole-note excision had been a foundational assumption, the targeted rematerialize-to-leaf walk would still sit beside `heal_view` rather than inside it, and captions would still be agent naps. Folding that walk into the shipped CLI is a later issue; keeping it in `surgery.py` is the same design with a smaller blast radius.
