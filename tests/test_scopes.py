"""Store walk-up, start, --path, per-store config, and root-wake catalog."""

from __future__ import annotations

import os
import re
import shlex
import shutil
import subprocess
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from random import Random

import pytest

from gitutil import git, git_free, init_repo


def test_resolve_subdir_without_store_is_git_root(tmp_path, summem):
    """A subdirectory with no nested store resolves to the git root."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    assert m.resolve_parent(nested) == repo.resolve()
    assert m.resolve_parent(nested / "fee.ts") == repo.resolve()


def test_resolve_inside_started_dir_is_that_store(tmp_path, summem):
    """Resolve from inside a started directory returns that directory."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    m.ensure_store(nested)
    assert m.is_store(nested)
    assert not m.is_store(repo / "foo")
    assert m.resolve_parent(nested) == nested.resolve()
    assert m.resolve_parent(nested / "src") == nested.resolve()


def test_resolve_path_file_walks_from_parent(tmp_path, summem):
    """An existing file path walks from the file's parent directory."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    fee = nested / "fee.ts"
    fee.write_text("x\n", encoding="utf-8")
    m.ensure_store(nested)
    assert m.resolve_parent(repo, "foo/packages/baz/fee.ts") == nested.resolve()


def test_resolve_missing_file_walks_from_parent(tmp_path, summem):
    """A missing file path walks from its parent directory."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    m.ensure_store(nested)
    assert m.resolve_parent(repo, "foo/packages/baz/fee.ts") == nested.resolve()


def test_resolve_omitted_path_uses_cwd(tmp_path, summem):
    """Omitting path_arg walks from cwd."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "pkg"
    nested.mkdir()
    m.ensure_store(nested)
    unstarted = repo / "other"
    unstarted.mkdir()
    assert m.resolve_parent(nested, None) == nested.resolve()
    assert m.resolve_parent(unstarted, None) == repo.resolve()
    assert m.resolve_parent(repo, None) == repo.resolve()


def test_start_creates_store_in_dir(tmp_path, monkeypatch, summem):
    """start creates a store in a directory that already exists."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "foo/packages/baz").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "foo/packages/baz"]) == 0
    store = repo / "foo" / "packages" / "baz" / ".summem"
    assert not (store / "summem").exists()
    assert (store / "notes").is_dir()
    assert (store / "naps").is_dir()
    config = (store / "config.toml").read_text(encoding="utf-8")
    assert tomllib.loads(config) == {}
    assert config.lstrip().startswith("#")


def test_start_does_not_create_ancestor_stores(tmp_path, monkeypatch, summem):
    """start does not create .summem on ancestor directories."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "foo/packages/baz").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert not (repo / "foo" / ".summem").exists()
    assert not (repo / "foo" / "packages" / ".summem").exists()
    assert (repo / "foo" / "packages" / "baz" / ".summem").is_dir()


def test_start_without_dir_is_usage(tmp_path, monkeypatch, summem):
    """start without a directory exits nonzero."""
    m = summem
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["start"]) == 2


def test_start_says_there_is_a_store(tmp_path, monkeypatch, capsys, summem):
    """start on an existing directory prints one line and creates the store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir()
    assert m.main(["start", "pkg"]) == 0
    out = capsys.readouterr().out
    assert out == "There is a store in `:/pkg`.\n"
    store = repo / "pkg" / ".summem"
    assert (store / "notes").is_dir()
    assert (store / "naps").is_dir()
    assert not (store / "summem").exists()
    config = (store / "config.toml").read_text(encoding="utf-8")
    assert config.lstrip().startswith("#")
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out.lower()


def test_start_again_prints_the_same_line(tmp_path, monkeypatch, capsys, summem):
    """A second start prints the same line and does not rewrite config."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir()
    assert m.main(["start", "pkg"]) == 0
    config = (repo / "pkg" / ".summem" / "config.toml").read_bytes()
    capsys.readouterr()
    assert m.main(["start", "pkg"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "There is a store in `:/pkg`.\n"
    assert captured.err == ""
    assert (repo / "pkg" / ".summem" / "config.toml").read_bytes() == config


def test_start_refuses_missing_directory(tmp_path, monkeypatch, capsys, summem):
    """start does not create a missing directory."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "missing"]) == 1
    err = capsys.readouterr().err
    assert err == "not a directory: `:/missing`\n"
    assert not (repo / "missing").exists()
    assert "git" not in err.lower()
    assert "notes/" not in err
    assert "naps/" not in err


