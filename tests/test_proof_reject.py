"""First proof 5: nap rejects ranges and missing ids without writing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import SCRIPT
from gitutil import init_repo


def _run_nap(cwd, extra):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "nap", *extra],
        cwd=cwd,
        capture_output=True,
    )


def _payload_files(repo: Path) -> list[Path]:
    store = repo / ".summem"
    if not store.is_dir():
        return []
    out = []
    for folder in ("notes", "naps"):
        root = store / folder
        if not root.is_dir():
            continue
        out.extend(p for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return out


def test_nap_help_exits_zero():
    """nap --help exits 0 because nap is a known subcommand."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "nap", "--help"],
        capture_output=True,
    )
    assert result.returncode == 0
    err = result.stderr.decode("utf-8", "replace").lower()
    assert "invalid choice" not in err


def test_nap_range_16_31_rejected_without_writing(tmp_path):
    """Process nap 16-31 … exits nonzero, names that token, writes no store files."""
    repo = init_repo(tmp_path / "r")
    result = _run_nap(repo, ["16-31", "aaaaaaaa", "caption"])
    err = result.stderr.decode("utf-8", "replace")
    assert result.returncode != 0
    assert "16-31" in err
    assert "invalid choice" not in err.lower()
    assert _payload_files(repo) == []


def test_nap_hash_range_rejected_without_writing(tmp_path):
    """Process nap #2-5 … exits nonzero, names that token, writes no store files."""
    repo = init_repo(tmp_path / "r")
    result = _run_nap(repo, ["#2-5", "aaaaaaaa", "caption"])
    err = result.stderr.decode("utf-8", "replace")
    assert result.returncode != 0
    assert "#2-5" in err
    assert "invalid choice" not in err.lower()
    assert _payload_files(repo) == []


def test_nap_no_ids_rejected_without_writing(tmp_path):
    """Process nap with no ids exits nonzero without calling nap an unknown command."""
    repo = init_repo(tmp_path / "r")
    result = _run_nap(repo, [])
    err = result.stderr.decode("utf-8", "replace")
    assert result.returncode != 0
    assert "invalid choice" not in err.lower()
    assert _payload_files(repo) == []
