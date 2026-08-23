"""Emergency zipper surgery: locate a raw note, break out, unlink, heal."""

from __future__ import annotations

import importlib.util
import shlex
import sys
from datetime import datetime, timedelta, timezone
from importlib.machinery import SourceFileLoader
from pathlib import Path
from random import Random

import pytest

from conftest import ROOT, load_summem
from gitutil import assert_unique_cover, init_repo, reaches

UTC = timezone.utc
SURGERY = ROOT / "surgery.py"


def load_surgery():
    """Load repo-root surgery.py via SourceFileLoader."""
    loader = SourceFileLoader("surgery", str(SURGERY))
    spec = importlib.util.spec_from_loader("surgery", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load surgery.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["surgery"] = mod
    spec.loader.exec_module(mod)
    return mod


def _write_notes(m, repo, texts, start=1):
    paths = []
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(texts):
        paths.append(
            m.write_note(
                repo, text, base + timedelta(seconds=start + i), Random(start + i)
            )
        )
    return paths


def _balanced_4(m, repo, texts, cap_ab, cap_cd, cap_p, start):
    paths = _write_notes(m, repo, texts, start=start)
    names = {p.name for p in paths}
    nodes = [n for n in m.list_view(repo) if n.name in names]
    m.write_nap(repo, nodes[0].id, nodes[1].id, cap_ab)
    c = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[2])
    d = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[3])
    m.write_nap(repo, c.id, d.id, cap_cd)
    ab = next(n for n in m.list_view(repo) if n.caption == cap_ab)
    cd = next(n for n in m.list_view(repo) if n.caption == cap_cd)
    m.write_nap(repo, ab.id, cd.id, cap_p)
    return paths, next(n for n in m.list_view(repo) if n.caption == cap_p)


def _payload_names(repo: Path) -> set[str]:
    names = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def test_contains_unique_nested_note(tmp_path):
    """--contains matching one nested NoteChild returns that filename."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-surgery-secret-aa11"
    paths, _parent = _balanced_4(m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1)
    assert s.locate_note(m, repo, contains=secret, name=None) == paths[0].name


def test_filename_locates_nested_note(tmp_path):
    """A unique note filename or seq prefix locates a nested NoteChild."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    paths, _parent = _balanced_4(m, repo, ["keep-a", "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1)
    assert s.locate_note(m, repo, contains=None, name=paths[2].name) == paths[2].name
    seq = m._seq_prefix(paths[2].name)
    assert s.locate_note(m, repo, contains=None, name=seq) == paths[2].name


def test_contains_duplicate_text_requires_filename(tmp_path):
    """--contains that matches two identical notes raises until a filename is given."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    paths = _write_notes(m, repo, ["same-line", "same-line"])
    with pytest.raises(ValueError):
        s.locate_note(m, repo, contains="same-line", name=None)
    assert s.locate_note(m, repo, contains=None, name=paths[1].name) == paths[1].name


def test_contains_nap_caption_only_is_not_found(tmp_path):
    """A substring that hits only a nap caption is not a delete target."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["alpha", "beta"])
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "SECRET_CAPTION_ONLY")
    with pytest.raises(ValueError):
        s.locate_note(m, repo, contains="SECRET_CAPTION_ONLY", name=None)


def test_unknown_target_errors(tmp_path):
    """A missing note raises ValueError and does not change the store."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["keep-me"])
    before = _payload_names(repo)
    with pytest.raises(ValueError):
        s.locate_note(m, repo, contains="no-such-sentence", name=None)
    assert _payload_names(repo) == before


def _plant_nap(m, repo, kids, caption: str):
    tree = m.Tree(kids=list(kids))
    digests = m._digests_of_tree(tree)
    child = m.NapChild(id=m.leafset_id(digests), sum=caption, tree=tree)
    m.rematerialize_child(repo, child)
    return child


def _tree_embeds(repo: Path, sentence: str) -> bool:
    naps = repo / ".summem" / "naps"
    if not naps.is_dir():
        return False
    needle = sentence.encode("utf-8")
    for path in naps.iterdir():
        if path.suffix == ".tree" and path.is_file() and needle in path.read_bytes():
            return True
    return False


def _store_bytes(repo: Path) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        for path in root.iterdir():
            if path.is_file() and not path.name.startswith("."):
                out[f"{folder}/{path.name}"] = path.read_bytes()
    return out


def test_excise_loose_note(tmp_path):
    """A loose note is unlinked; siblings remain; heal still covers unique leaves."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-loose-secret-cc33"
    paths = _write_notes(m, repo, [secret, "keep-sibling"])
    chain = s.excise_note(m, repo, paths[0].name)
    assert chain == [paths[0].name]
    assert not (repo / ".summem" / "notes" / paths[0].name).exists()
    assert (repo / ".summem" / "notes" / paths[1].name).is_file()
    assert_unique_cover(m, repo)
    assert not reaches(m, repo, secret)
    assert secret not in m.recall_text(repo, secret)
    assert reaches(m, repo, "keep-sibling")