def test_start_refuses_missing_nested_directory(tmp_path, monkeypatch, capsys, summem):
    """start does not create missing parents or the target."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "foo/packages/baz"]) == 1
    err = capsys.readouterr().err
    assert err == "not a directory: `:/foo/packages/baz`\n"
    assert not (repo / "foo").exists()


def test_start_refuses_a_file(tmp_path, monkeypatch, capsys, summem):
    """start on a file reports that it is not a directory and creates no store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "file").write_text("x", encoding="utf-8")
    assert m.main(["start", "file"]) == 1
    err = capsys.readouterr().err
    assert err == "not a directory: `:/file`\n"
    assert (repo / "file").is_file()
    assert list(repo.rglob(".summem")) == []


def test_note_path_writes_started_store(tmp_path, monkeypatch, summem):
    """note --path into a started package writes there, not at git root."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "foo/packages/baz").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert m.main(["note", "--path", "foo/packages/baz/fee.ts", "child"]) == 0
    child_notes = [
        p for p in (repo / "foo" / "packages" / "baz" / ".summem" / "notes").iterdir() if not p.name.startswith(".")
    ]
    root_notes = repo / ".summem" / "notes"
    assert len(child_notes) == 1
    assert child_notes[0].read_text(encoding="utf-8") == "child\n"
    assert not root_notes.exists() or not any(p.name.startswith(".") is False for p in root_notes.iterdir())


def test_note_path_rolls_up_when_unstarted(tmp_path, monkeypatch, summem):
    """note --path under an unstarted sibling writes to the git-root store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "foo/packages/baz").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert m.main(["note", "--path", "foo/packages/other/x.ts", "rootish"]) == 0
    root_notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(root_notes) == 1
    assert root_notes[0].read_text(encoding="utf-8") == "rootish\n"
    other = repo / "foo" / "packages" / "other" / ".summem"
    assert not other.exists()


def test_nap_zoom_recall_path_use_started_store(tmp_path, monkeypatch, capsys, summem):
    """nap, zoom, and recall --path operate on the child store only."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    assert m.main(["note", "--path", ":/", "root-only"]) == 0
    ids = [node.id for node in m.list_view(repo / "pkg")]
    assert len(ids) == 2
    assert m.main(["nap", "--path", "pkg", ids[0], ids[1], "pair"]) == 0
    root_captions = {node.caption for node in m.list_view(repo)}
    assert "root-only" in root_captions
    assert "alpha" not in root_captions
    pkg_nodes = m.list_view(repo / "pkg")
    nap = next(node for node in pkg_nodes if node.kind == "nap")
    capsys.readouterr()
    assert m.main(["zoom", "--path", "pkg", nap.id]) == 0
    zoomed = capsys.readouterr().out
    assert "alpha" in zoomed
    assert "root-only" not in zoomed
    assert m.main(["recall", "--path", "pkg", "alpha"]) == 0
    recalled = capsys.readouterr().out
    assert "alpha" in recalled
    assert "root-only" not in recalled


def test_note_path_fold_request_is_copy_paste_safe(tmp_path, monkeypatch, capsys, summem):
    """A fold request after note --path is a command that naps that store from $PWD."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    (repo / "pkg" / ".summem" / "config.toml").write_text("WAKE_LINES = 1\n", encoding="utf-8")
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    capsys.readouterr()
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    out = capsys.readouterr().out
    run = next(line for line in out.splitlines() if line.startswith("Run: "))
    tokens = shlex.split(run.removeprefix("Run: "))
    tokens[-1] = "pair"
    assert m.main(tokens[1:]) == 0
    view = m.list_view(repo / "pkg")
    assert len(view) == 1
    assert view[0].kind == "nap"
    assert view[0].caption == "pair"


