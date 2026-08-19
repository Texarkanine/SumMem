"""In-memory wake expand when the directory is shorter than WAKE_LINES."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import Random

from conftest import load_summem
from gitutil import fold_ids, init_repo

UTC = timezone.utc


def _add_notes(m, repo, count, offset, prefix):
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i in range(count):
        m.write_note(
            repo,
            f"{prefix}{i}",
            base + timedelta(seconds=offset + i),
            Random(offset + i),
        )


def _fold_loose_notes(m, repo, caption):
    ids = [node.id for node in m.list_view(repo) if node.kind == "note"]
    return fold_ids(m, repo, ids, caption)


def _two_eights(m, repo):
    _add_notes(m, repo, 8, 0, "a")
    _fold_loose_notes(m, repo, "eight-a")
    _add_notes(m, repo, 8, 8, "b")
    _fold_loose_notes(m, repo, "eight-b")


def _payload_names(repo: Path) -> set[str]:
    names = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def test_under_budget_expands_right_edge_until_budget(tmp_path, monkeypatch):
    """Two 8-packs at budget 4 print four lines; the directory still has two files."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    nodes = m.list_view(repo)
    assert len(nodes) == 2
    assert len(lines) == 4
    assert "x8" in lines[0]


def test_at_budget_does_not_expand(tmp_path, monkeypatch):
    """Two 8-packs at budget 2 print the two captions and do not split."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 2
    assert "eight-a" in lines[0]
    assert "eight-b" in lines[1]


def test_native_notes_fill_budget_without_split(tmp_path, monkeypatch):
    """Two 8-packs plus two later notes at budget 4 print four file lines."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    m.write_note(repo, "later-a", datetime(2026, 1, 1, 0, 1, 0, tzinfo=UTC), Random(80))
    m.write_note(repo, "later-b", datetime(2026, 1, 1, 0, 1, 1, tzinfo=UTC), Random(81))
    monkeypatch.setattr(m, "WAKE_LINES", 4)

    def boom(*_args, **_kwargs):
        raise AssertionError("loads_tree")

    monkeypatch.setattr(m, "loads_tree", boom)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 4
    assert len(m.list_view(repo)) == 4


def test_lone_note_does_not_split(tmp_path, monkeypatch):
    """A single note never splits, even when the budget is larger."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "solo", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    monkeypatch.setattr(m, "WAKE_LINES", 32)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 1
    assert lines[0] == "solo"


def test_expand_writes_nothing(tmp_path, monkeypatch):
    """Expanding an under-budget directory does not create or delete store files."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    before = _payload_names(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    m.wake_text(repo)
    assert _payload_names(repo) == before


def test_missing_tree_does_not_split(tmp_path, monkeypatch):
    """A nap whose .tree is missing prints as one line."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    trees = list((repo / ".summem" / "naps").glob("*.tree"))
    trees[0].unlink()
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 1
    assert "pair" in lines[0]


def test_malformed_tree_does_not_split(tmp_path, monkeypatch):
    """A nap whose .tree is malformed prints as one line."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    trees = list((repo / ".summem" / "naps").glob("*.tree"))
    trees[0].write_bytes(b"{not json\n")
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 1
    assert "pair" in lines[0]


def test_unreadable_tree_does_not_split(tmp_path, monkeypatch):
    """A nap whose .tree cannot be read prints as one line."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    tree = next((repo / ".summem" / "naps").glob("*.tree"))
    real = Path.read_bytes

    def patched(self):
        if self == tree:
            raise PermissionError
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", patched)
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 1
    assert "pair" in lines[0]


def test_nested_empty_nap_child_does_not_split(tmp_path, monkeypatch):
    """A valid JSON tree with a nap child that has no notes prints as one line."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    tree_path = next((repo / ".summem" / "naps").glob("*.tree"))
    tree_path.write_bytes(
        m.dumps_tree(
            m.Tree(
                kids=[
                    m.NoteChild(name="20260101T000001Z-aaaaaaaaaaaaaaaa", text="alpha"),
                    m.NapChild(id="0" * 64, sum="empty", tree=m.Tree(kids=[])),
                ]
            )
        )
    )
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 1
    assert "pair" in lines[0]


def test_malformed_tree_is_loaded_at_most_once(tmp_path, monkeypatch):
    """A failed file-backed .tree load is not retried during the same wake."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    nodes = m.list_view(repo)
    right = nodes[-1]
    assert right.tree_path is not None
    bad = b"{not json\n"
    right.tree_path.write_bytes(bad)
    real = m.loads_tree
    seen: list[bytes] = []

    def counted(data: bytes):
        seen.append(data)
        return real(data)

    monkeypatch.setattr(m, "loads_tree", counted)
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 4
    assert seen.count(bad) == 1


def test_zoom_expanded_child_id(tmp_path, monkeypatch):
    """An id printed by expand can be zoomed to that child's kids or text."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _two_eights(m, repo)
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    file_ids = {node.id for node in m.list_view(repo)}
    frontier = m.expand_frontier(m.list_view(repo), 4)
    child_ids = [row.id for row in frontier if row.id not in file_ids]
    assert child_ids
    out = m.zoom_text(repo, child_ids[0])
    assert out
