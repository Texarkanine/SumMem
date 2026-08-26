"""Word-for-word recall over the view and nested original notes."""

from __future__ import annotations

from datetime import datetime, timezone
from random import Random

from conftest import dated_leaf
from gitutil import init_repo

UTC = timezone.utc


def test_recall_matches_loose_note(tmp_path, summem):
    """Recall finds a sentence that is still a loose note."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    out = m.recall_text(repo, "hello")
    assert out == dated_leaf("20260101T000000Z", "alpha hello") + "\n"


def test_recall_matches_caption(tmp_path, monkeypatch, summem):
    """Recall finds a nap caption in the view."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "folded pair")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    out = m.recall_text(repo, "folded")
    assert "folded pair" in out


def test_recall_matches_sentence_inside_tree(tmp_path, summem):
    """Recall finds an original sentence that lives only inside a .tree."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "unique-leaf-sentence", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "other", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    out = m.recall_text(repo, "unique-leaf-sentence")
    assert out == dated_leaf("20260101T000001Z", "unique-leaf-sentence") + "\n"


def test_recall_output_omits_notes_naps_and_git(tmp_path, summem):
    """Recall output does not mention notes/, naps/, or git."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    out = m.recall_text(repo, "hello")
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out


def test_recall_matches_loose_note_when_over_budget(tmp_path, monkeypatch, summem):
    """Recall still finds a loose note when the view is over WAKE_LINES."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i in range(11):
        m.write_note(repo, f"n{i}", datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    assert "n0" in m.recall_text(repo, "n0")


def test_recall_skips_unreadable_sibling_warns(tmp_path, capsys, summem):
    """Recall still matches a good pack and warns when a sibling children file is unreadable."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ab = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ab[0], ab[1], "ab")
    m.write_note(repo, "unique-good-leaf", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "other-good", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "cd")
    first = next(node for node in m.list_view(repo) if node.kind == "nap")
    first.tree_path.write_bytes(b"{not json\n")
    capsys.readouterr()
    out = m.recall_text(repo, "unique-good-leaf")
    assert "unique-good-leaf" in out
    err = capsys.readouterr().err
    assert err == "skipped a pack\n"
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert "Traceback" not in err


def test_recall_malformed_tree_does_not_raise(tmp_path, capsys, summem):
    """A nap whose .tree is not JSON does not make recall raise."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    next((repo / ".summem" / "naps").glob("*.tree")).write_bytes(b"{not json\n")
    capsys.readouterr()
    out = m.recall_text(repo, "alpha")
    assert isinstance(out, str)
    err = capsys.readouterr().err
    assert err == "skipped a pack\n"
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    assert "Traceback" not in err


def test_recall_matches_nested_nap_caption(tmp_path, summem):
    """Recall finds a nap caption that lives only inside a parent children file."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["a1", "a2", "b1", "b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = [node.id for node in m.list_view(repo) if node.kind == "nap"]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    out = m.recall_text(repo, "pack-a")
    parent = m.list_view(repo)[0]
    tree = m.loads_tree(parent.tree_path.read_bytes())
    child = next(c for c in tree.kids if c.sum == "pack-a")
    ids = m.named_ids(repo)
    want = f"x2 {m.short_id(child.id, ids)}: pack-a"
    assert out.splitlines() == [want]
    prefix = want.split()[1].rstrip(":")
    zoomed = m.zoom_text(repo, prefix)
    assert dated_leaf("20260101T000001Z", "a1") in zoomed.splitlines()
    assert "both" not in out


def test_recall_nested_caption_omits_notes_naps_and_git(tmp_path, summem):
    """A nested-caption hit does not mention notes/, naps/, or git."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["a1", "a2", "b1", "b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = [node.id for node in m.list_view(repo) if node.kind == "nap"]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    out = m.recall_text(repo, "pack-a")
    assert "pack-a" in out
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out


def test_recall_does_not_match_grain_day_or_prefix(tmp_path, summem):
    """Recall matches captions and note text, not grain, day, or id prefix."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "folded pair")
    assert m.recall_text(repo, "x2") == ""
    assert m.recall_text(repo, "2026-01-01") == ""
    node = m.list_view(repo)[0]
    line = m.format_wake_line(node, m.named_ids(repo))
    prefix = line.split()[1].rstrip(":")
    ch = next(c for c in prefix if c not in node.caption)
    assert "folded pair" not in m.recall_text(repo, ch)


def test_recall_keeps_duplicate_note_dates(tmp_path, summem):
    """Recall prints both dated lines when two nested notes share text but not a day."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "same-text", datetime(2026, 1, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "same-text", datetime(2026, 1, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    out = m.recall_text(repo, "same-text")
    assert dated_leaf("20260101T000000Z", "same-text") in out.splitlines()
    assert dated_leaf("20260102T000000Z", "same-text") in out.splitlines()


def test_recall_nested_caption_before_matching_leaves(tmp_path, summem):
    """A nested nap caption hit is printed before matching leaves under that nap."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["theme-a1", "theme-a2", "other-b1", "other-b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "theme-inner")
    m.write_nap(repo, ids[2], ids[3], "other")
    nap_ids = [node.id for node in m.list_view(repo) if node.kind == "nap"]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")
    lines = m.recall_text(repo, "theme").splitlines()
    cap = next(i for i, line in enumerate(lines) if "theme-inner" in line)
    leaf = next(i for i, line in enumerate(lines) if "theme-a1" in line)
    assert cap < leaf


def test_recall_parses_each_view_tree_once(tmp_path, monkeypatch, summem):
    """recall_text parses each view children file once while searching nested leaves."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ab = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ab[0], ab[1], "ab")
    m.write_note(repo, "unique-good-leaf", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    m.write_note(repo, "other-good", datetime(2026, 1, 1, 0, 0, 4, tzinfo=UTC), Random(4))
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "cd")
    bodies = [path.read_bytes() for path in (repo / ".summem" / "naps").glob("*.tree")]
    assert len(bodies) == 2
    real = m.loads_tree
    seen: list[bytes] = []

    def counted(data: bytes):
        seen.append(data)
        return real(data)

    monkeypatch.setattr(m, "loads_tree", counted)
    out = m.recall_text(repo, "unique-good-leaf")
    assert "unique-good-leaf" in out
    for body in bodies:
        assert seen.count(body) == 1


def test_recall_does_not_call_short_id_per_hit(tmp_path, monkeypatch, summem):
    """recall_text formats pack hits from a prefix map and does not call short_id."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(["a1", "a2", "b1", "b2"], start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pack-a")
    m.write_nap(repo, ids[2], ids[3], "pack-b")
    nap_ids = [node.id for node in m.list_view(repo) if node.kind == "nap"]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "both")

    def boom(*_args, **_kwargs):
        raise AssertionError("short_id")

    monkeypatch.setattr(m, "short_id", boom)
    out = m.recall_text(repo, "pack-a")
    assert "pack-a" in out
    assert out.split()[0].startswith("x")


def test_recall_unprojectable_note_name_skips(tmp_path, capsys, summem):
    """Recall does not traceback when a note child's name is not a string."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    next((repo / ".summem" / "naps").glob("*.tree")).write_bytes(
        b'{"c":[{"type":"note","name":1,"text":"x"}]}\n'
    )
    capsys.readouterr()
    out = m.recall_text(repo, "x")
    assert isinstance(out, str)
    err = capsys.readouterr().err
    assert err == "skipped a pack\n"
    assert "Traceback" not in err


def test_recall_invalid_pattern_is_cli_error(tmp_path, monkeypatch, capsys, summem):
    """An invalid regex is a CLI error and does not mention store paths."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["recall", "["]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
