"""Store walk-up, start, --path, per-store config, and root-wake catalog."""

from __future__ import annotations

import shlex
import tomllib

from conftest import load_summem
from gitutil import init_repo


def test_resolve_subdir_without_store_is_git_root(tmp_path):
    """A subdirectory with no nested store resolves to the git root."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    assert m.resolve_parent(nested) == repo.resolve()
    assert m.resolve_parent(nested / "fee.ts") == repo.resolve()


def test_resolve_inside_started_dir_is_that_store(tmp_path):
    """Resolve from inside a started directory returns that directory."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    m.ensure_store(nested)
    assert m.is_store(nested)
    assert not m.is_store(repo / "foo")
    assert m.resolve_parent(nested) == nested.resolve()
    assert m.resolve_parent(nested / "src") == nested.resolve()


def test_resolve_path_file_walks_from_parent(tmp_path):
    """An existing file path walks from the file's parent directory."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    fee = nested / "fee.ts"
    fee.write_text("x\n", encoding="utf-8")
    m.ensure_store(nested)
    assert m.resolve_parent(repo, "foo/packages/baz/fee.ts") == nested.resolve()


def test_resolve_missing_file_walks_from_parent(tmp_path):
    """A missing file path walks from its parent directory."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    m.ensure_store(nested)
    assert m.resolve_parent(repo, "foo/packages/baz/fee.ts") == nested.resolve()


def test_resolve_omitted_path_uses_cwd(tmp_path):
    """Omitting path_arg walks from cwd."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    nested = repo / "pkg"
    nested.mkdir()
    m.ensure_store(nested)
    unstarted = repo / "other"
    unstarted.mkdir()
    assert m.resolve_parent(nested, None) == nested.resolve()
    assert m.resolve_parent(unstarted, None) == repo.resolve()
    assert m.resolve_parent(repo, None) == repo.resolve()


def test_start_creates_store_in_dir(tmp_path, monkeypatch):
    """start <dir> creates a store in that directory."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "foo/packages/baz"]) == 0
    store = repo / "foo" / "packages" / "baz" / ".summem"
    assert not (store / "summem").exists()
    assert (store / "notes").is_dir()
    assert (store / "naps").is_dir()
    config = (store / "config.toml").read_text(encoding="utf-8")
    assert tomllib.loads(config) == {}
    assert config.lstrip().startswith("#")


def test_start_does_not_create_ancestor_stores(tmp_path, monkeypatch):
    """start does not create .summem on ancestor directories."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert not (repo / "foo" / ".summem").exists()
    assert not (repo / "foo" / "packages" / ".summem").exists()
    assert (repo / "foo" / "packages" / "baz" / ".summem").is_dir()


def test_start_without_dir_is_usage(tmp_path, monkeypatch):
    """start without a directory exits nonzero."""
    m = load_summem()
    monkeypatch.chdir(init_repo(tmp_path / "r"))
    assert m.main(["start"]) != 0


def test_note_path_writes_started_store(tmp_path, monkeypatch):
    """note --path into a started package writes there, not at git root."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert m.main(["note", "--path", "foo/packages/baz/fee.ts", "child"]) == 0
    child_notes = [
        p for p in (repo / "foo" / "packages" / "baz" / ".summem" / "notes").iterdir() if not p.name.startswith(".")
    ]
    root_notes = repo / ".summem" / "notes"
    assert len(child_notes) == 1
    assert child_notes[0].read_text(encoding="utf-8") == "child\n"
    assert not root_notes.exists() or not any(p.name.startswith(".") is False for p in root_notes.iterdir())


def test_note_path_rolls_up_when_unstarted(tmp_path, monkeypatch):
    """note --path under an unstarted sibling writes to the git-root store."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "foo/packages/baz"]) == 0
    assert m.main(["note", "--path", "foo/packages/other/x.ts", "rootish"]) == 0
    root_notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(root_notes) == 1
    assert root_notes[0].read_text(encoding="utf-8") == "rootish\n"
    other = repo / "foo" / "packages" / "other" / ".summem"
    assert not other.exists()


def test_nap_zoom_recall_path_use_started_store(tmp_path, monkeypatch, capsys):
    """nap, zoom, and recall --path operate on the child store only."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    assert m.main(["note", "root-only"]) == 0
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


