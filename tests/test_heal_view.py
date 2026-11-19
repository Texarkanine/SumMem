"""Zipper set-cover and overlap healing (heal_view)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

from gitutil import (
    assert_unique_cover,
    balanced_4,
    init_repo,
    payload_names,
    plant_nap,
    plant_pack,
    reaches,
    write_notes,
    zoom_reaches,
)

UTC = timezone.utc


def _digest(m, text: str) -> str:
    return m.note_digest(m.note_file_bytes(text))


def _note_names(repo: Path) -> set[str]:
    root = repo / ".summem" / "notes"
    if not root.is_dir():
        return set()
    return {p.name for p in root.iterdir() if p.is_file() and not p.name.startswith(".")}


def _plant_variant(m, naps, seq, leafset, grain, tree_bytes, caption) -> str:
    """Write a complete nap pair named by nap_stem of *tree_bytes* and *caption*."""
    caption_bytes = m.note_file_bytes(caption)
    stem = m.nap_stem(seq, leafset, grain, tree_bytes, caption_bytes)
    (naps / f"{stem}.tree").write_bytes(tree_bytes)
    (naps / f"{stem}.summ").write_bytes(caption_bytes)
    return stem


def _sum_sentences(m, repo) -> set[str]:
    found: set[str] = set()
    naps = repo / ".summem" / "naps"
    if not naps.is_dir():
        return found
    for path in naps.iterdir():
        if path.suffix == ".summ" and path.is_file() and not path.name.startswith("."):
            text = path.read_text(encoding="utf-8")
            if text.endswith("\n"):
                text = text[:-1]
            found.add(text)
        if path.suffix == ".tree" and path.is_file() and not path.name.startswith("."):
            try:
                tree = m.loads_tree(path.read_bytes())
            except m._TREE_PARSE_ERRORS:
                continue
            pending = [tree]
            while pending:
                cur = pending.pop()
                for kid in cur.kids:
                    if isinstance(kid, m.NapChild):
                        found.add(kid.sum)
                        pending.append(kid.tree)
    return found


def test_heal_view_returns_final_view(tmp_path, summem):
    """heal_view returns the same nodes a subsequent list_view would."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    write_notes(m, repo, ["C", "D"], start=10)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "cd")
    returned = m.heal_view(repo)
    fresh = m.list_view(repo)
    assert [(n.id, n.kind, n.leaves) for n in returned] == [
        (n.id, n.kind, n.leaves) for n in fresh
    ]


def test_heal_two_identical_notes_keeps_newer(tmp_path, summem):
    """Two loose notes with the same text collapse on heal; the later filename remains."""
    m = summem
    repo = init_repo(tmp_path / "r")
    paths = write_notes(m, repo, ["hello", "hello"], start=1)
    m.heal_view(repo)
    remaining = [p for p in paths if p.is_file()]
    assert remaining == [paths[1]]
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].kind == "note"
    assert nodes[0].path == paths[1]
    assert_unique_cover(m, repo)


