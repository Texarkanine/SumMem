"""One-level zoom of a nap or a loose note."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

import pytest

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def _two_notes(m, repo):
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    return [line.split()[0] for line in m.wake_text(repo).splitlines() if line]


def test_zoom_two_note_nap_prints_both_texts(tmp_path):
    """Zoom of a two-note nap prints both original texts."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap_id = m.wake_text(repo).splitlines()[0].split()[0]
    out = m.zoom_text(repo, nap_id)
    lines = out.splitlines()
    assert len(lines) == 2
    assert lines[0] == f"{ids[0]}  alpha"
    assert lines[1] == f"{ids[1]}  beta"


def test_zoom_conflict_sum_still_prints_leaves(tmp_path):
    """Conflict markers in the parent .sum do not affect zoom of the leaves."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    sums[0].write_text("<<<<<<< HEAD\npair\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    nap_id = m.wake_text(repo).splitlines()[0].split()[0]
    out = m.zoom_text(repo, nap_id)
    assert "alpha" in out
    assert "beta" in out


def test_zoom_loose_note_id_prints_the_note(tmp_path):
    """Zoom of a loose-note id succeeds and prints that note."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    cid = m.wake_text(repo).splitlines()[0].split()[0]
    assert m.zoom_text(repo, cid) == f"{cid}  hello\n"


def test_zoom_unknown_id_omits_store_paths_and_git(tmp_path):
    """Unknown zoom id is rejected without mentioning notes/, naps/, or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError) as caught:
        m.zoom_text(repo, "0" * 64)
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
