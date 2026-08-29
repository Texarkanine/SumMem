---
task_id: heal-same-text
date: 2026-08-29
complexity_level: 3
---

# Reflection: heal-same-text

## Summary

Issue #77 is closed under the operator vote: `L` is a set of facts. Heal drops a packed-text loose note (trigger 1, the shoebox) and collapses two identical loose notes; `write_nap` rejects any digest overlap so a pack cannot claim grain 2 for one receipt. QA passed after a names-and-prose rework.

## Requirements vs Outcome

Every acceptance criterion shipped. `note_digest` stayed bytes-only; no migrate; `Saved.` stayed. Recency-by-renoting stayed out of scope. The first creative pass would have changed identity and added migrate; the operator vote discarded that. Zoom and recall tests that used to nap identical text were not in the plan; they now plant a children file so pre-change packs stay readable.

## Plan Accuracy

The four units were the right cuts: heal skip, nap overlap, fold/CLI retargets, atlas/theory. Preflight caught missing test names three times and was right to gate build. It could not catch lying names after retarget, because the plan kept citing the old names. Zoom and recall duplicate-date tests were a surprise: same writer path, not listed. `fold_request` needed no code, as the plan allowed.

## Creative Phase Review

The first pass treated `docs/theory.md` “Where the theory leaks” as spec and recommended per-file identity. That section was the bug report talking. The operator vote (`L` is a set; a sentence is one fact whenever it is noted) held through build and QA. The chosen layer — heal note/note plus nap-reject any overlap — did not need a new signature or a migrate. Recency-as-a-feature stayed out and did not leak back in.

## Build & QA Observations

Production was four lines. The cost was test retargets and prose. First QA failed because three tests still wore the old names, one docstring still denied unlink, and the theory closer was ungrammatical and had dropped `leafset_id` / `leaf_digests`. Second QA passed. Opening the draft PR before that loop was a process miss; the branch moved afterward.

## Cross-Phase Analysis

Treating the leak section as spec caused the first creative pass and a plan that would have migrated every id. The operator vote reset both. The plan then named old tests to retarget; build updated bodies and docstrings and left the names; QA’s first pass was that gap. Preflight’s “leave `test_two_identical_notes_stay` alone” correctly protected the body and accidentally protected a false docstring.

## Insights

### Technical

- `leafset_id` hashes a list and keeps repeats; `leaf_digests` is a set. Heal trusts the set. `write_nap` must refuse any intersecting digest sets or a list-hash can still mint a grain-2 pack with one fact.
- The shoebox is the spec: a loose copy of a packed sentence is thrown away. `Saved.` is true of `L`, not of the new file remaining.
- `docs/theory.md` Duplicate receipts states that clash in `L` / `leaves` / partition language. Helper names stay out of the why-page.

### Process

- A retargeted test is not done until the name matches the body. Docstrings do not show up in `-k` or failure output.
- Do not treat a “leak” or “bug” section of a why-page as the product contract until the operator has said so.
