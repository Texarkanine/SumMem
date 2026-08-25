---
task_id: wake-usage-prompt
date: 2026-08-24
complexity_level: 3
---

# Reflection: wake-usage-prompt

## Summary

The committed `AGENTS.md` prefix is now a small bootstrap (wake-if-needed, note, writer-only). Root `wake` prints the versioned how-to under `== SumMem Usage ==`, then catalog, then memories. QA passed. A consumer upgrade is copying the script.

## Requirements vs Outcome

All four brief requirements landed: small bootstrap, how-to on root wake, no `AGENTS.md` edit on script upgrade, work on `feat/wake-usage-prompt`. Constraints held: activation stays the committed block, `init` writes nothing, no `Run:` runbook, pulls omit Usage/catalog/Project-root, no `summem upgrade`, lockstep on the bootstrap only, 0BSD prompt / AGPL program / `surgery.py` untouched. Store, fold, note, nap, zoom, and recall are unchanged except the root-wake document. Nothing was dropped or added.

## Plan Accuracy

The four-unit sequence (how-to, bootstrap, root-wake compose, briefing) and the file list were right. No new test files. `test_cli.py` stayed off unit 3 after the re-plan. The challenges that actually showed up were the ones named: whole-stdout forbids of `.summem/summem` and `wake --path` fighting a Usage section that must contain both. Mitigation was catalog-section pins, as planned.

The first preflight FAIL was leftover pins the first plan's "retarget this test" steps did not name (`clone` / `another machine` still required on `prompt_text` invariants; ingest `set(lines[1:-1])`). The re-plan named those pins. That was plan incompleteness, not a wrong approach.

QA's leftover advisory — unit 1 listed "ignore `--path` without catalog" among red-test tokens, and the how-to test does not assert `ignore` — is the same class at a smaller scale. The sentence is in the product.

## Creative Phase Review

Stable verbs held. Bootstrap kept wake-if-needed, note, and writer-only; versioned HOW moved to `how_to_text()`. Pointer-only would have dropped the always-injected note duty. Dual-publish would have left the upgrade tax. Skip keyed off a Usage block the agent can see and follow, not the footer or "a prior root wake." Compaction false-skip was the failure mode the predicate is written to avoid; false re-wake is acceptable because wake never refuses.

Friction was small: how-to is a labeled document, not a command list. No `Run:` line. Catalog lines stayed `./path`. The one-time fat-prefix replace lives in the README, not in `init_text()`, so new-install `init` stays an insert recipe.

## Build & QA Observations

Build followed TDD in plan order. Tests went red for the right reasons (empty `how_to_text()`, fat `prompt_text()`, exact-string / `lines[0]` catalog pins), then green. Full `tox` was 284 on py311–py314. Named-section assembler (preflight radical) was not applied; inlined prepends in the existing `wake` branch were enough. QA passed on the first pass. Advisories are wording and pin hygiene, not acceptance blockers: pack `<hash>` vs unique prefix (carried from the old prompt), the missing `ignore` token pin, and the plan-kept whole-stdout `git` forbid.

## Cross-Phase Analysis

The first preflight FAIL and the QA `ignore`-token advisory are the same leftover-pin class: a surgical "retarget this test" step that lists some tokens leaves the unlisted asserts in place. Naming the leftover pins in numbered steps made the second preflight pass, and build did not rediscover them as mysterious reds.

Creative's skip-key decision prevented the compaction failure the pre-mortem named. Preflight's implementer cautions (`<path>` not `pkg`; no other section headers in how-to; ingest slices from the memories header) were applied in build and kept QA from treating leftover whole-stdout pins as product misses.

QA agreed the declined named-section assembler was KISS, not a miss. The remaining whole-stdout `git` forbid is plan-kept test fragility, not an incomplete split.

## Insights

### Technical

- Root-wake tests that pin catalog shape must slice the catalog section. Usage is required to contain `{AGENT_BIN}` and `wake --path`; a whole-stdout forbid of those strings will fail for the wrong reason once HOW lives on wake.
- Moving agent prose is a chance to drop stale grammar. Usage still says `x<N> <hash>:` because that sentence was copied; listings already print unique prefixes.

### Process

- A "retarget this test" step that names only some tokens leaves the rest as leftover pins. The first preflight FAIL and the QA `ignore` advisory are that class. Name every assert that must move, or say which exact-string / `lines[0]` pins to replace.
