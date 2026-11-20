"""CLI help routing, root usage_text() catalog, and store non-mutation."""

from __future__ import annotations

from gitutil import COMMAND_ONLY, fresh_imported, init_repo


def test_bare_invocation_prints_command_catalog(capsys, summem):
    """main([]) prints a catalog of every command; --path on store commands only."""
    m = summem
    catalog = m.usage_text()
    assert m.main([]) != 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert catalog in text
    lines = {
        name: ln
        for ln in catalog.splitlines()
        for name in ("wake", "note", "nap", "zoom", "recall", "start", "init", "version")
        if f"summem {name}" in ln
    }
    for name in ("wake", "note", "nap", "zoom", "recall"):
        assert name in lines
        assert "--path" in lines[name]
    for name in ("note", "nap", "zoom", "recall"):
        assert "[--path" not in lines[name]
    assert "[--path" in lines["wake"]
    assert "start" in lines
    assert "--path" not in lines["start"]
    assert "init" in lines
    assert "--path" not in lines["init"]
    assert "version" in lines
    assert "--path" not in lines["version"]


def test_bare_invocation_writes_catalog_to_stderr(capsys, summem):
    """A bare call prints the catalog on stderr and exits 2."""
    m = summem
    assert m.main([]) == 2
    captured = capsys.readouterr()
    assert captured.err == m.usage_text()
    assert captured.out == ""


def test_help_flag_prints_catalog(capsys, summem):
    """-h and --help print the catalog and exit 0."""
    m = summem
    catalog = m.usage_text()
    for flag in ("-h", "--help"):
        assert m.main([flag]) == 0
        captured = capsys.readouterr()
        assert captured.out == catalog
        assert captured.err == ""
    assert "PWD" not in catalog
    assert ":/" in catalog
    assert "--path" in catalog
    assert "file" in catalog.lower() or "directory" in catalog.lower()


def test_catalog_does_not_list_the_help_command(summem):
    """The printed catalog does not offer help as a command or <command> -h."""
    catalog = summem.usage_text()
    assert "summem help" not in catalog
    assert "<command> -h" not in catalog


def test_help_command_prints_catalog(capsys, summem):
    """help prints the same catalog as -h, on stdout, and exits 0."""
    m = summem
    assert m.main(["help"]) == 0
    captured = capsys.readouterr()
    assert captured.out == m.usage_text()
    assert captured.err == ""


def test_subcommand_help_prints_root_usage_without_touching_store(tmp_path, monkeypatch, capsys, summem):
    """Help flags before or after subcommands and help <cmd> print root usage, exit 0, and touch nothing."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    locks_dir = tmp_path / "locks"
    monkeypatch.setattr(m, "_runtime_lock_path", lambda _store: locks_dir / "store.lock")

    def boom(*_a, **_k):
        raise AssertionError("help must not lock or mutate")

    monkeypatch.setattr(m, "with_store_lock", boom)
    monkeypatch.setattr(m, "ensure_store", boom)
    catalog = m.usage_text()
    for argv in (
        ["note", "--help"],
        ["note", "-h"],
        ["note", "--path", ":/", "x", "--help"],
        ["-h"],
        ["--help"],
        ["help"],
        ["help", "note"],
        ["help", "start"],
        ["-h", "init"],
        ["init", "-h"],
        ["-h", "version"],
        ["version", "-h"],
        ["-h", "wake"],
        ["wake", "-h"],
        ["start", "-h"],
    ):
        assert m.main(argv) == 0, argv
        captured = capsys.readouterr()
        assert captured.out == catalog, argv
        assert captured.err == "", argv
    assert not (repo / ".summem").exists()
    assert list(repo.rglob(".summem")) == []
    assert not locks_dir.exists()
    assert not (repo / "help").exists()
    code, imported = fresh_imported(["note", "--path", ":/", "x", "--help"])
    assert code == 0
    for name in COMMAND_ONLY:
        assert imported[name] is False, name


def test_note_help_records_the_word(tmp_path, monkeypatch, summem):
    """note --path :/ help records the text help."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "--path", ":/", "help"]) == 0
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if p.is_file() and not p.name.startswith(".")]
    assert len(notes) == 1
    assert notes[0].read_text(encoding="utf-8") == "help\n"


def test_note_double_dash_records_help_flag(tmp_path, monkeypatch, summem):
    """note --path :/ -- --help records the literal --help."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "--path", ":/", "--", "--help"]) == 0
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if p.is_file() and not p.name.startswith(".")]
    assert len(notes) == 1
    assert notes[0].read_text(encoding="utf-8") == "--help\n"


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


def test_help_without_repository_still_prints_catalog(tmp_path, monkeypatch, capsys, summem):
    """-h still prints the catalog when cwd is not a repository."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["-h"]) == 0
    out = capsys.readouterr().out
    assert "summem wake" in out
    assert "--path" in out


def test_catalog_omits_store_driver_path(summem):
    """usage_text names summem, not .summem/summem."""
    m = summem
    catalog = m.usage_text()
    assert ".summem/summem" not in catalog
    for line in catalog.splitlines():
        if " wake " in line or line.endswith(" wake"):
            assert line.lstrip().startswith("summem wake")
