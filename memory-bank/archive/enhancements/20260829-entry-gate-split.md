---
task_id: entry-gate-split
complexity_level: 2
date: 2026-08-29
status: completed
---

# TASK ARCHIVE: entry-gate-split

## SUMMARY

The write rule (what a repository remembers, and when) now lives only in the `init`-emitted `AGENTS.md` prefix. Root-wake Usage teaches recipes and must not restate membership, so a consumer can edit the prefix without the next wake stamping the shipped default back over it. Drafted as [PR #75](https://github.com/Texarkanine/SumMem/pull/75). QA passed. py311: 371 passed.

## REQUIREMENTS

From the project brief:

- Disjoint split: `prompt_text()` / committed prefix owns WHAT and WHEN (including skip-if-already-woke). The only argv is root `wake`. The recording verb `note` may be named without a command line.
- `how_to_text()` / root-wake Usage owns command recipes (note argv, pack/leaf grammar, writer-only, fold follow-ups, catalog pull). No membership probe, genre list, denylist, personal/machine stay-out, or skip-if-nothing-qualifies.
- `init_text()` tells the operator the printed block is a starting write rule they may edit; command syntax comes from root wake and must not be copied into the prefix. Still no “paste.” Still writes nothing.
- This repo’s `AGENTS.md` locksteps with `prompt_text()` as dogfood of the shipped default, not as a consumer contract. Do not test that a foreign prefix matches.
- The shipped default write rule stays the membership probe, genre list, denylist, and personal/machine stay-out. This task does not change what this repository remembers.

## IMPLEMENTATION

Creative chose disjoint split over a store overlay, policy-in-Usage-only, and dual copy. Reinforcement is the failure: if Usage still prints the shipped membership paragraph, a customized prefix is contradicted every session. Overlay matched sovereignty and non-drift but lost the harness read trigger and added a file. Dual copy is not customization.

`prompt_text()` is the default write rule plus activation. The intro may say `invoked as {AGENT_BIN}`; only the wake line is a command. `how_to_text()` is recipes: `{AGENT_BIN} note "…"`, writer-only, nap-already-stored, recall/zoom grammar, catalog `wake --path`. It does not list `nap` argv; `fold_request` still prints the exact `Run:` line. `init_text()` is an operator wrapper, then `---`, then `prompt_text()`. Writer-only moved into Usage.

Briefing: `systemPatterns.md` (bootstrap owns the write rule; Usage must not repeat it), `docs/architecture/index.md` (activation is also the write rule; the script does not reassert its default), `productContext.md` (operator edits the activation block; copying a newer script updates Usage only), `README.md` Quick Start, `techContext.md` (lockstep is not a wording pin).

## TESTING

TDD in `tests/test_init.py`. Preflight: PASS WITH ADVISORY; no plan edits; advisories applied in-step (named `git` forbid on how-to, sovereignty on the atlas activation definition, productContext use case, skip-rule wording without the Usage token). `/niko-qa` round 1 FAIL: Usage omitted `nap` argv while claiming to own command syntax; `fold_request` is not a recipe book. Round 2 PASS after adding `{AGENT_BIN} nap ID-A ID-B CAPTION`. Post-reflect, the operator dropped that Usage line, restored the invoke-path intro, and deleted `test_prompt_text_invariants`. Remaining pins are lockstep, `init` identity, Usage recipes, and `test_prompt_and_how_to_are_disjoint`. `tox -e py311`: 371 passed at QA.

## LESSONS LEARNED

- A role change (“syntax comes from root wake”) makes holes in the inherited copy load-bearing. The old Usage had never taught `nap` argv; copying that body into the new role inherited the hole.
- `fold_request`’s `Run:` line is a specific fold, not the recipe book. Teaching `nap` argv on Usage was added for QA completeness, then dropped: `fold_request` remains the nap command teacher.
- Tweaking write-rule copy must not require test edits if `AGENTS.md` is updated. Prefix may name the invoke path; that is not a command recipe.
- A briefing sentence that forbids intro interpolation will fight the lockstep test the next time the intro is restored.
- Two prompt functions stay direct strings. Do not factor a `MEMBERSHIP_PROBE`.

## PROCESS IMPROVEMENTS

- When a claim says a surface owns every recipe, pin every verb in that claim, not only the sentences you moved.
- For an editable policy prefix, lockstep the committed copy against `prompt_text()`; do not pin the wording. Otherwise every copy tweak is a test edit.

## TECHNICAL IMPROVEMENTS

Preflight’s radical-innovation advisory (HTML comment delimiters around the write-rule span, so a later `init --diff` can show shipped default vs committed prefix) was not adopted. It is a seam for the upgrade tax the design accepts: the shipped default no longer upgrades when someone copies a new script.

## NEXT STEPS

None required for this task. PR #75 is open. If agents stop recording because `note` argv left the prefix, tighten the duty sentence; do not put argv back.
