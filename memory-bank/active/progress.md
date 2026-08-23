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
