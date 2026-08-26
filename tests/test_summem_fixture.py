"""Session-scoped summem fixture contract."""

from __future__ import annotations

import sys
import types
from pathlib import Path

from conftest import SCRIPT, load_summem


def test_load_summem_returns_cached_module():
    """load_summem returns the same module object on every call."""
    assert load_summem() is load_summem()


def test_summem_fixture_is_the_cached_module(summem):
    """The summem fixture is the cached SourceFileLoader module for repo-root summem."""
    assert summem is load_summem()
    assert summem.__file__ == str(SCRIPT)
    assert hasattr(summem, "main")


def test_load_summem_ignores_later_sys_modules_replace(summem):
    """migrate.py and surgery.py overwrite sys.modules['summem']; the test cache must not follow."""
    impostor = types.ModuleType("summem")
    impostor.__file__ = str(SCRIPT)
    sys.modules["summem"] = impostor
    try:
        assert load_summem() is summem
    finally:
        sys.modules["summem"] = summem


def test_monkeypatch_on_summem_restores_after_undo(summem, monkeypatch):
    """monkeypatch.setattr on the session module restores after undo."""
    original = summem.WAKE_LINES
    monkeypatch.setattr(summem, "WAKE_LINES", 1)
    assert summem.WAKE_LINES == 1
    monkeypatch.undo()
    assert summem.WAKE_LINES == original
    assert original == 32


def test_test_modules_do_not_reference_load_summem():
    """Product tests request the summem fixture; they do not call load_summem."""
    tests = Path(__file__).resolve().parent
    offenders = [
        path.name
        for path in sorted(tests.glob("test_*.py"))
        if path.name != Path(__file__).name and "load_summem" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []
