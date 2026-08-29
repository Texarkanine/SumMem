# Progress

Split the agent write rule out of root-wake Usage and into the `init`-emitted `AGENTS.md` prefix so consuming repos can edit what they remember without forking the script, while command recipes stay versioned with the running script.

**Complexity:** Level 2

## 2026-08-29 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Standalone creative already recorded the disjoint-split decision in `memory-bank/active/creative/creative-entry-gate-split.md`.
    - `/niko` on `who-gates-entry`: intent approved; classified Level 2.
* Decisions made
    - Level 2, not Level 3: the architecture is already chosen; remaining work is prompt copy, tests, lockstep, and briefing in one subsystem.
* Insights
    - Reinforcement on wake is what makes a customized prefix fake; the plan must keep membership tokens out of `how_to_text()`.
