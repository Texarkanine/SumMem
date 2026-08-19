"""First proof 1: two worktrees note, merge, both notes in the view."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import SCRIPT
from gitutil import init_repo


def _run(args, cwd, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(result.stderr.decode("utf-8", "replace") or result.stdout.decode("utf-8", "replace"))
    return result


def test_two_worktrees_note_merge_without_conflict(tmp_path):
    """Two worktrees each note once; merge has zero conflicts; wake shows both texts."""
    main = init_repo(tmp_path / "main")
    wt_a = tmp_path / "wt-a"
    wt_b = tmp_path / "wt-b"
    _run(["git", "worktree", "add", "-b", "wt-a", str(wt_a)], main)
    _run(["git", "worktree", "add", "-b", "wt-b", str(wt_b)], main)

    def note_and_commit(tree: Path, text: str) -> None:
        noted = _run([sys.executable, str(SCRIPT), "note", text], tree)
        assert noted.returncode == 0
        _run(["git", "add", ".summem"], tree)
        _run(["git", "commit", "-m", text], tree)

    note_and_commit(wt_a, "alpha")
    note_and_commit(wt_b, "beta")

    merged_a = _run(["git", "merge", "--no-edit", "wt-a"], main)
    merged_b = _run(["git", "merge", "--no-edit", "wt-b"], main)
    assert merged_a.returncode == 0
    assert merged_b.returncode == 0
    for path in (main / ".summem").rglob("*"):
        if path.is_file():
            assert b"<<<<<<<" not in path.read_bytes()
            assert b"=======" not in path.read_bytes()
            assert b">>>>>>>" not in path.read_bytes()

    wake = _run([sys.executable, str(SCRIPT), "wake"], main)
    out = wake.stdout.decode("utf-8")
    assert "alpha" in out
    assert "beta" in out
    lines = [line for line in out.splitlines() if line]
    assert len(lines) == 2
    assert set(lines) == {"alpha", "beta"}
