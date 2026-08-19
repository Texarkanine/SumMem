"""Left-fold request when the view exceeds WAKE_LINES."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def test_nap_stem_inherits_left_child_seq_prefix(tmp_path):
    """Nap stem is {left.stamp}-{left.rand}-{leafset}-2 from the left child's filename."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa = m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    pb = m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    leafset = m.leafset_id([m.note_digest(pa.read_bytes()), m.note_digest(pb.read_bytes())])
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    stem = f"{m._seq_prefix(pa.name)}-{leafset}-2"
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.sum").is_file()
    assert (naps / f"{stem}.tree").is_file()


def test_same_second_nap_stays_in_left_slot(tmp_path):
    """Four notes in one UTC second: napping the oldest two leaves grains [2, 1, 1]."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = Random(0)
    for text in ("a", "b", "c", "d"):
        m.write_note(repo, text, now, rng)
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    assert [n.leaves for n in m.list_view(repo)] == [2, 1, 1]


def test_oldest_adjacent_returns_two_oldest_ids(tmp_path):
    """oldest_adjacent returns the ids of the two oldest view nodes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    nodes = m.list_view(repo)
    assert m.oldest_adjacent(nodes) == (nodes[0].id, nodes[1].id)


def test_over_budget_note_requests_oldest_pair_and_writes_no_nap(tmp_path, monkeypatch, capsys):
    """With WAKE_LINES=3, a fourth note prints the two oldest ids and writes no nap."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 3)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["note", "delta"]) == 0
    out = capsys.readouterr().out
    assert ids[0] in out
    assert ids[1] in out
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(notes) == 4
    naps = repo / ".summem" / "naps"
    assert list(naps.glob("*.sum")) == []
    assert list(naps.glob("*.tree")) == []


def test_default_wake_lines_is_32():
    """Default WAKE_LINES is 32."""
    m = load_summem()
    assert m.WAKE_LINES == 32


def test_config_toml_is_not_read(tmp_path, monkeypatch, capsys):
    """A committed config.toml WAKE_LINES value is ignored; the constant is used."""
    m = load_summem()
    assert not hasattr(m, "tomllib")
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 1\n", encoding="utf-8")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    assert m.main(["note", "beta"]) == 0
    out = capsys.readouterr().out
    assert out == ""
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(notes) == 2
    assert list((repo / ".summem" / "naps").glob("*.sum")) == []
