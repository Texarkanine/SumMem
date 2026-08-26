"""Operator helper: rewrite complete 4-part-64 and 5-part-64 nap pairs to five-part-16."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from importlib.machinery import SourceFileLoader

from conftest import ROOT
from gitutil import init_repo

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


def _full_leafset(digests: list[str]) -> str:
    """Return the 64-hex SHA-256 of sorted concatenated digest hex (pre-truncate)."""
    full = hashlib.sha256("".join(sorted(digests)).encode("ascii")).hexdigest()
    assert len(full) == 64
    return full


def _note(m, text: str, second: int, nibble: int):
    """Return a NoteChild and its file-byte digest with a deterministic name."""
    name = f"20260101T0000{second:02d}Z-{f'{nibble:x}' * 16}"
    return m.NoteChild(name=name, text=text), m.note_digest(m.note_file_bytes(text))


def _leftmost_note(m, tree):
    """Return the leftmost NoteChild under *tree*."""
    child = tree.kids[0]
    if isinstance(child, m.NoteChild):
        return child
    return _leftmost_note(m, child.tree)


def _truncate_nap_ids(m, tree):
    """Return a copy of *tree* with every 64-hex NapChild.id shortened to 16 hex."""
    kids = []
    for child in tree.kids:
        if isinstance(child, m.NapChild):
            nested = _truncate_nap_ids(m, child.tree)
            nid = child.id[:16] if len(child.id) == 64 else child.id
            kids.append(m._replace(child, id=nid, tree=nested))
        else:
            kids.append(child)
    return m._replace(tree, kids=kids)


def _all_nap_ids(m, tree) -> list[str]:
    """Return every NapChild.id under *tree*, recursively."""
    ids = []
    for child in tree.kids:
        if isinstance(child, m.NapChild):
            ids.append(child.id)
            ids.extend(_all_nap_ids(m, child.tree))
    return ids


def _oracle(m, seq: str, full: str, grain: int, tree, caption_bytes: bytes):
    """Return dest stem and rewritten tree bytes after shortening nested nap ids."""
    rewritten = m.dumps_tree(_truncate_nap_ids(m, tree))
    dest = m.nap_stem(seq, full[:16], grain, rewritten, caption_bytes)
    return dest, rewritten


def _plant(naps, stem: str, tree_bytes: bytes, caption_bytes: bytes) -> None:
    (naps / f"{stem}.tree").write_bytes(tree_bytes)
    (naps / f"{stem}.summ").write_bytes(caption_bytes)


def _grain2(m, a="alpha", b="beta", sa=1, sb=2, na=1, nb=2):
    """Return note-only grain-2 tree, digests, and seq prefix."""
    left, da = _note(m, a, sa, na)
    right, db = _note(m, b, sb, nb)
    tree = m.Tree(kids=[left, right])
    return tree, [da, db], m._seq_prefix(left.name)


def _grain2_child(m, texts, caption, seconds, nibbles):
    """Return a 64-hex-id grain-2 NapChild plus its note digests."""
    kids = []
    digests = []
    for text, second, nibble in zip(texts, seconds, nibbles, strict=True):
        child, digest = _note(m, text, second, nibble)
        kids.append(child)
        digests.append(digest)
    tree = m.Tree(kids=kids)
    return m.NapChild(id=_full_leafset(digests), sum=caption, tree=tree), digests


def _grain4(m):
    """Return a grain-4 tree whose two NapChild ids are 64 hex."""
    ab, d_ab = _grain2_child(m, ("A", "B"), "ab", (1, 2), (1, 2))
    cd, d_cd = _grain2_child(m, ("C", "D"), "cd", (3, 4), (3, 4))
    tree = m.Tree(kids=[ab, cd])
    return tree, d_ab + d_cd, m._seq_prefix(_leftmost_note(m, tree).name)


def _grain8(m):
    """Return a grain-8 tree with 64-hex nap ids at two nested depths."""
    ab, d_ab = _grain2_child(m, ("A", "B"), "ab", (1, 2), (1, 2))
    cd, d_cd = _grain2_child(m, ("C", "D"), "cd", (3, 4), (3, 4))
    ef, d_ef = _grain2_child(m, ("E", "F"), "ef", (5, 6), (5, 6))
    gh, d_gh = _grain2_child(m, ("G", "H"), "gh", (7, 8), (7, 8))
    abcd = m.NapChild(id=_full_leafset(d_ab + d_cd), sum="abcd", tree=m.Tree(kids=[ab, cd]))
    efgh = m.NapChild(id=_full_leafset(d_ef + d_gh), sum="efgh", tree=m.Tree(kids=[ef, gh]))
    tree = m.Tree(kids=[abcd, efgh])
    return tree, d_ab + d_cd + d_ef + d_gh, m._seq_prefix(_leftmost_note(m, tree).name)


def _plant_legacy(m, repo, tree, caption: str, full: str, grain: int, form: str):
    """Write a 4-part-64 or 5-part-64 pair. Return stem, on-disk bytes, and seq."""
    naps = m.ensure_store(repo) / "naps"
    seq = m._seq_prefix(_leftmost_note(m, tree).name)
    tree_bytes = m.dumps_tree(tree)
    caption_bytes = m.note_file_bytes(caption)
    if form == "four":
        stem = f"{seq}-{full}-{grain}"
    elif form == "five64":
        stem = m.nap_stem(seq, full, grain, tree_bytes, caption_bytes)
    else:
        raise ValueError(form)
    _plant(naps, stem, tree_bytes, caption_bytes)
    return stem, tree_bytes, caption_bytes, seq


def test_migrate_renames_four_part_complete_pair(tmp_path, monkeypatch, summem):
    """A complete four-part-64 pair is rewritten to nap_stem of the shortened tree."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _seq = _grain2(m)
    full = _full_leafset(digests)
    stem, tree_bytes, caption_bytes, seq = _plant_legacy(m, repo, tree, "pair", full, 2, "four")
    dest, rewritten = _oracle(m, seq, full, 2, tree, caption_bytes)
    assert rewritten == tree_bytes
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    naps = repo / ".summem" / "naps"
    assert not (naps / f"{stem}.tree").exists()
    assert not (naps / f"{stem}.summ").exists()
    assert (naps / f"{dest}.tree").read_bytes() == rewritten
    assert (naps / f"{dest}.summ").read_bytes() == caption_bytes
    nodes = [n for n in m.list_view(repo) if n.kind == "nap"]
    assert len(nodes) == 1
    assert nodes[0].name == dest
    parsed = m._parse_nap_stem(nodes[0].name)
    assert parsed is not None and parsed[4]
    assert len(parsed[2]) == 16


