"""Binary nap writer: two adjacent notes, parent files, then unlink children."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

import pytest

from conftest import dated_leaf, load_summem
from gitutil import init_repo

UTC = timezone.utc


def _two_notes(m, repo, a="alpha", b="beta"):
    pa = m.write_note(repo, a, datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    pb = m.write_note(repo, b, datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    return pa, pb


def _ids(m, repo):
    return [node.id for node in m.list_view(repo)]


def _payload_names(repo: Path) -> set[str]:
    names = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def test_nap_two_adjacent_notes_writes_pair_and_unlinks(tmp_path, monkeypatch):
    """Two adjacent notes become one nap pair; both notes are gone."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa, pb = _two_notes(m, repo)
    da = m.note_digest(pa.read_bytes())
    db = m.note_digest(pb.read_bytes())
    leafset = m.leafset_id([da, db])
    stem = f"{pa.name}-{leafset}-2"
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
    assert sum_path == naps / f"{stem}.summ"
    assert tree_path.read_bytes() == m.dumps_tree(expected)
    assert sum_path.read_bytes() == b"pair\n"
    assert not pa.exists()
    assert not pb.exists()
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    nap = m.list_view(repo)[0]
    prefix = m.short_id(nap.id, [nap.id])
    lines = m.wake_text(repo).splitlines()
    assert lines == [f"x2 {prefix}: pair"]


def test_same_children_same_tree_bytes_and_paths(tmp_path):
    """Same two notes and different captions share .tree bytes and dest paths."""
    m = load_summem()
    repo_a = init_repo(tmp_path / "a")
    repo_b = init_repo(tmp_path / "b")
    _two_notes(m, repo_a)
    _two_notes(m, repo_b)
    ids = _ids(m, repo_a)
    # Same text and timestamps in both repos → same content ids.
    m.write_nap(repo_a, ids[0], ids[1], "one")
    m.write_nap(repo_b, ids[0], ids[1], "two")
    naps_a = sorted(p.name for p in (repo_a / ".summem" / "naps").iterdir() if not p.name.startswith("."))
    naps_b = sorted(p.name for p in (repo_b / ".summem" / "naps").iterdir() if not p.name.startswith("."))
    assert naps_a == naps_b
    tree_name = [name for name in naps_a if name.endswith(".tree")][0]
    assert (repo_a / ".summem" / "naps" / tree_name).read_bytes() == (
        repo_b / ".summem" / "naps" / tree_name
    ).read_bytes()
    sum_name = tree_name.removesuffix(".tree") + ".summ"
    assert (repo_a / ".summem" / "naps" / sum_name).read_bytes() != (
        repo_b / ".summem" / "naps" / sum_name
    ).read_bytes()


def test_first_unlink_sees_both_parent_files(tmp_path, monkeypatch):
    """At the first child unlink, both parent .summ and .tree already exist."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    seen = {}
    real = m.Path.unlink

    def wrapped(self, *args, **kwargs):
        if not seen:
            naps = repo / ".summem" / "naps"
            seen["sum"] = list(naps.glob("*.summ"))
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
    assert list(naps.glob("*.summ")) == []
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


def test_nap_overlong_caption_message_is_a_ratchet(tmp_path):
    """An over-long nap caption names actual UTF-8 bytes, the limit, and the compress hint."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    caption = "x" * (m.ENTRY_CHARS + 1)
    with pytest.raises(ValueError) as caught:
        m.write_nap(repo, ids[0], ids[1], caption)
    err = str(caught.value)
    assert str(len(caption.encode("utf-8"))) in err
    assert str(m.ENTRY_CHARS) in err
    assert "Accented characters cost 2 bytes" in err
    assert "Compress it further" in err
    assert _payload_names(repo) == before


def test_nap_rejects_newline_caption(tmp_path):
    """A caption with a newline is rejected and the store is unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError) as caught:
        m.write_nap(repo, ids[0], ids[1], "hello\n")
    err = str(caught.value)
    assert "One line only" in err
    assert "Merge the lines" in err
    assert "note each line" not in err.lower()
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
    assert "not adjacent" in err
    assert "sit next to each other in wake" in err
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
    assert "unknown id" in err
    assert "Copy an id from wake" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert _payload_names(repo) == before


def test_nap_missing_tree_unknown_id_has_no_wake_hint(tmp_path):
    """A view nap with no .tree raises unknown id and does not say to copy from wake."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    nap = next(n for n in m.list_view(repo) if n.kind == "nap")
    note = next(n for n in m.list_view(repo) if n.kind == "note")
    nap.tree_path.unlink()
    with pytest.raises(ValueError) as caught:
        m.write_nap(repo, nap.id, note.id, "nope")
    err = str(caught.value)
    assert "unknown id" in err
    assert "Copy an id from wake" not in err


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
    assert trees[0].name.split("-")[-2] == m.leafset_id(digests)
    assert {kid.sum for kid in tree.kids} == {"pack-a", "pack-b"}
    out = m.zoom_text(repo, tree.kids[0].id)
    assert out.splitlines() == [
        dated_leaf("20260101T000001Z", "a1"),
        dated_leaf("20260101T000002Z", "a2"),
    ]