def test_excise_nested_note_unzips_then_unlinks(tmp_path):
    """Nested target is rematerialized to notes/, unlinked, and gone from remaining trees."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-nested-secret-dd44"
    paths, parent = _balanced_4(
        m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1
    )
    assert _tree_embeds(repo, secret)
    chain = s.excise_note(m, repo, paths[0].name)
    assert chain[-1] == paths[0].name
    assert parent.name in chain
    assert not (repo / ".summem" / "notes" / paths[0].name).exists()
    assert not _tree_embeds(repo, secret)
    assert_unique_cover(m, repo)
    assert not reaches(m, repo, secret)
    assert secret not in m.recall_text(repo, secret)
    assert reaches(m, repo, "keep-b")
    assert reaches(m, repo, "keep-c")
    assert reaches(m, repo, "keep-d")


def test_excise_overlapping_packs_clears_remaining_trees(tmp_path):
    """Every view nap that embeds the target is split before unlink."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-overlap-secret-ee55"
    paths = _write_notes(m, repo, [secret, "keep-b", "keep-c", "keep-d"])
    kids = [
        m.NoteChild(name=path.name, text=path.read_text(encoding="utf-8").removesuffix("\n"))
        for path in paths
    ]
    for node in list(m.list_view(repo)):
        m._unlink_node(node)
    _plant_nap(m, repo, kids[:2], "ab")
    _plant_nap(m, repo, kids, "abcd")
    assert _tree_embeds(repo, secret)
    chain = s.excise_note(m, repo, kids[0].name)
    assert kids[0].name == chain[-1]
    assert len(chain) >= 3
    assert not _tree_embeds(repo, secret)
    assert_unique_cover(m, repo)
    assert not reaches(m, repo, secret)
    assert secret not in m.recall_text(repo, secret)
    assert reaches(m, repo, "keep-b")
    assert reaches(m, repo, "keep-d")


def test_excise_does_not_call_write_nap(tmp_path, monkeypatch):
    """Excise never invents a caption via write_nap."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-nonap-secret-ff66"
    paths, _parent = _balanced_4(
        m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1
    )

    def boom(*_args, **_kwargs):
        raise AssertionError("write_nap must not be called")

    monkeypatch.setattr(m, "write_nap", boom)
    s.excise_note(m, repo, paths[0].name)
    assert not reaches(m, repo, secret)


def test_dry_run_prints_chain_and_writes_nothing(tmp_path):
    """Dry-run returns the rematerialize chain and does not change store bytes."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-dryrun-secret-gg77"
    paths, parent = _balanced_4(
        m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1
    )
    before = _store_bytes(repo)
    chain = s.excise_note(m, repo, paths[0].name, dry_run=True)
    assert chain[-1] == paths[0].name
    assert parent.name in chain
    assert _store_bytes(repo) == before
    assert _tree_embeds(repo, secret)
    assert reaches(m, repo, secret)


def test_dry_run_unknown_writes_nothing(tmp_path):
    """Dry-run of a missing note still errors and writes nothing."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _write_notes(m, repo, ["keep-me"])
    before = _store_bytes(repo)
    with pytest.raises(ValueError):
        s.excise_note(m, repo, "no-such-note-name", dry_run=True)
    assert _store_bytes(repo) == before


def test_identical_text_deletes_only_named_file(tmp_path):
    """Filename addressing drops one of two identical notes and keeps the other."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    paths = _write_notes(m, repo, ["same-line", "same-line"])
    s.excise_note(m, repo, paths[0].name)
    assert not (repo / ".summem" / "notes" / paths[0].name).exists()
    assert (repo / ".summem" / "notes" / paths[1].name).is_file()
    assert reaches(m, repo, "same-line")
    assert "same-line" in m.recall_text(repo, "same-line")


