---
task_id: entry-gate-split
date: 2026-08-29
complexity_level: 2
---

# Reflection: entry-gate-split

## Summary

The write rule now lives only in the `init`-emitted `AGENTS.md` prefix. Root-wake Usage teaches argv, including `nap`. A disjointness test is the fence that makes a consumer's edited prefix real.

## Requirements vs Outcome

All six brief requirements and five acceptance criteria landed. Nothing was dropped. Additions were the preflight briefing advisories (activation sovereignty, productContext use case, skip-rule wording, named `git` forbid) and QA's `nap` argv line — both in the original duty, not extra product.

## Plan Accuracy

File list and TDD sequence were right. The leftover-pin list missed `nap` argv because the old Usage had never taught it either; copying that body into the new role inherited the hole. Challenges that hit were leftover pins and the `git` forbid on how-to, both named. The surprise was QA, not preflight.

## Build & QA Observations

First red was clean (five tests). Lockstep stayed green until `prompt_text()` and `AGENTS.md` moved together. QA round 1 failed on completeness, not on the split. Round 2 passed. `tox -e py311`: 371 passed.

## Insights

### Technical

- `fold_request`'s `Run:` line is a specific fold, not the recipe book. Once Usage claims to own command syntax, every taught verb needs an argv pin. `note`/`recall`/`zoom` had them; `nap` did not.

### Process

- A role change ("syntax comes from root wake") makes holes in the inherited copy load-bearing. Pin every verb in the new claim, not only the sentences you moved.

### Million-Dollar Question

This is the design that should have existed when wake-usage-prompt split bootstrap from Usage: prefix owns the gate, Usage owns every recipe. What we built is that, plus the `nap` line the first how-to never had.
