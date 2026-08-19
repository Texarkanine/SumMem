---
task_id: single-store
date: 2026-08-18
complexity_level: 3
---

# Reflection: single-store

## Summary

Single-store memory landed on `.summem/summem`: binary `nap`, pair-aware wait-free `wake`, `zoom`, `recall`, and a fold request (not an auto-nap). Proofs 2–6 hold. 79 tests. QA failed once on duplicate-content ids and an obsolete CLI row, then passed.

## Requirements vs Outcome

The brief's Phase 2 bar is met: two-id `nap`, nap-of-naps, mixed wake that degrades a missing or conflict-marked caption without opening `.tree`, zoom after squash from a clone, recall of view and nested originals, proofs 2–6. Out of milestone as planned: `start`, `--path`, cover, config parsing. Sequential catch-up (keep requesting the oldest pair until the view fits) was named and omitted; over-budget `note` prints one pair. Nested `zoom` of ids no longer on disk was not a separate plan unit but is required for proofs 4 and 6 after unlink.

## Plan Accuracy

The replan after the first preflight FAIL was the plan that got built: proof-first slices, binary `nap`, 40/30/30 packs, pair-aware missing `.sum`, `leaves` in the filename. Slice order held. Unit 5 named the naps table and the missing-caption sentence and did not name the agent-interface table, so `nap <id> "…"` survived the first build. Duplicate-content notes were not in the plan; ingest already made two identical texts two paths and one id.

## Creative Phase Review

No creative phase. `VISION.md` was the architecture. That held. The holes that remained were implementer pins and one identity/multiplicity gap, not option studies.

## Build & QA Observations

Proof-first slices kept production behind tests. Proof 4's 100 commits plus 97 in-process folds is slow (~25s) but honest. First QA (gpt-5.6-sol-high) caught a real blocker: `write_nap` keyed a dict by id, so two adjacent `hello` notes could not be napped. Second QA (gemini-3.1-pro) passed the multiplicity fix and the CLI table edit.

## Cross-Phase Analysis

The first preflight FAIL prevented building a three-id nap and a proof 4 that folded to one nap plus two notes. The second preflight's vacuous-rejection finding is why `nap --help` exists. Unit 5's narrow doc list is why QA had to send the CLI table back. The duplicate-id bug is a Phase 1 identity contract meeting a Phase 2 lookup that assumed ids were unique in the view; the plan never stated that assumption, so QA found it rather than preflight.

## Insights

### Technical
- A content id names leaves, not a unique view row. Do not index the view with a dict keyed by id.
- Do not put seven chevrons in the driver source: `ensure_store` copies that file into the store, and proof 1 scans every store file for conflict markers.
- Short tokens (`a1`, `b1`) appear inside hex ids; assert field suffixes, not substrings.

### Process
- A surgical docs unit that lists specific sentences will miss the CLI table sitting next to them. If the interface changed, name the interface table.
- Preflight on the plan and QA on the tree catch different classes of error; the duplicate-id hole was not visible in the plan text.
