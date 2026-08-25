"""Zipper-heal: leaf-sets, rematerialize, overlapping packs, flock."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import Random

from conftest import load_summem
from gitutil import assert_unique_cover, init_repo, reaches, zoom_reaches

UTC = timezone.utc


def _write_notes(m, repo, texts, start=1):
    paths = []
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(texts):
        paths.append(
            m.write_note(
                repo, text, base + timedelta(seconds=start + i), Random(start + i)
            )
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


def _digest(m, text: str) -> str:
    return m.note_digest(m.note_file_bytes(text))


def _note_names(repo: Path) -> set[str]:
    root = repo / ".summem" / "notes"
    if not root.is_dir():
        return set()
    return {p.name for p in root.iterdir() if p.is_file() and not p.name.startswith(".")}


def _plant_nap(m, repo, kids, caption: str):
    tree = m.Tree(kids=list(kids))
    digests = m._digests_of_tree(tree)
    child = m.NapChild(id=m.leafset_id(digests), sum=caption, tree=tree)
    m.rematerialize_child(repo, child)
    return child


def _balanced_4(m, repo, texts, cap_ab, cap_cd, cap_p, start):
    paths = _write_notes(m, repo, texts, start=start)
    names = {p.name for p in paths}
    nodes = [n for n in m.list_view(repo) if n.name in names]
    m.write_nap(repo, nodes[0].id, nodes[1].id, cap_ab)
    c = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[2])
    d = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[3])
    m.write_nap(repo, c.id, d.id, cap_cd)
    ab = next(n for n in m.list_view(repo) if n.caption == cap_ab)
    cd = next(n for n in m.list_view(repo) if n.caption == cap_cd)
    m.write_nap(repo, ab.id, cd.id, cap_p)
    return next(n for n in m.list_view(repo) if n.caption == cap_p)


def _fold_balanced(m, repo, texts, caption, start):
    paths = _write_notes(m, repo, texts, start=start)
    remaining = [n.id for n in m.list_view(repo) if n.name in {p.name for p in paths}]
    step = 0
    while len(remaining) > 1:
        nxt = []
        for i in range(0, len(remaining) - 1, 2):
            before = {n.id for n in m.list_view(repo)}
            m.write_nap(repo, remaining[i], remaining[i + 1], f"{caption}-{step}")
            created = [cid for cid in [n.id for n in m.list_view(repo)] if cid not in before]
            nxt.extend(created)
            step += 1
        if len(remaining) % 2:
            nxt.append(remaining[-1])
        remaining = nxt
    return remaining[0]


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
    stem = f"{paths[0].name}-{child.id}-2"
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.tree").read_bytes() == m.dumps_tree(inner)
    assert (naps / f"{stem}.summ").read_bytes() == m.note_file_bytes("pair")


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


def test_heal_ab_vs_abcd_keeps_coarse_pack(tmp_path):
    """{A,B} next to {A,B,C,D} drops the 2-pack and does not write {C,D}."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    parent = _balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    cd_id = m.leafset_id([_digest(m, "C"), _digest(m, "D")])
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert [n.leaves for n in nodes] == [4]
    assert nodes[0].id == parent.id
    assert not any(cd_id in name for name in _payload_names(repo))
    assert reaches(m, repo, "A") and reaches(m, repo, "D")


def test_heal_parent_plus_children_keeps_parent(tmp_path):
    """Parent plus both children with no neighbor keeps the parent and drops the kids."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    parent = _balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
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


def test_heal_parent_plus_children_plus_neighbor_resplits(tmp_path):
    """Parent plus children plus an overlapping neighbor drops kids, then splits the parent."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    parent = _balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
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
    _plant_nap(m, repo, [ab, ce], "abce")
    m.heal_view(repo)
    assert_unique_cover(m, repo)
    for sentence in ("A", "B", "C", "D", "E"):
        assert reaches(m, repo, sentence)


