---
task_id: agpl-carve-outs
date: 2026-08-23
complexity_level: 3
---

# Reflection: agpl-carve-outs

## Summary

The program stays AGPL. The `summem` header is the authoritative grant: §7 additional permissions for invocation, and 0BSD terms for the agent prompt template. `surgery.py` echoes invocation only. `LICENSE` is untouched. Operator-settled wording survived QA as-is.

## Requirements vs Outcome

Delivered. A script-only reader sees AGPL, the invocation permission, and 0BSD prompt terms. The paste files carry no license notice. Publishing a modified version outside the organization still trips AGPL. Two brief sentences did not land as written: “even if” / “not conveyance.” QA treated those as non-blocking because the operator locked a three-paragraph form whose §1 / covered-work paragraph is the same instrument. Requirement 6 (REUSE → `COPYING`) stayed unused.

## Plan Accuracy

The four-unit file list and the “no tests / no change-detectors” call were right. The plan’s “copy Creative draft terms” step was the wrong build instruction for license prose: the operator rewrote the grant after preflight (AGPL-first, org vs network, drop “must retain” and the unmodified-source paragraph, keep the outside-org override). File targets did not move. The identified challenges (grant drift, accidental paste, editing `LICENSE`) were the real ones; the surprise was how much of the draft the operator replaced.

## Creative Phase Review

**Legal instruments:** §7 additional permissions held. Dual-license and SPDX `WITH` stayed out. The prompt instrument changed after Creative: the draft was a part-of-program no-copyright claim; the operator chose 0BSD in the header. That is a separately licensed template, not a dual-license of the Program.

**Authority and echoes:** Script-complete, no REUSE held. Verbatim `LICENSE`, README pointer, `surgery.py` invocation echo, and no grant text in the paste all held. The preflight capsule-before-AGPL advisory did not: the operator kept the FSF short notice first.

## Build & QA Observations

Build was comment and docs only. The hard part was legal wording, not code. The operator iterated the header after the first draft; a later session confirmed the text as-is. Full suite stayed green (262 pytest, py311–py314), including `test_init` lockstep. QA passed with two advisories: Creative-vs-live wording, and README restating two header conclusions. Nothing required a rebuild.

## Cross-Phase Analysis

Creative produced a one-paragraph “even if” draft. The plan told Build to copy it. Preflight accepted that plan and advised header *order*, not grant shape. The operator then changed grant shape. QA correctly judged the live header against the brief and the operator lock, not against Creative verbatim. The causal chain is: treating license prose as a Creative artifact to copy, rather than as a draft the copyright holder will replace. Preflight’s `paste` substring advisory was useful and unused — the paste was never edited.

## Insights

### Technical
- The live §13 cut is organizational, not network-shaped: §13’s own “users / remotely / network” words would catch employees on a VPN, so paragraph 3 keys on “available outside your organization.”
- §7 plus a §1 / covered-work paragraph is the “even if” instrument. The brief’s extra sentence is not load-bearing once that paragraph exists.
- Verbatim root `LICENSE` plus a complete script header is how a typical-install grant stays self-contained without breaking GitHub / SCA AGPL detection.

### Process
- For license L3s, Creative draft terms are a starting copy. The operator-settled header is the artifact. Plan steps that say “copy the Creative paragraph” will disagree with QA unless the plan is updated after the lock.
- Preflight advisories about skimmability (capsule first) are optional. Do not apply them over an AGPL-first operator choice.