def test_migrate_second_run_is_noop(tmp_path, monkeypatch, summem):
    """A second run on an already five-part-16 store exits 0 and does not rename."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _seq = _grain2(m)
    _plant_legacy(m, repo, tree, "pair", _full_leafset(digests), 2, "four")
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    names = sorted(p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file())
    assert mig.main([]) == 0
    assert sorted(p.name for p in (repo / ".summem" / "naps").iterdir() if p.is_file()) == names


def test_migrate_skips_incomplete_pair(tmp_path, monkeypatch, capsys, summem):
    """An incomplete four-part-64 pair is skipped with a stderr message and non-zero exit."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _seq = _grain2(m)
    stem, tree_bytes, _caption_bytes, _seq = _plant_legacy(
        m, repo, tree, "pair", _full_leafset(digests), 2, "four"
    )
    naps = repo / ".summem" / "naps"
    (naps / f"{stem}.summ").unlink()
    monkeypatch.chdir(repo)
    assert mig.main([]) != 0
    err = capsys.readouterr().err
    assert "incomplete pair:" in err
    assert stem in err
    assert (naps / f"{stem}.tree").read_bytes() == tree_bytes
    assert not (naps / f"{stem}.summ").exists()


def test_migrate_path_leaves_other_store_untouched(tmp_path, monkeypatch, summem):
    """--path rewrites one store and does not touch another."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree_root, d_root, _ = _grain2(m, "root-a", "root-b", 1, 2, 1, 2)
    stem_root, _, _, _ = _plant_legacy(
        m, repo, tree_root, "root-pair", _full_leafset(d_root), 2, "four"
    )
    pkg = repo / "pkg"
    tree_pkg, d_pkg, _ = _grain2(m, "pkg-a", "pkg-b", 3, 4, 3, 4)
    stem_pkg, tree_bytes, cap, seq = _plant_legacy(
        m, pkg, tree_pkg, "pkg-pair", _full_leafset(d_pkg), 2, "four"
    )
    dest_pkg, _rewritten = _oracle(m, seq, _full_leafset(d_pkg), 2, tree_pkg, cap)
    monkeypatch.chdir(repo)
    assert mig.main(["--path", "pkg"]) == 0
    assert (pkg / ".summem" / "naps" / f"{dest_pkg}.tree").is_file()
    assert (repo / ".summem" / "naps" / f"{stem_root}.tree").is_file()
    assert not (pkg / ".summem" / "naps" / f"{stem_pkg}.tree").exists()


def test_migrate_default_rewrites_root_and_cataloged_store(tmp_path, monkeypatch, summem):
    """A default run rewrites the root store and a cataloged child store."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree_root, d_root, _ = _grain2(m, "root-a", "root-b", 1, 2, 1, 2)
    stem_root, _tb, cap_root, seq_root = _plant_legacy(
        m, repo, tree_root, "root-pair", _full_leafset(d_root), 2, "four"
    )
    pkg = repo / "pkg"
    tree_pkg, d_pkg, _ = _grain2(m, "pkg-a", "pkg-b", 3, 4, 3, 4)
    stem_pkg, _tb2, cap_pkg, seq_pkg = _plant_legacy(
        m, pkg, tree_pkg, "pkg-pair", _full_leafset(d_pkg), 2, "four"
    )
    dest_root, _ = _oracle(m, seq_root, _full_leafset(d_root), 2, tree_root, cap_root)
    dest_pkg, _ = _oracle(m, seq_pkg, _full_leafset(d_pkg), 2, tree_pkg, cap_pkg)
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    assert (repo / ".summem" / "naps" / f"{dest_root}.tree").is_file()
    assert (pkg / ".summem" / "naps" / f"{dest_pkg}.tree").is_file()
    assert not (repo / ".summem" / "naps" / f"{stem_root}.tree").exists()
    assert not (pkg / ".summem" / "naps" / f"{stem_pkg}.tree").exists()