def test_config_wake_lines_is_per_store(tmp_path, monkeypatch, capsys, summem):
    """WAKE_LINES in one store's config does not change another store's budget."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 1\n", encoding="utf-8")
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", ":/", "root-a"]) == 0
    capsys.readouterr()
    assert m.main(["note", "--path", ":/", "root-b"]) == 0
    root_out = capsys.readouterr().out
    assert "Run:" in root_out
    assert "root-a" in root_out
    assert "root-b" in root_out
    assert m.main(["note", "--path", "pkg", "pkg-a"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-b"]) == 0
    pkg_out = capsys.readouterr().out
    assert "Saved to `:/pkg`" in pkg_out
    assert "Run:" not in pkg_out


def test_config_entry_chars_is_per_store_for_notes_and_naps(tmp_path, monkeypatch, capsys, summem):
    """ENTRY_CHARS applies per store to notes and nap captions, including above 280."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "tight").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "tight"]) == 0
    (repo / "wide").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "wide"]) == 0
    (repo / "tight" / ".summem" / "config.toml").write_text("ENTRY_CHARS = 5\n", encoding="utf-8")
    (repo / "wide" / ".summem" / "config.toml").write_text("ENTRY_CHARS = 300\n", encoding="utf-8")
    too_long = "toolong"
    n = len(too_long.encode("utf-8"))
    assert n == 7
    assert m.main(["note", "--path", "tight", too_long]) == 1
    note_err = capsys.readouterr().err
    assert str(n) in note_err
    assert "5" in note_err
    assert "280" not in note_err
    assert m.main(["note", "--path", ":/", too_long]) == 0
    assert m.main(["note", "--path", "tight", "ok"]) == 0
    assert m.main(["note", "--path", "tight", "ab"]) == 0
    ids = [node.id for node in m.list_view(repo / "tight")]
    capsys.readouterr()
    assert m.main(["nap", "--path", "tight", ids[0], ids[1], too_long]) == 1
    nap_err = capsys.readouterr().err
    assert str(n) in nap_err
    assert "5" in nap_err
    assert "280" not in nap_err
    assert m.main(["note", "--path", "wide", "x" * 281]) == 0


def test_unreadable_config_uses_defaults(tmp_path, monkeypatch, capsys, summem):
    """Unreadable config.toml uses defaults and is not rewritten."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    config = repo / ".summem" / "config.toml"
    config.write_text("{not toml", encoding="utf-8")
    before = config.read_bytes()
    assert m.main(["note", "--path", ":/", "hello"]) == 0
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "hello" in out
    assert config.read_bytes() == before


def test_omitted_config_wake_lines_uses_default_budget(tmp_path, monkeypatch, capsys, summem):
    """A store whose config.toml omits WAKE_LINES uses the default budget."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    assert m.main(["note", "--path", ":/", "alpha"]) == 0
    capsys.readouterr()
    assert m.main(["note", "--path", ":/", "beta"]) == 0
    out = capsys.readouterr().out
    assert "Run:" in out
    assert "alpha" in out
    assert "beta" in out


def _catalog_section(out: str) -> str:
    """Return the catalog section of a root-wake document, excluding later sections."""
    lines = out.splitlines()
    start = lines.index("== Additional SumMem Catalogs ==")
    end = len(lines)
    if "== Project-root Memories ==" in lines:
        end = lines.index("== Project-root Memories ==")
    elif lines and lines[-1] == "You are up to speed.":
        end = len(lines) - 1
    return "\n".join(lines[start:end])


def test_root_wake_catalog_is_labeled_paths_not_commands(tmp_path, monkeypatch, capsys, summem):
    """Root wake labels extra stores as :/paths, not as wake --path commands."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert lines[0] == "== SumMem Usage =="
    catalog = _catalog_section(out)
    assert "1: :/pkg" in lines
    assert ":/pkg" in catalog
    assert "summem wake --path pkg" not in catalog
    assert "wake --path" not in catalog
    assert "== Project-root Memories ==" not in out
    assert lines[-1] == "You are up to speed."
    assert "pkg-note" not in out


def test_empty_root_omits_project_root_header(tmp_path, monkeypatch, capsys, summem):
    """A cataloged repo with no root notes omits == Project-root Memories ==."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert out == m.how_to_text(catalog=True) + "\n" + m.catalog_text(repo, repo) + "You are up to speed.\n"
    assert "== Project-root Memories ==" not in out
    assert "Listed catalog lines" in out
    assert f"{m.AGENT_BIN} wake --path <path>" in out


