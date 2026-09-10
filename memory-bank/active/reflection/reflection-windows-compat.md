---
task_id: windows-compat
date: 2026-09-09
complexity_level: 2
---

# Reflection: windows-compat

## Summary

Minimal internals port so native Windows can launch and run: LF-canonical store reads, capability lock (directory flock else runtime-dir file), host invoke plus an init warning above `---`. Stock `AGENTS.md` stays Unix. QA PASS. Native `C:\Python313\python.exe` `note` saved.

## Requirements vs Outcome

Delivered the audit internals plus the init warning. Item 3 (git symlink) stayed won’t-do. No README Windows paragraph. Tests patch `_host_needs_interpreter` rather than `os.name`. Runtime lock file is `"ab+"` so the one-byte range is binary.

## Plan Accuracy

Sequence was right. First preflight correctly failed: a fallback-ran test is not an `msvcrt` oracle. The surprise was `os.name = "nt"` on Linux: pathlib tries to construct `WindowsPath` and dies during pytest reporting.

## Build & QA Observations

TDD red/green was uneventful after the pathlib fix. QA PASS; two non-blocking advisories (OptMem retry loop is not a 30s wall-clock cap; `_COMMAND_ONLY` omits `msvcrt`).

## Insights

### Technical
- Do not monkeypatch `os.name` to `"nt"` on a POSIX pytest run. Patch a one-line host check instead.
- Content-addressed identity is LF bytes. Canonicalize on every read; do not rewrite the working tree.

### Process
- A lock fallback that only asserts `fn` ran will fail preflight. Fake the missing backend (`msvcrt`) and assert open mode, byte range, retry, and unlock.

### Million-Dollar Question

This is the design you would have wanted on day one: Unix committed prefix, runtime invoke when the shebang is not argv0, directory flock when it exists, otherwise a lock file that is not in the store. No second advertised product.
