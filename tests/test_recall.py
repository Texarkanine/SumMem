"""Word-for-word recall over the view and nested original notes."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def test_recall_matches_loose_note(tmp_path):
    """Recall finds a sentence that is still a loose note."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    out = m.recall_text(repo, "hello")
    assert "alpha hello" in out


def test_recall_matches_caption(tmp_path, monkeypatch):
    """Recall finds a nap caption in the view."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "folded pair")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    out = m.recall_text(repo, "folded")
    assert "folded pair" in out


def test_recall_matches_sentence_inside_tree(tmp_path):
    """Recall finds an original sentence that lives only inside a .tree."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "unique-leaf-sentence", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "other", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    out = m.recall_text(repo, "unique-leaf-sentence")
    assert "unique-leaf-sentence" in out
    assert "pair" not in out


def test_recall_output_omits_notes_naps_and_git(tmp_path):
    """Recall output does not mention notes/, naps/, or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    out = m.recall_text(repo, "hello")
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out


def test_recall_invalid_pattern_is_cli_error(tmp_path, monkeypatch, capsys):
    """An invalid regex is a CLI error and does not mention store paths."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["recall", "["]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
