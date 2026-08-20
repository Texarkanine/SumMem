# Project Brief

## User Story

As a contributor, I want `VISION.md` and `ROADMAP.md` retired in favor of a real README, a reconciled memory-bank, and `docs/` leftovers so the living documents describe the product as it is, not as a sequencing contract.

## Use-Case(s)

### Sunset the directional files

Triage `VISION.md` and `ROADMAP.md`: drop what is now simply true of the tree, drop what we built differently, keep leftovers.

### Publish user-facing docs

Write a README in the vein of stockroom, ai-rizz, and slobac. Put leftovers in `docs/notes.md`. Put leftover architecture or other relevant information in `docs/` as ordinary markdown in a mkdocs-shaped layout (not a site). An architecture page that explains the algorithm and store layout is expected unless triage shows it is unnecessary.

### Reconcile the memory-bank

Initialization and reconciliation so README and memory-bank describe the same product. `VISION.md` is no longer the design contract.

## Requirements

1. Delete information in `VISION.md` and `ROADMAP.md` that is now simply true of the codebase.
2. Delete information in those files that we ended up building something else for.
3. Store leftovers in `docs/notes.md`.
4. Write a good README (see `../stockroom`, `../ai-rizz`, and `../slobac`).
5. Perform an initialization and reconciliation pass on the memory-bank so user-facing docs — README and memory-bank — are consistent.
6. Identify any leftover architecture *or other relevant information* that warrants a home in `docs/`. `docs/` may become a mkdocs site later; for now it holds markdown in that shape.
7. An architecture page that clearly explains the algorithm and the memory store layout is the expected leftover unless triage finds none.

## Constraints

1. Do not stand up a mkdocs site.
2. Leftovers are any relevant leftover, not architecture-only. Architecture was the operator's first guess; there may be none, but an algorithm/layout page is expected.
3. Persistent memory-bank is a deliberately incomplete subset: omission is fine, wrong content is not.
4. This task does not change executable product behavior. QA must not fail on former VISION/ROADMAP vs codebase conflicts that this sunset is meant to retire.
5. Issue-wave fan-out stays on hold until this sunset is done.

## Acceptance Criteria

1. `VISION.md` and `ROADMAP.md` are gone.
2. `README.md` is a real project README in the sibling-repo vein.
3. Leftovers that survived triage live under `docs/` (`notes.md` and any warranted pages).
4. Memory-bank persistent files no longer treat `VISION.md` as the design contract and agree with the README.
5. If an architecture page is written, it explains the algorithm and store layout as they exist, not as a future contract.