def test_heal_equal_five_part_variants_keeps_lex_greatest(tmp_path, summem):
    """Two five-part equal-set pairs collapse to the lexicographically greatest stem."""
    m = summem
    repo = init_repo(tmp_path / "r")
    paths = write_notes(m, repo, ["alpha", "beta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "one")
    node = m.list_view(repo)[0]
    tree_bytes = node.tree_path.read_bytes()
    seq = m._seq_prefix(paths[0].name)
    naps = repo / ".summem" / "naps"
    stem_two = _plant_variant(m, naps, seq, node.id, 2, tree_bytes, "two")
    stems = sorted({node.name, stem_two})
    m.heal_view(repo)
    left = [n for n in m.list_view(repo) if n.kind == "nap"]
    assert len(left) == 1
    assert left[0].name == max(stems)
    assert (naps / f"{left[0].name}.tree").is_file()
    assert (naps / f"{left[0].name}.summ").is_file()
    assert reaches(m, repo, "alpha") and reaches(m, repo, "beta")


def test_heal_three_equal_variants_same_survivor_any_order(tmp_path, summem):
    """Three equal-set variants collapse to the same lex-greatest stem in any plant order."""
    m = summem
    captions_orders = [("one", "two", "zzz"), ("zzz", "one", "two"), ("two", "zzz", "one")]
    survivors = []
    for i, captions in enumerate(captions_orders):
        repo = init_repo(tmp_path / f"r{i}")
        paths = write_notes(m, repo, ["alpha", "beta"])
        ids = [node.id for node in m.list_view(repo)]
        m.write_nap(repo, ids[0], ids[1], captions[0])
        node = m.list_view(repo)[0]
        tree_bytes = node.tree_path.read_bytes()
        seq = m._seq_prefix(paths[0].name)
        naps = repo / ".summem" / "naps"
        stems = {node.name}
        for caption in captions[1:]:
            stems.add(_plant_variant(m, naps, seq, node.id, 2, tree_bytes, caption))
        m.heal_view(repo)
        left = [n for n in m.list_view(repo) if n.kind == "nap"]
        assert len(left) == 1
        assert left[0].name == max(stems)
        survivors.append(left[0].name)
        assert reaches(m, repo, "alpha") and reaches(m, repo, "beta")
    assert len(set(survivors)) == 1


def test_heal_ignores_four_part_twin(tmp_path, summem):
    """A four-part equal-set twin is not a view node; heal leaves those files and the five-part pair."""
    m = summem
    repo = init_repo(tmp_path / "r")
    paths = write_notes(m, repo, ["alpha", "beta"])
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    tree_bytes = node.tree_path.read_bytes()
    caption_bytes = node.sum_path.read_bytes()
    four = f"{m._seq_prefix(paths[0].name)}-{node.id}-2"
    naps = repo / ".summem" / "naps"
    (naps / f"{four}.tree").write_bytes(tree_bytes)
    (naps / f"{four}.summ").write_bytes(caption_bytes)
    m.heal_view(repo)
    left = [n for n in m.list_view(repo) if n.kind == "nap"]
    assert len(left) == 1
    assert left[0].name == node.name
    assert (naps / f"{four}.tree").is_file()
    assert (naps / f"{four}.summ").is_file()
    assert reaches(m, repo, "alpha") and reaches(m, repo, "beta")


def test_heal_ab_vs_abcd_keeps_coarse_pack(tmp_path, summem):
    """{A,B} next to {A,B,C,D} drops the 2-pack and does not write {C,D}."""
    m = summem
    repo = init_repo(tmp_path / "r")
    parent = balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    cd_id = m.leafset_id([_digest(m, "C"), _digest(m, "D")])
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert [n.leaves for n in nodes] == [4]
    assert nodes[0].id == parent.id
    assert not any(cd_id in name for name in payload_names(repo))
    assert reaches(m, repo, "A") and reaches(m, repo, "D")


def test_heal_parent_plus_children_keeps_parent(tmp_path, summem):
    """Parent plus both children with no neighbor keeps the parent and drops the kids."""
    m = summem
    repo = init_repo(tmp_path / "r")
    parent = balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    for kid in tree.kids:
        m.rematerialize_child(repo, kid)
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].id == parent.id
    assert nodes[0].leaves == 4
    for sentence in ("A", "B", "C", "D"):
        zoom_reaches(repo, parent.id, sentence)


def test_heal_parent_plus_children_plus_neighbor_resplits(tmp_path, summem):
    """Parent plus children plus an overlapping neighbor drops kids, then splits the parent."""
    m = summem
    repo = init_repo(tmp_path / "r")
    parent = balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    ab, cd = tree.kids
    for kid in tree.kids:
        m.rematerialize_child(repo, kid)
    e_note = m.NoteChild(name="20260101T000200Z-eeeeeeeeeeeeeeee", text="E")
    c_note = cd.tree.kids[0]
    ce = m.NapChild(
        id=m.leafset_id([_digest(m, c_note.text), _digest(m, "E")]),
        sum="ce",
        tree=m.Tree(kids=[c_note, e_note]),
    )
    plant_nap(m, repo, [ab, ce], "abce")
    m.heal_view(repo)
    assert_unique_cover(m, repo)
    for sentence in ("A", "B", "C", "D", "E"):
        assert reaches(m, repo, sentence)


def test_heal_abd_vs_abe_unique_cover(tmp_path, summem):
    """Prefix overlap heals to a unique-leaf cover without new caption text or O(T) notes."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B", "D"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    ab = next(n for n in m.list_view(repo) if n.kind == "nap")
    d = next(n for n in m.list_view(repo) if n.kind == "note")
    plant_pack(m, repo, ab, d, "abd")
    abd = m.list_view(repo)[0]
    abd_tree = m.loads_tree(abd.tree_path.read_bytes())
    ab_child = abd_tree.kids[0]
    e_note = m.NoteChild(name="20260101T000010Z-eeeeeeeeeeeeeeee", text="E")
    plant_nap(m, repo, [ab_child, e_note], ab_child.sum)
    before_sums = _sum_sentences(m, repo)
    m.heal_view(repo)
    assert_unique_cover(m, repo)
    for sentence in ("A", "B", "D", "E"):
        assert reaches(m, repo, sentence)
    assert len(_note_names(repo)) < 4
    after_sums = set()
    for path in (repo / ".summem" / "naps").glob("*.summ"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if text.endswith("\n"):
            text = text[:-1]
        after_sums.add(text)
    assert after_sums <= before_sums


def test_heal_note_covered_by_nap_dropped(tmp_path, summem):
    """A loose note whose digest sits inside a nap is unlinked; zoom still reaches it."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    nap = m.list_view(repo)[0]
    tree = m.loads_tree(nap.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    assert any(n.kind == "note" for n in m.list_view(repo))
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert all(n.kind == "nap" for n in nodes)
    assert nap.id in {n.id for n in nodes}
    zoom_reaches(repo, nap.id, "A")


def test_note_after_packed_text_is_healed_away(tmp_path, summem):
    """A write_note of packed text is gone after heal_view; zoom still reaches the pack."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    nap = m.list_view(repo)[0]
    later = m.write_note(
        repo, "A", datetime(2026, 1, 1, 0, 0, 10, tzinfo=UTC), Random(10)
    )
    assert later.is_file()
    m.heal_view(repo)
    assert not later.is_file()
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].kind == "nap"
    assert nodes[0].id == nap.id
    zoom_reaches(repo, nap.id, "A")


def test_heal_disjoint_is_noop(tmp_path, summem):
    """Disjoint packs are left unchanged."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    write_notes(m, repo, ["C", "D"], start=10)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "cd")
    before = payload_names(repo)
    m.heal_view(repo)
    assert payload_names(repo) == before
    assert_unique_cover(m, repo)


def test_heal_odd_arity_finishes_under_iteration_cap(tmp_path, monkeypatch, summem):
    """A one-kid or three-kid nap finishes without hanging."""
    m = summem
    repo = init_repo(tmp_path / "r")
    one = m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="solo")
    plant_nap(m, repo, [one], "one")
    three = [
        m.NoteChild(name="20260101T000010Z-bbbbbbbbbbbbbbbb", text="t0"),
        m.NoteChild(name="20260101T000011Z-cccccccccccccccc", text="t1"),
        m.NoteChild(name="20260101T000012Z-dddddddddddddddd", text="t2"),
    ]
    plant_nap(m, repo, three, "three")
    calls = {"n": 0}
    real = m.list_view

    def wrapped(parent):
        calls["n"] += 1
        if calls["n"] > 50:
            raise AssertionError("heal did not terminate")
        return real(parent)

    monkeypatch.setattr(m, "list_view", wrapped)
    m.heal_view(repo)
    assert calls["n"] <= 50
    monkeypatch.setattr(m, "list_view", real)
    assert reaches(m, repo, "solo")
    assert reaches(m, repo, "t1")


def test_heal_malformed_overlapping_nap_skipped(tmp_path, summem):
    """An overlapping pair with a malformed .tree does not raise and does not drop leaves."""
    m = summem
    repo = init_repo(tmp_path / "r")
    parent = balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    ab = next(n for n in m.list_view(repo) if n.leaves == 2)
    ab.tree_path.write_bytes(b"{not json")
    m.heal_view(repo)
    assert parent.tree_path.is_file()
    assert ab.tree_path.is_file()
    inner = m.loads_tree(parent.tree_path.read_bytes())
    assert set(m._digests_of_tree(inner)) == {_digest(m, text) for text in ("A", "B", "C", "D")}


def test_heal_idempotent_on_disjoint_store(tmp_path, summem):
    """heal_view is a no-op the second time on an already-disjoint store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    write_notes(m, repo, ["C", "D"], start=10)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "cd")
    m.heal_view(repo)
    before = payload_names(repo)
    m.heal_view(repo)
    assert payload_names(repo) == before


def test_heal_ignores_dot_prefixed_temp(tmp_path, summem):
    """Dot-prefixed temp files in naps/ stay ignored."""
    m = summem
    repo = init_repo(tmp_path / "r")
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    tmp = repo / ".summem" / "naps" / ".tmp-deadbeef"
    tmp.write_bytes(b"scratch")
    m.heal_view(repo)
    assert tmp.is_file()
    assert tmp.read_bytes() == b"scratch"
