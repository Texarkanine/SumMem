---
task_id: wake-usage-prompt
complexity_level: 3
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: wake-usage-prompt

## SUMMARY

The committed `AGENTS.md` prefix is a small bootstrap. Root `wake` prints the versioned how-to under `== SumMem Usage ==`, then catalog, then memories. Pulls omit those sections. A consumer upgrade is copying the script. After reflect, skip is always-unless a prior project-root wake (no output-flag coupling), and `docs/agents-prompt.md` was deleted: `init` prints `prompt_text()` only. [PR #44](https://github.com/Texarkanine/SumMem/pull/44) on `feat/wake-usage-prompt`. `tox -e py311` 283 passed. QA PASS.

## REQUIREMENTS

- A small `AGENTS.md` bootstrap that does not change when the script’s usage details change.
- Repository-root `wake` prints the versioned how-to: note, nap, zoom/recall grammar, catalog pull.
- A consumer upgrade does not require editing `AGENTS.md`.
- Work on a feature branch, not `main`.
- Activation stays the committed `AGENTS.md` block. `init` writes nothing. No `summem upgrade`. Wake is a document (no `Run:` runbook). Pulls omit Usage, catalog, and the Project-root header. Prompt template 0BSD; program AGPL; `surgery.py` out of scope.

Post-reflect (operator): do not name Usage/footer flags in the bootstrap. One shipped bootstrap (`prompt_text()` / `init`). This repo’s `AGENTS.md` prefix remains dogfood lockstep.

## IMPLEMENTATION

Level 3. Creative chose **Stable verbs**: bootstrap keeps wake-if-needed, note, and writer-only. Versioned HOW is `how_to_text()` on root wake. Pointer-only was rejected (note duty only after a successful wake). Dual-publish was rejected (upgrade tax remains).

First preflight FAIL (fixable): leftover pins (`clone` / `another machine` still on `prompt_text` invariants; ingest `set(lines[1:-1])`). Re-plan named those pins. Second preflight PASS WITH ADVISORY. Named-section wake assembler (radical) was not applied.

- [`summem`](../../../summem): `how_to_text()` (header `== SumMem Usage ==`). Root `wake` prepends it, then catalog, then Project-root header + `wake_text` when the view is non-empty. Pulls skip Usage. `WAKE_LINES` still counts the view only. `prompt_text()` is the bootstrap. `init_text()` is an insert recipe plus that function. `PROMPT_DOC` / `docs/agents-prompt.md` removed after reflect.
- Bootstrap skip (final): always run root `wake`; do not run it again if a prior **project-root** SumMem wake is still in the conversation. A pull does not count. No `== SumMem Usage ==` or `You are up to speed.` in the prefix.
- Tests: `tests/test_init.py` (how-to tokens, bootstrap invariants, `AGENTS.md` prefix, `init` does not name the deleted file). `tests/test_scopes.py` and proofs retargeted so catalog forbids apply to the catalog section only; ingest slices from the memories header to the footer.
- Briefing: README Quick Start is copy script, run `init`, insert that print (one-time fat-prefix replace). `systemPatterns.md`, `techContext.md`, `docs/architecture/index.md`, `docs/notes.md`, `productContext.md` session-start use case.

## TESTING

TDD in plan order. First preflight FAIL, then PASS WITH ADVISORY. Build: full `tox` 284 on py311–py314. `/niko-qa` PASS (advisories: pack `<hash>` vs unique prefix in Usage; how-to test does not pin `ignore`; whole-stdout `git` forbid kept). After dropping the prompt file: `tox -e py311` 283 passed (one lockstep test removed).

## LESSONS LEARNED

- Root-wake tests that pin catalog shape must slice the catalog section. Usage must contain `{AGENT_BIN}` and `wake --path`.
- A “retarget this test” step that names only some tokens leaves leftover pins. First preflight FAIL and the QA `ignore` advisory are that class.
- Skip polarity: always-unless (OptMem shape), not if-missing-then-run. Skip key: project-root wake, not any wake and not output flags.
- A second copy of the bootstrap (`docs/agents-prompt.md`) only existed to lockstep with `init`. Delete the file; keep the function the script can print.

## PROCESS IMPROVEMENTS

- Name every leftover assert when retargeting a test, or say which exact-string / `lines[0]` pins to replace.
- Do not couple the committed prefix to stdout headers. That puts the upgrade tax back.

## TECHNICAL IMPROVEMENTS

Usage still says `x<N> <hash>:` for packs; listings print unique prefixes. Fix the next time that paragraph is touched. Catalog-section helpers are duplicated between `test_scopes.py` and `test_proof_scopes.py` (QA advisory).

## NEXT STEPS

- [PR #44](https://github.com/Texarkanine/SumMem/pull/44) on `feat/wake-usage-prompt`. This archive commit should land on that branch so the PR drops `memory-bank/active/`.
