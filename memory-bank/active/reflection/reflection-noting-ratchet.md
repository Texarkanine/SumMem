---
task_id: noting-ratchet
date: 2026-08-20
complexity_level: 2
---

# Reflection: noting-ratchet

## Summary

Over-long `note` and `nap` now print OptMem’s byte/limit/compress footer. Other agent-facing errors got a next step only at raise sites where that step is known and not obvious. QA passed; 221 pytest.

## Requirements vs Outcome

Delivered [SumMem#16](https://github.com/Texarkanine/SumMem/issues/16) and the bounded walk. Empty stayed `note is empty`. Missing-`.tree` `unknown id` stayed a problem statement. No atlas edit. No invented repairs.

## Plan Accuracy

The first plan keyed Unit 2 on unique strings. That was wrong: `unknown id` is two causes, and shared `require_entry` cannot say “note each line.” One preflight FAIL (fixable) fixed both. The rewritten raise-site table matched the build. Advisories (7-byte `toolong`, no line-627 fixture) were followed.

## Build & QA Observations

TDD reds were the old strings. QA passed with advisories only; no rework.

## Insights

### Technical
- A unique error string is not a unique cause. Attach the next step at the raise site, not with a global replace.

### Process
- Preflight caught the shared-`require_entry` lie before build. That is the check earning its keep.

### Million-Dollar Question

If ratchets had been the rule from the start, `require_entry` would never have said `note is too long`, and identity-miss vs missing children file would never have shared one sentence. Per-site strings in one script are that design; a helper or exception type would only pay off when the raise list grows again.
