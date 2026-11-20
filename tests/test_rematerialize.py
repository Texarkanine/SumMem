"""Leaf digests, child rematerialization, and write_nap node reuse."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from gitutil import balanced_4, init_repo, write_notes

UTC = timezone.utc


def test_leaf_digests_of_note_is_its_digest(tmp_path, summem):
    """A note's leaf-set is the digest of its file bytes."""
    m = summem
    repo = init_repo(tmp_path / "r")
    path = write_notes(m, repo, ["alpha"])[0]
    node = m.list_view(repo)[0]
    assert m.leaf_digests(node) == {m.note_digest(path.read_bytes())}


def test_leaf_digests_of_nap_is_union_of_tree_digests(tmp_path, summem):
    """A nap's leaf-set is the set of digests in its canonical tree."""
    m = summem
    repo = init_repo(tmp_path / "r")
    texts = ["alpha", "beta"]
    write_notes(m, repo, texts)
    expected = {m.note_digest(m.note_file_bytes(text)) for text in texts}
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    assert m.leaf_digests(node) == expected


def test_leaf_digests_none_when_tree_missing_or_malformed(tmp_path, summem):
    """Missing, unreadable, or malformed .tree yields no leaf-set."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["alpha", "beta", "gamma", "delta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    m.write_nap(repo, ids[2], ids[3], "cd")
    nodes = m.list_view(repo)
    assert m.leaf_digests(nodes[0]) is not None
    nodes[0].tree_path.write_bytes(b"{not json")
    assert m.leaf_digests(nodes[0]) is None
    nodes[1].tree_path.unlink()
    assert m.leaf_digests(m.list_view(repo)[1]) is None
    write_notes(m, repo, ["epsilon", "zeta"], start=5)
    ids = [node.id for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "ez")
    ez = [node for node in m.list_view(repo) if node.kind == "nap" and node.caption == "ez"][0]
    ez.tree_path.write_bytes(b'{"v":1}\n')
    assert m.leaf_digests(ez) is None


def test_leaf_digests_shared_for_identical_notes(tmp_path, summem):
    """Two notes with the same text share a leaf digest before heal runs."""
    m = summem
    repo = init_repo(tmp_path / "r")
    paths = write_notes(m, repo, ["hello", "hello"])
    nodes = m.list_view(repo)
    digest = m.note_digest(paths[0].read_bytes())
    assert m.leaf_digests(nodes[0]) == {digest}
    assert m.leaf_digests(nodes[1]) == {digest}
    assert paths[0].is_file() and paths[1].is_file()


def test_write_nap_reuses_nodes(tmp_path, monkeypatch, summem):
    """write_nap(nodes=...) does not call list_view."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["alpha", "beta"])
    nodes = m.list_view(repo)
    ids = [n.id for n in nodes]
    real = m.list_view

    def boom(_parent):
        raise AssertionError("write_nap must reuse nodes")

    monkeypatch.setattr(m, "list_view", boom)
    m.write_nap(repo, ids[0], ids[1], "pair", nodes=nodes)
    monkeypatch.setattr(m, "list_view", real)
    assert all(n.kind == "nap" for n in m.list_view(repo))


def test_rematerialize_note_writes_name_and_bytes(tmp_path, summem):
    """A NoteChild is written to notes/{name} with note_file_bytes."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    child = m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="alpha")
    m.rematerialize_child(repo, child)
    dest = repo / ".summem" / "notes" / child.name
    assert dest.read_bytes() == m.note_file_bytes("alpha")


def test_rematerialize_nap_stem_uses_leftmost_seq_child_id_and_leaves(tmp_path, summem):
    """A NapChild stem is nap_stem of the same tree and caption bytes later written."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["alpha", "beta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    inner = m.loads_tree(node.tree_path.read_bytes())
    child = m.NapChild(id=node.id, sum=node.caption, tree=inner)
    m._unlink_node(node)
    m.rematerialize_child(repo, child)
    stem, tree_bytes, caption_bytes = m.child_nap_stem(child)
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.tree").read_bytes() == tree_bytes
    assert (naps / f"{stem}.summ").read_bytes() == caption_bytes


