"""CLI: wake, note, nap, zoom, and recall."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from random import Random

import pytest

from conftest import SCRIPT, load_summem
from gitutil import init_repo


def test_note_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys):
    """main(['note', text]) writes a note; main(['wake']) prints it."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "hello"]) == 0
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "hello" in out
    assert len(out.splitlines()) == 1


def test_nap_one_id_rejected(tmp_path, monkeypatch, capsys):
    """nap with one id exits nonzero without calling nap an unknown command."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["nap", "a" * 64]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_three_ids_rejected(tmp_path, monkeypatch, capsys):
    """nap with three ids and a caption exits nonzero without calling nap an unknown command."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    ids = ["a" * 64, "b" * 64, "c" * 64]
    assert m.main(["nap", *ids, "caption"]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys):
    """main(['nap', id_a, id_b, caption]) folds two notes; wake prints the caption."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "alpha"]) == 0
    assert m.main(["note", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["nap", ids[0], ids[1], "pair"]) == 0
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "pair" in out
    assert "alpha" not in out
    assert len(out.splitlines()) == 1


def test_path_flag_is_known_on_all_non_start_commands(tmp_path, monkeypatch):
    """--path is accepted on wake, note, nap, zoom, and recall, and rejected on start."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    fake = "a" * 64
    assert m.main(["wake", "--path", "."]) == 0
    assert m.main(["note", "--path", ".", "hello"]) == 0
    assert m.main(["nap", "--path", ".", fake, fake, "pair"]) == 0
    assert m.main(["zoom", "--path", ".", fake]) != 2
    assert m.main(["recall", "--path", ".", "hello"]) == 0
    assert m.main(["start", "pkg", "--path", "."]) != 0


def test_note_without_text_fails(tmp_path, monkeypatch):
    """note without text exits nonzero."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note"]) != 0


def test_note_error_text_omits_store_paths_and_git(tmp_path, monkeypatch, capsys):
    """Rejection text for an over-long note mentions neither notes/, naps/, nor git."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note", "x" * 281]) == 1
    err = capsys.readouterr().err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_wake_prints_chinese_under_ascii_io_encoding(tmp_path):
    """A 你好 note wakes when the child process has PYTHONIOENCODING=ascii."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "你好", datetime(2026, 1, 1, tzinfo=timezone.utc), Random(0))
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "ascii"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "wake"],
        cwd=repo,
        env=env,
        capture_output=True,
    )
    assert result.returncode == 0
    assert "你好".encode("utf-8") in result.stdout


def test_refuses_python_before_311():
    """require_python rejects a version tuple older than 3.11."""
    m = load_summem()
    with pytest.raises(SystemExit) as caught:
        m.require_python((3, 10, 12))
    assert caught.value.code == 1
    m.require_python((3, 11, 0))
    m.require_python((3, 12, 0))


def test_shebang_and_executable_bit():
    """The driver starts with the python3 shebang and is executable."""
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first == "#!/usr/bin/env python3"
    assert SCRIPT.stat().st_mode & stat.S_IXUSR


def test_cli_malformed_tree_returns_1_without_traceback(tmp_path, monkeypatch, capsys):
    """A malformed .tree via CLI nap returns 1 without a traceback or store paths."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "alpha"]) == 0
    assert m.main(["note", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["nap", ids[0], ids[1], "pair"]) == 0
    assert m.main(["note", "gamma"]) == 0
    nap = next(n for n in m.list_view(repo) if n.kind == "nap")
    note = next(n for n in m.list_view(repo) if n.kind == "note")
    nap.tree_path.write_bytes(b"{not json")
    capsys.readouterr()
    assert m.main(["nap", nap.id, note.id, "nope"]) == 1
    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert "unreadable pack" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
