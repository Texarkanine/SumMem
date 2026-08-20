"""Store auto-create and immutable note writes."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

import pytest
import tomllib

from conftest import load_summem
from gitutil import init_repo

UTC = timezone.utc


def _write(m, repo, text="hello", now=None, rng=None):
    now = now or datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = rng or Random(0)
    return m.write_note(repo, text, now, rng)


def test_note_rejects_empty(tmp_path):
    """Empty note text is rejected."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError):
        _write(m, repo, text="")


def test_note_rejects_over_280_bytes(tmp_path):
    """A note longer than 280 UTF-8 bytes is rejected."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError):
        _write(m, repo, text="x" * (m.ENTRY_CHARS + 1))


def test_note_rejects_newline(tmp_path):
    """A note containing a newline or carriage return is rejected."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError):
        _write(m, repo, text="hello\n")
    with pytest.raises(ValueError):
        _write(m, repo, text="hello\rworld")


def test_note_accepts_280_bytes(tmp_path):
    """A note of exactly 280 UTF-8 bytes is accepted."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    text = "x" * m.ENTRY_CHARS
    path = _write(m, repo, text=text)
    assert path.read_bytes() == m.note_file_bytes(text)


def test_note_280_is_utf8_bytes_not_chars(tmp_path):
    """The 280 limit is UTF-8 bytes, not characters."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError):
        _write(m, repo, text="你" * 94)
    text = ("你" * 93) + "a"
    assert len(text.encode("utf-8")) == 280
    path = _write(m, repo, text=text, rng=Random(1))
    assert path.read_bytes() == m.note_file_bytes(text)


def test_note_rejects_non_utc_now(tmp_path):
    """A naive or non-UTC now is rejected."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError):
        m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 0), Random(0))
    local = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=-5)))
    with pytest.raises(ValueError):
        m.write_note(repo, "hello", local, Random(0))


def test_first_note_creates_config_notes_and_driver(tmp_path):
    """First note creates commented config, a notes file, and the driver if missing."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    path = _write(m, repo, text="hello")
    store = repo / ".summem"
    config = (store / "config.toml").read_text(encoding="utf-8")
    assert tomllib.loads(config) == {}
    assert config.lstrip().startswith("#")
    assert path.read_bytes() == m.note_file_bytes("hello")
    assert (store / "summem").is_file()
    notes = [p for p in (store / "notes").iterdir() if not p.name.startswith(".")]
    assert len(notes) == 1


def test_existing_driver_is_not_overwritten(tmp_path):
    """An existing .summem/summem is left unchanged."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    driver = repo / ".summem" / "summem"
    driver.parent.mkdir()
    driver.write_bytes(b"NOPE")
    _write(m, repo, text="hello")
    assert driver.read_bytes() == b"NOPE"


def test_ensure_store_creates_naps_dir(tmp_path):
    """ensure_store creates naps/ and does not overwrite an existing driver."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    driver = repo / ".summem" / "summem"
    driver.parent.mkdir()
    driver.write_bytes(b"NOPE")
    m.ensure_store(repo)
    assert (repo / ".summem" / "naps").is_dir()
    assert driver.read_bytes() == b"NOPE"



def test_note_name_uses_injected_utc_clock_and_rand(tmp_path):
    """Note names use the injected UTC clock and rng bytes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 8, 18, 12, 30, 5, tzinfo=UTC)
    path = m.write_note(repo, "hello", now, Random(42))
    assert path.name == f"20260818T123005Z-{Random(42).randbytes(8).hex()}"


def test_same_second_notes_are_two_paths(tmp_path):
    """Two notes in the same UTC second still produce two paths."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = Random(0)
    a = m.write_note(repo, "alpha", now, rng)
    b = m.write_note(repo, "beta", now, rng)
    assert a != b
    names = {p.name for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")}
    assert names == {a.name, b.name}
