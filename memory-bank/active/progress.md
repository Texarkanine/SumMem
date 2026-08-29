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

## 2026-08-29 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan in `tasks.md`: seven testable prompt-contract behaviors, two implementation units (executable prompt contract, prose briefing), leftover-pin list for `test_init.py`.
* Decisions made
    - One executable unit covering tests + three prompt functions + lockstep prefix. Briefing is a separate prose/policy step. No new test file. No shared membership constant.
* Insights
    - `test_scopes.py` equality against `how_to_text()` will follow the new Usage body without pin surgery. The leftover-pin risk is `test_init.py` only.

## 2026-08-29 - PREFLIGHT - COMPLETE

* Work completed
    - Preflight subagent ([Preflight](ba942c51-2601-4879-9c11-e3dc302587b3)): PASS WITH ADVISORY. No plan edits. Traced every consumer of the three prompt functions; `test_scopes.py` and `test_path_walkup_and_catalog.py` need no pin surgery.
* Decisions made
    - Build as written. Apply advisories in-step (not as plan edits): name the `how_to_text()` `git` forbid; drop intro `{AGENT_BIN}`; while briefing files are open, add sovereignty to the activation definition and a productContext use case, and restate the skip rule without the Usage token. Do not adopt invisible write-rule delimiters.
* Insights
    - Writer-only moving into Usage is live against `"git" not in how_to`. Keep "untracked"; do not say "git".
    - The atlas definition of activation and productContext's use cases go stale on the sovereignty fact; expand the scheduled briefing while those files are open.

## 2026-08-29 - BUILD - COMPLETE

* Work completed
    - Prompt contract split shipped: write rule in `prompt_text` / `AGENTS.md`, recipes in `how_to_text`, editable-template recipe in `init_text`. Disjointness test in `tests/test_init.py`. Briefing updated. `tox -e py311`: 371 passed.
* Decisions made
    - Intro sentence keeps "shared memory" and drops "invoked as `{AGENT_BIN}`". Register Memories is not `(mandatory)`. Writer-only uses "untracked", not "git".
    - Applied preflight briefing advisories in-step. No write-rule delimiters.
* Insights
    - Red was 5 tests: init recipe, prefix genre pins, writer-only missing from Usage, and disjointness on membership still in how-to. Lockstep stayed green until `prompt_text()` moved, then both moved together.
