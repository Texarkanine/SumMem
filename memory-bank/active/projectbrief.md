# Project Brief

## User Story

As the maintainer of PR #84, I want the three judged CodeRabbit findings fixed on `windows-support` so the `msvcrt` lock wait is a real 30s deadline, invoke tests pin the host, and a regression test pins the timeout.

## Use-Case(s)

### Use-Case 1

Two agents contend for the same store on native Windows. `note` / `nap` retry `msvcrt.locking` for at most 30 seconds of elapsed time, then raise `ValueError("cannot lock")`.

### Use-Case 2

The pytest suite is run on a host where `_host_needs_interpreter()` is true. POSIX-named assertions still check bare `AGENT_BIN` / `Run:` output because they pin the host check to false; Windows assertions pin it to true.

## Requirements

1. `_with_runtime_lock`'s `msvcrt` retry loop uses a `time.monotonic()` deadline of 30 seconds, clamps each sleep to the remainder, and preserves the existing backoff (`min(0.01 + waited * 0.2, 0.25)`).
2. POSIX-only `agent_invoke` / `init` / Usage / `Run:` assertions monkeypatch `_host_needs_interpreter` to `False` before asserting bare `AGENT_BIN`; Windows assertions set it to `True`. Cover the older asserts this PR made host-dependent (`test_init.py`, `test_fold.py`, `test_scopes.py`, `test_surgery.py` as needed). Do not monkeypatch `os.name`.
3. A regression test keeps `msvcrt.locking` busy, advances a fake monotonic clock from `sleep`, and asserts `ValueError` with `sum(sleeps) <= 30.0`.

## Constraints

1. Rework of archived windows-compat / [PR #84](https://github.com/Texarkanine/SumMem/pull/84). Do not advertise Windows. No `windows-latest` CI. No lock file under `.summem/`.
2. Do not monkeypatch `os.name` to `"nt"` on Linux pytest.

## Acceptance Criteria

1. A held `msvcrt` lock raises `cannot lock` once elapsed retry time reaches 30 seconds, not after ~12 minutes of 0.25s sleeps.
2. Tests that expect bare `.summem/summem` recipes pin `_host_needs_interpreter` to `False`; tests that expect the interpreter prefix pin it to `True`.
3. `tox -e py311` passes.

## Rework

Operator asked to apply PR #84 judge items 1–3 as a rework of windows-compat (archived). Head: `36c7375345f8c5a8091d5dbfa912a6bb3ff9aadc`.

## Rework

Native Windows PowerShell/CMD: it technically works. Refine invoke recipes:

1. `summem init` always says to run `python .summem/summem wake` (python on PATH; Windows and *nix).
2. `summem wake` prints host-specific recipes: bare `.summem/summem` on *nix, `python ` prefixed on Windows.
3. A clone with python 3.11+ on PATH can first-wake from the bootstrap; wake then prints the rest of the commands for that host.
4. Push `windows-support` when the refinement is on the branch.
