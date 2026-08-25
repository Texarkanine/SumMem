"""Load the no-suffix SumMem driver for tests."""

from __future__ import annotations

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "summem"


def dated_leaf(stamp: str, text: str) -> str:
    """Return the expected leaf wake line for a 16-character UTC stamp and note text."""
    day = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
    if text:
        return f"x1 {day}: {text}"
    return f"x1 {day}:"


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
