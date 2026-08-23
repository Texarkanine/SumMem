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
