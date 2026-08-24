"""Wait-free wake listing of loose notes."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from random import Random

import pytest

from conftest import dated_leaf, load_summem
from gitutil import init_repo

UTC = timezone.utc


def test_wake_without_store_creates_and_prints_nothing(tmp_path):
    """First wake in a git repo with no store creates the store and prints nothing."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    assert m.wake_text(repo) == ""
    assert (repo / ".summem" / "config.toml").is_file()
    assert (repo / ".summem" / "notes").is_dir()
    assert not (repo / ".summem" / "summem").exists()


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
    assert lines[0] == dated_leaf("20260101T000001Z", "first")
    assert lines[1] == dated_leaf("20260101T000002Z", "second")


def test_day_from_stamp_formats_utc_calendar_date():
    """_day_from_stamp maps a 16-char UTC filename stamp to YYYY-MM-DD."""
    m = load_summem()
    assert m._day_from_stamp("20260824T123005Z") == "2026-08-24"


def test_wake_line_is_dated_grain_for_a_note(tmp_path):
    """A note wake line is x1 YYYY-MM-DD: text from the filename stamp."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 8, 18, 12, 30, 5, tzinfo=UTC)
    path = m.write_note(repo, "hello", now, Random(42))
    os.utime(path, (0, 0))
    line = m.wake_text(repo).splitlines()[0]
    assert line == dated_leaf("20260818T123005Z", "hello")
    assert path.read_bytes() == b"hello\n"
    assert len(m.list_view(repo)[0].id) == 64


def test_wake_pack_line_has_no_date(tmp_path, monkeypatch):
    """A pack wake line has grain and prefix and contains no YYYY-MM-DD."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    nap_id = m.list_view(repo)[0].id
    prefix = m.short_id(nap_id, [nap_id])
    line = m.wake_text(repo).splitlines()[0]
    assert line == f"x2 {prefix}: pair"
    assert re.search(r"\d{4}-\d{2}-\d{2}", line) is None


def test_format_wake_line_grain1_pack_is_undated_caption():
    """A grain-1 pack (kind nap, leaves 1) prints the caption only."""
    m = load_summem()
    node = m.ProjectedNode(
        id="ab" * 32,
        kind="nap",
        caption="solo",
        leaves=1,
        stamp="20260824T123005Z",
    )
    assert m.format_wake_line(node, [node.id]) == "solo"


def test_format_wake_line_empty_note_caption_keeps_trailing_colon():
    """A note with an empty caption prints x1 day: with no extra space."""
    m = load_summem()
    node = m.ProjectedNode(
        id="cd" * 32,
        kind="note",
        caption="",
        leaves=1,
        stamp="20260824T123005Z",
    )
    assert m.format_wake_line(node, [node.id]) == dated_leaf("20260824T123005Z", "")


def test_resolve_id_rejects_hyphenated_day():
    """A YYYY-MM-DD token is not a content-id prefix."""
    m = load_summem()
    cid = "a3f2c1b8" + "ab" * 28
    with pytest.raises(ValueError, match="unknown id"):
        m.resolve_id("2026-08-24", [cid])


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


def test_wake_mixed_view_sorts_by_filename(tmp_path, monkeypatch):
    """A nap and a later loose note sort by filename; grain comes from the name."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    lines = m.wake_text(repo).splitlines()
    assert len(lines) == 2
    prefix = m.short_id(m.list_view(repo)[0].id, [node.id for node in m.list_view(repo)])
    assert lines[0] == f"x2 {prefix}: pair"
    assert lines[1] == dated_leaf("20260101T000003Z", "gamma")


def test_wake_missing_sum_prints_id_and_grain_without_caption(tmp_path, monkeypatch):
    """Missing .sum: wake prints id and grain, not a caption, and does not refuse."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    leafset = sums[0].name.split("-")[-2]
    sums[0].unlink()
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    out = m.wake_text(repo)
    prefix = m.short_id(leafset, [leafset])
    assert out == f"x2 {prefix}:\n"
    assert "pair" not in out


