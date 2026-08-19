"""Binary nap writer: two adjacent notes, parent files, then unlink children."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

import pytest

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def _two_notes(m, repo, a="alpha", b="beta"):
    pa = m.write_note(repo, a, datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    pb = m.write_note(repo, b, datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    return pa, pb


def _ids(m, repo):
    return [line.split()[0] for line in m.wake_text(repo).splitlines() if line]


def _payload_names(repo: Path) -> set[str]:
    names = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def test_nap_two_adjacent_notes_writes_pair_and_unlinks(tmp_path):
    """Two adjacent notes become one nap pair; both notes are gone."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa, pb = _two_notes(m, repo)
    da = m.note_digest(pa.read_bytes())
    db = m.note_digest(pb.read_bytes())
    leafset = m.leafset_id([da, db])
    min_stamp = pa.name.split("-")[0]
    stem = f"{min_stamp}-{leafset}-2"
    expected = m.Tree(
        kids=[
            m.NoteChild(name=pa.name, text="alpha"),
            m.NoteChild(name=pb.name, text="beta"),
        ]
    )
    id_a, id_b = _ids(m, repo)
    sum_path = m.write_nap(repo, id_a, id_b, "pair")
    naps = repo / ".summem" / "naps"
    tree_path = naps / f"{stem}.tree"
    assert sum_path == naps / f"{stem}.sum"
    assert tree_path.read_bytes() == m.dumps_tree(expected)
    assert sum_path.read_bytes() == b"pair\n"
    assert not pa.exists()
    assert not pb.exists()
    lines = m.wake_text(repo).splitlines()
    assert lines == [f"{leafset}  (2 notes, from 2026-01-01)  pair"]


def test_same_children_same_tree_bytes_and_paths(tmp_path):
    """Same two notes and different captions share .tree bytes and dest paths."""
    m = load_summem()
    repo_a = init_repo(tmp_path / "a")
    repo_b = init_repo(tmp_path / "b")
    _two_notes(m, repo_a)
    _two_notes(m, repo_b)
    ids = _ids(m, repo_a)
    m.write_nap(repo_a, ids[0], ids[1], "one")
    m.write_nap(repo_b, ids[0], ids[1], "two")
    naps_a = sorted(p.name for p in (repo_a / ".summem" / "naps").iterdir() if not p.name.startswith("."))
    naps_b = sorted(p.name for p in (repo_b / ".summem" / "naps").iterdir() if not p.name.startswith("."))
    assert naps_a == naps_b
    tree_name = [name for name in naps_a if name.endswith(".tree")][0]
    assert (repo_a / ".summem" / "naps" / tree_name).read_bytes() == (
        repo_b / ".summem" / "naps" / tree_name
    ).read_bytes()
    sum_name = tree_name.removesuffix(".tree") + ".sum"
    assert (repo_a / ".summem" / "naps" / sum_name).read_bytes() != (
        repo_b / ".summem" / "naps" / sum_name
    ).read_bytes()


def test_first_unlink_sees_both_parent_files(tmp_path, monkeypatch):
    """At the first child unlink, both parent .sum and .tree already exist."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    seen = {}
    real = m.Path.unlink

    def wrapped(self, *args, **kwargs):
        if not seen:
            naps = repo / ".summem" / "naps"
            seen["sum"] = list(naps.glob("*.sum"))
            seen["tree"] = list(naps.glob("*.tree"))
        return real(self, *args, **kwargs)

    monkeypatch.setattr(m.Path, "unlink", wrapped)
    m.write_nap(repo, ids[0], ids[1], "pair")
    assert seen["sum"] and seen["tree"]


def test_tree_replace_failure_leaves_children(tmp_path, monkeypatch):
    """If parent .tree replace fails, both notes remain and no nap pair is left."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa, pb = _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    real = m.os.replace

    def wrapped(src, dst):
        dest = Path(dst)
        if dest.suffix == ".tree" and dest.parent.name == "naps":
            raise OSError("injected tree replace failure")
        return real(src, dst)

    monkeypatch.setattr(m.os, "replace", wrapped)
    with pytest.raises(OSError, match="injected tree replace failure"):
        m.write_nap(repo, ids[0], ids[1], "pair")
    assert pa.exists() and pb.exists()
    naps = repo / ".summem" / "naps"
    assert list(naps.glob("*.sum")) == []
    assert list(naps.glob("*.tree")) == []
    assert _payload_names(repo) == before


