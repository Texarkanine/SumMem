---
task_id: windows-compat
complexity_level: 2
date: 2026-09-09
status: completed
---

# TASK ARCHIVE: windows-compat

## SUMMARY

Level 2 internals port so native Windows can launch and run. Store reads canonicalize CRLF to LF. `with_store_lock` tries directory flock of `naps/`, else a runtime-dir file (`fcntl` then `msvcrt`). Usage/`Run:` use `agent_invoke()`; `prompt_text()` stays Unix. `init` on that host warns above `---` that the printed invoke lines only work on Windows. Do not advertise Windows. Spec: [windows-compat-audit](20260909-windows-compat-audit.md).

## REQUIREMENTS

- Audit items 1, 2, 4, 5: lock, CRLF-on-read, runtime invoke, no `fcntl` traceback.
- Item 3 (this-repo git symlink) remains won’t-do.
- Capability lock, not `if windows` except the one host check for invoke/init.
- Init warning above `---` on Windows. Stock `AGENTS.md` Unix. No README Windows paragraph. No lock file in `.summem/`.

## IMPLEMENTATION

[`summem`](../../../summem): `store_bytes`; `_try_fcntl` / `_runtime_lock_path` / `_with_runtime_lock`; `agent_invoke` / `_host_needs_interpreter`; init wrapper. Tests in `tests/test_codec.py`, `tests/test_zipper.py`, `tests/test_init.py`, `tests/test_fold.py`, `tests/test_cli.py`. Docs: `docs/notes.md`, atlas lock sentence. Surgical persistent memory-bank wording. Tests patch `_host_needs_interpreter`, not `os.name`. Runtime lock file opened `"ab+"`.

## TESTING

TDD red then green. `tox -e py311`: 387 passed. `/niko-qa`: PASS. Native `C:\Python313\python.exe` `version`, `init` warning, and `note` Saved. QA advisories (non-blocking): OptMem retry loop is not a 30s wall-clock cap; `_COMMAND_ONLY` omits `msvcrt`.

## LESSONS LEARNED

- Do not monkeypatch `os.name` to `"nt"` on Linux pytest: pathlib instantiates `WindowsPath` and crashes in the report. Patch a one-line host check.
- A lock fallback that only asserts `fn` ran is not an `msvcrt` test. Fake the backend: append open, one-byte range, retry, unlock.

## PROCESS IMPROVEMENTS

First preflight FAIL (no `msvcrt` oracle) was the right catch. Keep that bar.

## TECHNICAL IMPROVEMENTS

This is the day-one shape: Unix committed prefix, runtime invoke when the shebang is not argv0, directory flock when it exists, otherwise a lock file that is not in the store.

## NEXT STEPS

None. Item 3 stays won’t-do. Optional later: `windows-latest` CI, add `msvcrt` to `_COMMAND_ONLY`.