def test_rematerialize_nap_is_idempotent_on_five_part(tmp_path, summem):
    """A second rematerialize of the same NapChild is a no-op on five-part dests."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["alpha", "beta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    inner = m.loads_tree(node.tree_path.read_bytes())
    child = m.NapChild(id=node.id, sum=node.caption, tree=inner)
    first = {p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file()}
    tree_bytes = node.tree_path.read_bytes()
    sum_bytes = node.sum_path.read_bytes()
    m.rematerialize_child(repo, child)
    m.rematerialize_child(repo, child)
    names = {p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file()}
    assert names == first
    assert node.tree_path.read_bytes() == tree_bytes
    assert node.sum_path.read_bytes() == sum_bytes


def test_rematerialize_nested_child_uses_child_pair_bytes(tmp_path, summem):
    """Rematerializing a nested grain-2 NapChild hashes that child's pair, not the parent's."""
    m = summem
    repo = init_repo(tmp_path / "r")
    parent = balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    inner = m.loads_tree(parent.tree_path.read_bytes())
    child = inner.kids[0]
    assert isinstance(child, m.NapChild)
    m._unlink_node(parent)
    m.rematerialize_child(repo, child)
    stem, tree_bytes, caption_bytes = m.child_nap_stem(child)
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.tree").read_bytes() == tree_bytes
    assert (naps / f"{stem}.summ").read_bytes() == caption_bytes
    parent_as_child = m.NapChild(id=parent.id, sum=parent.caption, tree=inner)
    parent_stem, _, _ = m.child_nap_stem(parent_as_child)
    assert stem != parent_stem


def test_rematerialize_does_not_clobber_existing_dest(tmp_path, summem):
    """A second rematerialize leaves an existing dest unchanged, including at the child's actual nap stem."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    name = "20260101T000001Z-aaaaaaaaaaaaaaaa"
    dest = repo / ".summem" / "notes" / name
    dest.write_bytes(m.note_file_bytes("kept"))
    m.rematerialize_child(repo, m.NoteChild(name=name, text="new"))
    assert dest.read_bytes() == m.note_file_bytes("kept")
    repo2 = init_repo(tmp_path / "r2")
    write_notes(m, repo2, ["alpha", "beta"], start=10)
    ids = [node.id for node in m.list_view(repo2)]
    m.write_nap(repo2, ids[0], ids[1], "pair")
    node = m.list_view(repo2)[0]
    inner = m.loads_tree(node.tree_path.read_bytes())
    child = m.NapChild(id=node.id, sum=node.caption, tree=inner)
    sentinel_tree = b"SENTINEL_TREE\n"
    sentinel_summ = b"SENTINEL_SUMM\n"
    node.tree_path.write_bytes(sentinel_tree)
    node.sum_path.write_bytes(sentinel_summ)
    m.rematerialize_child(repo2, child)
    assert node.tree_path.read_bytes() == sentinel_tree
    assert node.sum_path.read_bytes() == sentinel_summ


def test_same_second_notes_keep_left_child_stem(tmp_path, summem):
    """Same-second notes inside a rematerialized pack keep the left child's {stamp}-{rand} stem."""
    m = summem
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = Random(0)
    for text in ("a", "b", "c", "d"):
        m.write_note(repo, text, now, rng)
    nodes = m.list_view(repo)
    left_seq = nodes[0].name
    m.write_nap(repo, nodes[0].id, nodes[1].id, "ab")
    m.write_nap(repo, nodes[2].id, nodes[3].id, "cd")
    naps = [n for n in m.list_view(repo) if n.kind == "nap"]
    m.write_nap(repo, naps[0].id, naps[1].id, "abcd")
    parent = m.list_view(repo)[0]
    tree = m.loads_tree(parent.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    ab = next(n for n in m.list_view(repo) if n.kind == "nap" and n.leaves == 2)
    assert ab.name.startswith(left_seq)
    m.heal_view(repo)
