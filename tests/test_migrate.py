"""Operator helper: rename complete four-part nap pairs to five-part stems."""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timezone
from importlib.machinery import SourceFileLoader
from random import Random

from conftest import ROOT, load_summem
from gitutil import init_repo

UTC = timezone.utc
MIGRATE = ROOT / "migrate.py"


def load_migrate():
    """Load repo-root migrate.py via SourceFileLoader."""
    loader = SourceFileLoader("migrate", str(MIGRATE))
    spec = importlib.util.spec_from_loader("migrate", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load migrate.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["migrate"] = mod
    spec.loader.exec_module(mod)
    return mod


def _two_notes(m, repo):
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))


def _legacy_complete_pair(m, repo, caption="pair"):
    """Fold two notes, then rename the five-part pair to its four-part stem."""
    _two_notes(m, repo)
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], caption)
    node = next(n for n in m.list_view(repo) if n.kind == "nap")
    parsed = m._parse_nap_stem(node.name)
    assert parsed is not None
    stamp, rand, leafset, grain, tag = parsed
    assert tag
    four = f"{stamp}-{rand}-{leafset}-{grain}"
    naps = repo / ".summem" / "naps"
    dest_tree = naps / f"{four}.tree"
    dest_summ = naps / f"{four}.summ"
    node.tree_path.rename(dest_tree)
    node.sum_path.rename(dest_summ)
    return four, dest_tree.read_bytes(), dest_summ.read_bytes()


def _five_part(m, four: str, tree_bytes: bytes, caption_bytes: bytes) -> str:
    parsed = m._parse_nap_stem(four)
    assert parsed is not None
    stamp, rand, leafset, grain, _variant = parsed
    return m.nap_stem(f"{stamp}-{rand}", leafset, grain, tree_bytes, caption_bytes)


def test_migrate_renames_four_part_complete_pair(tmp_path, monkeypatch):
    """A complete four-part pair is renamed to nap_stem of the on-disk bytes."""
    mig = load_migrate()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    four, tree_bytes, caption_bytes = _legacy_complete_pair(m, repo)
    expected = _five_part(m, four, tree_bytes, caption_bytes)
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    naps = repo / ".summem" / "naps"
    assert not (naps / f"{four}.tree").exists()
    assert not (naps / f"{four}.summ").exists()
    assert (naps / f"{expected}.tree").read_bytes() == tree_bytes
    assert (naps / f"{expected}.summ").read_bytes() == caption_bytes
    nodes = [n for n in m.list_view(repo) if n.kind == "nap"]
    assert len(nodes) == 1
    assert nodes[0].name == expected
    parsed = m._parse_nap_stem(nodes[0].name)
    assert parsed is not None and parsed[4]


def test_migrate_second_run_is_noop(tmp_path, monkeypatch):
    """A second run on an already five-part store exits 0 and does not rename."""
    mig = load_migrate()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _legacy_complete_pair(m, repo)
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    names = sorted(p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file())
    assert mig.main([]) == 0
    assert sorted(p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file()) == names


def test_migrate_skips_incomplete_pair(tmp_path, monkeypatch, capsys):
    """An incomplete four-part pair is skipped with a stderr message and non-zero exit."""
    mig = load_migrate()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    four, tree_bytes, _caption_bytes = _legacy_complete_pair(m, repo)
    naps = repo / ".summem" / "naps"
    (naps / f"{four}.summ").unlink()
    monkeypatch.chdir(repo)
    assert mig.main([]) != 0
    err = capsys.readouterr().err
    assert four in err
    assert (naps / f"{four}.tree").read_bytes() == tree_bytes
    assert not (naps / f"{four}.summ").exists()


def test_migrate_path_leaves_other_store_untouched(tmp_path, monkeypatch):
    """--path rewrites one store and does not touch another."""
    mig = load_migrate()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    four_root, _, _ = _legacy_complete_pair(m, repo, "root-pair")
    pkg = repo / "pkg"
    m.ensure_store(pkg)
    four_pkg, tree_pkg, cap_pkg = _legacy_complete_pair(m, pkg, "pkg-pair")
    monkeypatch.chdir(repo)
    assert mig.main(["--path", "pkg"]) == 0
    expected_pkg = _five_part(m, four_pkg, tree_pkg, cap_pkg)
    assert (pkg / ".summem" / "naps" / f"{expected_pkg}.tree").is_file()
    assert (repo / ".summem" / "naps" / f"{four_root}.tree").is_file()


def test_migrate_default_rewrites_root_and_cataloged_store(tmp_path, monkeypatch):
    """A default run rewrites the root store and a cataloged child store."""
    mig = load_migrate()
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    four_root, tree_root, cap_root = _legacy_complete_pair(m, repo, "root-pair")
    pkg = repo / "pkg"
    m.ensure_store(pkg)
    four_pkg, tree_pkg, cap_pkg = _legacy_complete_pair(m, pkg, "pkg-pair")
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    expected_root = _five_part(m, four_root, tree_root, cap_root)
    expected_pkg = _five_part(m, four_pkg, tree_pkg, cap_pkg)
    assert (repo / ".summem" / "naps" / f"{expected_root}.tree").is_file()
    assert (pkg / ".summem" / "naps" / f"{expected_pkg}.tree").is_file()
    assert not (repo / ".summem" / "naps" / f"{four_root}.tree").exists()
    assert not (pkg / ".summem" / "naps" / f"{four_pkg}.tree").exists()