def test_migrate_rewrites_five_part_64_grain2(tmp_path, monkeypatch, summem):
    """A complete five-part-64 grain-2 pair becomes five-part-16; a second run is a no-op."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _ = _grain2(m)
    full = _full_leafset(digests)
    stem, tree_bytes, caption_bytes, seq = _plant_legacy(m, repo, tree, "pair", full, 2, "five64")
    dest, rewritten = _oracle(m, seq, full, 2, tree, caption_bytes)
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    naps = repo / ".summem" / "naps"
    assert not (naps / f"{stem}.tree").exists()
    assert (naps / f"{dest}.tree").read_bytes() == rewritten
    assert (naps / f"{dest}.summ").read_bytes() == caption_bytes
    names = sorted(p.name for p in naps.iterdir() if p.is_file())
    assert mig.main([]) == 0
    assert sorted(p.name for p in naps.iterdir() if p.is_file()) == names


def test_migrate_rewrites_five_part_64_grain4_nested_ids(tmp_path, monkeypatch, summem):
    """A five-part-64 grain-4 pair shortens nested nap ids and recomputes the variant tag."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _ = _grain4(m)
    full = _full_leafset(digests)
    stem, tree_bytes, caption_bytes, seq = _plant_legacy(m, repo, tree, "abcd", full, 4, "five64")
    dest, rewritten = _oracle(m, seq, full, 4, tree, caption_bytes)
    assert rewritten != tree_bytes
    old_tag = stem.split("-")[-1]
    new_tag = dest.split("-")[-1]
    assert new_tag != old_tag
    assert new_tag == m.variant_tag(rewritten, caption_bytes)
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    naps = repo / ".summem" / "naps"
    assert (naps / f"{dest}.tree").read_bytes() == rewritten
    assert (naps / f"{dest}.summ").read_bytes() == caption_bytes
    loaded = m.loads_tree((naps / f"{dest}.tree").read_bytes())
    nested = _all_nap_ids(m, loaded)
    assert nested
    assert all(len(cid) == 16 for cid in nested)
    assert dest == m.nap_stem(seq, full[:16], 4, rewritten, caption_bytes)