def test_root_wake_starts_with_usage(tmp_path, monkeypatch, capsys, summem):
    """Empty root wake is how_to_text() plus the footer; no other sections."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert out == m.how_to_text() + "You are up to speed.\n"
    assert out.startswith("== SumMem Usage ==")
    assert "== Project-root Memories ==" not in out
    assert "== Additional SumMem Catalogs ==" not in out
    assert "catalog" not in out.lower()
    assert "wake --path" not in out


def test_pull_wake_omits_usage(tmp_path, monkeypatch, capsys, summem):
    """wake --path omits the Usage section."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake", "--path", "pkg"]) == 0
    out = capsys.readouterr().out
    assert "pkg-note" in out
    assert "== SumMem Usage ==" not in out
    assert out.endswith("You are up to speed.\n")


def test_root_wake_catalogs_other_store(tmp_path, monkeypatch, capsys, summem):
    """Root wake lists another started store under a catalog header."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", ":/", "root-note"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "root-note" in out
    assert ":/pkg" in out
    assert "== Additional SumMem Catalogs ==" in out
    assert "== Project-root Memories ==" in out
    assert "Listed catalog lines" in out
    assert f"{m.AGENT_BIN} wake --path <path>" in out
    catalog = _catalog_section(out)
    assert "summem wake --path pkg" not in catalog
    assert ".summem/summem" not in catalog
    assert "notes/" not in out
    assert "naps/" not in out
    assert git_free(out)


def test_catalog_hides_zero_count_child_store(tmp_path, monkeypatch, capsys, summem):
    """An empty started child store is omitted from catalog_text while started_stores still lists it."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "0: :/pkg" not in out.splitlines()
    assert ":/pkg" not in out
    assert "== Additional SumMem Catalogs ==" not in out
    assert (repo / "pkg").resolve() in {p.resolve() for p in m.started_stores(repo)}


