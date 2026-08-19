"""Zipper-heal: leaf-sets, rematerialize, overlapping packs, flock."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def _write_notes(m, repo, texts, start=1):
    paths = []
    for i, text in enumerate(texts, start=start):
        paths.append(
            m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
        )
    return paths


def _payload_names(repo: Path) -> set[str]:
    names = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def test_leaf_digests_of_note_is_its_digest(tmp_path):
    """A note's leaf-set is the digest of its file bytes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    path = _write_notes(m, repo, ["alpha"])[0]
    node = m.list_view(repo)[0]
    assert m.leaf_digests(node) == {m.note_digest(path.read_bytes())}


def test_leaf_digests_of_nap_is_union_of_tree_digests(tmp_path):
    """A nap's leaf-set is the set of digests in its canonical tree."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    texts = ["alpha", "beta"]
    _write_notes(m, repo, texts)
    expected = {m.note_digest(m.note_file_bytes(text)) for text in texts}
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    assert m.leaf_digests(node) == expected


def test_leaf_digests_none_when_tree_missing_or_malformed(tmp_path):
    """Missing, unreadable, or malformed .tree yields no leaf-set."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["alpha", "beta", "gamma", "delta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    m.write_nap(repo, ids[2], ids[3], "cd")
    nodes = m.list_view(repo)
    assert m.leaf_digests(nodes[0]) is not None
    nodes[0].tree_path.write_bytes(b"{not json")
    assert m.leaf_digests(nodes[0]) is None
    nodes[1].tree_path.unlink()
    assert m.leaf_digests(m.list_view(repo)[1]) is None
    _write_notes(m, repo, ["epsilon", "zeta"], start=5)
    ids = [node.id for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "ez")
    ez = [node for node in m.list_view(repo) if node.kind == "nap" and node.caption == "ez"][0]
    ez.tree_path.write_bytes(b'{"v":1}\n')
    assert m.leaf_digests(ez) is None


def test_two_identical_notes_stay(tmp_path):
    """Two notes with the same text are not unlinked by leaf-set helpers."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    paths = _write_notes(m, repo, ["hello", "hello"])
    nodes = m.list_view(repo)
    digest = m.note_digest(paths[0].read_bytes())
    assert m.leaf_digests(nodes[0]) == {digest}
    assert m.leaf_digests(nodes[1]) == {digest}
    assert paths[0].is_file() and paths[1].is_file()


def test_rematerialize_note_writes_name_and_bytes(tmp_path):
    """A NoteChild is written to notes/{name} with note_file_bytes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    child = m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="alpha")
    m.rematerialize_child(repo, child)
    dest = repo / ".summem" / "notes" / child.name
    assert dest.read_bytes() == m.note_file_bytes("alpha")


def test_rematerialize_nap_stem_uses_leftmost_seq_child_id_and_leaves(tmp_path):
    """A NapChild stem is {leftmost NoteChild seq}-{child.id}-{leaves}."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    paths = _write_notes(m, repo, ["alpha", "beta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    inner = m.loads_tree(node.tree_path.read_bytes())
    child = m.NapChild(id=node.id, sum=node.caption, tree=inner)
    m._unlink_node(node)
    m.rematerialize_child(repo, child)
    leftmost = m._seq_prefix(paths[0].name)
    leaves = len(m._digests_of_tree(inner))
    stem = f"{leftmost}-{child.id}-{leaves}"
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.tree").read_bytes() == m.dumps_tree(inner)
    assert (naps / f"{stem}.sum").read_bytes() == m.note_file_bytes("pair")
    assert m._nap_stem(child) == stem


def test_rematerialize_does_not_clobber_existing_dest(tmp_path):
    """A second rematerialize leaves an existing dest unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    name = "20260101T000001Z-aaaaaaaaaaaaaaaa"
    dest = repo / ".summem" / "notes" / name
    dest.write_bytes(m.note_file_bytes("kept"))
    m.rematerialize_child(repo, m.NoteChild(name=name, text="new"))
    assert dest.read_bytes() == m.note_file_bytes("kept")
    repo2 = init_repo(tmp_path / "r2")
    _write_notes(m, repo2, ["alpha", "beta"], start=10)
    ids = [node.id for node in m.list_view(repo2)]
    m.write_nap(repo2, ids[0], ids[1], "pair")
    node = m.list_view(repo2)[0]
    inner = m.loads_tree(node.tree_path.read_bytes())
    child = m.NapChild(id=node.id, sum="other", tree=inner)
    tree_bytes = node.tree_path.read_bytes()
    sum_bytes = node.sum_path.read_bytes()
    m.rematerialize_child(repo2, child)
    assert node.tree_path.read_bytes() == tree_bytes
    assert node.sum_path.read_bytes() == sum_bytes
    assert m._nap_stem(child) == node.name
