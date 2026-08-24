"""Proof walkers enqueue nested packs from children trees, not zoom stdout."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo, reaches

UTC = timezone.utc


def _find_nap(m, tree, cid: str):
    for child in tree.kids:
        if not isinstance(child, m.NapChild):
            continue
        if child.id == cid:
            return child
        found = _find_nap(m, child.tree, cid)
        if found is not None:
            return found
    return None


def _tree_for(m, parent, cid: str):
    for node in m.list_view(parent):
        if node.kind != "nap" or node.tree_path is None or not node.tree_path.is_file():
            continue
        loaded = m.loads_tree(node.tree_path.read_bytes())
        if node.id == cid:
            return loaded
        found = _find_nap(m, loaded, cid)
        if found is not None:
            return found.tree
    return None


def test_reaches_nested_sentence_when_zoom_prints_wake_lines(tmp_path, monkeypatch):
    """reaches finds a nested original when zoom_text prints wake grammar, not 64-hex ids."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["a1", "a2", "b1", "b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = [node.id for node in m.list_view(repo) if node.kind == "nap"]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    named = m.named_ids(repo)

    def fake_zoom(parent, token: str) -> str:
        cid = m.resolve_id(token, named)
        tree = _tree_for(m, parent, cid)
        if tree is None:
            raise ValueError("unknown id")
        rows = [m._projected_child(child) for child in tree.kids]
        return "\n".join(m.format_wake_line(row, named) for row in rows if row) + "\n"

    monkeypatch.setattr(m, "zoom_text", fake_zoom)
    assert reaches(m, repo, "a1")