def test_wake_conflict_sum_omits_caption(tmp_path, monkeypatch):
    """A .sum containing <<<<<<< omits the caption and still prints id and grain."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    sums = list((repo / ".summem" / "naps").glob("*.sum"))
    leafset = sums[0].name.split("-")[-2]
    sums[0].write_text("<<<<<<< HEAD\npair\n=======\nother\n>>>>>>>\n", encoding="utf-8")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    out = m.wake_text(repo)
    prefix = m.short_id(leafset, [leafset])
    assert out == f"x2 {prefix}:\n"
    assert "pair" not in out


def test_wake_does_not_call_loads_tree(tmp_path, monkeypatch):
    """At-budget wake lists files and does not open .tree."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")

    def boom(*_args, **_kwargs):
        raise AssertionError("loads_tree")

    monkeypatch.setattr(m, "WAKE_LINES", 1)
    monkeypatch.setattr(m, "loads_tree", boom)
    out = m.wake_text(repo)
    assert "pair" in out


def test_wake_pack_line_is_grain_prefix_caption(tmp_path, monkeypatch):
    """A pack wake line is xN prefix: caption."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    nap_id = m.list_view(repo)[0].id
    prefix = m.short_id(nap_id, [nap_id])
    assert m.wake_text(repo) == f"x2 {prefix}: pair\n"


def test_wake_prints_at_most_wake_lines_newest(tmp_path, monkeypatch):
    """Eleven notes at WAKE_LINES=4 print the newest four texts, no hashes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i in range(11):
        m.write_note(repo, f"n{i}", datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = m.wake_text(repo).splitlines()
    assert lines == [
        dated_leaf(datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC).strftime("%Y%m%dT%H%M%SZ"), f"n{i}")
        for i in range(7, 11)
    ]
    assert all(len(part) != 64 for line in lines for part in line.split())


def test_wake_does_not_print_a_nap_request(tmp_path, monkeypatch):
    """Wake never prints Run: or a nap invocation, even when over budget."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i in range(5):
        m.write_note(repo, f"n{i}", datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    out = m.wake_text(repo)
    assert "Run:" not in out
    assert "nap " not in out


def test_short_id_is_8_hex_when_unique():
    """short_id is 8 hex when that prefix is unique among the given ids."""
    m = load_summem()
    cid = "a3f2c1b8" + "ab" * 28
    other = "b3f2c1b8" + "cd" * 28
    assert m.short_id(cid, [cid, other]) == "a3f2c1b8"


def test_short_id_lengthens_until_unique():
    """short_id grows past 8 hex when two ids share the floor prefix."""
    m = load_summem()
    a = "a3f2c1b8" + "0" * 56
    b = "a3f2c1b8" + "1" * 56
    assert m.short_id(a, [a, b]) == "a3f2c1b80"
    assert m.short_id(b, [a, b]) == "a3f2c1b81"


def test_resolve_id_returns_full_id_for_unique_prefix():
    """resolve_id maps a unique prefix to the full id."""
    m = load_summem()
    cid = "a3f2c1b8" + "ab" * 28
    other = "b3f2c1b8" + "cd" * 28
    assert m.resolve_id("a3f2c1b8", [cid, other]) == cid


def test_resolve_id_rejects_ambiguous_or_unknown_prefix():
    """resolve_id raises ValueError when the prefix matches none or many ids."""
    m = load_summem()
    a = "a3f2c1b8" + "0" * 56
    b = "a3f2c1b8" + "1" * 56
    with pytest.raises(ValueError, match="ambiguous") as caught:
        m.resolve_id("a3f2c1b8", [a, b])
    assert "Give a longer prefix" in str(caught.value)
    with pytest.raises(ValueError, match="unknown id") as caught:
        m.resolve_id("deadbeef", [a, b])
    assert "Copy an id from wake" in str(caught.value)


def test_short_id_is_8_hex_when_id_repeats():
    """A repeated content id still shortens to 8 hex; uniqueness is among distinct ids."""
    m = load_summem()
    cid = "a3f2c1b8" + "ab" * 28
    other = "b3f2c1b8" + "cd" * 28
    assert m.short_id(cid, [cid, cid, other]) == "a3f2c1b8"


def test_resolve_id_accepts_prefix_when_id_repeats():
    """resolve_id treats a repeated content id as one identity, not an ambiguous clash."""
    m = load_summem()
    cid = "a3f2c1b8" + "ab" * 28
    other = "b3f2c1b8" + "cd" * 28
    assert m.resolve_id("a3f2c1b8", [cid, cid, other]) == cid
    assert m.resolve_id(cid, [cid, cid]) == cid

