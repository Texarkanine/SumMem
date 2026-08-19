"""Load the no-suffix SumMem driver for tests."""

from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "summem"


def load_summem():
    """Load repo-root `summem` via SourceFileLoader (no .py suffix)."""
    loader = SourceFileLoader("summem", str(SCRIPT))
    spec = importlib.util.spec_from_loader("summem", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load summem")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["summem"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def summem():
    return load_summem()
