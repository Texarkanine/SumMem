"""CLI: wake, note, nap, zoom, and recall."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from dataclasses import replace
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
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["wake", "--path", "."]) == 0
    assert m.main(["note", "--path", ".", "hello"]) == 0
    assert m.main(["note", "--path", ".", "world"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["nap", "--path", ".", ids[0], ids[1], "pair"]) == 0
    nap_id = m.list_view(repo)[0].id
    assert m.main(["zoom", "--path", ".", nap_id]) != 2
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


def test_nap_accepts_unique_prefix(tmp_path, monkeypatch, capsys):
    """nap accepts unique 8-hex prefixes of two view ids."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    pa, pb = m.short_id(ids[0], ids), m.short_id(ids[1], ids)
    assert m.main(["nap", pa, pb, "pair"]) == 0
    capsys.readouterr()
    view = m.list_view(repo)
    assert len(view) == 1
    assert view[0].kind == "nap"


def test_unknown_prefix_is_error(tmp_path, monkeypatch, capsys):
    """An unknown nap prefix exits 1 and writes no nap."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    assert m.main(["nap", "deadbeef", "cafebabe", "pair"]) == 1
    err = capsys.readouterr().err
    assert "unknown id" in err
    assert list((repo / ".summem" / "naps").glob("*.sum")) == []


def test_ambiguous_prefix_is_error(tmp_path, monkeypatch, capsys):
    """An 8-hex prefix that matches two view ids exits 1 and writes no nap."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    nodes = m.list_view(repo)
    a = "aabbccdd" + "0" * 56
    b = "aabbccdd" + "1" * 56
    colliding = [replace(nodes[0], id=a), replace(nodes[1], id=b)]
    monkeypatch.setattr(m, "list_view", lambda _parent: colliding)
    assert m.main(["nap", "aabbccdd", "aabbccdd", "pair"]) == 1
    err = capsys.readouterr().err
    assert "ambiguous" in err
    assert list((repo / ".summem" / "naps").glob("*.sum")) == []


def test_nap_accepts_prefix_of_identical_notes(tmp_path, monkeypatch, capsys):
    """Two identical notes nap via the same unique prefix; the prompt is not 64-hex."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    assert ids[0] == ids[1]
    prefix = m.short_id(ids[0], ids)
    assert len(prefix) == 8
    prompt = m.fold_request(repo, 1)
    assert ids[0] not in prompt
    assert f"nap {prefix} {prefix} " in prompt
    assert m.main(["nap", prefix, prefix, "twins"]) == 0
    capsys.readouterr()
    view = m.list_view(repo)
    assert len(view) == 1
    assert view[0].kind == "nap"


def test_bare_invocation_prints_command_catalog(capsys):
    """main([]) prints a catalog of every command; --path on all but start."""
    m = load_summem()
    catalog = m.usage_text()
    assert m.main([]) != 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert catalog in text
    lines = {name: ln for ln in catalog.splitlines() for name in ("wake", "note", "nap", "zoom", "recall", "start") if f"summem {name}" in ln}
    for name in ("wake", "note", "nap", "zoom", "recall"):
        assert name in lines
        assert "--path" in lines[name]
    assert "start" in lines
    assert "--path" not in lines["start"]


def test_help_flag_prints_catalog(capsys):
    """-h and --help print the catalog and exit 0."""
    m = load_summem()
    catalog = m.usage_text()
    for flag in ("-h", "--help"):
        assert m.main([flag]) == 0
        captured = capsys.readouterr()
        text = captured.out + captured.err
        assert catalog in text
        assert captured.out
    assert "PWD" in catalog
    assert "--path" in catalog
    assert "file" in catalog.lower() or "directory" in catalog.lower()


def test_help_before_command_prints_command_help(capsys):
    """-h wake prints wake help including --path, not top-level-only usage."""
    m = load_summem()
    assert m.main(["-h", "wake"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" in text
    assert "{wake,note" not in text


def test_command_help_still_shows_path(capsys):
    """wake -h still shows --path."""
    m = load_summem()
    assert m.main(["wake", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" in text


def test_start_help_omits_path(capsys):
    """start -h does not list --path."""
    m = load_summem()
    assert m.main(["start", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" not in text


def test_catalog_omits_store_paths_and_git(capsys):
    """Catalog mentions neither notes/, naps/, nor git, and still shows --path."""
    m = load_summem()
    catalog = m.usage_text()
    assert m.main([]) != 0
    captured = capsys.readouterr()
    text = catalog + captured.out + captured.err
    assert "notes/" not in text
    assert "naps/" not in text
    assert "git" not in text.lower()
    assert "--path" in catalog
    assert "summem wake" in catalog


def test_wake_without_repository_errors(tmp_path, monkeypatch, capsys):
    """wake outside a repository exits 1, names repository, and creates no store."""
    m = load_summem()
    monkeypatch.chdir(tmp_path)
    assert m.main(["wake"]) == 1
    err = capsys.readouterr().err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / ".summem").exists()


def test_start_without_repository_errors(tmp_path, monkeypatch, capsys):
    """start outside a repository exits 1 and does not create a store."""
    m = load_summem()
    monkeypatch.chdir(tmp_path)
    assert m.main(["start", "pkg"]) == 1
    err = capsys.readouterr().err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / "pkg" / ".summem").exists()


def test_help_without_repository_still_prints_catalog(tmp_path, monkeypatch, capsys):
    """-h still prints the catalog when cwd is not a repository."""
    m = load_summem()
    monkeypatch.chdir(tmp_path)
    assert m.main(["-h"]) == 0
    out = capsys.readouterr().out
    assert "summem wake" in out
    assert "--path" in out
