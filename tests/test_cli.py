"""CLI: wake, note, nap, zoom, and recall."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from random import Random

import pytest

from conftest import ROOT, SCRIPT
from gitutil import init_repo


def test_note_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys, summem):
    """main(['note', text]) writes a note; main(['wake']) prints it."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "hello"]) == 0
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "hello" in out
    assert "You are up to speed." in out
    assert out.splitlines()[-1] == "You are up to speed."


def test_nap_one_id_rejected(tmp_path, monkeypatch, capsys, summem):
    """nap with one id exits nonzero without calling nap an unknown command."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["nap", "a" * 64]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_three_ids_rejected(tmp_path, monkeypatch, capsys, summem):
    """nap with three ids and a caption exits nonzero without calling nap an unknown command."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    ids = ["a" * 64, "b" * 64, "c" * 64]
    assert m.main(["nap", *ids, "caption"]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys, summem):
    """main(['nap', id_a, id_b, caption]) folds two notes; wake prints the caption."""
    m = summem
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
    assert out.splitlines()[-1] == "You are up to speed."


def test_path_flag_is_known_on_all_non_start_commands(tmp_path, monkeypatch, summem):
    """--path is accepted on wake, note, nap, zoom, and recall, and rejected on start, init, and version."""
    m = summem
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
    assert m.main(["init", "--path", "."]) != 0
    assert m.main(["version", "--path", "."]) != 0


def test_note_without_text_fails(tmp_path, monkeypatch, summem):
    """note without text exits nonzero."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note"]) != 0


def test_cli_nap_overlong_prints_ratchet(tmp_path, monkeypatch, capsys, summem):
    """CLI nap with an over-long caption prints the length ratchet and writes no nap."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "alpha"]) == 0
    assert m.main(["note", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    capsys.readouterr()
    caption = "x" * (m.ENTRY_CHARS + 1)
    assert m.main(["nap", ids[0], ids[1], caption]) == 1
    err = capsys.readouterr().err
    assert str(len(caption.encode("utf-8"))) in err
    assert str(m.ENTRY_CHARS) in err
    assert "Accented characters cost 2 bytes" in err
    assert "Compress it further" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err
    naps = repo / ".summem" / "naps"
    assert not naps.exists() or not any(p.is_file() and not p.name.startswith(".") for p in naps.iterdir())


def test_rejected_nap_does_not_print_saved(tmp_path, monkeypatch, capsys, summem):
    """A too-long nap caption exits 1 and does not print Saved."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "alpha"]) == 0
    assert m.main(["note", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    capsys.readouterr()
    assert m.main(["nap", ids[0], ids[1], "x" * 281]) == 1
    captured = capsys.readouterr()
    assert "Saved." not in captured.out
    assert "Compress it further" in captured.err


def test_rejected_note_does_not_print_saved(tmp_path, monkeypatch, capsys, summem):
    """A too-long note exits 1 and does not print Saved."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note", "x" * 281]) == 1
    captured = capsys.readouterr()
    assert "Saved." not in captured.out


