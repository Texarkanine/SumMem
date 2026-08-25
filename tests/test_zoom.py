"""One-level zoom of a nap or a loose note."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

import pytest

from conftest import dated_leaf, load_summem
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
    assert lines[0] == dated_leaf("20260101T000001Z", "alpha")
    assert lines[1] == dated_leaf("20260101T000002Z", "beta")


def test_zoom_conflict_sum_still_prints_leaves(tmp_path):
    """Conflict markers in the parent .summ do not affect zoom of the leaves."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.summ"))
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
    assert m.zoom_text(repo, cid) == dated_leaf("20260101T000000Z", "hello") + "\n"


def test_zoom_unknown_id_omits_store_paths_and_git(tmp_path):
    """Unknown zoom id is rejected without mentioning notes/, naps/, or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError) as caught:
        m.zoom_text(repo, "0" * 64)
    err = str(caught.value)
    assert "unknown id" in err
    assert "Copy an id from wake" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_zoom_missing_tree_unknown_id_has_no_wake_hint(tmp_path):
    """Zoom of a view nap with no .tree says unknown id and does not say to copy from wake."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    nap.tree_path.unlink()
    with pytest.raises(ValueError) as caught:
        m.zoom_text(repo, nap.id)
    err = str(caught.value)
    assert "unknown id" in err
    assert "Copy an id from wake" not in err


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
    parent = m.list_view(repo)[0]
    out = m.zoom_text(repo, parent.id)
    lines = out.splitlines()
    assert len(lines) == 2
    ids = m.named_ids(repo)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    want = [m.format_wake_line(m._projected_child(child), ids) for child in tree.kids]
    assert lines == want
    assert all(len(m.short_id(child.id, ids)) == 8 for child in tree.kids)


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
    with pytest.raises(ValueError, match="ambiguous") as caught:
        m.zoom_text(repo, "a3f2c1b8")
    assert "Give a longer prefix" in str(caught.value)


def test_zoom_skips_unreadable_sibling_warns(tmp_path, capsys):
    """Zoom of a nested id still works and warns when a sibling children file is unreadable."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "A", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "B", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ab = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ab[0], ab[1], "ab")
    m.write_note(repo, "C", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "D", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "cd")
    naps = [node for node in m.list_view(repo) if node.kind == "nap"]
    first, second = naps[0], naps[1]
    tree = m.loads_tree(second.tree_path.read_bytes())
    child_id = m.leafset_id([m.note_digest(m.note_file_bytes(tree.kids[0].text))])
    first.tree_path.write_bytes(b"{not json")
    capsys.readouterr()
    out = m.zoom_text(repo, child_id)
    assert tree.kids[0].text in out
    err = capsys.readouterr().err
    assert err == "skipped a pack\n"
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert "Traceback" not in err


def test_named_ids_skips_non_mapping_tree_child(tmp_path):
    """A children file whose child is not a mapping does not make named_ids raise."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    nap.tree_path.write_bytes(b'{"c":[1]}\n')
    named = m.named_ids(repo)
    assert nap.id in named


def test_zoom_non_mapping_child_is_unreadable_pack(tmp_path, capsys):
    """zoom_text on a nap whose tree child is not a mapping raises unreadable pack."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    nap.tree_path.write_bytes(b'{"c":[1]}\n')
    capsys.readouterr()
    with pytest.raises(ValueError, match="unreadable pack") as caught:
        m.zoom_text(repo, nap.id)
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert capsys.readouterr().err == ""


def test_zoom_skips_sibling_non_mapping_child_warns(tmp_path, capsys):
    """Zoom of a nested id still works and warns when a sibling tree child is not a mapping."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "A", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "B", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ab = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ab[0], ab[1], "ab")
    m.write_note(repo, "C", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "D", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "cd")
    naps = [node for node in m.list_view(repo) if node.kind == "nap"]
    first, second = naps[0], naps[1]
    tree = m.loads_tree(second.tree_path.read_bytes())
    child_id = m.leafset_id([m.note_digest(m.note_file_bytes(tree.kids[0].text))])
    first.tree_path.write_bytes(b'{"c":[1]}\n')
    capsys.readouterr()
    out = m.zoom_text(repo, child_id)
    assert tree.kids[0].text in out
    err = capsys.readouterr().err
    assert err == "skipped a pack\n"
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert "Traceback" not in err


def test_zoom_unreadable_tree_is_unreadable_pack(tmp_path, capsys):
    """zoom_text on a nap whose .tree is not JSON raises unreadable pack."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    nap.tree_path.write_bytes(b"{not json")
    capsys.readouterr()
    with pytest.raises(ValueError, match="unreadable pack") as caught:
        m.zoom_text(repo, nap.id)
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert capsys.readouterr().err == ""


def test_zoom_nested_note_id_prints_dated_leaf(tmp_path):
    """Zoom of a note id that lives only inside a children file prints a dated leaf."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    ids = _two_notes(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    tree = m.loads_tree(nap.tree_path.read_bytes())
    child = tree.kids[0]
    cid = m.leafset_id([m.note_digest(m.note_file_bytes(child.text))])
    stamp = child.name.split("-")[0]
    assert m.zoom_text(repo, cid) == dated_leaf(stamp, child.text) + "\n"
