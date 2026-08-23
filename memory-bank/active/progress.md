# Progress

Add two AGPL carve-outs (obligation-free prompt text; full permission for AI-agent invocation, including if a reviewer would call it conveyance or §13) with the script as the authoritative source, so use is allowed and a published fork still trips AGPL.

**Complexity:** Level 3

## 2026-08-23 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated and confirmed intent (full carve-out, not interpretation-only)
    - Recorded script-as-authority and conditional LICENSE→COPYING-if-REUSE constraint
    - Classified Level 3
* Decisions made
    - Program stays AGPL; no dual-license
    - Invocation grant is permission, not only a scope claim
    - Script is the full authoritative source; repo files echo it
* Insights
    - Typical install copies only the script; a repo-only rider would not travel
    - Creative must choose REUSE/COPYING vs keeping `LICENSE`, and how to write the additional permission without turning AGPL into `LicenseRef-`

## 2026-08-23 - CREATIVE - COMPLETE

* Work completed
    - Explored legal instruments for the two carve-outs
* Decisions made
    - AGPL §7 additional permissions in the source, not an interpretation-only rider, not a dual-license, not an SPDX exception
    - Prompt: part-of-program permission plus no-copyright claim; no 0BSD/MIT on the program
    - Invocation: exception for *running* only; distributing copies of the Program stays AGPL
* Insights
    - §7 already requires the terms (or a pointer) in the relevant source files; a repo-only `LICENSING.md` would fail both the license and the script-as-authority rule
    - Recipients may strip additional permissions; the fork remains AGPL

## 2026-08-23 - CREATIVE - COMPLETE

* Work completed
    - Explored where the grant lives so a script-only install is complete
* Decisions made
    - Script-complete, no REUSE: authority is the `summem` header
    - `LICENSE` stays verbatim AGPL (detector-safe)
    - README License section is a short premise + pointer
    - `surgery.py` echoes the invocation permission only
    - `version` unchanged; no grant text in the paste prompt
* Insights
    - REUSE is for mixed licenses; Q1 refused a second license on the program
    - A `LICENSE` preamble can break GitHub detection; COPYING was tied to the REUSE branch we are not taking

## 2026-08-23 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 3 plan: four prose/policy units, no new executable behavior
* Decisions made
    - No tests for header/README/license wording
    - Build copies §7 draft terms from the legal-instruments creative doc
* Insights
    - Existing `test_init.py` lockstep is a safety net against accidentally editing the paste, not a license test

## 2026-08-23 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated the four prose/policy units against current headers, README License section, lockstep tests, and the two creative drafts
    - Wrote `memory-bank/active/.preflight-status` with first line `PASS WITH ADVISORY`
* Decisions made
    - Plan is acceptable as-is; no TDD step swap and no change-detector strike
* Insights
    - Comment insertion after the FSF short notice does not touch the shebang test or version machinery
    - The `init` “paste” substring check is a tripwire if Build accidentally puts grant text in the prompt

## 2026-08-23 - BUILD - COMPLETE

* Work completed
    - Drafted §7 Invocation + 0BSD Prompt template in `summem`; echoed Invocation on `surgery.py`; README License points at the script
    - Operator iterated wording (AGPL-first, org vs network, no “must retain”, drop unmodified-source paragraph, keep outside-org override)
    - Operator: likes current header as-is after further manual revision; do not reopen wording
    - Four planned units landed; `LICENSE` and paste files untouched
    - Full suite: 262 pytest via `uvx --with tox tox` on py311–py314
* Decisions made
    - 0BSD on the prompt, not a dual-license of the Program
    - §1 + covered-work never revoked; only the §13 paragraph is withdrawn for outside-org modified availability
    - “Agent acting for your organization” covers autonomous internal invoke; common-control is affiliates only
    - Preflight capsule-before-AGPL advisory not applied (operator chose AGPL-first)
* Insights
    - §13’s own “users / remotely / network” words catch employees on a VPN; the live cut is organizational
    - A conveyor may strip additional permissions; a stripped fork is still AGPL, not more permissive

## 2026-08-23 - QA - COMPLETE (PASS)

* Work completed
    - Semantic review of the four prose/policy units against the plan, creative docs, and operator-settled header
    - Wrote `memory-bank/active/.qa-validation-status` (`PASS`)
* Decisions made
    - Accept the live header as-is; wording divergence from the Creative draft is operator-approved, not a rebuild
    - Advisories only: missing literal “even if” / “not conveyance” sentences; README restates two header conclusions
* Insights
    - §7 additional permissions plus the §1 / covered-work paragraph are the “even if” instrument; the brief’s extra sentence is not load-bearing once the operator locked the three-paragraph form
    - Paragraph 3 withdraws only the §13 paragraph, so unmodified customer-facing invoke stays carved out and a modified version offered outside the org does not