def test_note_error_text_omits_store_paths_and_git(tmp_path, monkeypatch, capsys, summem):
    """Rejection text for an over-long note mentions neither notes/, naps/, nor git."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note", "x" * 281]) == 1
    err = capsys.readouterr().err
    assert "281" in err
    assert "280" in err
    assert "Accented characters cost 2 bytes" in err
    assert "Compress it further" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_wake_prints_chinese_under_ascii_io_encoding(tmp_path, summem):
    """A 你好 note wakes when the child process has PYTHONIOENCODING=ascii."""
    m = summem
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


def test_refuses_python_before_311(summem):
    """require_python rejects a version tuple older than 3.11."""
    m = summem
    with pytest.raises(SystemExit) as caught:
        m.require_python((3, 10, 12))
    assert caught.value.code == 1
    m.require_python((3, 11, 0))
    m.require_python((3, 12, 0))


def test_version_info_is_checked_before_import_tomllib():
    """The driver reads sys.version_info after import sys and before import tomllib."""
    text = SCRIPT.read_text(encoding="utf-8")
    marker = "\nimport sys\n"
    sys_at = text.find(marker)
    assert sys_at != -1
    after_sys = text[sys_at + len(marker) :]
    gate_at = after_sys.find("version_info")
    tomllib_at = after_sys.find("import tomllib")
    assert tomllib_at != -1
    assert 0 <= gate_at < tomllib_at


def _cpython_310() -> str | None:
    """Return a CPython 3.10 executable, or None if this host has none."""
    candidates: list[str] = []
    uv = shutil.which("uv")
    if uv:
        found = subprocess.run(
            [uv, "python", "find", "3.10"],
            capture_output=True,
            text=True,
        )
        path = found.stdout.strip()
        if found.returncode == 0 and path:
            candidates.append(path)
    which = shutil.which("python3.10")
    if which:
        candidates.append(which)
    for path in candidates:
        probe = subprocess.run(
            [path, "-c", "import sys; print(sys.version_info[:2])"],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip() == "(3, 10)":
            return path
    return None


def test_driver_refuses_python_310_before_tomllib():
    """On Python 3.10 the driver prints the floor message, not a tomllib ImportError."""
    py310 = _cpython_310()
    if py310 is None:
        pytest.skip("Python 3.10 is not available")
    result = subprocess.run(
        [py310, str(SCRIPT), "version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "SumMem needs Python 3.11 or newer" in result.stderr
    assert "tomllib" not in result.stderr
    assert "Traceback" not in result.stderr


_COMMAND_ONLY = ("tomllib", "fcntl", "subprocess", "dataclasses", "argparse")

_IMPORT_PROBE = r"""
import builtins
import importlib.util
import json
import sys
from importlib.machinery import SourceFileLoader

watched = ("tomllib", "fcntl", "subprocess", "dataclasses", "argparse")
from_driver = {name: False for name in watched}
real_import = builtins.__import__

def tracked(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".", 1)[0]
    if root in from_driver and globals and globals.get("__name__") == "summem_probe":
        from_driver[root] = True
    return real_import(name, globals, locals, fromlist, level)

builtins.__import__ = tracked
path, *cmd = sys.argv[1:]
loader = SourceFileLoader("summem_probe", path)
spec = importlib.util.spec_from_loader("summem_probe", loader)
mod = importlib.util.module_from_spec(spec)
sys.modules["summem_probe"] = mod
spec.loader.exec_module(mod)
code = mod.main(cmd)
sys.stdout.write("\n")
sys.stdout.write(json.dumps(from_driver))
raise SystemExit(0 if code is None else code)
"""


def _fresh_imported(cmd: list[str]) -> tuple[int, dict[str, bool]]:
    """Run *cmd* in a new interpreter and report modules the driver itself imported.

    3.14's pathlib imports fcntl, so sys.modules is the wrong oracle.
    """
    result = subprocess.run(
        [sys.executable, "-c", _IMPORT_PROBE, str(SCRIPT), *cmd],
        capture_output=True,
        text=True,
    )
    payload = result.stdout.splitlines()[-1] if result.stdout.splitlines() else ""
    imported = json.loads(payload)
    return result.returncode, imported


def test_version_skips_command_only_imports():
    """version in a fresh interpreter does not import command-only modules."""
    code, imported = _fresh_imported(["version"])
    assert code == 0
    for name in _COMMAND_ONLY:
        assert imported[name] is False, name


def test_init_skips_command_only_imports():
    """init in a fresh interpreter does not import command-only modules."""
    code, imported = _fresh_imported(["init"])
    assert code == 0
    for name in _COMMAND_ONLY:
        assert imported[name] is False, name


def test_help_skips_command_only_imports():
    """-h in a fresh interpreter does not import command-only modules."""
    code, imported = _fresh_imported(["-h"])
    assert code == 0
    for name in _COMMAND_ONLY:
        assert imported[name] is False, name


def test_shebang_and_executable_bit():
    """The driver starts with the python3 shebang and is executable."""
    first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
    assert first == "#!/usr/bin/env python3"
    assert SCRIPT.stat().st_mode & stat.S_IXUSR


def test_cli_malformed_tree_returns_1_without_traceback(tmp_path, monkeypatch, capsys, summem):
    """A malformed .tree via CLI nap returns 1 without a traceback or store paths."""
    m = summem
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


def test_nap_accepts_unique_prefix(tmp_path, monkeypatch, capsys, summem):
    """nap accepts unique 8-hex prefixes of two view ids."""
    m = summem
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


def test_unknown_prefix_is_error(tmp_path, monkeypatch, capsys, summem):
    """An unknown nap prefix exits 1 and writes no nap."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    assert m.main(["nap", "deadbeef", "cafebabe", "pair"]) == 1
    err = capsys.readouterr().err
    assert "unknown id" in err
    assert "Copy an id from wake" in err
    assert list((repo / ".summem" / "naps").glob("*.summ")) == []


