# Progress

Omit `== Project-root memories ==` when the root decaying document is empty.

**Complexity:** Level 1

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent from [issue #2](https://github.com/Texarkanine/SumMem/issues/2), `memo init`, and the operator’s AGENTS.md / all-agents-always correction; operator approved.
    - Classified Level 2.
* Decisions made
    - Level 2: one CLI command, one baked string, this repo’s `AGENTS.md`. Not L3 — no new activation architecture.
    - `init` prints; it does not write `AGENTS.md`.
    - Recommend `AGENTS.md` top plus thin `CLAUDE.md` pointer, not OptMem’s “AGENTS.md or CLAUDE.md.”
* Insights
    - OptMem’s useful half is bake-and-print. The halves we must not copy: “before any other tool call,” and treating CLAUDE.md as an equal paste target.

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 plan: `init` + `prompt_text()`, AGENTS.md lockstep, design-contract docs, Composer 2.5 instrument.
* Decisions made
    - `init` is help-shaped: no `--path`, works outside a repo, writes nothing.
    - Prompt heading is `## SumMem`, not OptMem’s `## Memory`.
    - Test invariants and lockstep, not a golden prompt file.
    - Composer 2.5 probes are Build verification, not pytest.
* Insights
    - Existing CLI tests encode “every command except start takes `--path`”; `init` must join `start` in those assertions in the same unit.

## 2026-08-19 - PREFLIGHT - COMPLETE (PASS)

* Work completed
    - Preflight validation of the plan completed successfully with PASS.
* Decisions made
    - Validated that the `AGENTS.md` lockstep test is a valid cross-file contract test, not a change-detector.
* Insights
    - The plan's test coverage appropriately handles all required aspects without change-detector tests.

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - `summem init` prints paste recipe + `prompt_text()`; works outside a repo; no `--path`; catalog names it.
    - `AGENTS.md` starts with the same prompt. `CLAUDE.md` still `@AGENTS.md`.
    - VISION CLI/Activation, ROADMAP Later, systemPatterns, techContext updated.
    - Composer 2.5 Probe A: ran `./summem wake` from repo root, then `wake --path dogfood` because the catalog prints a bare command. Probe B: skipped second root wake. Tightened prompt pull sentence after A.
    - 204 pytest passed.
* Decisions made
    - `init` is handled before `resolve_parent`.
    - Prompt heading `## SumMem`. Did not name `.summem/summem` even to forbid it (substring test).
    - Did not change catalog_text; that VISION miss is outside issue #2.
* Insights
    - Cheap agents treat a catalog line that is only `summem wake --path dogfood` as something to run now. The prompt now says pull when you work under that path. The catalog still prints the bare command.

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the build against the approved Level 2 plan, project brief, issue #2, and established system patterns.
    - Confirmed the CLI implementation, baked prompt, repository lockstep, documentation updates, and Composer probe results are complete and acceptable as-is.
    - Ran the full test suite: 204 passed.
* Decisions made
    - QA passed with no required build or plan changes.
    - Recorded the repo-root executable spelling as an advisory only: the prompt identifies the driver and the instrumented agent successfully inferred `./summem` when needed.
* Insights
    - The implementation remains direct: `prompt_text()` is the single prompt source, `init_text()` only adds the operator recipe, and the lockstep test prevents repository drift.

## 2026-08-19 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-agents-prompt.md`.
    - productContext: outside a repository, help and `init` still print.
* Decisions made
    - Catalog-as-command is a later VISION fix, not a reflect-time rewrite.
* Insights
    - Cheap agents run a catalog line that is only a command. Lockstep `prompt_text()` into `AGENTS.md` is the right activation shape.

## 2026-08-19 - REWORK - INITIATED

* Work completed
    - Operator requested rework after reflect: strike driver copy from `ensure_store`; align prompt, `AGENTS.md`, and docs with onboarding (place `.summem/summem`, `init`, paste).
* Decisions made
    - `ensure_store` keeps dirs + default config; it does not copy or create the driver.
    - This repo: repo-root `summem` remains the record; store drivers are symlinks.
    - Agents invoke `.summem/summem`.
* Insights
    - Issue #2 comments that forbade teaching `.summem/summem` are superseded for the invoke path.

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the rework as Level 2.
* Decisions made
    - Level 2: one function to stop copying, plus lockstep prompt/docs. Not L3 — onboarding is already specified.
* Insights
    - Tests that expect a first note to create `.summem/summem` are now wrong, not incomplete.

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Wrote Level 2 rework plan: no driver copy; prompt lockstep; VISION/memory-bank docs.
* Decisions made
    - Nested `start` does not get a driver. Agents run root `.summem/summem` and pass `--path`.
    - Catalog still says `summem`; the prompt says `.summem/summem`.
    - Fix `./summem/summem` in the operator draft to `.summem/summem`.

## 2026-08-19 - PREFLIGHT - FAIL (fixable)

* Work completed
    - Preflight found unit-2 invariant/onboarding gaps and unit-1 leftover-copy details.
* Decisions made
    - Replan. Do not parameterize `prompt_text()`.
    - Brief requirement 6 and AC 3 now say invoke `.summem/summem`.
* Insights
    - Lockstep is already red because `AGENTS.md` was edited before `prompt_text()`.

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Replanned: enumerated `test_prompt_text_invariants` edits; one invoke spelling; delete shutil/driver local; locate `test_start_creates_store_in_dir`; skip `ROADMAP.md`.
* Insights
    - “Store exists” tests that check for a `summem` file were testing the copy.

## 2026-08-19 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the Level 2 rework plan against the tree. `.preflight-status` first line: `FAIL (fixable)`.
    - TDD encoding passed; no step swap and no change-detector strike were needed.
    - Traced dependencies: `test_proof_ingest`, `test_zipper` lock probe, `usage_text` catalog tests, and the repo-root loader are all unaffected by dropping the copy.
* Decisions made
    - Two fixable blockers in unit 2: it never schedules the `"## SumMem"` invariant it breaks, and it inherits the draft’s “driver is repo-root `summem`” sentence plus a mixed invoke spelling.
    - Three low fixables in unit 1: unused `import shutil`, the stranded `driver` local, and mis-located test edits (`test_scopes.py:77` is the `start` case; `test_ensure_store_creates_naps_dir` carries the same assertion).
    - `ROADMAP.md` needs no edit — it already says `.summem/summem` — but the plan should say that instead of omitting it.
* Insights
    - The lockstep test is already red before build: `AGENTS.md` was edited to the draft while `prompt_text()` still returns the `## SumMem` version.
    - `.summem/summem` is an uncommitted typechange to a symlink and `dogfood/.summem/summem` is already a committed symlink, so “store drivers symlink to it” needs no plan unit.
    - Proof 1 only caught chevrons in the driver source because `ensure_store` copied it into the scanned store; that guard goes away with the copy.

## 2026-08-19 - PREFLIGHT - COMPLETE (FAIL (fixable))

* Work completed
    - Revalidated the revised Level 2 rework plan against the implementation, tests, documentation, and project brief.
    - Swapped unit 1's test-writing step ahead of its premature production deletion, as authorized by Preflight.
    - Wrote `.preflight-status` with first line `FAIL (fixable)`.
* Decisions made
    - Replan before Build: add a concrete Composer 2.5 (not fast) verification of the rewritten prompt.
    - All earlier path, invariant, dead-code, test-location, and `ROADMAP.md` findings are resolved.
* Insights
    - The prior Composer probe exercised the pre-rework prompt and cannot prove the revised `.summem/summem` instructions satisfy requirement 7 and acceptance criterion 5.

## 2026-08-19 - PLAN - COMPLETE

* Work completed
    - Added unit 4: Composer 2.5 probes of the rewritten prompt. Collapsed unit 1 leftover stub/code overlap.

## 2026-08-19 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Validated the Level 2 rework plan against the implementation, tests, documentation, and project brief.
    - Confirmed TDD plan encoding is acceptable.
* Decisions made
    - Found an incorrect string `./summem/summem` in the `AGENTS.md` draft instead of `.summem/summem` and recorded it as an advisory.
    - Recorded a radical innovation advisory for `ensure_store` to write `.summem/summem` as a relative symlink to the root script to completely prevent nested execution issues.
* Insights
    - Lockstep test is valid and not a change-detector; it enforces the contract between the executable and `AGENTS.md`.

## 2026-08-19 - BUILD - COMPLETE (PASS)

* Work completed
    - Unit 1: `ensure_store` no longer copies `__file__`. Dirs + default config only. `import shutil` removed. Existing driver still left alone.
    - Unit 2: `prompt_text()` / `AGENTS.md` invoke `.summem/summem`. Dropped `"## SumMem"` and `"repository root"` invariants; lockstep holds.
    - Unit 3: `VISION.md` Onboarding/Activation, `systemPatterns.md`, `techContext.md` aligned. `ROADMAP.md` already said `.summem/summem`. Archives not rewritten.
    - Unit 4: Composer 2.5 Probe A ran `.summem/summem wake` from repo root (not `./summem` or `./summem/summem`), then `.summem/summem wake --path dogfood` because the catalog printed that pull. Probe B skipped a second root wake.
    - This repo: `.summem/summem` → `../summem` (typechange). `dogfood/.summem/summem` already a symlink.
    - pytest 205 passed.
* Decisions made
    - Did not add nested-store driver symlinks (preflight advisory). Agents keep using root `.summem/summem` + `--path`.
    - Did not treat Probe A’s extra dogfood pull as a prompt miss. Invoke path was the rework bar; catalog over-pull is the same pull the first Composer probe showed.
    - Left the `.gitignore` `__pycache__/` slash fix unstaged.
* Insights
    - Git-root auto-create without a driver is the intended onboard gap: dirs + config appear; agents cannot invoke `.summem/summem` until someone places it.
    - Catalog still advertises a pull in wake output; a fresh agent may run it even when not working under that path.

## 2026-08-19 - QA - COMPLETE (PASS)

* Work completed
    - Reviewed the rework against the approved Level 2 plan, project brief, and system patterns. Did not edit the implementation.
    - Confirmed driver-copy removal, `.summem/summem` prompt lockstep, docs, tests, and Composer probe record are complete and acceptable as-is.
* Decisions made
    - QA passed. No build or plan rerun.
    - Catalog-as-command over-pull stays an advisory, not a blocker: the plan kept `usage_text` as `summem`, and Probe A still used `.summem/summem` for the root wake.
    - Nested-store driver symlink stays out (preflight advisory, not plan).
* Insights
    - Striking the copy left `ensure_store` as dirs plus default config, which is the onboarding story: the operator places `.summem/summem`.

## 2026-08-19 - REFLECT - COMPLETE

* Work completed
    - Wrote `memory-bank/active/reflection/reflection-agents-prompt.md` for the rework.
    - Reconciled persistent files: `systemPatterns.md` / `techContext.md` already matched; `productContext.md` has no driver-copy claim.
* Decisions made
    - Kept catalog-as-command out of this task. Encode the positive invoke path, not a ban that matches it.
* Insights
    - Store, driver, and activation are three objects. `ensure_store` copying `__file__` had collapsed the first two.

## 2026-08-19 - POST-REFLECT - catalog headers

* Work completed
    - Operator showed a root wake whose catalog was `dogfood` plus `summem wake --path dogfood` with no label; a subagent ran that line as an instruction.
    - Root wake now prints `== Additional memory catalogs ==` and `./path` lines first, then `== Project-root memories ==` and the root document. Empty extra-store list omits both headers. Pull wakes still omit the catalog.
    - Dropped catalog note counts, dates, and the `summem wake --path` command line. `VISION.md` Activation and `systemPatterns.md` match.
    - pytest 206 passed. Smoke: `./.summem/summem wake` shows `./dogfood` under the catalog header.
* Decisions made
    - Instruction to pull stays in `AGENTS.md` (“when you work under that path”), not in wake output.
    - Did not add nested-store driver symlinks.
* Insights
    - A catalog line that is only a shell command will be executed. Label it and print paths.

## 2026-08-19 - REWORK - INITIATED

* Work completed
    - Operator requested a teeny rework: omit `== Project-root memories ==` when the root decaying document is empty.
* Decisions made
    - Catalog-first stays. Catalog heading stays a label (no `wake --path`). Wake is a document, not a script.
* Insights
    - Empty root currently prints the header and glues `You are up to speed.` under it like a memory.

## 2026-08-19 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the empty-header rework as Level 1: one wake-print condition, one component.
* Decisions made
    - Header prints only when catalog and `wake_text` are both non-empty. Catalog-first stays.
* Insights
    - `test_root_wake_catalog_is_labeled_paths_not_commands` notes only in `pkg` and currently locks the empty-root header.

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - Memories header prints only when catalog and root document are both non-empty.
    - Tests: empty-root omits the header; catalog-plus-notes still has it. pytest 207 passed.
    - `VISION.md` Activation matches.
* Decisions made
    - Empty catalog+empty doc is closer only. `cat + footer` (no extra blank line).
* Insights
    - The header is a splitter, not a label for an empty section.

## 2026-08-19 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the implementation against the approved Level 1 empty-root-header plan and established design contract.
    - Ran the full suite under Python 3.11: 1 failed, 206 passed.
* Decisions made
    - QA failed because the working tree renames the catalog heading outside the plan, leaves the proof-scope test failing, and conflicts with `VISION.md`.
    - Build must rerun to restore the approved contract. If the rename is intentional, Plan must first establish it as a requirement.
* Insights
    - The planned empty-root-header behavior in `HEAD` is complete; the blocker is an additional unrecorded heading rename.

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - Operator renamed the catalog heading to `== Additional SumMem Catalogs ==`. Restored that string after a mistaken revert. Updated tests and `VISION.md`. pytest 207 passed.
* Decisions made
    - The heading rename is in scope. Do not treat it as an unplanned defect.
* Insights
    - Proof 7 locked the old heading; a rename has to move VISION and the proof together.

## 2026-08-19 - QA - COMPLETE (FAIL)

* Work completed
    - Reviewed the implementation against the approved Level 1 empty-root-header plan and established design contract.
* Decisions made
    - QA failed because the working tree changes `CONFIG_TEMPLATE` terminology from "knobs" to "settings" outside the plan, leaving `memory-bank/systemPatterns.md` out of sync.
    - Build must rerun to update the documentation or revert the code change.
* Insights
    - The planned empty-root-header behavior in `HEAD` is complete; the blocker is an additional unrecorded terminology change.

## 2026-08-19 - BUILD - COMPLETE

* Work completed
    - Operator kept CONFIG_TEMPLATE “settings/values”. Lockstepped `systemPatterns.md`, `techContext.md`, and VISION. Did not rename `knobs()`.
    - AGENTS.md note-policy sentence already matches `prompt_text()`.
* Decisions made
    - Wording tweaks in this rework are in scope. Do not revert operator strings.
* Insights
    - Adding the whole `summem` file also committed the template comment. Ask before treating a dirty string as a defect.