def test_heal_abd_vs_abe_unique_cover(tmp_path):
    """Prefix overlap heals to a unique-leaf cover without new caption text or O(T) notes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["A", "B", "D"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    ab = next(n for n in m.list_view(repo) if n.kind == "nap")
    d = next(n for n in m.list_view(repo) if n.kind == "note")
    m.write_nap(repo, ab.id, d.id, "abd")
    abd = m.list_view(repo)[0]
    abd_tree = m.loads_tree(abd.tree_path.read_bytes())
    ab_child = abd_tree.kids[0]
    e_note = m.NoteChild(name="20260101T000010Z-eeeeeeeeeeeeeeee", text="E")
    _plant_nap(m, repo, [ab_child, e_note], ab_child.sum)
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


def test_heal_note_covered_by_nap_dropped(tmp_path):
    """A loose note whose digest sits inside a nap is unlinked; zoom still reaches it."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["A", "B"], start=1)
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


def test_heal_disjoint_is_noop(tmp_path):
    """Disjoint packs are left unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    _write_notes(m, repo, ["C", "D"], start=10)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "cd")
    before = _payload_names(repo)
    m.heal_view(repo)
    assert _payload_names(repo) == before
    assert_unique_cover(m, repo)


def test_heal_odd_arity_finishes_under_iteration_cap(tmp_path, monkeypatch):
    """A one-kid or three-kid nap finishes without hanging."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    one = m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="solo")
    _plant_nap(m, repo, [one], "one")
    three = [
        m.NoteChild(name="20260101T000010Z-bbbbbbbbbbbbbbbb", text="t0"),
        m.NoteChild(name="20260101T000011Z-cccccccccccccccc", text="t1"),
        m.NoteChild(name="20260101T000012Z-dddddddddddddddd", text="t2"),
    ]
    _plant_nap(m, repo, three, "three")
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


def test_heal_malformed_overlapping_nap_skipped(tmp_path):
    """An overlapping pair with a malformed .tree does not raise and does not drop leaves."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    parent = _balanced_4(m, repo, ["A", "B", "C", "D"], "ab", "cd", "abcd", start=1)
    tree = m.loads_tree(parent.tree_path.read_bytes())
    m.rematerialize_child(repo, tree.kids[0])
    ab = next(n for n in m.list_view(repo) if n.leaves == 2)
    ab.tree_path.write_bytes(b"{not json")
    m.heal_view(repo)
    assert parent.tree_path.is_file()
    assert ab.tree_path.is_file()
    inner = m.loads_tree(parent.tree_path.read_bytes())
    assert set(m._digests_of_tree(inner)) == {_digest(m, text) for text in ("A", "B", "C", "D")}


def test_heal_to_8_2_1_empty_fold_request_wake_projects(tmp_path, monkeypatch):
    """Heal to grains 8,2,1: fold_request is empty at budget 2; wake caps at budget and expands when short."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _fold_balanced(m, repo, [f"a{i}" for i in range(8)], "eight", start=1)
    _write_notes(m, repo, ["b0", "b1"], start=100)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "two")
    _write_notes(m, repo, ["c0"], start=200)
    m.heal_view(repo)
    grains = sorted(n.leaves for n in m.list_view(repo))
    assert grains == [1, 2, 8]
    assert m.fold_request(repo, 2) == ""
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 2
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 4


def test_heal_idempotent_on_disjoint_store(tmp_path):
    """heal_view is a no-op the second time on an already-disjoint store."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    _write_notes(m, repo, ["C", "D"], start=10)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "cd")
    m.heal_view(repo)
    before = _payload_names(repo)
    m.heal_view(repo)
    assert _payload_names(repo) == before


def test_heal_ignores_dot_prefixed_temp(tmp_path):
    """Dot-prefixed temp files in naps/ stay ignored."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    tmp = repo / ".summem" / "naps" / ".tmp-deadbeef"
    tmp.write_bytes(b"scratch")
    m.heal_view(repo)
    assert tmp.is_file()
    assert tmp.read_bytes() == b"scratch"


def test_same_second_notes_keep_left_child_stem(tmp_path):
    """Same-second notes inside a rematerialized pack keep the left child's {stamp}-{rand} stem."""
    m = load_summem()
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