def test_note_path_fold_request_is_copy_paste_safe(tmp_path, monkeypatch, capsys):
    """A fold request after note --path is a command that naps that store from $PWD."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
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


def test_config_wake_lines_is_per_store(tmp_path, monkeypatch, capsys):
    """WAKE_LINES in one store's config does not change another store's budget."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 1\n", encoding="utf-8")
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "root-a"]) == 0
    capsys.readouterr()
    assert m.main(["note", "root-b"]) == 0
    root_out = capsys.readouterr().out
    assert "Run:" in root_out
    assert "root-a" in root_out
    assert "root-b" in root_out
    assert m.main(["note", "--path", "pkg", "pkg-a"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-b"]) == 0
    pkg_out = capsys.readouterr().out
    assert "Saved." in pkg_out
    assert "Run:" not in pkg_out


def test_config_entry_chars_is_per_store_for_notes_and_naps(tmp_path, monkeypatch, capsys):
    """ENTRY_CHARS applies per store to notes and nap captions, including above 280."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "tight"]) == 0
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
    assert m.main(["note", too_long]) == 0
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


def test_unreadable_config_uses_defaults(tmp_path, monkeypatch, capsys):
    """Unreadable config.toml uses defaults and is not rewritten."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    config = repo / ".summem" / "config.toml"
    config.write_text("{not toml", encoding="utf-8")
    before = config.read_bytes()
    assert m.main(["note", "hello"]) == 0
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "hello" in out
    assert config.read_bytes() == before


def test_monkeypatch_wake_lines_still_applies_when_config_omits_knob(tmp_path, monkeypatch, capsys):
    """Omitted WAKE_LINES still follows the module constant, including a monkeypatch."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    assert m.main(["note", "alpha"]) == 0
    capsys.readouterr()
    assert m.main(["note", "beta"]) == 0
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


def test_root_wake_catalog_is_labeled_paths_not_commands(tmp_path, monkeypatch, capsys):
    """Root wake labels extra stores as ./paths, not as wake --path commands."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert lines[0] == "== SumMem Usage =="
    catalog = _catalog_section(out)
    assert "./pkg" in lines
    assert "summem wake --path pkg" not in catalog
    assert "wake --path" not in catalog
    assert "== Project-root Memories ==" not in out
    assert lines[-1] == "You are up to speed."
    assert "pkg-note" not in out


def test_empty_root_omits_project_root_header(tmp_path, monkeypatch, capsys):
    """A cataloged repo with no root notes omits == Project-root Memories ==."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert out == m.how_to_text() + "\n" + m.catalog_text(repo, repo) + "You are up to speed.\n"
    assert "== Project-root Memories ==" not in out


def test_root_wake_starts_with_usage(tmp_path, monkeypatch, capsys):
    """Empty root wake is how_to_text() plus the footer; no other sections."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert out == m.how_to_text() + "You are up to speed.\n"
    assert out.startswith("== SumMem Usage ==")
    assert "== Project-root Memories ==" not in out
    assert "== Additional SumMem Catalogs ==" not in out


def test_pull_wake_omits_usage(tmp_path, monkeypatch, capsys):
    """wake --path omits the Usage section."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake", "--path", "pkg"]) == 0
    out = capsys.readouterr().out
    assert "pkg-note" in out
    assert "== SumMem Usage ==" not in out
    assert out.endswith("You are up to speed.\n")


def test_root_wake_catalogs_other_store(tmp_path, monkeypatch, capsys):
    """Root wake lists another started store under a catalog header."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "root-note"]) == 0
    assert m.main(["note", "--path", "pkg", "pkg-note"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "root-note" in out
    assert "./pkg" in out
    assert "== Additional SumMem Catalogs ==" in out
    assert "== Project-root Memories ==" in out
    catalog = _catalog_section(out)
    assert "summem wake --path pkg" not in catalog
    assert "notes/" not in out
    assert "naps/" not in out
    assert "git" not in out


def test_catalog_count_preserves_folded_note_grain(tmp_path, monkeypatch, capsys):
    """Catalog note count keeps encoded nap grain after a fold."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "pkg", "alpha"]) == 0
    assert m.main(["note", "--path", "pkg", "beta"]) == 0
    ids = [node.id for node in m.list_view(repo / "pkg")]
    assert m.main(["nap", "--path", "pkg", ids[0], ids[1], "pair"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "./pkg" in out
    assert "(2 notes" not in out
    loose = [
        p
        for p in (repo / "pkg" / ".summem" / "notes").iterdir()
        if p.is_file() and not p.name.startswith(".")
    ]
    assert loose == []


def test_pull_wake_omits_catalog_and_root_notes(tmp_path, monkeypatch, capsys):
    """wake --path on a child store omits the catalog and root notes."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "root-note"]) == 0
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


def test_ignored_store_omitted_from_catalog(tmp_path, monkeypatch, capsys):
    """A gitignored store is omitted from the catalog."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    (repo / ".git" / "info" / "exclude").write_text("secret/.summem\n", encoding="utf-8")
    assert m.main(["start", "secret"]) == 0
    assert m.main(["start", "pkg"]) == 0
    assert m.main(["note", "--path", "secret", "hidden"]) == 0
    assert m.main(["note", "--path", "pkg", "visible"]) == 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    out = capsys.readouterr().out
    assert "./pkg" in out
    assert "./secret" not in out
    assert "wake --path pkg" not in out
    assert "wake --path secret" not in out


def test_root_only_wake_labels_nonempty_document(tmp_path, monkeypatch, capsys):
    """A repo with only the git-root store labels a non-empty document."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "hello"]) == 0
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

