# Task: docs-sunset

* Task ID: docs-sunset
* Complexity: Level 2
* Type: simple enhancement

Sunset `VISION.md` and `ROADMAP.md`. Drop what is now true of the tree and what we built differently. Keep leftovers under `docs/`. Write a sibling-quality README. Reconcile the memory-bank so it no longer treats VISION as the design contract. Write an architecture page that explains the algorithm and store layout as they exist.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`
- Test location: `tests/`
- Conventions: `tests/test_*.py`; proofs live in `tests/test_proof_*.py`. Tests load repo-root `summem` via `SourceFileLoader`.
- New test files: none
- Survey: no `VISION` / `ROADMAP` references in `*.py`. Deleting those files does not change executable behavior. Do not add change-detectors on README or `docs/` contents.

## Implementation Plan

### 1. Triage VISION and ROADMAP — prose/policy

- Files: `VISION.md`, `ROADMAP.md`
- No tests: prose/policy artifact

1. Read both files against the working tree and `memory-bank/archive/`.
2. Bucket every load-bearing claim: **true of the tree** (drop as leftover; eligible for README / `docs/architecture` / memory-bank as *what is*), **built something else** (drop; do not document the abandoned design), **leftover** (not true, not superseded — goes to `docs/notes.md`).
3. Record the buckets in `memory-bank/active/progress.md` so build does not re-litigate them.

Expected first-pass buckets (confirm in build; do not treat this list as closed):

- **True:** ingest/nap/wake model; file store roles; hashing and `.tree` schema; scopes/`start`/`--path`; root catalog; wait-free wake; equal-grain fold + in-memory expand; zipper on overlap; invariants that the tests already enforce.
- **Built else:** wake as a script the agent must “do”; driver-only-at-`.summem/summem` with `ensure_store` copy; ROADMAP Phase 1–3 sequencing (done, not leftover); proof 6 as disjoint-only (overlap is zipper); any remaining 8-character-id picture vs unique prefix of 64 hex.
- **Leftover:** second backend / sqlite; harness hooks; full OptMem aligned `cover(T)` after merge; pack-size cap; hot margin (named in VISION, absent from `summem`).

### 2. Architecture page — prose/policy

- Files: `docs/architecture/index.md` (create)
- No tests: prose/policy artifact

1. Follow `.cursor/skills/ai-rizz/architecture-docs/SKILL.md` (Diátaxis explanation, inclusion bar, invariants, change-surface routing) and `.cursor/skills/shared/illustrate-complexity/SKILL.md` (Mermaid).
2. Write **what is**: algorithm (ingest commute, content-addressed naps, equal-grain fold, under-budget expand, zipper) and store layout (`.summem/notes`, `naps/*.sum` + `*.tree`, `config.toml`; driver vs store vs activation).
3. Include an orientation diagram, named invariants / deliberate absences, and a short “when you change X, read Y” table.
4. Do not paste the VISION CLI table, ROADMAP phases, or First-proof numbered list. CLI belongs in the README. Proofs live in `tests/test_proof_*.py`. Later items belong in `docs/notes.md`.
5. Present tense only. This page must not become VISION 2.0.

### 3. Leftovers and docs landing — prose/policy

- Files: `docs/notes.md`, `docs/index.md` (create)
- No tests: prose/policy artifact

1. Write `docs/notes.md` from the leftover bucket only. If a leftover is empty after confirmation, say so in one line — do not invent work.
2. Write `docs/index.md` as a mkdocs-shaped home: what the docs are, links to architecture and notes. No user-guide / contributing trees unless triage found a leftover that needs its own page.

### 4. README — prose/policy

- Files: `README.md`
- No tests: prose/policy artifact

1. Read `../stockroom/README.md`, `../ai-rizz/README.md`, and `../slobac/README.md` again at write time.
2. Match that genre: one-line what it is, Why bullets, a Quickstart that works from a clone (no docs site), pointers into `docs/`, license. No hero asset required.
3. Quickstart: place `.summem/summem`, `init`, paste the prompt, `wake` / `note`. Point at `AGENTS.md` rather than duplicating the baked block.
4. Command table may live here (public agent interface). Keep it short and present-tense.
5. Link `docs/architecture/index.md` and `docs/notes.md` with relative paths.

### 5. Memory-bank reconciliation — prose/policy

- Files: `memory-bank/productContext.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. `productContext.md`: stop calling `VISION.md` the design contract. Success criteria point at shipped behavior / `tests/test_proof_*.py`, not a retired file. Omission is fine; wrong citations are not.
2. `systemPatterns.md`: drop the “VISION/ROADMAP are directional leftovers” sentence. Keep briefing altitude. Point at `docs/architecture/index.md` for the atlas. Soften “missing piece of the model is unfinished work” so the code + architecture page are the model, not a retired contract.
3. `techContext.md`: canonical documents become README, `docs/architecture/index.md`, `LICENSE`, and the proof tests. Drop “CLI table in VISION.md must not.”
4. Do not rewrite `memory-bank/archive/**`. Historical VISION mentions stay historical.

### 6. Delete the sunset files — prose/policy

- Files: `VISION.md`, `ROADMAP.md`
- No tests: prose/policy artifact

1. Delete both files after the new docs and memory-bank cite the replacements.
2. Grep the working tree (excluding `memory-bank/archive/` and this task’s ephemeral files) for living “VISION.md is the contract” citations and fix any that remain.

## Technology Validation

No new technology - validation not required

## Dependencies

- Sibling README genre: `/home/mobaxterm/git/stockroom/README.md`, `/home/mobaxterm/git/ai-rizz/README.md`, `/home/mobaxterm/git/slobac/README.md`
- Architecture craft: architecture-docs skill; stockroom `docs/architecture/index.md` is a shape reference, not an outline to copy
- Proofs as success criteria: `tests/test_proof_*.py`

## Challenges & Mitigations

- **Architecture page becomes VISION 2.0:** write present tense; Later stays in `docs/notes.md`; inclusion bar from architecture-docs.
- **Triage dump vs empty notes:** confirm buckets against `summem` before writing. Expected leftovers are the Later items and unbuilt knobs, not a second VISION.
- **Memory-bank / README drift:** write README and `docs/` first, then reconcile persistent MB to those pages.
- **QA treats archive mentions of VISION as living contract:** archives are out of scope for rewrite; preflight/QA should treat them as history.

## Pre-Mortem

- **The README is a shortened VISION (too long, still a contract):** already covered by Challenge 1 and step 4’s sibling-genre constraint.
- **We omit the algorithm because systemPatterns already briefs it:** do not cut step 2. systemPatterns stays a briefing; the operator asked for an architecture page that explains algorithm + layout.
- **We add change-detector tests on docs:** already covered — no new tests.
- **We re-level to L3 for “architecture”:** reject. Product architecture is unchanged; this is one docs surface.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA — FAIL; Build rework complete; QA must rerun

## QA Findings

- [x] Replace physical “file count” with view-node count in the architecture algorithm, diagram, and Fold / Expand prose.
- [x] Narrow “same leaves, same `.tree` bytes” to the deterministic serialization guarantee the implementation actually provides.
- [x] Correct the claim that a requested nap id vanishing during heal is CLI success; the command exits 1 while preserving the leaves.
- [x] Remove temporal “This milestone” language from the present-tense atlas.