def test_catalog_one_note_prints_one(tmp_path, monkeypatch, capsys, summem):
    """One loose note in a child store catalogs as 1: :/pkg without the note text."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert "1: :/pkg" in lines
    assert "pkg-note" not in out


def test_catalog_does_not_pad_count_width(tmp_path, monkeypatch, capsys, summem):
    """Catalog count prefixes are not digit-padded: 1: :/a next to 10: :/b."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "a").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "a"]) == 0
    assert m.main(["note", "--path", "a", "only"]) == 0
    (repo / "b").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "b"]) == 0
    for i in range(10):
        assert m.main(["note", "--path", "b", f"n{i}"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert "1: :/a" in lines
    assert "10: :/b" in lines
    assert "1:  ./a" not in lines


def test_catalog_text_does_not_list_view(tmp_path, monkeypatch, summem):
    """catalog_text counts filenames without parsing note UTF-8 or healing overlapping packs."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo / "pkg")]
    assert m.main(["nap", "--path", "pkg", ids[0], ids[1], "one"]) == 0
    node = m.list_view(repo / "pkg")[0]
    tree_bytes = node.tree_path.read_bytes()
    caption_two = m.note_file_bytes("two")
    stem_two = m.nap_stem(m._seq_prefix(node.name), node.id, 2, tree_bytes, caption_two)
    naps = repo / "pkg" / ".summem" / "naps"
    (naps / f"{stem_two}.tree").write_bytes(tree_bytes)
    (naps / f"{stem_two}.summ").write_bytes(caption_two)
    bad_note = repo / "pkg" / ".summem" / "notes" / "20260101T000099Z-0000000000000099"
    bad_note.write_bytes(b"\xff\xfe\n")
    text = m.catalog_text(repo, repo)
    assert "5: :/pkg" in text.splitlines()
    assert (naps / f"{node.name}.tree").is_file()
    assert (naps / f"{stem_two}.tree").is_file()


def test_catalog_folded_pair_counts_as_two(tmp_path, monkeypatch, capsys, summem):
    """A folded pair catalogs as 2: :/pkg, not 0: (lost) or 4: (both suffixes)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo / "pkg")]
    assert m.main(["nap", "--path", "pkg", ids[0], ids[1], "pair"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert "2: :/pkg" in lines
    assert "0: :/pkg" not in lines
    assert "4: :/pkg" not in lines
    loose = [
        p
        for p in (repo / "pkg" / ".summem" / "notes").iterdir()
        if p.is_file() and not p.name.startswith(".")
    ]
    assert loose == []


def test_catalog_skips_cached_notes_nap_unlinked(tmp_path, monkeypatch, capsys, summem):
    """Committed notes nap unlinked do not add to N before deletions are staged."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    git(["add", "-A"], repo)
    git(["commit", "-m", "two notes"], repo)
    ids = [node.id for node in m.list_view(repo / "pkg")]
    assert m.main(["nap", "--path", "pkg", ids[0], ids[1], "pair"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert "2: :/pkg" in lines
    assert "4: :/pkg" not in lines


def test_pull_wake_omits_catalog_and_root_notes(tmp_path, monkeypatch, capsys, summem):
    """wake --path on a child store omits the catalog and root notes."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", ":/", "root-note"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake", "--path", "pkg"]) == 0
    out = capsys.readouterr().out
    assert "pkg-note" in out
    assert "root-note" not in out
    assert "wake --path pkg" not in out
    assert "== Additional SumMem Catalogs ==" not in out
    assert "== Project-root Memories ==" not in out
    assert "== SumMem Usage ==" not in out
    assert "1: :/pkg" not in out.splitlines()


def test_ignored_store_omitted_from_catalog(tmp_path, monkeypatch, capsys, summem):
    """A gitignored store is omitted from the catalog."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / ".git" / "info" / "exclude").write_text("secret/.summem\n", encoding="utf-8")
    (repo / "secret").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "secret"]) == 0
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "secret", "hidden"]) == 0
    assert m.main(["note", "--path", "pkg", "visible"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert ":/pkg" in out
    assert ":/secret" not in out
    assert "wake --path pkg" not in out
    assert "wake --path secret" not in out


def test_gitignore_store_omitted_from_catalog(tmp_path, monkeypatch, capsys, summem):
    """A store ignored by .gitignore is omitted from the catalog."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / ".gitignore").write_text("hidden/.summem\n", encoding="utf-8")
    (repo / "hidden").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "hidden"]) == 0
    assert m.main(["note", "--path", "hidden", "hidden-note"]) == 0
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "visible-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert ":/pkg" in out
    assert ":/hidden" not in out


def test_file_ignored_config_still_catalogs_store(tmp_path, monkeypatch, capsys, summem):
    """A file-level gitignore of config.toml does not hide a store that has notes."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / ".gitignore").write_text("config.toml\n", encoding="utf-8")
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "visible"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert ":/pkg" in out
    assert "== Additional SumMem Catalogs ==" in out


def test_empty_summem_dir_without_files_is_not_started_or_cataloged(tmp_path, monkeypatch, capsys, summem):
    """An empty child .summem directory with no files is neither in started_stores nor cataloged."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "bare" / ".summem").mkdir(parents=True)
    (repo / "pkg").mkdir(parents=True, exist_ok=True)
    assert m.main(["start", "pkg"]) == 0
    stores = {p.resolve() for p in m.started_stores(repo)}
    assert (repo / "pkg").resolve() in stores
    assert (repo / "bare").resolve() not in stores
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert ":/pkg" in out
    assert ":/bare" not in out


