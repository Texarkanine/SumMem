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
