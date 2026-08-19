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
    return [node.id for node in m.list_view(repo)]


def test_zoom_two_note_nap_prints_both_texts(tmp_path):
    """Zoom of a two-note nap prints both original texts."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap_id = m.list_view(repo)[0].id
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
    nap_id = m.list_view(repo)[0].id
    out = m.zoom_text(repo, nap_id)
    assert "alpha" in out
    assert "beta" in out


def test_zoom_loose_note_id_prints_the_note(tmp_path):
    """Zoom of a loose-note id succeeds and prints that note."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    cid = m.list_view(repo)[0].id
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


def test_zoom_nap_of_naps_prints_two_children_not_leaves(tmp_path):
    """Zoom of a nap-of-naps prints two child ids and captions, not all original texts."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["a1", "a2", "b1", "b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    parent_id = m.list_view(repo)[0].id
    out = m.zoom_text(repo, parent_id)
    lines = out.splitlines()
    assert len(lines) == 2
    captions = [line.split("  ", 1)[1] for line in lines]
    assert captions == ["pack-a", "pack-b"]


def test_zoom_accepts_unique_prefix(tmp_path):
    """zoom accepts a unique prefix of a pack id."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap_id = m.list_view(repo)[0].id
    prefix = m.short_id(nap_id, m.named_ids(repo))
    out = m.zoom_text(repo, prefix)
    assert "alpha" in out
    assert "beta" in out


def test_ambiguous_prefix_is_error(tmp_path, monkeypatch):
    """zoom raises ValueError when a prefix matches two ids."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    a = "a3f2c1b8" + "0" * 56
    b = "a3f2c1b8" + "1" * 56
    monkeypatch.setattr(m, "named_ids", lambda _parent: [a, b])
    with pytest.raises(ValueError, match="ambiguous"):
        m.zoom_text(repo, "a3f2c1b8")


def test_zoom_unreadable_tree_is_unreadable_pack(tmp_path):
    """zoom_text on a nap whose .tree is not JSON raises unreadable pack."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    nap.tree_path.write_bytes(b"{not json")
    with pytest.raises(ValueError, match="unreadable pack") as caught:
        m.zoom_text(repo, nap.id)
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