def test_nap_rejects_empty_caption(tmp_path):
    """An empty caption is rejected and the store is unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError):
        m.write_nap(repo, ids[0], ids[1], "")
    assert _payload_names(repo) == before


def test_nap_rejects_overlong_caption(tmp_path):
    """A caption over ENTRY_CHARS is rejected and the store is unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError):
        m.write_nap(repo, ids[0], ids[1], "x" * (m.ENTRY_CHARS + 1))
    assert _payload_names(repo) == before


def test_nap_rejects_newline_caption(tmp_path):
    """A caption with a newline is rejected and the store is unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError):
        m.write_nap(repo, ids[0], ids[1], "hello\n")
    assert _payload_names(repo) == before


def test_nap_rejects_non_adjacent_ids(tmp_path):
    """Non-adjacent ids are rejected without mentioning store paths or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError) as caught:
        m.write_nap(repo, ids[0], ids[2], "skip")
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert _payload_names(repo) == before


def test_nap_rejects_unknown_id(tmp_path):
    """An unknown id is rejected without mentioning store paths or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError) as caught:
        m.write_nap(repo, ids[0], "0" * 64, "pair")
    err = str(caught.value)
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert _payload_names(repo) == before


def test_nap_of_two_naps_nests_napchild_and_unions_digests(tmp_path):
    """A nap of two naps stores NapChild nodes and the union of original digests."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    texts = ["a1", "a2", "b1", "b2"]
    for i, text in enumerate(texts, start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = _ids(m, repo)
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    trees = list((repo / ".summem" / "naps").glob("*.tree"))
    assert len(trees) == 1
    tree = m.loads_tree(trees[0].read_bytes())
    assert len(tree.kids) == 2
    assert all(isinstance(kid, m.NapChild) for kid in tree.kids)
    digests = [m.note_digest(m.note_file_bytes(text)) for text in texts]
    assert trees[0].name.split("-")[1] == m.leafset_id(digests)
    assert {kid.sum for kid in tree.kids} == {"pack-a", "pack-b"}
    out = m.zoom_text(repo, tree.kids[0].id)
    suffixes = [line.split("  ", 1)[1] for line in out.splitlines()]
    assert suffixes == ["a1", "a2"]


def test_napchild_sum_empty_when_child_sum_missing(tmp_path):
    """Napping a child whose .sum is missing stores an empty NapChild.sum."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "a1", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "a2", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "b1", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "b2", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    sums = sorted((repo / ".summem" / "naps").glob("*.sum"))
    sums[0].unlink()
    nap_ids = _ids(m, repo)
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    tree = m.loads_tree(next((repo / ".summem" / "naps").glob("*.tree")).read_bytes())
    assert tree.kids[0].sum == ""
    out = m.zoom_text(repo, tree.kids[0].id)
    assert "a1" in out and "a2" in out


def test_napchild_sum_empty_when_child_sum_conflict(tmp_path):
    """Napping a child whose .sum is conflict-marked stores an empty NapChild.sum."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "a1", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "a2", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "b1", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "b2", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    sums = sorted((repo / ".summem" / "naps").glob("*.sum"))
    sums[0].write_text("<" * 7 + " HEAD\npack-a\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    nap_ids = _ids(m, repo)
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    tree = m.loads_tree(next((repo / ".summem" / "naps").glob("*.tree")).read_bytes())
    assert tree.kids[0].sum == ""
    out = m.zoom_text(repo, tree.kids[0].id)
    assert "a1" in out and "a2" in out
