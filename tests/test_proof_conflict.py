"""First proofs 2 and 3: caption conflict and planted conflict markers."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from random import Random

from conftest import SCRIPT, load_summem
from gitutil import init_repo

UTC = timezone.utc


def _run(args, cwd, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            result.stderr.decode("utf-8", "replace") or result.stdout.decode("utf-8", "replace")
        )
    return result


def test_same_pair_two_captions_conflict_only_on_sum(tmp_path, monkeypatch):
    """Two nappers of the same pair conflict on .sum only; both resolutions wake and zoom."""
    m = load_summem()
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    main = init_repo(tmp_path / "main")
    _run([sys.executable, str(SCRIPT), "note", "alpha"], main)
    _run([sys.executable, str(SCRIPT), "note", "beta"], main)
    _run(["git", "add", ".summem"], main)
    _run(["git", "commit", "-m", "two notes"], main)

    ids = [node.id for node in m.list_view(main)]
    assert len(ids) == 2

    wt_a = tmp_path / "wt-a"
    wt_b = tmp_path / "wt-b"
    _run(["git", "worktree", "add", "-b", "nap-a", str(wt_a)], main)
    _run(["git", "worktree", "add", "-b", "nap-b", str(wt_b)], main)

    def nap_and_commit(tree, caption):
        noted = _run([sys.executable, str(SCRIPT), "nap", ids[0], ids[1], caption], tree)
        assert noted.returncode == 0
        _run(["git", "add", "-A"], tree)
        _run(["git", "commit", "-m", caption], tree)

    nap_and_commit(wt_a, "ours caption")
    nap_and_commit(wt_b, "theirs caption")

    merged = _run(["git", "merge", "--no-edit", "nap-b"], wt_a, check=False)
    assert merged.returncode != 0
    unmerged = _run(["git", "diff", "--name-only", "--diff-filter=U"], wt_a)
    names = [line for line in unmerged.stdout.decode("utf-8").splitlines() if line]
    assert names
    assert all(name.endswith(".sum") for name in names)
    assert not any(name.endswith(".tree") for name in names)
    sumfile = names[0]

    def check_resolution(which, expected, forbidden):
        _run(["git", "checkout", f"--{which}", "--", sumfile], wt_a)
        wake_out = m.wake_text(wt_a)
        assert expected in wake_out
        assert forbidden not in wake_out
        nap_id = wake_out.splitlines()[0].split()[0]
        zoom_out = _run([sys.executable, str(SCRIPT), "zoom", nap_id], wt_a).stdout.decode("utf-8")
        assert "alpha" in zoom_out
        assert "beta" in zoom_out

    check_resolution("ours", "ours caption", "theirs caption")
    check_resolution("theirs", "theirs caption", "ours caption")


def test_planted_conflict_markers_wake_skips_caption_zoom_prints_leaves(tmp_path, monkeypatch):
    """Planted <<<<<<< in a .sum: wake omits the caption; zoom still prints the leaves."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "secret caption")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    sums[0].write_text("<<<<<<< HEAD\nsecret caption\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    wake = m.wake_text(repo)
    assert "secret caption" not in wake
    assert "<<<<<<<" not in wake
    nap_id = wake.splitlines()[0].split()[0]
    assert len(nap_id) == 64
    assert "(2 notes, from 2026-01-01)" in wake
    zoom = m.zoom_text(repo, nap_id)
    assert "alpha" in zoom
    assert "beta" in zoom
