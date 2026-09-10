---
task_id: windows-compat-audit
date: 2026-09-09
complexity_level: 2
---

# Reflection: windows-compat-audit

## Summary

Native-Windows audit with CMD probes on CPython 3.13.3. Path resolution is not the hole; `note`/`nap` and shebang exec are. QA passed. No port shipped.

## Requirements vs Outcome

Delivered the findings list with resolutions. Operator added mid-build: `AGENTS.md` stays clone-portable; runtime prints may be host-specific. That constraint is in the findings. No product code changed.

## Plan Accuracy

Four prose units were the right shape. The surprise was how much already works: `python C:\…\.summem\summem`, `--path` backslashes, Git `ls-files` with `/`. The plan listed path handling as a candidate; probes retired it.

## Build & QA Observations

Probes from WSL `cmd.exe` default to `C:\Windows` because UNC cwd is illegal — had to `cd /d` a Windows temp dir and pin `C:\Python313\python.exe`. QA PASS; one cosmetic `tasks.md` dup, fixed.

## Insights

### Technical
- OptMem’s Windows lock is the right *mechanism* (`msvcrt`, `"a"`, backoff) and the wrong *target* (a file in the store).
- `os.open` on a directory is `PermissionError` on Windows even before `fcntl` is missing, so a Windows branch cannot keep “flock `naps/`”.
- Forward-slash relative paths are accepted by Windows Python; committed recipes can stay `.summem/summem` as a *file name* if they are not treated as a POSIX exec.

### Process
- From WSL, `cmd.exe` PATH can prefer Moba shims. Pin the native interpreter by full path.

### Million-Dollar Question

If Windows had been a host from day one: `AGENTS.md` would name the driver file and never an argv0; Usage/`Run:` would print `sys.executable` plus that file; `with_store_lock` would lock a runtime-dir file on every OS (POSIX directory flock of `naps/` is a Unix-only convenience); `.gitattributes` would mark notes/naps `-text` before the first digest.
