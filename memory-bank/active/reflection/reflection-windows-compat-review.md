---
task_id: windows-compat-review
date: 2026-09-10
complexity_level: 2
---

# Reflection: windows-compat-review

## Summary

Native Windows PowerShell/CMD could run the driver; invoke recipes now match that. `init`/`prompt_text` always teach `python .summem/summem wake`. Wake Usage/`Run:` stay host-specific. QA passed.

## Requirements vs Outcome

Lock-deadline items from the first rework still hold. This round delivered the four Rework requirements except pushing, which is the remaining delivery step. No extra scope.

## Plan Accuracy

File list and TDD order were right. The substring trap (`python .summem/summem note` contains `.summem/summem note`) showed up in tests exactly as the plan's challenge predicted. No reordering.

## Build & QA Observations

Red tests failed on the old quoted `sys.executable` strings, then went green in one pass. QA PASS; one non-blocking DRY advisory (POSIX-only init test now redundant with host-agnostic init).

## Insights

### Technical
- Windows Usage tests must forbid a backtick-bare recipe (`\`.summem/summem note\``), not the substring `.summem/summem note`.
- `python` on PATH is clone-portable; `sys.executable` is a machine path and does not belong in `AGENTS.md` or Usage.

### Process
- An archived "stock AGENTS.md stays Unix" decision can be reversed after a native-host probe without advertising Windows as a supported host.

### Million-Dollar Question

If python-on-PATH had been the bootstrap from day one, this is the shape: one portable wake line in `AGENTS.md`, shebang-bare recipes only on Unix wake. A polyglot `.cmd` launcher would erase the host branch; it was recorded in preflight and not built.