def test_migrate_rewrites_five_part_64_grain8_two_depths(tmp_path, monkeypatch, summem):
    """A five-part-64 grain-8 pair shortens child and grandchild nap ids; dest hashes rewritten bytes."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _ = _grain8(m)
    full = _full_leafset(digests)
    stem, tree_bytes, caption_bytes, seq = _plant_legacy(m, repo, tree, "abcdefgh", full, 8, "five64")
    dest, rewritten = _oracle(m, seq, full, 8, tree, caption_bytes)
    assert rewritten != tree_bytes
    assert len(_all_nap_ids(m, tree)) == 6
    assert any(len(cid) == 64 for cid in _all_nap_ids(m, tree))
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    naps = repo / ".summem" / "naps"
    assert not (naps / f"{stem}.tree").exists()
    dest_tree = naps / f"{dest}.tree"
    assert dest_tree.read_bytes() == rewritten
    loaded = m.loads_tree(dest_tree.read_bytes())
    ids = _all_nap_ids(m, loaded)
    assert len(ids) == 6
    assert all(len(cid) == 16 for cid in ids)
    shallow = [child.id for child in loaded.kids if isinstance(child, m.NapChild)]
    assert len(shallow) == 2
    assert dest == m.nap_stem(seq, full[:16], 8, rewritten, caption_bytes)
    assert dest.split("-")[-1] == m.variant_tag(rewritten, caption_bytes)


def test_migrate_leaves_five_part_16_untouched(tmp_path, monkeypatch, summem):
    """A five-part-16 pair already on disk is not renamed or rewritten."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    m.ensure_store(repo)
    left, da = _note(m, "alpha", 1, 1)
    right, db = _note(m, "beta", 2, 2)
    notes = repo / ".summem" / "notes"
    (notes / left.name).write_bytes(m.note_file_bytes("alpha"))
    (notes / right.name).write_bytes(m.note_file_bytes("beta"))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    naps = repo / ".summem" / "naps"
    before = {p.name: p.read_bytes() for p in naps.iterdir() if p.is_file()}
    assert before
    stem = next(naps.glob("*.tree")).stem
    parsed = m._parse_nap_stem(stem)
    assert parsed is not None and len(parsed[2]) == 16
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    after = {p.name: p.read_bytes() for p in naps.iterdir() if p.is_file()}
    assert after == before


def test_migrate_dest_exists_skips_silently(tmp_path, monkeypatch, capsys, summem):
    """If the destination already exists, skip silently, leave the source, and exit 0."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _ = _grain2(m)
    full = _full_leafset(digests)
    stem, tree_bytes, caption_bytes, seq = _plant_legacy(m, repo, tree, "pair", full, 2, "four")
    dest, rewritten = _oracle(m, seq, full, 2, tree, caption_bytes)
    naps = repo / ".summem" / "naps"
    (naps / f"{dest}.tree").write_bytes(b"already-tree\n")
    (naps / f"{dest}.summ").write_bytes(b"already-summ\n")
    monkeypatch.chdir(repo)
    assert mig.main([]) == 0
    err = capsys.readouterr().err
    assert err == ""
    assert (naps / f"{stem}.tree").read_bytes() == tree_bytes
    assert (naps / f"{stem}.summ").read_bytes() == caption_bytes
    assert (naps / f"{dest}.tree").read_bytes() == b"already-tree\n"
    assert (naps / f"{dest}.summ").read_bytes() == b"already-summ\n"
    assert rewritten


def test_migrate_unreadable_tree_is_incomplete(tmp_path, monkeypatch, capsys, summem):
    """An old stem whose .tree cannot be parsed prints incomplete pair and exits 1."""
    mig = load_migrate()
    m = summem
    repo = init_repo(tmp_path / "r")
    tree, digests, _ = _grain2(m)
    stem, _tree_bytes, caption_bytes, _seq = _plant_legacy(
        m, repo, tree, "pair", _full_leafset(digests), 2, "five64"
    )
    naps = repo / ".summem" / "naps"
    garbage = b"not-json\n"
    (naps / f"{stem}.tree").write_bytes(garbage)
    before = sorted(p.name for p in naps.iterdir() if p.is_file())
    monkeypatch.chdir(repo)
    assert mig.main([]) != 0
    err = capsys.readouterr().err
    assert "incomplete pair:" in err
    assert stem in err
    assert (naps / f"{stem}.tree").read_bytes() == garbage
    assert (naps / f"{stem}.summ").read_bytes() == caption_bytes
    assert sorted(p.name for p in naps.iterdir() if p.is_file()) == before
