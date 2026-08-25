"""First proofs 7 and 8: --path walk-up and root-wake catalog."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from conftest import SCRIPT
from gitutil import init_repo


def _run(args, cwd, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            result.stderr.decode("utf-8", "replace") or result.stdout.decode("utf-8", "replace")
        )
    return result


def _notes(store: Path) -> list[Path]:
    notes = store / "notes"
    if not notes.is_dir():
        return []
    return [p for p in notes.iterdir() if p.is_file() and not p.name.startswith(".")]


def test_note_path_lands_in_started_store_else_ancestor(tmp_path):
    """note --path writes into a started store, else the next ancestor."""
    repo = init_repo(tmp_path / "r")
    _run([sys.executable, str(SCRIPT), "start", "foo/packages/baz"], repo)
    _run(
        [sys.executable, str(SCRIPT), "note", "--path", "foo/packages/baz/fee.ts", "child"],
        repo,
    )
    _run(
        [sys.executable, str(SCRIPT), "note", "--path", "foo/packages/other/x.ts", "rootish"],
        repo,
    )
    child_notes = _notes(repo / "foo" / "packages" / "baz" / ".summem")
    root_notes = _notes(repo / ".summem")
    assert len(child_notes) == 1
    assert child_notes[0].read_text(encoding="utf-8") == "child\n"
    assert len(root_notes) == 1
    assert root_notes[0].read_text(encoding="utf-8") == "rootish\n"
    assert not (repo / "foo" / "packages" / "other" / ".summem").exists()


def test_root_wake_lists_other_stores_pull_prints_only_that_store(tmp_path):
    """Root wake lists other stores; wake --path prints that store only."""
    repo = init_repo(tmp_path / "r")
    _run([sys.executable, str(SCRIPT), "start", "pkg"], repo)
    _run([sys.executable, str(SCRIPT), "note", "root-note"], repo)
    _run([sys.executable, str(SCRIPT), "note", "--path", "pkg", "pkg-note"], repo)
    root_wake = _run([sys.executable, str(SCRIPT), "wake"], repo)
    root_out = root_wake.stdout.decode("utf-8")
    assert "root-note" in root_out
    assert "./pkg" in root_out
    assert "== Additional SumMem Catalogs ==" in root_out
    assert "== SumMem Usage ==" in root_out
    root_lines = root_out.splitlines()
    cat_start = root_lines.index("== Additional SumMem Catalogs ==")
    cat_end = (
        root_lines.index("== Project-root Memories ==")
        if "== Project-root Memories ==" in root_lines
        else len(root_lines) - 1
    )
    catalog = "\n".join(root_lines[cat_start:cat_end])
    assert "summem wake --path pkg" not in catalog
    assert ".summem/summem" not in catalog
    pull = _run([sys.executable, str(SCRIPT), "wake", "--path", "pkg"], repo)
    pull_out = pull.stdout.decode("utf-8")
    assert "pkg-note" in pull_out
    assert "root-note" not in pull_out
    assert "wake --path pkg" not in pull_out
    assert "== SumMem Usage ==" not in pull_out
