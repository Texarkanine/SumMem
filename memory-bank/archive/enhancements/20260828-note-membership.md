---
task_id: note-membership
complexity_level: 3
date: 2026-08-28
status: completed
---

# TASK ARCHIVE: note-membership

## SUMMARY

Retargeted shipped `note` membership so agents record lore and tree-affecting in-flight work, not process telemetry. The probe on both agent surfaces is “another contributor needs to work on this repository.” Root-wake how-to still carries the genre list, PR/checks/archive denylist, and skip-if-nothing. Drafted as [PR #74](https://github.com/Texarkanine/SumMem/pull/74). QA passed. py311/py314: 369 passed, 1 skipped.

## REQUIREMENTS

From the project brief:

- Retarget `prompt_text()` (committed `AGENTS.md` bootstrap) and `how_to_text()` (root-wake Usage) so a `note` is something another contributor working on this repository would still need.
- That set includes lore (gotchas, team norms, failed approaches, uncanonicalized invariants) and in-flight work that changes how someone else should use the tree.
- Routine process telemetry stays out: opened a PR, still needs merge, QA PASS, archived to X.
- Personal, machine-local, and user-preference facts still stay out.
- Wording is every-context-window: as few sentences as today, denser, no lecture.
- SumMem states its own test. Do not name OptMem or any sibling memory product.
- Do not change the store, CLI, or nap/zoom/recall mechanics. Do not restore `must still be true after a fresh clone`. Do not rewrite existing store notes.

## IMPLEMENTATION

Agent-facing prompt contract only. `prompt_text()` Register Memories body and `how_to_text()` note paragraph now share this probe: “records one short line another contributor needs to work on this repository.” How-to continues with the genre list, denylist, personal/machine/preference stay-out, and “Skip if nothing qualifies or it is already remembered.” Writer-only paragraph and nap/recall/catalog paragraphs are unchanged. `AGENTS.md` stays lockstep with `prompt_text()`.

`tests/test_init.py` pins `work on this repository` on both surfaces. The old bootstrap `clone` forbid and how-to `another machine` / `clone` requires were dropped. Denylist examples were not pinned.

A shared `MEMBERSHIP_PROBE` constant was applied during the PR-feedback revision, then removed: two short adjacent prompt sentences stay direct. `AGENTS.md` lockstep still covers the generated bootstrap copy.

## TESTING

TDD in `tests/test_init.py`. Retargeted `test_prompt_text_invariants` and `test_how_to_text_is_the_usage_section`; `test_agents_md_starts_with_prompt_text` unchanged. Red on the two probe pins before shipped text moved; lockstep stayed green until `prompt_text()` changed. Preflight: PASS WITH ADVISORY (shared-constant hoist, later rejected). `/niko-qa`: PASS. `tests/test_init.py`: 11 passed. `tox run-parallel`: py311/py314 OK, py312/py313 skip (no interpreters). Direct-wording correction re-ran the same matrix green.

## LESSONS LEARNED

- Clone-portability answered whose fact; it did not answer what the fact is for. “Would still need” is true of the next agent on this PR. “Needs to work on this repository” is true of someone using the committed tree.
- “This clone” usefully rejected telemetry but implied contributors share one checkout. They do not; SumMem travels with committed repository history.
- “Decisions” in the old how-to is how “opened PR #70” qualified. The genre list must not include it.
- `(mandatory)` without skip-if-nothing still emits a tweet to satisfy the heading.
- Two short adjacent prompt literals do not justify a constant. Readability of the prompt functions is the point; `AGENTS.md` lockstep already covers the third copy.
- Write-time gotchas stay legal: the denylist is events, not truth-over-time. Do not restore `must still be true after a fresh clone`.

## PROCESS IMPROVEMENTS

- For prompt-copy tasks, preflight that reads proposed bodies against every surviving assertion is the load-bearing gate; build will not discover what that check already proved.
- A repeated preflight advisory still needs a readability check before it becomes a constant. Two local copies of one short sentence are cheaper than an interpolation that makes the prompt harder to read.

## TECHNICAL IMPROVEMENTS

None. Persistent files (`productContext.md`, `systemPatterns.md`, `techContext.md`) were left unchanged: the membership sentences are agent-facing prompt copy, not a product, architecture, or tooling change.

## NEXT STEPS

None. Drafted as PR #74.
