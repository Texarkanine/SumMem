---
task_id: ingest
date: 2026-08-18
complexity_level: 3
---

# Reflection: ingest

## Summary

Milestone 1 of L4 `file-backend` shipped: one shebang driver at `.summem/summem` that auto-creates the git-root store, records immutable notes, and wakes a wait-free listing. First proof 1 passed. Identity (no-delimiter hex join, canonical `.tree` bytes, 64-hex wake ids, UTC names) is frozen in code and in `VISION.md`.

## Requirements vs Outcome

Every ingest requirement landed. The product is one stdlib file, not a package. `wake` and `note` exist; `nap` / `--path` / catalog are errors. Proof 1 is an executable worktree merge, not a document assertion. The 280 limit is UTF-8 bytes. The driver copies only when missing. Wake never refuses. Python older than 3.11 is refused without importing `tomllib`.

Nothing was descoped. Strict argparse was kept on purpose (`note "-foo"` still needs `--`). This tree is not a store: `.gitignore` drops generated data and tracks only the driver.

## Plan Accuracy

The TDD order (codec → store → wake → CLI → proof 1 → docs) was the right sequence. File list was right: one script, pytest outside it, no `pyproject.toml`.

The plan's load recipe (`SourceFileLoader` + `spec_from_loader` + `exec_module`) was incomplete: dataclasses with postponed annotations need the module registered in `sys.modules`. The throwaway PoC never used dataclasses, so preflight did not see it. That was the only build surprise. Temp names via `os.urandom` (rng reserved for the public note name) was a small, justified deviation so injected-clock tests stay deterministic.

Identified challenges that actually showed up: no-suffix import, this machine's `python3` 3.10, and not overwriting an existing driver. Challenges that did not: canonical JSON drift, proof 1 needing extra merge machinery.

## Creative Phase Review

No creative phase. `VISION.md` already settled the architecture; the operator chose the shebang path. That held. Remaining format choices were pinned in the plan and then written into `VISION.md` so Phase 2 cannot invent a second identity scheme.

## Build & QA Observations

Build was linear. Codec, store, and wake went green after one implementation pass each. Proof 1 passed on the first run: identical driver bytes plus two note paths merge with zero conflicts.

QA passed with no blocking findings. Advisories: unused `summem` pytest fixture; `find_store_parent` walk untested except via CLI chdir to repo root; `VISION.md` Sequence still shows an 8-character id example while the product prints 64 hex; copied-driver mode `0o755` is not asserted on the copy. Those do not need a rebuild. Phase 2 should copy the product's 64-hex ids, not the Sequence illustration.

## Cross-Phase Analysis

The first hatchling plan would have been the wrong product. Operator pushback plus a second plan/preflight was cheaper than building a package and tearing it out.

Preflight's real catches (UTF-8 reconfigure as a red/green vector, error text that must not leak store paths, version guard not preempted by `tomllib`, identity bytes belonging in `VISION.md`) showed up in tests and docs. The `sys.modules` gap slipped through because the loader PoC was too small.

The advisory that "this repo becomes a store because the driver lives here" was resolved before build: presence of `.summem/summem` is the product, not activation. That gitignore rule kept the development tree honest.

## Insights

### Technical

- A no-suffix shebang loaded with `SourceFileLoader` is not a normal module: `from __future__ import annotations` plus `@dataclass` looks up `sys.modules[cls.__module__]`. Register the module before `exec_module`, or skip postponed annotations on dataclasses.
- Phase 2 identity must call the functions in `.summem/summem` (`leafset_id`, `dumps_tree`). The Sequence section's 8-character id is a picture, not the contract; tests and the Identifiers section are.

### Process

- A loader PoC that does not instantiate the types the product will use (here: dataclasses) is not a load proof.
- When the operator rejects the product shape after preflight, replan. Do not implement the discarded layout.
