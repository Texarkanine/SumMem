"""Left-fold request when the view exceeds WAKE_LINES."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


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
