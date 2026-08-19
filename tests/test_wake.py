"""Wait-free wake listing of loose notes."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from random import Random

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def test_wake_without_store_creates_and_prints_nothing(tmp_path):
    """First wake in a git repo with no store creates the store and prints nothing."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    assert m.wake_text(repo) == ""
    assert (repo / ".summem" / "config.toml").is_file()
    assert (repo / ".summem" / "notes").is_dir()
    assert (repo / ".summem" / "summem").is_file()


def test_wake_lists_two_notes_sorted_by_filename(tmp_path):
    """Wake prints two notes sorted by filename."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    later = datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC)
    earlier = datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC)
    m.write_note(repo, "second", later, Random(2))
    m.write_note(repo, "first", earlier, Random(1))
    lines = m.wake_text(repo).splitlines()
    assert len(lines) == 2
    assert lines[0].endswith("  first")
    assert lines[1].endswith("  second")


def test_wake_line_has_full_id_and_grain_date_from_name(tmp_path):
    """Each wake line has a 64-hex id and a grain date taken from the filename."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 8, 18, 12, 30, 5, tzinfo=UTC)
    path = m.write_note(repo, "hello", now, Random(42))
    os.utime(path, (0, 0))
    cid = m.leafset_id([m.note_digest(path.read_bytes())])
    line = m.wake_text(repo).splitlines()[0]
    assert len(cid) == 64
    assert line == f"{cid}  (1 note, from 2026-08-18)  hello"


def test_wake_output_omits_notes_naps_and_git(tmp_path):
    """Wake output does not mention notes/, naps/, or git."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    out = m.wake_text(repo)
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out


def test_wake_skips_unreadable_note_and_still_prints(tmp_path):
    """An unreadable note is skipped; readable notes still print."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(0))
    bad = repo / ".summem" / "notes" / "20260101T000000Z-ffffffffffffffff"
    bad.write_bytes(b"\xff")
    out = m.wake_text(repo)
    assert "hello" in out
    assert out.count("\n") == 1


def test_wake_skips_dot_prefixed_temp_file(tmp_path):
    """A leftover dot-prefixed temp file in notes/ is not listed."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "hello", datetime(2026, 1, 1, tzinfo=UTC), Random(0))
    leftover = repo / ".summem" / "notes" / ".tmp-deadbeefdeadbeef"
    leftover.write_text("orphan\n", encoding="utf-8")
    out = m.wake_text(repo)
    assert "hello" in out
    assert "orphan" not in out
    lines = [p.name for p in (repo / ".summem" / "notes").iterdir()]
    assert leftover.name in lines


def test_wake_mixed_view_sorts_by_filename(tmp_path):
    """A nap and a later loose note sort by filename; grain comes from the name."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")
    lines = m.wake_text(repo).splitlines()
    assert len(lines) == 2
    assert "(2 notes, from 2026-01-01)  pair" in lines[0]
    assert lines[1].endswith("  gamma")
    assert "(1 note, from 2026-01-01)" in lines[1]


def test_wake_missing_sum_prints_id_and_grain_without_caption(tmp_path):
    """Missing .sum: wake prints id and grain, not a caption, and does not refuse."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    leafset = sums[0].name.split("-")[-2]
    sums[0].unlink()
    out = m.wake_text(repo)
    assert out == f"{leafset}  (2 notes, from 2026-01-01)\n"
    assert "pair" not in out


def test_wake_conflict_sum_omits_caption(tmp_path):
    """A .sum containing <<<<<<< omits the caption and still prints id and grain."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    leafset = sums[0].name.split("-")[-2]
    sums[0].write_text("<<<<<<< HEAD\npair\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    out = m.wake_text(repo)
    assert out == f"{leafset}  (2 notes, from 2026-01-01)\n"
    assert "pair" not in out


def test_wake_does_not_call_loads_tree(tmp_path, monkeypatch):
    """Wake never opens .tree: loads_tree is not called."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [line.split()[0] for line in m.wake_text(repo).splitlines() if line]
    m.write_nap(repo, ids[0], ids[1], "pair")

    def boom(*_args, **_kwargs):
        raise AssertionError("loads_tree")

    monkeypatch.setattr(m, "loads_tree", boom)
    out = m.wake_text(repo)
    assert "pair" in out

