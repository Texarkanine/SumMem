"""Load the no-suffix SumMem driver for tests."""

from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "summem"
_SUMMEM = None


def dated_leaf(stamp: str, text: str) -> str:
    """Return the expected leaf wake line for a 16-character UTC stamp and note text."""
    day = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
    if text:
        return f"x1 {day}: {text}"
    return f"x1 {day}:"


def load_summem():
    """Load repo-root `summem` via SourceFileLoader (no .py suffix). Cached for the process.

    The cache is this module's `_SUMMEM`, not `sys.modules["summem"]`. migrate.py and
    surgery.py overwrite that dict entry on each CLI run.
    """
    global _SUMMEM
    if _SUMMEM is not None:
        return _SUMMEM
    loader = SourceFileLoader("summem", str(SCRIPT))
    spec = importlib.util.spec_from_loader("summem", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load summem")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["summem"] = mod
    spec.loader.exec_module(mod)
    _SUMMEM = mod
    return mod


@pytest.fixture(scope="session")
def summem():
    """Session-scoped loaded repo-root `summem` module."""
    return load_summem()
