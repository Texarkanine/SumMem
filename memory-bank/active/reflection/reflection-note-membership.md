---
task_id: note-membership
date: 2026-08-28
complexity_level: 3
---

# Reflection: note-membership

## Summary

Retargeted shipped `note` membership to “work in this clone”: bootstrap probe plus a how-to genre list, denylist, and skip-if-nothing. Build copied the creative sentences; QA passed with no new findings.

## Requirements vs Outcome

Delivered as specified. Both surfaces carry the probe; how-to carries genre and the PR/checks/archive denylist; OptMem unnamed and unedited; writer-only and wake-usage split untouched; eternal-currency phrase not restored; sentence counts unchanged (3 bootstrap, 4 how-to). No requirements dropped or added.

## Plan Accuracy

File list, TDD order, and scope were right. The only imprecision was “red on the new pin and lockstep”: tests-first went red on the new `work in this clone` pins only. Lockstep stays green until `prompt_text()` changes without `AGENTS.md`. Named challenges (denylist phrase tests, `(mandatory)` as emit-every-session, store rewrite) did not materialize because the plan already declined them.

## Creative Phase Review

Option A held: the sentences landed verbatim. The `clone not in prompt_text` pin was the predicted test break, not a design surprise. Split surfaces kept the denylist off the always-loaded bootstrap. The accepted miss (agent notes without waking) was not revisited.

## Build & QA Observations

Build was transcription after preflight’s body-vs-assertion check. `tox -e py311 -- tests/test_init.py` then `tox run-parallel` (369 passed, 1 skipped) went green first try. QA confirmed the diff matches the plan, lockstep holds, and no stale phrasing remains in shipped docs. The shared-constant advisory was carried forward, not re-raised.

## Cross-Phase Analysis

Preflight’s hand-check of proposed bodies against every surviving assertion made build a copy step — that gate earned its keep. The same preflight named the two-surface drift class that bit `wake-usage-prompt`, then “judge, do not fix” plus build-to-plan plus QA-carry-forward left two independent literals in the tree. Planning did not cause build problems; creative did not cause QA findings. The residual risk is the next wording pass editing one surface.

## Insights

### Technical

- `AGENTS.md` lockstep only binds bootstrap to the committed prefix. The how-to probe is a second copy of the same phrase; a pin on the retyped literal will not catch one surface drifting. A module constant both functions interpolate is the structural fix, still unapplied.

### Process

- For prompt-copy tasks, preflight that reads the proposed bodies against every surviving assertion is the load-bearing gate; build will not discover what that check already proved.
- An advisory that names a drift class this repo has already shipped through as a FAIL should be adopted in the plan, not carried across three phases as “not applied.”