def test_root_only_wake_labels_nonempty_document(tmp_path, monkeypatch, capsys, summem):
    """A repo with only the git-root store labels a non-empty document."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "--path", ":/", "hello"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert (
        out
        == m.how_to_text()
        + "\n== Project-root Memories ==\n"
        + m.wake_text(repo)
        + "You are up to speed.\n"
    )
    assert "== Additional SumMem Catalogs ==" not in out
    assert "catalog" not in out.lower()
    assert "wake --path" not in out


def test_started_stores_includes_root_and_other_parents(tmp_path, summem):
    """started_stores lists the git root store and a cataloged child store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    pkg = repo / "pkg"
    m.ensure_store(pkg)
    stores = {path.resolve() for path in m.started_stores(repo)}
    assert repo.resolve() in stores
    assert pkg.resolve() in stores


def test_started_stores_omits_root_without_store_directory(tmp_path, summem):
    """Tracked .summem paths do not list the git root if .summem is not a directory."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    (repo / ".summem" / "notes" / "placeholder").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", ".summem"], cwd=repo, check=True, capture_output=True)
    shutil.rmtree(repo / ".summem")
    stores = {path.resolve() for path in m.started_stores(repo)}
    assert repo.resolve() not in stores


def test_note_root_from_subdir_writes_git_root_store(tmp_path, monkeypatch, capsys, summem):
    """note --path :/ from any subdirectory (including inside a child store) writes to the root store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    sub = repo / "packages" / "cli" / "src"
    sub.mkdir(parents=True)
    monkeypatch.chdir(repo)
    assert m.main(["start", "packages/cli"]) == 0
    capsys.readouterr()
    monkeypatch.chdir(sub)
    assert m.main(["note", "--path", ":/", "whole-project"]) == 0
    assert capsys.readouterr().out == "Saved to `:/`\n"
    root_notes = [p for p in (repo / ".summem" / "notes").iterdir() if p.is_file() and not p.name.startswith(".")]
    child_notes = [
        p for p in (repo / "packages" / "cli" / ".summem" / "notes").iterdir() if p.is_file() and not p.name.startswith(".")
    ]
    assert len(root_notes) == 1
    assert root_notes[0].read_text(encoding="utf-8") == "whole-project\n"
    assert child_notes == []


def test_saved_to_and_start_paths_are_root_relative_from_subdir(tmp_path, monkeypatch, capsys, summem):
    """note, nap, and start run from a subdirectory print paths relative to the git root, not $PWD."""
    m = summem
    repo = init_repo(tmp_path / "r")
    cli_src = repo / "packages" / "cli" / "src"
    cli_src.mkdir(parents=True)
    monkeypatch.chdir(repo / "packages")
    assert m.main(["start", "cli"]) == 0
    assert capsys.readouterr().out == "There is a store in `:/packages/cli`.\n"
    assert m.main(["start", "missing"]) == 1
    assert capsys.readouterr().err == "not a directory: `:/packages/missing`\n"
    monkeypatch.chdir(repo)
    assert m.main(["note", "--path", "packages/cli/src/index.ts", "first"]) == 0
    assert capsys.readouterr().out == "Saved to `:/packages/cli`\n"
    monkeypatch.chdir(cli_src)
    assert m.main(["note", "--path", "index.ts", "second"]) == 0
    assert capsys.readouterr().out == "Saved to `:/packages/cli`\n"
    ids = [node.id for node in m.list_view(repo / "packages" / "cli")]
    assert m.main(["nap", "--path", ".", ids[0], ids[1], "both"]) == 0
    assert capsys.readouterr().out == "Saved to `:/packages/cli`\n\nNothing left to compress.\n"


def test_catalog_omits_empty_child_stores_and_header_when_none_remain(tmp_path, monkeypatch, capsys, summem):
    """Child stores with 0 notes are hidden from catalog_text, and the header disappears when all are empty."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / "empty").mkdir()
    (repo / "filled").mkdir()
    assert m.main(["start", "empty"]) == 0
    assert m.main(["start", "filled"]) == 0
    assert m.catalog_text(repo, repo) == ""
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    empty_wake = capsys.readouterr().out
    assert "== Additional SumMem Catalogs ==" not in empty_wake
    assert "wake --path" not in empty_wake

    assert m.main(["note", "--path", "filled", "one"]) == 0
    assert m.catalog_text(repo, repo) == "== Additional SumMem Catalogs ==\n1: :/filled\n"
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    mixed_wake = capsys.readouterr().out
    assert "1: :/filled" in mixed_wake.splitlines()
    assert ":/empty" not in mixed_wake



def test_resolve_colon_slash_is_root_from_any_dir(tmp_path, summem):
    """`:/` names the git root whatever the cwd; `:/rel` is root-relative (B1, B2)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    pkg = repo / "pkg"
    sib = repo / "sib" / "deep"
    pkg.mkdir()
    sib.mkdir(parents=True)
    m.ensure_store(pkg)
    assert m.resolve_parent(sib, ":/") == repo.resolve()
    assert m.resolve_parent(pkg, ":/") == repo.resolve()
    assert m.resolve_parent(sib, ":/pkg/f.py") == pkg.resolve()


