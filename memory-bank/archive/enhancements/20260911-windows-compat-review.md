---
task_id: windows-compat-review
complexity_level: 2
date: 2026-09-11
status: completed
---

# TASK ARCHIVE: windows-compat-review

## SUMMARY

Level 2 rework of PR #84 after CodeRabbit judge items and native Windows PowerShell/CMD. `msvcrt` lock wait is 30s elapsed (`time.monotonic()`), not ~12 min from `waited += 0.01`. Bootstrap / `init` / committed `AGENTS.md` teach `python .summem/summem wake`. The prefix names SumMem only — no `invoked as` path. Root-wake Usage/`Run:` stay host-specific: bare `.summem/summem` on POSIX, `python .summem/summem` on Windows. No quoted `sys.executable`, no Windows-only init warning. Do not advertise Windows. Spec [windows-compat-audit](20260909-windows-compat-audit.md) Unix-only wake / `sys.executable` recipes are superseded. Internals port: [windows-compat](20260909-windows-compat.md).

## REQUIREMENTS

- Judge 1–3: elapsed `msvcrt` deadline; pin `_host_needs_interpreter` not `os.name`; regression test `sum(sleeps) <= 30.0` (plus 1e-9 IEEE slack).
- Native-host recipe rework: portable python-on-PATH first-wake; host-specific Usage/`Run:`; push `windows-support`.
- Post-reflect: drop `invoked as {AGENT_BIN}` so the intro cannot contradict the wake command.
- Do not advertise Windows. No `windows-latest` CI. No lock file under `.summem/`.

## IMPLEMENTATION

[`summem`](../../../summem): `_with_runtime_lock` deadline + remainder-clamped sleep; `agent_invoke()` returns `python {AGENT_BIN}` on nt; `prompt_text()` wake is that command with no invoke intro; `init_text()` is host-agnostic. Lockstep [`AGENTS.md`](../../../AGENTS.md). Tests: [`tests/test_zipper.py`](../../../tests/test_zipper.py), [`tests/test_init.py`](../../../tests/test_init.py), [`tests/test_fold.py`](../../../tests/test_fold.py) and older host-dependent asserts. Briefing: `systemPatterns.md`, `techContext.md`, `docs/notes.md`.

## TESTING

TDD red then green (lock wait 735s then 30s; then quoted `sys.executable` then python prefix). `tox -e py311`: 389 passed. `/niko-qa`: PASS (DRY advisory: POSIX-only init test redundant with host-agnostic init). GHA py311–py314 green. Operator confirmed native Windows: the command works. Cursor auto-approve with a weak model blocked the `python` call; that is a harness policy, not a driver failure. IEEE: `sum(sleeps)` can land at `30.000000000000007` on 3.12+.

## LESSONS LEARNED

- Do not monkeypatch `os.name` to `"nt"` on Linux pytest (`WindowsPath` crash). Patch `_host_needs_interpreter`.
- `python .summem/summem note` contains `.summem/summem note`; Windows tests must forbid backtick-bare recipes, not that substring.
- `python` on PATH is clone-portable; `sys.executable` is a machine path.
- An intro that names `{AGENT_BIN}` next to a `python … wake` line will confuse agents. Name SumMem; put recipes on wake.
- `waited += 0.01` is backoff only; elapsed deadline is monotonic wall time.

## PROCESS IMPROVEMENTS

An archived “stock AGENTS.md stays Unix” decision can reverse after a native-host probe without advertising support. Keep historical archives; update `docs/notes.md`.

## TECHNICAL IMPROVEMENTS

Preflight recorded a `cmd`/POSIX polyglot launcher as a way to drop `agent_invoke()`’s host branch. Not built. Optional later: `windows-latest` CI; add `msvcrt` to `_COMMAND_ONLY`.

## NEXT STEPS

PR #84 remains open for merge. No further Niko work on this task.
