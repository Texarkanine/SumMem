"""CLI: core subcommand dispatch, flag validation, length ratchets, and outside-repo errors."""

from __future__ import annotations

from gitutil import init_repo


def test_note_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys, summem):
    """main(['note', '--root', text]) writes a note; main(['wake']) prints it."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "--root", "hello"]) == 0
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "hello" in out
    assert "You are up to speed." in out
    assert out.splitlines()[-1] == "You are up to speed."


def test_nap_one_id_rejected(tmp_path, monkeypatch, capsys, summem):
    """nap with one id exits nonzero without calling nap an unknown command."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["nap", "--root", "a" * 64]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_three_ids_rejected(tmp_path, monkeypatch, capsys, summem):
    """nap with three ids and a caption exits nonzero without calling nap an unknown command."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    ids = ["a" * 64, "b" * 64, "c" * 64]
    assert m.main(["nap", "--root", *ids, "caption"]) != 0
    err = capsys.readouterr().err.lower()
    assert "invalid choice" not in err


def test_nap_subcommand_writes_and_wake_reads(tmp_path, monkeypatch, capsys, summem):
    """main(['nap', '--root', id_a, id_b, caption]) folds two notes; wake prints the caption."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "--root", "alpha"]) == 0
    assert m.main(["note", "--root", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["nap", "--root", ids[0], ids[1], "pair"]) == 0
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "pair" in out
    assert "alpha" not in out
    assert out.splitlines()[-1] == "You are up to speed."


def test_path_flag_accepted_on_store_commands_and_rejected_elsewhere(tmp_path, monkeypatch, summem):
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
    assert m.main(["note", "--root", "alpha"]) == 0
    assert m.main(["note", "--root", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    capsys.readouterr()
    caption = "x" * (m.ENTRY_CHARS + 1)
    assert m.main(["nap", "--root", ids[0], ids[1], caption]) == 1
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
    assert m.main(["note", "--root", "alpha"]) == 0
    assert m.main(["note", "--root", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo)]
    capsys.readouterr()
    assert m.main(["nap", "--root", ids[0], ids[1], "x" * 281]) == 1
    captured = capsys.readouterr()
    assert "Saved" not in captured.out
    assert "Compress it further" in captured.err


def test_rejected_note_does_not_print_saved(tmp_path, monkeypatch, capsys, summem):
    """A too-long note exits 1 and does not print Saved."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note", "--root", "x" * 281]) == 1
    captured = capsys.readouterr()
    assert "Saved" not in captured.out


def test_note_error_text_omits_store_paths_and_git(tmp_path, monkeypatch, capsys, summem):
    """Rejection text for an over-long note mentions neither notes/, naps/, nor git."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["note", "--root", "x" * 281]) == 1
    err = capsys.readouterr().err
    assert "281" in err
    assert "280" in err
    assert "Accented characters cost 2 bytes" in err
    assert "Compress it further" in err
    assert "notes/" not in err
    assert "naps/" not in err
    assert "git" not in err


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
    (tmp_path / "pkg").mkdir()
    assert m.main(["start", "pkg"]) == 1
    err = capsys.readouterr().err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / "pkg" / ".summem").exists()


def test_start_missing_dir_outside_repository_errors(tmp_path, monkeypatch, capsys, summem):
    """start on a missing directory outside a repository exits 1 without a traceback."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["start", "missing"]) == 1
    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert "repository" in err.lower()
    assert "git" not in err.lower()
    assert not (tmp_path / "missing").exists()


def test_store_commands_require_root_or_path_flag(tmp_path, monkeypatch, capsys, summem):
    """note, nap, zoom, and recall with no store flag exit 2 and write nothing."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    for argv in (
        ["note", "x"],
        ["nap", "deadbeef", "cafebabe", "cap"],
        ["zoom", "deadbeef"],
        ["recall", "pat"],
    ):
        assert m.main(argv) == 2, argv
        captured = capsys.readouterr()
        assert captured.out == "", argv
        assert len(captured.err.splitlines()) == 1, argv
        assert "--root" in captured.err, argv
        assert "--path" in captured.err, argv
        assert "git" not in captured.err.lower(), argv
        assert "notes/" not in captured.err, argv
        assert "naps/" not in captured.err, argv
        assert not (repo / ".summem").exists(), argv


def test_store_commands_reject_both_root_and_path(tmp_path, monkeypatch, capsys, summem):
    """note, nap, zoom, and recall with both --root and --path exit 2 and write nothing."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    for argv in (
        ["note", "--root", "--path", "a", "x"],
        ["nap", "--root", "--path", "a", "deadbeef", "cafebabe", "cap"],
        ["zoom", "--root", "--path", "a", "deadbeef"],
        ["recall", "--root", "--path", "a", "pat"],
    ):
        assert m.main(argv) == 2, argv
        captured = capsys.readouterr()
        assert captured.out == "", argv
        assert len(captured.err.splitlines()) == 1, argv
        assert not (repo / ".summem").exists(), argv


def test_wake_start_init_version_reject_root_flag(tmp_path, monkeypatch, summem):
    """wake, start, init, and version do not accept --root."""
    m = summem
    repo = init_repo(tmp_path / "r")
    (repo / "pkg").mkdir()
    monkeypatch.chdir(repo)
    assert m.main(["wake", "--root"]) == 2
    assert m.main(["start", "--root", "pkg"]) == 2
    assert m.main(["init", "--root"]) == 2
    assert m.main(["version", "--root"]) == 2


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
    assert m.main(["note", "--root", "ok"]) == 0
    assert any(p.is_file() and not p.name.startswith(".") for p in notes.iterdir())
