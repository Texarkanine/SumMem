---
task_id: nap-variant-stems
date: 2026-08-25
complexity_level: 3
---

# Reflection: nap-variant-stems

## Summary

Five-part nap stems landed as specified: pair-bytes variant tag, shared constructor, dual-read of four-part names, union-then-zipper, sibling `migrate.py`, and this clone's stores rewritten. All 15 acceptance criteria are pinned; `tox` is 346 green on py311–py314; QA passed with advisories and no rework.

## Requirements vs Outcome

The brief and issue #61 were delivered. Nothing was dropped from the eight-unit plan. Two things stayed out on purpose:

- `--dry-run` on `migrate.py` (preflight advisory, not a planned unit).
- Closing #59 as superseded (PR body, not code).

No extra product surface was added: README command table unchanged, no `summem migrate` verb, heal and `_first_overlap` untouched. The only reinterpretation was scheduling: caption-conflict inversion moved from unit 5 into unit 2 after the first preflight, which is the same requirement, not a new one.

## Plan Accuracy

The second plan's sequence, file list, and scope were right. The first plan was not: it inverted the caption-conflict process test in unit 5, three units after `write_nap` would turn it red. Preflight caught that as `FAIL (fixable)` before any production code. After the re-plan, units 2–4 stayed green and unit 5 was only new proofs.

Identified challenges that actually materialized: `split("-")[-2]` oracles, the two tests that asserted four-part same-path / caption-only conflict, and dogfood rewrite of committed stores. Challenges that did not: heal survivor order (unit 4 pins passed with no production change), Windows path length, hash-then-write drift (`_write_pair` made that structural).

The plan named deleting `_nap_stem` and having rematerialize plus `surgery.plan_break_out` call `nap_stem` with child pair bytes. That is what shipped. QA later showed the cost: four copies of the serialize-then-name block, and surgery's prediction unpinned against rematerialize's write. That was a plan-shaped advisory, not a surprise from elsewhere.

## Creative Phase Review

One mega-unknown: where the migration helper lives. Option A (sibling `migrate.py`) held through build and QA. Hash-on-disk-bytes, no re-`dumps_tree`, no heal, no `__version__`, not a CLI verb — all translated cleanly.

Friction that the creative doc accepted and QA restated:

- Discoverability is "PR + atlas row," not `docs/surgery.md`-class. A consumer repo has `.summem/summem` and no `migrate.py`; the atlas line "run from the repository root" does not say the script loads sibling `summem` by `__file__` and selects stores from `cwd`. Carry that into the PR.
- Dest-exists skip is silent with exit 0. That matches the creative notes; an operator cannot tell a clean run from a partial one.

Nothing that should have been a mega-unknown was missed. `--dry-run` was an optional trust aid, not a home-of-script question.

## Build & QA Observations

Build was smooth after the re-plan. TDD order held. Heal production code was a no-op, as unit 4 predicted. Shared `_write_pair` made "bytes hashed are bytes written" a structural property. This clone's root and `dogfood` stores migrated in unit 7 and QA independently re-checked every committed pair.

QA (`/niko-qa`, PASS) did not catch incorrect behavior. It caught remaining shape: DRY copies of the child-stem block, migrate operator docs, a dead `SystemExit` guard, a near-dead `started_stores` branch, and two tests that five-part stems made vacuous (`test_rematerialize_does_not_clobber_existing_dest` nap half; an unrelated `assert pa.exists() is False` on the serialize-once test). None required a Build rerun.

## Cross-Phase Analysis

Preflight's TDD Plan Encoding check earned the FAIL: scheduling an inversion three units after the behavior change would have left the suite red across progress commits. The re-plan put inversion with the write. That is the causal chain that mattered.

Creative "skip if dest exists" became a QA advisory about operator trust, not a correctness miss. Creative "document in the PR and atlas" became a QA advisory that Use-Case 3 still needs a consumer-repo sentence in the PR. Both were accepted tradeoffs, restated with sharper operator framing.

The plan's delete-`_nap_stem` shape passed preflight and shipped; QA named it the strongest advisory. Preflight is not a DRY review. If a later change feeds different bytes into the stem, surgery's predicted dest and rematerialize's written dest can drift without a red test.

## Insights

### Technical

- A four-part stem is a proper prefix of the matching five-part stem, so lexicographic order already makes legacy lose to new without a heal special case. Unit 4 pinned that; do not add a format-aware branch.
- Deleting a private wrapper in favor of a public constructor is not reuse if every caller still serializes the pair itself. `child_nap_stem(child) -> (stem, tree_bytes, caption_bytes)` would be the actual shared write path; `nap_stem` is only the name grammar.
- `migrate.py` must not grow a `__version__` or a Release Please extra-file: it is a one-shot store rewrite, not a versioned product surface. `surgery.py` is the opposite (it already versions).

### Process

- Invert or retire tests in the same unit that changes the behavior they pin. "We'll fix that oracle in a later unit" fails the encoding check and, if it slipped through, would strand intermediate commits red.
- A sibling operator script that loads `summem` by `__file__` needs the same "from a clone of this repository" sentence `surgery.py` already has. An atlas change-surface row is not that sentence.

## Post-reflect operator change

After QA PASS and reflect, the operator dropped dual-read. `_parse_nap_stem` is five-part only; `migrate.py` is the only four-part reader. Draft PR #62 carries the migrate `BREAKING CHANGE:` footer. `child_nap_stem` landed as the post-QA DRY fix the reflection recommended.