def test_main_contains_excises(tmp_path, monkeypatch, capsys):
    """main(['--contains', sentence]) excises that nested note from cwd's store."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-cli-secret-hh88"
    paths, parent = _balanced_4(
        m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1
    )
    monkeypatch.chdir(repo)
    assert s.main(["--contains", secret]) == 0
    out = capsys.readouterr().out
    assert parent.name in out
    assert paths[0].name in out.splitlines()[-1]
    assert not reaches(m, repo, secret)
    assert not _tree_embeds(repo, secret)
    assert_unique_cover(m, repo)


def test_main_dry_run(tmp_path, monkeypatch, capsys):
    """main(['--dry-run', '--contains', sentence]) prints the chain and writes nothing."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-clidry-secret-ii99"
    paths, parent = _balanced_4(
        m, repo, [secret, "keep-b", "keep-c", "keep-d"], "ab", "cd", "abcd", start=1
    )
    before = _store_bytes(repo)
    monkeypatch.chdir(repo)
    assert s.main(["--dry-run", "--contains", secret]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert parent.name in lines
    assert paths[0].name == lines[-1]
    assert _store_bytes(repo) == before
    assert reaches(m, repo, secret)


def test_main_path_flag(tmp_path, monkeypatch):
    """--path aims at a started store the same way resolve_parent does."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    secret = "sentinel-path-secret-jj00"
    path = m.write_note(repo / "pkg", secret, datetime(2026, 1, 1, tzinfo=UTC), Random(1))
    assert s.main(["--path", "pkg", "--contains", secret]) == 0
    assert not (repo / "pkg" / ".summem" / "notes" / path.name).exists()
    assert not reaches(m, repo / "pkg", secret)


def test_main_usage_without_target(tmp_path, monkeypatch, capsys):
    """Neither --contains nor a name is usage (exit 2)."""
    s = load_surgery()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert s.main([]) == 2
    err = capsys.readouterr().err
    assert err


def test_main_version_prints_script_version(capsys):
    """main(['version']) exits 0 and prints surgery.__version__ plus a newline."""
    s = load_surgery()
    assert s.main(["version"]) == 0
    assert capsys.readouterr().out == f"{s.__version__}\n"


def test_main_version_outside_repository(tmp_path, monkeypatch, capsys):
    """version outside a repository exits 0 and creates no store."""
    s = load_surgery()
    monkeypatch.chdir(tmp_path)
    assert s.main(["version"]) == 0
    assert capsys.readouterr().out == f"{s.__version__}\n"
    assert not (tmp_path / ".summem").exists()


def test_main_version_rejects_extra_args():
    """version with an extra token exits nonzero."""
    s = load_surgery()
    assert s.main(["version", "x"]) != 0


def test_main_prints_fold_request_when_over_budget(tmp_path, monkeypatch, capsys):
    """After excision, stdout includes fold_request so an agent can start the nap cascade."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-fold-secret-kk11"
    paths = _write_notes(m, repo, [secret, "keep-b", "keep-c", "keep-d"])
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 2\n", encoding="utf-8")
    ids_before = [node.id for node in m.list_view(repo)]
    monkeypatch.chdir(repo)
    assert s.main(["--contains", secret]) == 0
    out = capsys.readouterr().out
    assert paths[0].name in out.splitlines()
    assert "Compress these two into one line of at most 280 characters." in out
    assert 'Run: .summem/summem nap ' in out
    remain = [node for node in m.list_view(repo) if node.kind == "note"]
    assert len(remain) == 3
    remain_ids = [node.id for node in remain]
    pa = m.short_id(remain_ids[0], remain_ids)
    pb = m.short_id(remain_ids[1], remain_ids)
    assert f"nap {pa} {pb} " in out
    assert ids_before[0] not in out


def test_main_path_fold_request_is_copy_paste_safe(tmp_path, monkeypatch, capsys):
    """After --path excision over budget, Run: naps that store from $PWD."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["start", "pkg"]) == 0
    secret = "sentinel-fold-path-secret-mm33"
    _write_notes(m, repo / "pkg", [secret, "keep-b", "keep-c", "keep-d"])
    (repo / "pkg" / ".summem" / "config.toml").write_text("WAKE_LINES = 2\n", encoding="utf-8")
    assert s.main(["--path", "pkg", "--contains", secret]) == 0
    out = capsys.readouterr().out
    run = next(line for line in out.splitlines() if line.startswith("Run: "))
    tokens = shlex.split(run.removeprefix("Run: "))
    tokens[-1] = "pair"
    assert m.main(tokens[1:]) == 0
    view = m.list_view(repo / "pkg")
    assert any(node.kind == "nap" and node.caption == "pair" for node in view)


def test_main_dry_run_omits_fold_request(tmp_path, monkeypatch, capsys):
    """Dry-run does not print a fold request; the store is unchanged."""
    s = load_surgery()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    secret = "sentinel-dryfold-secret-ll22"
    _write_notes(m, repo, [secret, "keep-b", "keep-c", "keep-d"])
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 2\n", encoding="utf-8")
    monkeypatch.chdir(repo)
    assert s.main(["--dry-run", "--contains", secret]) == 0
    out = capsys.readouterr().out
    assert "Compress these two" not in out
    assert "Run: .summem/summem nap" not in out
