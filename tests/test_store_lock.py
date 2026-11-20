"""Cross-platform store locking (with_store_lock across POSIX flock, runtime fallback, and msvcrt)."""

from __future__ import annotations

import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

from gitutil import init_repo


@pytest.mark.skipif(os.name == "nt", reason="POSIX directory flock requires fcntl")
def test_with_store_lock_blocks_and_writes_no_lock_file(tmp_path, summem):
    """A second non-blocking flock of naps/ fails while the lock is held; no lock file appears."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    naps = repo / ".summem" / "naps"
    probe = (
        "import fcntl, os, sys\n"
        "fd = os.open(sys.argv[1], os.O_RDONLY)\n"
        "try:\n"
        "    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
        "except BlockingIOError:\n"
        "    raise SystemExit(2)\n"
        "raise SystemExit(0)\n"
    )
    seen = {}

    def held():
        seen["names"] = [p.name for p in (repo / ".summem").rglob("*") if p.is_file()]
        result = subprocess.run(
            [sys.executable, "-c", probe, str(naps)],
            capture_output=True,
        )
        seen["code"] = result.returncode

    m.with_store_lock(repo, held)
    assert "lock" not in seen["names"]
    assert seen["code"] == 2


def _block_naps_dir_open(monkeypatch, m, naps: Path) -> None:
    real = m.os.open

    def wrapped(path, flags, *args, **kwargs):
        if os.fspath(path) == os.fspath(naps) and flags == os.O_RDONLY:
            raise OSError(13, "blocked")
        return real(path, flags, *args, **kwargs)

    monkeypatch.setattr(m.os, "open", wrapped)


def test_with_store_lock_fallback_lock_is_outside_store(tmp_path, monkeypatch, summem):
    """When naps/ cannot be flocked, the lock file lives under the runtime dir."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    naps = repo / ".summem" / "naps"
    lock_dir = tmp_path / "locks"
    monkeypatch.setattr(m, "_runtime_lock_path", lambda store: lock_dir / "store.lock")
    _block_naps_dir_open(monkeypatch, m, naps)
    ran = {"n": 0}

    def held():
        ran["n"] += 1
        ran["store"] = [p.name for p in (repo / ".summem").rglob("*") if p.is_file()]
        ran["runtime"] = list(lock_dir.rglob("*")) if lock_dir.exists() else []

    m.with_store_lock(repo, held)
    assert ran["n"] == 1
    assert "lock" not in ran["store"]
    assert ran["runtime"]


def test_with_store_lock_msvcrt_locks_one_byte_and_unlocks(tmp_path, monkeypatch, summem):
    """msvcrt backend: append-open, one-byte range, LK_NBLCK then LK_UNLCK after fn."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    lock_path = tmp_path / "locks" / "store.lock"
    monkeypatch.setattr(m, "_try_fcntl", lambda: None)
    monkeypatch.setattr(m, "_runtime_lock_path", lambda store: lock_path)
    fake = types.SimpleNamespace(LK_NBLCK=1, LK_UNLCK=2, calls=[])

    def locking(fd, mode, n):
        fake.calls.append((mode, n, os.fstat(fd).st_size))

    fake.locking = locking
    monkeypatch.setitem(sys.modules, "msvcrt", fake)
    opens = []
    real_open = open

    def wrapped_open(path, mode="r", *args, **kwargs):
        opens.append((os.fspath(path), mode))
        return real_open(path, mode, *args, **kwargs)

    monkeypatch.setattr("builtins.open", wrapped_open)
    ran = {"n": 0}

    def held():
        ran["n"] += 1

    m.with_store_lock(repo, held)
    assert ran["n"] == 1
    lock_opens = [mode for path, mode in opens if os.fspath(path) == os.fspath(lock_path)]
    assert lock_opens
    assert lock_opens[0].startswith("a")
    assert not lock_opens[0].startswith("w")
    assert fake.calls[0] == (fake.LK_NBLCK, 1, 1)
    assert fake.calls[-1][0] == fake.LK_UNLCK
    assert fake.calls[-1][1] == 1
    assert "lock" not in [p.name for p in (repo / ".summem").rglob("*") if p.is_file()]


def test_with_store_lock_msvcrt_retries_then_acquires(tmp_path, monkeypatch, summem):
    """msvcrt LK_NBLCK OSError retries with a bounded sleep, then acquires."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    lock_path = tmp_path / "locks" / "store.lock"
    monkeypatch.setattr(m, "_try_fcntl", lambda: None)
    monkeypatch.setattr(m, "_runtime_lock_path", lambda store: lock_path)
    fake = types.SimpleNamespace(LK_NBLCK=1, LK_UNLCK=2, n=0)
    sleeps = []

    def locking(fd, mode, n):
        if mode == fake.LK_NBLCK and fake.n == 0:
            fake.n += 1
            raise OSError("busy")
        fake.n += 1

    fake.locking = locking
    monkeypatch.setitem(sys.modules, "msvcrt", fake)
    import time as time_mod

    monkeypatch.setattr(time_mod, "sleep", sleeps.append)
    m.with_store_lock(repo, lambda: None)
    assert sleeps
    assert all(d <= 0.25 for d in sleeps)


def test_with_store_lock_msvcrt_retry_deadline_is_elapsed(tmp_path, monkeypatch, summem):
    """A busy msvcrt lock raises cannot lock within 30s of elapsed retry time."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    lock_path = tmp_path / "locks" / "store.lock"
    monkeypatch.setattr(m, "_try_fcntl", lambda: None)
    monkeypatch.setattr(m, "_runtime_lock_path", lambda store: lock_path)
    fake = types.SimpleNamespace(LK_NBLCK=1, LK_UNLCK=2)

    def locking(fd, mode, n):
        if mode == fake.LK_NBLCK:
            raise OSError("busy")

    fake.locking = locking
    monkeypatch.setitem(sys.modules, "msvcrt", fake)
    import time as time_mod

    sleeps = []
    now = [0.0]

    def fake_sleep(d):
        sleeps.append(d)
        now[0] += d

    monkeypatch.setattr(time_mod, "sleep", fake_sleep)
    monkeypatch.setattr(time_mod, "monotonic", lambda: now[0])
    with pytest.raises(ValueError, match="cannot lock"):
        m.with_store_lock(repo, lambda: None)
    assert sleeps
    assert all(d <= 0.25 for d in sleeps)
    assert sum(sleeps) <= 30.0 + 1e-9


def test_cli_note_lock_fallback_has_no_traceback(tmp_path, monkeypatch, capsys, summem):
    """CLI note with directory flock blocked still saves; no traceback or fcntl on stderr."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    monkeypatch.setattr(m, "_runtime_lock_path", lambda store: tmp_path / "locks" / "store.lock")
    _block_naps_dir_open(monkeypatch, m, repo / ".summem" / "naps")
    capsys.readouterr()
    assert m.main(["note", "--path", ":/", "hello"]) == 0
    captured = capsys.readouterr()
    assert "Saved to `:/`" in captured.out
    assert "Traceback" not in captured.err
    assert "fcntl" not in captured.err
