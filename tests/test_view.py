"""Pair-aware view: notes plus nap stems, including a missing .sum."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def _nap_two(m, repo):
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")
    return ids


def test_view_includes_nap_stem_when_sum_is_missing(tmp_path):
    """A .tree without a .sum is still one view node."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _nap_two(m, repo)
    naps = repo / ".summem" / "naps"
    sums = list(naps.glob("*.sum"))
    assert len(sums) == 1
    leafset = sums[0].name.split("-")[1]
    sums[0].unlink()
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].id == leafset
    assert nodes[0].caption == ""


def test_view_includes_nap_stem_when_sum_has_conflict_markers(tmp_path):
    """A .sum containing <<<<<<< is still one view node."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _nap_two(m, repo)
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    leafset = sums[0].name.split("-")[1]
    sums[0].write_text("<<<<<<< HEAD\npair\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].id == leafset
    assert nodes[0].caption == ""


def test_view_sorts_notes_and_naps_by_filename(tmp_path):
    """Mixed notes and naps sort by filename, not by kind."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")
    nodes = m.list_view(repo)
    assert [node.kind for node in nodes] == ["nap", "note"]
    assert nodes[0].name < nodes[1].name
    assert nodes[1].caption == "gamma"
