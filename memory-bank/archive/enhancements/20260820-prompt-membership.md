---
task_id: prompt-membership
complexity_level: 2
date: 2026-08-20
status: completed
---

# TASK ARCHIVE: prompt-membership

## SUMMARY

Split the baked Register Memories paragraph so the dump imperative and the clone-portability membership test are separate sentences. `prompt_text()` and `AGENTS.md` stay lockstep. No store or CLI change. The leaked uv/rc3 note was left in place.

## REQUIREMENTS

- Separate *when* to note from *what* belongs in a note.
- Membership is clone-portability (true after a fresh clone on another machine); personal, machine-local, and preference facts stay out.
- Do not name OptMem, redact the leak, add a denylist, or add phrase tests on `prompt_text()`.
- Keep existing `test_init.py` invariants and the AGENTS.md lockstep test.

## IMPLEMENTATION

Creative decision B (prompt structure only): rewrite Register Memories in [`summem`](../../../summem) `prompt_text()` and copy the prefix into [`AGENTS.md`](../../../AGENTS.md). The dump line no longer says “acceptable in git forever.” Did not take the first-preflight advisory (labeled When to note / What belongs headings).

## TESTING

No new tests. Existing `tests/test_init.py` stayed green. `uvx --with tox tox`: 215 passed on py311–py314. First QA failed on a duplicated `tasks.md` block; rework deleted it; second QA passed.

## LESSONS LEARNED

- The stay-out clause was already the next sentence. The clause still jammed into the dump imperative was `acceptable in git forever`.
- Asserting on `prompt_text()` sentences is a change-detector. `init` printing that string does not make the wording an executable unit. The lockstep test is the contract that belongs.
- Do not check off a plan unit by duplicating its body.

## PROCESS IMPROVEMENTS

Treat baked-prompt wording as prose/policy from the first plan. Phrase tests on `init` output will fail preflight or QA as change-detectors.

## TECHNICAL IMPROVEMENTS

Labeled child blocks under Register Memories (`When to note` / `What belongs`) would match the catalog-heading lesson. Not built.

## NEXT STEPS

None.
