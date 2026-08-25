# Active Context

## Current Task: wake-usage-prompt
**Phase:** BUILD - COMPLETE

## What Was Done
- `how_to_text()` prints the versioned how-to under `== SumMem Usage ==`.
- `prompt_text()` is the bootstrap (wake-if-needed, note, writer-only). Lockstep `docs/agents-prompt.md` and this repo's `AGENTS.md` prefix match it.
- Root `wake` prepends Usage, then catalog, then memories. Pulls omit Usage. `WAKE_LINES` still counts the view only.
- Briefing docs: one-time fat-prefix replace lives in the README; skip keys off a readable Usage block; document order includes Usage.
- Full `tox`: 284 passed on py311–py314.

## Files created or modified
- `summem` — `how_to_text()`, bootstrap `prompt_text()`, root-wake compose
- `docs/agents-prompt.md`, `AGENTS.md` prefix
- `tests/test_init.py`, `tests/test_scopes.py`, `tests/test_proof_ingest.py`, `tests/test_proof_scopes.py`
- `README.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `docs/architecture/index.md`, `docs/notes.md`

## Key implementation decisions
- Composition stays in the existing `wake` branch (named-section assembler not applied).
- How-to teaches `wake --path <path>`, not `pkg`.
- Skip predicate is see-and-follow the Usage block, not the heading substring.

## Deviations from Plan
None — built to plan. Preflight advisories applied as implementer cautions.

## Integration test results
284 passed (`tox` py311–py314), including retargeted ingest and scopes proofs.

## Next Step
- QA review runs automatically
