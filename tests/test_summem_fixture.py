"""Session-scoped summem fixture contract."""

from __future__ import annotations

from pathlib import Path

import conftest
from conftest import SCRIPT


def test_summem_fixture_is_session_scoped():
    """The summem fixture is session-scoped."""
    marker = getattr(conftest.summem, "_fixture_function_marker", None)
    assert marker is not None
    assert marker.scope == "session"


def test_summem_is_repo_root_driver(summem):
    """The summem fixture is the SourceFileLoader module for repo-root summem."""
    assert summem.__file__ == str(SCRIPT)
    assert hasattr(summem, "main")


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