def test_napchild_sum_empty_when_child_sum_missing(tmp_path):
    """Napping a child whose .summ is missing stores an empty NapChild.sum."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "a1", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "a2", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "b1", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "b2", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    sums = sorted((repo / ".summem" / "naps").glob("*.summ"))
    sums[0].unlink()
    nap_ids = _ids(m, repo)
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    tree = m.loads_tree(next((repo / ".summem" / "naps").glob("*.tree")).read_bytes())
    assert tree.kids[0].sum == ""
    out = m.zoom_text(repo, tree.kids[0].id)
    assert "a1" in out and "a2" in out


def test_napchild_sum_empty_when_child_sum_conflict(tmp_path):
    """Napping a child whose .summ is conflict-marked stores an empty NapChild.sum."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "a1", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "a2", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "b1", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "b2", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    sums = sorted((repo / ".summem" / "naps").glob("*.summ"))
    sums[0].write_text("<" * 7 + " HEAD\npack-a\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    nap_ids = _ids(m, repo)
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    tree = m.loads_tree(next((repo / ".summem" / "naps").glob("*.tree")).read_bytes())
    assert tree.kids[0].sum == ""
    out = m.zoom_text(repo, tree.kids[0].id)
    assert "a1" in out and "a2" in out


def test_nap_two_identical_notes_by_repeated_id(tmp_path, monkeypatch):
    """Two adjacent notes with the same text share an id and can still be napped."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = _ids(m, repo)
    assert ids[0] == ids[1]
    m.write_nap(repo, ids[0], ids[1], "twins")
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert notes == []
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    lines = m.wake_text(repo).splitlines()
    assert len(lines) == 1
    assert lines[0].endswith("twins")
    assert lines[0].startswith("x2 ")
    assert "2026-" not in lines[0]


def _agent_err(err: str) -> None:
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_write_nap_overlapping_adjacent_naps_raises(tmp_path):
    """Adjacent naps whose leaf-sets intersect raise before writing a parent."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    shared = m.NoteChild(name="20260101T000002Z-bbbbbbbbbbbbbbbb", text="B")
    left = m.NapChild(
        id=m.leafset_id(
            [m.note_digest(m.note_file_bytes("A")), m.note_digest(m.note_file_bytes("B"))]
        ),
        sum="ab",
        tree=m.Tree(
            kids=[
                m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="A"),
                shared,
            ]
        ),
    )
    right = m.NapChild(
        id=m.leafset_id(
            [m.note_digest(m.note_file_bytes("B")), m.note_digest(m.note_file_bytes("C"))]
        ),
        sum="bc",
        tree=m.Tree(
            kids=[
                shared,
                m.NoteChild(name="20260101T000003Z-cccccccccccccccc", text="C"),
            ]
        ),
    )
    m.rematerialize_child(repo, left)
    m.rematerialize_child(repo, right)
    ids = _ids(m, repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError, match="overlapping packs") as caught:
        m.write_nap(repo, ids[0], ids[1], "nope")
    _agent_err(str(caught.value))
    assert _payload_names(repo) == before


def test_write_nap_note_inside_adjacent_nap_raises(tmp_path):
    """A note whose digest sits in the adjacent nap is overlapping packs."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa, _pb = _two_notes(m, repo)
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = m.list_view(repo)[0]
    tree = m.loads_tree(nap.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    nodes = m.list_view(repo)
    before = _payload_names(repo)
    with pytest.raises(ValueError, match="overlapping packs") as caught:
        m.write_nap(repo, nodes[0].id, nodes[1].id, "nope")
    _agent_err(str(caught.value))
    assert _payload_names(repo) == before
    assert pa.name in _payload_names(repo)


def test_write_nap_disjoint_adjacent_naps_still_concat(tmp_path):
    """Disjoint adjacent naps still unlink and concat."""
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
    assert all(isinstance(kid, m.NapChild) for kid in tree.kids)


def test_write_nap_identical_text_notes_still_concat(tmp_path):
    """Two identical-text notes still concat; the overlap guard requires a nap."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "twins")
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert notes == []
    trees = list((repo / ".summem" / "naps").glob("*.tree"))
    assert len(trees) == 1


def test_write_nap_malformed_tree_raises_unreadable_pack(tmp_path):
    """A selected nap whose .tree is malformed raises ValueError without store paths."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_notes(m, repo)
    ids = _ids(m, repo)
    m.write_nap(repo, ids[0], ids[1], "pair")
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    nap = next(n for n in m.list_view(repo) if n.kind == "nap")
    note = next(n for n in m.list_view(repo) if n.kind == "note")
    nap.tree_path.write_bytes(b"{not json")
    before = _payload_names(repo)
    with pytest.raises(ValueError, match="unreadable pack") as caught:
        m.write_nap(repo, nap.id, note.id, "nope")
    _agent_err(str(caught.value))
    assert _payload_names(repo) == before