def test_resolve_plain_path_stays_cwd_relative(tmp_path, summem):
    """A path without `:/` resolves against cwd, as before (B3)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    pkg = repo / "pkg"
    pkg.mkdir()
    m.ensure_store(pkg)
    assert m.resolve_parent(repo, "pkg/f.py") == pkg.resolve()
    assert m.resolve_parent(pkg, "f.py") == pkg.resolve()


@pytest.mark.parametrize("arg", [":x", ":(top)", ":!pkg"])
def test_resolve_refuses_unknown_colon_prefix(tmp_path, summem, arg):
    """Only `:/` is path magic; any other leading `:` is refused (B6)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError, match="unknown path prefix"):
        m.resolve_parent(repo, arg)


def test_resolve_dot_slash_escapes_a_literal_colon_name(tmp_path, summem):
    """`./:name` is a literal path, as in git."""
    m = summem
    repo = init_repo(tmp_path / "r")
    odd = repo / ":odd"
    odd.mkdir()
    m.ensure_store(odd)
    assert m.resolve_parent(repo, "./:odd") == odd.resolve()


def test_resolve_refuses_root_anchor_outside_repo(tmp_path, summem):
    """`:/..` leaves the repository and is refused (B7)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    with pytest.raises(ValueError, match="outside the repository"):
        m.resolve_parent(repo, ":/../elsewhere")


@pytest.mark.skipif(os.name == "nt", reason="POSIX symlinks")
def test_note_refuses_store_symlinked_outside_repo(tmp_path, monkeypatch, capsys, summem):
    """A `.summem` that resolves outside the repo is one stderr line, exit 1, no write (B8)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    outside = tmp_path / "outside"
    outside.mkdir()
    (repo / ".summem").symlink_to(outside, target_is_directory=True)
    monkeypatch.chdir(repo)
    assert m.main(["note", "--path", ":/", "x"]) == 1
    err = capsys.readouterr().err
    assert err.count("\n") == 1 and "outside the repository" in err
    assert list(outside.iterdir()) == []


def test_start_accepts_root_anchor_and_refuses_outside(tmp_path, monkeypatch, capsys, summem):
    """`start :/dir` works from any subdirectory; `start :/../x` is refused (B12)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    (repo / "newdir").mkdir()
    deep = repo / "a" / "b"
    deep.mkdir(parents=True)
    monkeypatch.chdir(deep)
    assert m.main(["start", ":/newdir"]) == 0
    assert capsys.readouterr().out == "There is a store in `:/newdir`.\n"
    assert m.is_store(repo / "newdir")
    (tmp_path / "x").mkdir()
    assert m.main(["start", ":/../x"]) == 1
    assert "outside the repository" in capsys.readouterr().err
    assert not m.is_store(tmp_path / "x")


def _printed_store_paths(m, repo, child, capsys):
    """Return every store path SumMem prints for *child* and the root, as printed."""
    printed = []
    assert m.main(["start", str(child)]) == 0
    printed.append(capsys.readouterr().out.removeprefix("There is a store in `").removesuffix("`.\n"))
    assert m.main(["note", "--path", str(child), "hello"]) == 0
    printed.append(capsys.readouterr().out.split("`")[1])
    assert m.main(["note", "--path", ":/", "root hello"]) == 0
    printed.append(capsys.readouterr().out.split("`")[1])
    m.write_note(child, "second", datetime.now(timezone.utc), Random(7))
    run = m.fold_request(child, 1)
    printed.append(re.search(r" nap --path ('[^']*'|\S+) ", run).group(1))
    assert m.main(["wake"]) == 0
    printed += [ln.split(": ", 1)[1] for ln in capsys.readouterr().out.splitlines() if ln[:1].isdigit()]
    return printed


@pytest.mark.parametrize("where", ["root", "child", "sibling"])
def test_every_printed_path_round_trips_as_path_arg(tmp_path, monkeypatch, capsys, summem, where):
    """Every path SumMem prints, passed back as --path from anywhere, names the same store (B16)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    child = repo / "team docs"
    child.mkdir()
    (repo / "sib").mkdir()
    monkeypatch.chdir(repo)
    printed = _printed_store_paths(m, repo, child, capsys)
    assert set(printed) == {"':/team docs'", ":/"}
    monkeypatch.chdir({"root": repo, "child": child, "sibling": repo / "sib"}[where])
    for shown in printed:
        (arg,) = shlex.split(shown)
        expect = repo.resolve() if arg == ":/" else child.resolve()
        assert m.resolve_parent(Path.cwd(), arg) == expect, shown


