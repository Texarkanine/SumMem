---
task_id: slobac-audit-ratchet
date: 2026-08-25
complexity_level: 2
---

# Reflection: slobac-audit-ratchet

## Summary

Applied 19 obviously wrong SLOBAC remediations in existing tests. Proofs stayed. `tox` py311–py314 stayed at 284 passed. QA passed.

## Requirements vs Outcome

Delivered the ratchet: stronger oracles and less private-helper coupling where the hole was real. Did not golden prompts, add typed exceptions, or Phase B regroup. Finding 14 stayed after preflight showed the subprocess 3.10 proof skips in CI. Rework: Phase A on finding 59 — stripped `First proof N`, renamed off `test_proof_*`.

## Plan Accuracy

First plan over-accepted finding 14. One re-plan. Advisories (branchless lcov snapshot, `pa.name` as prefix, exact public wake lines) were cheaper and better than the first wording. Expand-child content is on the right 8-pack (`eight-b`), not `eight-a-5`.

## Build & QA Observations

Build was test-only and went green on the first named-test run. QA found nothing.

## Insights

### Technical
- A note filename is already `{stamp}-{rand}`. `_seq_prefix` on that name is the name. Tests that call the helper are coupling to a no-op.
- `test_driver_refuses_python_310_before_tomllib` is not CI coverage. It skips unless CPython 3.10 is on the host. The source-order pin is the floor guard that actually runs in this repo's CI.

### Process
- An all-smells audit is a filter, not a punch list. Pair findings that cancel (vacuous `raises` vs loose-text `match=`) and keep the product ratchet.

### Million-Dollar Question

The suite already has `dated_leaf` as an independent leaf grammar. A matching pack-line helper in `conftest.py` would have made findings 3, 18, and 19 a one-line oracle from the start. Not added here; the ratchet did not need a new vocabulary.