def _plant_abd_abe(m, repo):
    _write_notes(m, repo, ["A", "B", "D"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    ab = next(n for n in m.list_view(repo) if n.kind == "nap")
    d = next(n for n in m.list_view(repo) if n.kind == "note")
    m.write_nap(repo, ab.id, d.id, "abd")
    abd = m.list_view(repo)[0]
    abd_tree = m.loads_tree(abd.tree_path.read_bytes())
    e_note = m.NoteChild(name="20260101T000010Z-eeeeeeeeeeeeeeee", text="E")
    _plant_nap(m, repo, [abd_tree.kids[0], e_note], "abe")
    return abd


def test_cli_note_and_nap_call_heal(tmp_path, monkeypatch, capsys):
    """main(['note', ...]) and main(['nap', ...]) call heal; wake does not."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    calls = {"n": 0}
    real = m.heal_view

    def wrapped(parent):
        calls["n"] += 1
        return real(parent)

    monkeypatch.setattr(m, "heal_view", wrapped)
    assert m.main(["note", "hello"]) == 0
    assert m.main(["note", "world"]) == 0
    assert calls["n"] == 2
    ids = [n.id for n in m.list_view(repo)]
    assert m.main(["nap", ids[0], ids[1], "pair"]) == 0
    assert calls["n"] == 3
    calls["n"] = 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    assert calls["n"] == 0


def test_cli_wake_on_overlapping_head_writes_nothing(tmp_path, monkeypatch):
    """CLI wake on overlapping HEAD prints and adds no file; wake must not flock."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    before = _payload_names(repo)
    flocks = {"n": 0}
    real = m.fcntl.flock

    def wrapped(fd, op):
        flocks["n"] += 1
        return real(fd, op)

    monkeypatch.setattr(m.fcntl, "flock", wrapped)
    assert m.main(["wake"]) == 0
    assert flocks["n"] == 0
    assert _payload_names(repo) == before


def test_cli_nap_overlapping_ids_exits_1_without_concat(tmp_path, monkeypatch):
    """nap of two overlapping ids exits 1, does not concat, writes no new .summ sentence."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    ids = [n.id for n in m.list_view(repo)]
    assert m.main(["nap", ids[0], ids[1], "concat-caption"]) == 1
    sum_texts = []
    for path in (repo / ".summem" / "naps").glob("*.summ"):
        text = path.read_text(encoding="utf-8")
        if text.endswith("\n"):
            text = text[:-1]
        sum_texts.append(text)
    assert "concat-caption" not in sum_texts
    assert_unique_cover(m, repo)


def test_cli_note_text_inside_nap_exits_0_no_loose_note(tmp_path, monkeypatch):
    """note of text already in a nap exits 0; that note does not remain in the view."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    assert m.main(["note", "A"]) == 0
    nodes = m.list_view(repo)
    assert all(n.kind == "nap" for n in nodes)
    assert not any(n.kind == "note" and n.caption == "A" for n in nodes)


def test_cli_invalid_nap_caption_does_not_heal(tmp_path, monkeypatch):
    """Invalid nap caption on an overlapping store exits nonzero and leaves payloads unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    ids = [n.id for n in m.list_view(repo)]
    before = _payload_names(repo)
    calls = {"n": 0}
    real = m.heal_view

    def wrapped(parent):
        calls["n"] += 1
        return real(parent)

    monkeypatch.setattr(m, "heal_view", wrapped)
    assert m.main(["nap", ids[0], ids[1], ""]) != 0
    assert calls["n"] == 0
    assert _payload_names(repo) == before


def test_identical_notes_nappable_after_heal_view(tmp_path):
    """Two identical notes stay through heal_view and can still be napped via write_nap."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["hello", "hello"], start=1)
    m.heal_view(repo)
    ids = [n.id for n in m.list_view(repo)]
    assert len(ids) == 2
    m.write_nap(repo, ids[0], ids[1], "twins")
    assert all(n.kind == "nap" for n in m.list_view(repo))


def test_with_store_lock_blocks_and_writes_no_lock_file(tmp_path):
    """A second non-blocking flock of naps/ fails while the lock is held; no lock file appears."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    naps = repo / ".summem" / "naps"
    probe = (
        "import fcntl, os, sys\n"
        "fd = os.open(sys.argv[1], os.O_RDONLY)\n"
        "try:\n"
        "    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
        "except BlockingIOError:\n"
        "    raise SystemExit(2)\n"
        "raise SystemExit(0)\n"
    )
    seen = {}

    def held():
        result = subprocess.run(
            [sys.executable, "-c", probe, str(naps)],
            capture_output=True,
        )
        seen["code"] = result.returncode
        seen["names"] = [p.name for p in (repo / ".summem").rglob("*") if p.is_file()]

    m.with_store_lock(repo, held)
    assert seen["code"] == 2
    assert "lock" not in seen["names"]