def test_ambiguous_prefix_is_error(tmp_path, monkeypatch, capsys, summem):
    """An 8-hex prefix that matches two view ids exits 1 and writes no nap."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    nodes = m.list_view(repo)
    a = "aabbccdd" + "0" * 56
    b = "aabbccdd" + "1" * 56
    colliding = [m._replace(nodes[0], id=a), m._replace(nodes[1], id=b)]
    monkeypatch.setattr(m, "list_view", lambda _parent: colliding)
    assert m.main(["nap", "aabbccdd", "aabbccdd", "pair"]) == 1
    err = capsys.readouterr().err
    assert "ambiguous" in err
    assert "Give a longer prefix" in err
    assert list((repo / ".summem" / "naps").glob("*.summ")) == []


def test_cli_nap_identical_notes_prefix_not_adjacent(tmp_path, monkeypatch, capsys, summem):
    """CLI nap of one id twice after heal fails; no pack is written."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    assert ids[0] == ids[1]
    prefix = m.short_id(ids[0], ids)
    assert len(prefix) == 8
    assert m.main(["nap", prefix, prefix, "twins"]) == 1
    err = capsys.readouterr().err
    assert "not adjacent" in err
    view = m.list_view(repo)
    assert len(view) == 1
    assert view[0].kind == "note"
    assert list((repo / ".summem" / "naps").glob("*.summ")) == []
    assert list((repo / ".summem" / "naps").glob("*.tree")) == []


def test_bare_invocation_prints_command_catalog(capsys, summem):
    """main([]) prints a catalog of every command; --path on store commands only."""
    m = summem
    catalog = m.usage_text()
    assert m.main([]) != 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert catalog in text
    lines = {name: ln for ln in catalog.splitlines() for name in ("wake", "note", "nap", "zoom", "recall", "start", "init", "version") if f"summem {name}" in ln}
    for name in ("wake", "note", "nap", "zoom", "recall"):
        assert name in lines
        assert "--path" in lines[name]
    assert "start" in lines
    assert "--path" not in lines["start"]
    assert "init" in lines
    assert "--path" not in lines["init"]
    assert "version" in lines
    assert "--path" not in lines["version"]


def test_help_flag_prints_catalog(capsys, summem):
    """-h and --help print the catalog and exit 0."""
    m = summem
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


