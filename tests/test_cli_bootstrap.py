"""CLI driver bootstrap: shebang, Python floor, stdio encoding, and lazy imports."""

from __future__ import annotations

import builtins
import importlib.util
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from importlib.machinery import SourceFileLoader
from random import Random

import pytest

from conftest import ROOT, SCRIPT
from gitutil import COMMAND_ONLY, fresh_imported, init_repo


def test_script_is_repo_root_driver():
    """Tests load the committed repo-root summem file."""
    assert SCRIPT == ROOT / "summem"
    assert SCRIPT.is_file()


def test_driver_has_python3_shebang():
    """The driver starts with the python3 shebang."""
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first == "#!/usr/bin/env python3"


@pytest.mark.skipif(os.name == "nt", reason="POSIX execute bit is not tracked on Windows")
def test_driver_has_executable_bit():
    """The driver carries the user execute bit on POSIX."""
    assert SCRIPT.stat().st_mode & stat.S_IXUSR


def test_wake_prints_chinese_under_ascii_io_encoding(tmp_path, summem):
    """A 你好 note wakes when the child process has PYTHONIOENCODING=ascii."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "你好", datetime(2026, 1, 1, tzinfo=timezone.utc), Random(0))
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "ascii"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "wake"],
        cwd=repo,
        env=env,
        capture_output=True,
    )
    assert result.returncode == 0
    assert "你好".encode("utf-8") in result.stdout


def test_refuses_python_before_311(summem):
    """require_python rejects a version tuple older than 3.11."""
    m = summem
    with pytest.raises(SystemExit) as caught:
        m.require_python((3, 10, 12))
    assert caught.value.code == 1
    m.require_python((3, 11, 0))
    m.require_python((3, 12, 0))


def test_driver_checks_python_floor_before_importing_tomllib(monkeypatch, capsys):
    """Executing the driver on Python <3.11 exits 1 with the floor message before importing tomllib."""
    real_import = builtins.__import__

    def guard_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.split(".", 1)[0] == "tomllib":
            raise AssertionError("tomllib imported before Python version check")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", guard_import)
    monkeypatch.setattr(sys, "version_info", (3, 10, 0))
    name = "summem_py310_probe"
    monkeypatch.delitem(sys.modules, name, raising=False)
    loader = SourceFileLoader(name, str(SCRIPT))
    spec = importlib.util.spec_from_loader(name, loader)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, mod)
    with pytest.raises(SystemExit) as caught:
        spec.loader.exec_module(mod)
    assert caught.value.code == 1
    err = capsys.readouterr().err
    assert "SumMem needs Python 3.11 or newer" in err
    assert "tomllib" not in err


def _cpython_310() -> str | None:
    """Return a CPython 3.10 executable, or None if this host has none."""
    candidates: list[str] = []
    uv = shutil.which("uv")
    if uv:
        found = subprocess.run(
            [uv, "python", "find", "3.10"],
            capture_output=True,
            text=True,
        )
        path = found.stdout.strip()
        if found.returncode == 0 and path:
            candidates.append(path)
    which = shutil.which("python3.10")
    if which:
        candidates.append(which)
    for path in candidates:
        probe = subprocess.run(
            [path, "-c", "import sys; print(sys.version_info[:2])"],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip() == "(3, 10)":
            return path
    return None


def test_driver_refuses_python_310_before_tomllib():
    """On Python 3.10 the driver prints the floor message, not a tomllib ImportError."""
    py310 = _cpython_310()
    if py310 is None:
        pytest.skip("Python 3.10 is not available")
    result = subprocess.run(
        [py310, str(SCRIPT), "version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "SumMem needs Python 3.11 or newer" in result.stderr
    assert "tomllib" not in result.stderr
    assert "Traceback" not in result.stderr


def test_version_skips_command_only_imports():
    """version in a fresh interpreter does not import command-only modules."""
    code, imported = fresh_imported(["version"])
    assert code == 0
    for name in COMMAND_ONLY:
        assert imported[name] is False, name


def test_init_skips_command_only_imports():
    """init in a fresh interpreter does not import command-only modules."""
    code, imported = fresh_imported(["init"])
    assert code == 0
    for name in COMMAND_ONLY:
        assert imported[name] is False, name


def test_help_skips_command_only_imports():
    """-h in a fresh interpreter does not import command-only modules."""
    code, imported = fresh_imported(["-h"])
    assert code == 0
    for name in COMMAND_ONLY:
        assert imported[name] is False, name