def test_fold_run_line_for_spaced_store_runs_from_sibling(tmp_path, monkeypatch, capsys, summem):
    """The quoted `Run:` line for `team docs`, shell-split and run from elsewhere, folds that store (B10)."""
    m = summem
    repo = init_repo(tmp_path / "r")
    child = repo / "team docs"
    child.mkdir()
    (repo / "sib").mkdir()
    m.ensure_store(child)
    for i, text in enumerate(["alpha", "beta"], 1):
        m.write_note(child, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=timezone.utc), Random(i))
    run = m.fold_request(child, 1).split("Run: ", 1)[1].splitlines()[0]
    assert "--path ':/team docs' " in run
    argv = shlex.split(run)[1:]
    argv[-1] = "alpha and beta"
    monkeypatch.chdir(repo / "sib")
    assert m.main(argv) == 0
    assert "Saved to `':/team docs'`" in capsys.readouterr().out
    assert [n.kind for n in m.list_view(child)] == ["nap"]


def test_sentence_paths_are_backticked_and_shell_quoted(tmp_path, monkeypatch, capsys, summem):
    """Paths inside sentences sit in backticks; a path needing quotes is shell-quoted everywhere."""
    m = summem
    repo = init_repo(tmp_path / "r")
    (repo / "team docs").mkdir()
    monkeypatch.chdir(repo)
    assert m.main(["start", "team docs"]) == 0
    assert capsys.readouterr().out == "There is a store in `':/team docs'`.\n"
    assert m.main(["start", "no such dir"]) == 1
    assert capsys.readouterr().err == "not a directory: `':/no such dir'`\n"
    assert m.main(["note", "--path", ":/team docs", "x"]) == 0
    assert capsys.readouterr().out == "Saved to `':/team docs'`\n"
    assert m.main(["note", "--path", ":/../out", "x"]) == 1
    assert capsys.readouterr().err == "outside the repository: `:/../out`\n"
    assert m.main(["note", "--path", ":x", "x"]) == 1
    assert capsys.readouterr().err.startswith("unknown path prefix: `:x`")
    assert m.main(["wake"]) == 0
    assert "1: ':/team docs'" in capsys.readouterr().out.splitlines()


@pytest.mark.parametrize("name", ["team’s docs", "‘a’ ‚b‛", "plain's"])
def test_printed_path_quoting_is_posix_and_powershell_safe(tmp_path, summem, name):
    """A printed path splits back exactly in POSIX, and no typographic single quote sits inside
    a single-quoted run, where PowerShell would read it as the closing quote."""
    m = summem
    repo = init_repo(tmp_path / "r")
    (repo / name).mkdir()
    shown = m._root_path(repo / name, repo)
    assert shlex.split(shown) == [f":/{name}"]
    in_single = False
    for ch in shown:
        if ch == "'":
            in_single = not in_single
        elif in_single:
            assert ch not in "‘’‚‛", shown
