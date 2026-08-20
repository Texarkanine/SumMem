---
task_id: agents-prompt
date: 2026-08-19
complexity_level: 2
---

# Reflection: agents-prompt

## Summary

Rework struck driver placement from `ensure_store` and aligned the baked prompt, `AGENTS.md`, and docs with onboarding: place `.summem/summem`, run `init`, paste. Composer 2.5 woke via that path and skipped a second root wake. QA passed.

## Requirements vs Outcome

Delivered as specified. `ensure_store` creates `notes/`, `naps/`, and missing config only. Prompt and `AGENTS.md` lockstep on `.summem/summem`. Presence of the driver is not activation. Nested `start` does not get a driver. Catalog `usage_text` still names the product `summem`. Did not add nested-store driver symlinks (preflight advisory, not the plan).

## Plan Accuracy

Units 1–4 were the right split. The first pass had taught repo-root `summem` and forbade naming `.summem/summem` (substring invariant). Operator correction flipped that invoke path; the plan had to rewrite invariants, not just docs. Catalog-as-command over-pull was already known and stayed out of scope.

## Build & QA Observations

TDD on store/wake/start/init was straightforward once “store exists” tests stopped checking for a `summem` file. 205 pytest passed. QA passed with the same catalog-over-pull advisory; no implementation gap.

## Insights

### Technical
- `ensure_store` copying `__file__` made “the store exists” look like “an agent can run the script.” Store creation is dirs plus config. The driver is operator-placed. Activation is the `AGENTS.md` block.
- A substring invariant that forbids the real invoke path will fight the next policy correction. Encode the positive command, not a ban list that happens to match it.
- Catalog lines that look like `summem wake --path …` over-pull a cheap agent after a correct `.summem/summem` root wake. After reflect the operator had us label the catalog and print `./path` only; the pull recipe stays in `AGENTS.md`.

### Process
- First-pass Composer probes do not count after the prompt is rewritten. Unit 4 had to re-instrument.
- Nothing notable on Niko sequencing; rework → plan → preflight → build → QA was the right loop.

### Million-Dollar Question

If driver placement had never been `ensure_store`’s job, onboarding would always have been: place `.summem/summem`, `init`, paste. Three objects stay distinct: store (dirs + config), driver (operator-placed file; this repo a symlink to the record), activation (`AGENTS.md` block). That is what we built. The copy was the wrong convenience.