def test_help_before_command_prints_command_help(capsys, summem):
    """-h wake prints wake help including --path, not top-level-only usage."""
    m = summem
    assert m.main(["-h", "wake"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" in text
    assert "{wake,note" not in text


def test_command_help_still_shows_path(capsys, summem):
    """wake -h still shows --path."""
    m = summem
    assert m.main(["wake", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" in text


def test_start_help_omits_path(capsys, summem):
    """start -h does not list --path."""
    m = summem
    assert m.main(["start", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" not in text


def test_catalog_omits_store_paths_and_git(capsys, summem):
    """Catalog mentions neither notes/, naps/, nor git, and still shows --path."""
    m = summem
    catalog = m.usage_text()
    assert m.main([]) != 0
    captured = capsys.readouterr()
    text = catalog + captured.out + captured.err
    assert "notes/" not in text
    assert "naps/" not in text
    assert "git" not in text.lower()
    assert "--path" in catalog
    assert "summem wake" in catalog


def test_wake_without_repository_errors(tmp_path, monkeypatch, capsys, summem):
    """wake outside a repository exits 1, names repository, and creates no store."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["wake"]) == 1
    err = capsys.readouterr().err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / ".summem").exists()


def test_start_without_repository_errors(tmp_path, monkeypatch, capsys, summem):
    """start outside a repository exits 1 and does not create a store."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["start", "pkg"]) == 1
    err = capsys.readouterr().err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / "pkg" / ".summem").exists()


def test_help_without_repository_still_prints_catalog(tmp_path, monkeypatch, capsys, summem):
    """-h still prints the catalog when cwd is not a repository."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["-h"]) == 0
    out = capsys.readouterr().out
    assert "summem wake" in out
    assert "--path" in out


def test_script_is_repo_root_driver():
    """Tests load the committed repo-root summem file."""
    assert SCRIPT == ROOT / "summem"
    assert SCRIPT.is_file()


def test_catalog_omits_store_driver_path(summem):
    """usage_text names summem, not .summem/summem."""
    m = summem
    catalog = m.usage_text()
    assert ".summem/summem" not in catalog
    for line in catalog.splitlines():
        if " wake " in line or line.endswith(" wake"):
            assert line.lstrip().startswith("summem wake")


def test_unknown_token_does_not_write_a_note(tmp_path, monkeypatch, capsys, summem):
    """A non-command token is argparse invalid choice and writes no note."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["raw invocation of random stuff"]) != 0
    err = capsys.readouterr().err
    assert "invalid choice" in err
    notes = repo / ".summem" / "notes"
    written = list(notes.glob("*")) if notes.is_dir() else []
    assert written == []
    assert m.main(["note", "ok"]) == 0
    assert any(p.is_file() and not p.name.startswith(".") for p in notes.iterdir())


def test_cli_zoom_range_token_is_not_a_content_id(tmp_path, monkeypatch, capsys, summem):
    """CLI zoom of a range token names the token and says to copy an id from wake."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["zoom", "16-31"]) == 2
    err = capsys.readouterr().err
    assert "not a content id: 16-31" in err
    assert "Copy an id from wake" in err


def test_cli_zoom_malformed_tree_returns_1(tmp_path, monkeypatch, capsys, summem):
    """CLI zoom of a nap whose .tree is not JSON exits 1 with unreadable pack."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = next(n for n in m.list_view(repo) if n.kind == "nap")
    nap.tree_path.write_bytes(b"{not json")
    capsys.readouterr()
    assert m.main(["zoom", nap.id]) == 1
    err = capsys.readouterr().err
    assert "unreadable pack" in err
    assert "Traceback" not in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_cli_zoom_oserror_returns_1(tmp_path, monkeypatch, capsys, summem):
    """CLI zoom of a nap whose .tree read raises OSError exits 1 with unreadable pack."""
    from pathlib import Path

    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    nap = next(n for n in m.list_view(repo) if n.kind == "nap")
    tree = nap.tree_path
    real = Path.read_bytes

    def patched(self):
        if self == tree:
            raise OSError("boom")
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", patched)
    capsys.readouterr()
    assert m.main(["zoom", nap.id]) == 1
    err = capsys.readouterr().err
    assert "unreadable pack" in err
    assert "Traceback" not in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


def test_cli_zoom_nested_id_skips_sibling_bad_tree(tmp_path, monkeypatch, capsys, summem):
    """Zoom of a nested id still works when another view nap has a bad tree."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.write_note(repo, "A", datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc), Random(1))
    m.write_note(repo, "B", datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc), Random(2))
    ab = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ab[0], ab[1], "ab")
    m.write_note(repo, "C", datetime(2026, 1, 1, 0, 0, 3, tzinfo=timezone.utc), Random(3))
    m.write_note(repo, "D", datetime(2026, 1, 1, 0, 0, 4, tzinfo=timezone.utc), Random(4))
    notes = [n for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "cd")
    naps = [n for n in m.list_view(repo) if n.kind == "nap"]
    first, second = naps[0], naps[1]
    tree = m.loads_tree(second.tree_path.read_bytes())
    child_id = m.leafset_id([m.note_digest(m.note_file_bytes(tree.kids[0].text))])
    first.tree_path.write_bytes(b"{not json")
    capsys.readouterr()
    assert m.main(["zoom", child_id]) == 0
    captured = capsys.readouterr()
    assert tree.kids[0].text in captured.out
    assert captured.err == "skipped a pack\n"
    assert "notes/" not in captured.err
    assert "naps/" not in captured.err
    assert "git" not in captured.err
    assert "Traceback" not in captured.err
