# Task: wake-usage-prompt

* Task ID: wake-usage-prompt
* Complexity: Level 3
* Type: feature

A small committed `AGENTS.md` bootstrap that stays put, and a root `wake` that prints the versioned how-to, so a consumer upgrade is copying the script.

## Component Analysis

### Affected Components
- `prompt_text()` / `docs/agents-prompt.md` / `AGENTS.md` prefix: today one baked prompt is activation, session-start, note membership, nap protocol, and zoom/recall/catalog recipes. Becomes the insertable bootstrap only; this repo may keep the Niko suffix after that prefix.
- `init_text()` / `init`: prints insert recipe plus `prompt_text()`. Must print the new bootstrap, still write nothing.
- Root `wake` (`main` wake branch, `catalog_text`, `wake_text`): today catalog + optional `== Project-root Memories ==` + view + `You are up to speed.` Must also print the versioned how-to on root only.
- Lockstep and prompt tests (`tests/test_init.py`): `AGENTS.md` starts with `prompt_text()`; `docs/agents-prompt.md` equals `prompt_text()`; membership / writer-only invariants sit on `prompt_text()` today and will need a new home if those sentences move.
- Root-wake tests (`tests/test_scopes.py`, `tests/test_proof_ingest.py`, `tests/test_proof_scopes.py`): pin catalog headers, empty-root omission, pull-omits-catalog, and exact wake stdout. A new root-only section changes those expected strings.
- Briefing docs (`README.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `docs/architecture/index.md` if it names the prompt): describe activation and onboarding.

### Cross-Module Dependencies
- `AGENTS.md` prefix → agent runs `{AGENT_BIN} wake` at repo root.
- Root `wake` → `catalog_text(root, parent)` then `wake_text(parent)` then footer. How-to must compose here without leaking onto pulls (`catalog_text` already empty when `parent != root`).
- `prompt_text()` → `init_text()` and both lockstep files. Splitting the function splits those pins.
- `usage_text()` (`-h`) is the operator catalog (`CLI_NAME`). It is not the agent how-to (`AGENT_BIN`). Do not merge them.

### Boundary Changes
- Public agent document: `AGENTS.md` prefix shrinks; root `wake` stdout gains a usage section. This is the product’s activation contract.
- `prompt_text()` meaning: either it becomes bootstrap-only, or a new function is the bootstrap and `prompt_text()` is retired or narrowed.
- Pull `wake --path` stdout must stay catalog-free and how-to-free.

### Invariants & Constraints
- Activation is the committed bootstrap. Driver presence is not activation.
- `init` does not write `AGENTS.md`.
- Wake is a document. Catalog paths stay labeled paths, not commands. How-to must not read as a script to execute.
- Pull wakes omit catalog, root memories header, and the new how-to.
- Wake never refuses to print.
- Copying the script remains the upgrade path. No `summem upgrade`.
- Prompt template stays 0BSD. Program stays AGPL. `surgery.py` is out of scope.
- Store, fold, note, nap, zoom, and recall behavior stay the same except the root-wake document.
- Lockstep remains for the insertable bootstrap file, not for versioned how-to prose in `AGENTS.md`.

## Open Questions

- [x] **Agent-document split** → Resolved: Stable verbs. Bootstrap keeps wake-if-needed (key off a readable `== SumMem Usage ==` block, not the footer), note, and writer-only. Root `wake` prints `how_to_text()` (membership, nap protocol, id grammar, catalog pull). See `memory-bank/active/creative/creative-agent-document-split.md`.

## Status

- [x] Component analysis complete
- [ ] Open questions resolved
- [ ] Test planning complete (TDD)
- [ ] Implementation plan complete
- [ ] Technology validation complete
- [ ] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
