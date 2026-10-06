"""Middle orphans: a node stranded beside a bigger newer node must still fold.

Fold requests pair two view nodes of the same grain that sit next to each other.
A merge, a late note, a zipper reopen, surgery, or an odd-grain pack can leave an
older node next to a bigger, newer one. Nothing new ever lands beside it, so that
node and every node older than it never fold again: dead wake lines.

These tests follow fold requests the way an agent does. They pin the outcome,
not which pair is requested. Every grain in the view stays a power of two:
the fix must never write a pack whose grain is not one.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import datetime, timedelta, timezone
from importlib.machinery import SourceFileLoader
from random import Random

from conftest import ROOT
from gitutil import git, init_repo

UTC = timezone.utc
RUN = re.compile(r' nap(?: --path \S+)? (\S+) (\S+) "')


def _at(t: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=t)


def _note(m, repo, text: str, t: int):
    return m.write_note(repo, text, _at(t), Random(t))


def _assert_powers_of_two(view) -> None:
    odd = [node.leaves for node in view if node.leaves & (node.leaves - 1)]
    assert not odd, f"grain that is not a power of two in view: {odd}; grains {_grains(view)}"


def _obey(m, repo, budget: int, cap: int = 500):
    """Heal, then nap every requested pair until fold asks for nothing. Return the view."""
    for step in range(cap):
        view = m.heal_view(repo)
        _assert_powers_of_two(view)
        out = m.fold_request(repo, budget, nodes=view)
        if not out:
            return view
        id_a, id_b = RUN.search(out).groups()
        ids = [node.id for node in view]
        m.write_nap(repo, m.resolve_id(id_a, ids), m.resolve_id(id_b, ids), f"fold {step}", nodes=view)
    raise AssertionError("fold requests did not finish")


def _live(m, repo, budget: int, first: int, count: int):
    """Record *count* notes from second *first*, obeying fold requests after each."""
    view = None
    for t in range(first, first + count):
        _note(m, repo, f"later {t}", t)
        view = _obey(m, repo, budget)
    return view


def _grains(view) -> list[int]:
    return [node.leaves for node in view]


def _assert_none_survive(m, repo, names: set[str]) -> None:
    view = m.list_view(repo)
    left = sorted(node.name for node in view if node.name in names)
    assert not left, f"stranded view nodes never folded: {left}; grains {_grains(view)}"


def _commit(repo, message: str) -> None:
    git(["add", "-A"], repo)
    git(["commit", "-m", message], repo)


def _operator_merge(m, tmp_path):
    """Main folds to 8, 4, 2, then notes foo; two branches that never saw foo fold later notes."""
    repo = init_repo(tmp_path / "main")
    for t in range(1, 15):
        _note(m, repo, f"main {t}", t)
    _obey(m, repo, 1)
    assert _grains(m.list_view(repo)) == [8, 4, 2]
    _commit(repo, "base")
    git(["branch", "side-b"], repo)
    git(["branch", "side-c"], repo)
    _note(m, repo, "foo", 15)
    _commit(repo, "foo")
    git(["checkout", "side-b"], repo)
    _note(m, repo, "concurrent B 16", 16)
    _note(m, repo, "concurrent B 17", 17)
    assert _grains(_obey(m, repo, 4)) == [8, 4, 2, 2]
    _commit(repo, "b")
    git(["checkout", "side-c"], repo)
    _note(m, repo, "concurrent C 18", 18)
    _note(m, repo, "concurrent C 19", 19)
    assert _grains(_obey(m, repo, 4)) == [8, 4, 2, 2]
    _commit(repo, "c")
    git(["checkout", "main"], repo)
    git(["merge", "--no-edit", "side-b"], repo)
    git(["merge", "--no-edit", "side-c"], repo)
    view = m.list_view(repo)
    assert _grains(view) == [8, 4, 2, 1, 2, 2]
    return repo, {node.name for node in view[:4]}


def test_merged_branch_naps_fold_back_to_budget(tmp_path, summem):
    """Two branches that never saw foo nap later notes; after merge, fold requests reach budget."""
    m = summem
    repo, _stranded = _operator_merge(m, tmp_path)
    view = _obey(m, repo, 4)
    assert len(view) <= 4, f"over budget with no fold requested: grains {_grains(view)}"


def test_merged_branch_naps_do_not_strand_older_nodes(tmp_path, summem):
    """foo and the packs older than it fold once later notes arrive; none stay listed forever."""
    m = summem
    repo, stranded = _operator_merge(m, tmp_path)
    _obey(m, repo, 4)
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def test_late_note_between_packs_is_not_stranded(tmp_path, summem):
    """A note stamped before a pack that main already folded (a late merge) still folds."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for t in range(1, 9):
        _note(m, repo, f"old {t}", t)
    for t in range(20, 24):
        _note(m, repo, f"mid {t}", t)
    _obey(m, repo, 1)
    _note(m, repo, "late", 10)
    view = m.list_view(repo)
    assert _grains(view) == [8, 1, 4]
    stranded = {node.name for node in view[:2]}
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def test_zipper_reopen_orphan_is_not_stranded(tmp_path, summem):
    """Zipper reopens one of two overlapping packs and leaves a lone note before a later pair."""
    m = summem
    repo = init_repo(tmp_path / "main")
    _note(m, repo, "a1", 1)
    _commit(repo, "base")
    git(["branch", "side-y"], repo)

    git(["checkout", "-b", "side-x"], repo)
    for text, t in (("a2", 2), ("a3", 5), ("a4", 6)):
        _note(m, repo, text, t)
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "a1 a2")
    m.write_nap(repo, ids[2], ids[3], "a3 a4")
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "x four")
    _commit(repo, "x")

    git(["checkout", "side-y"], repo)
    for text, t in (("f", 3), ("g", 4), ("h", 7)):
        _note(m, repo, text, t)
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "a1 f")
    m.write_nap(repo, ids[2], ids[3], "g h")
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "y four")
    _commit(repo, "y")

    git(["checkout", "main"], repo)
    git(["merge", "--no-edit", "side-x"], repo)
    git(["merge", "--no-edit", "side-y"], repo)
    view = m.heal_view(repo)
    assert _grains(view) == [4, 1, 2]
    stranded = {node.name for node in view[:2]}
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def _load_surgery():
    loader = SourceFileLoader("surgery", str(ROOT / "surgery.py"))
    spec = importlib.util.spec_from_loader("surgery", loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["surgery"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_surgery_orphan_is_not_stranded(tmp_path, summem):
    """Excising one note from a balanced 8-pack leaves 2, 1, 4; the lone sibling still folds."""
    m = summem
    surgery = _load_surgery()
    repo = init_repo(tmp_path / "r")
    paths = [_note(m, repo, f"n{t}", t) for t in range(1, 9)]
    _obey(m, repo, 1)
    surgery.excise_note(m, repo, paths[2].name)
    view = m.list_view(repo)
    assert _grains(view) == [2, 1, 4]
    stranded = {node.name for node in view[:2]}
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def _plant_pack(m, repo, left, right, caption: str) -> None:
    """Write a nap of two view nodes with no pairing policy: the shape a legacy store can hold."""
    child_l, digs_l = m._as_child(left)
    child_r, digs_r = m._as_child(right)
    tree_bytes = m.dumps_tree(m.Tree(kids=[child_l, child_r]))
    caption_bytes = m.note_file_bytes(caption)
    digests = digs_l + digs_r
    stem = m.nap_stem(m._seq_prefix(left.name), m.leafset_id(digests), len(digests), tree_bytes, caption_bytes)
    m._write_pair(m.ensure_store(repo) / "naps", stem, tree_bytes, caption_bytes)
    m._unlink_node(left)
    m._unlink_node(right)


def test_odd_grain_pack_is_not_stranded(tmp_path, summem):
    """A legacy 6-pack (4 + 2, napped off-request) never meets another 6; heal must not leave it listed."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for t in range(1, 7):
        _note(m, repo, f"n{t}", t)
    _obey(m, repo, 1)
    view = m.list_view(repo)
    assert _grains(view) == [4, 2]
    _plant_pack(m, repo, view[0], view[1], "four plus two")
    view = m.list_view(repo)
    assert _grains(view) == [6]
    stranded = {view[0].name}
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def test_oldest_same_grain_pair_folds_before_newer_notes(tmp_path, summem):
    """Grains 4, 4, 1, 1 over budget: fold names the two 4s, so the newest notes stay verbatim."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for t in range(1, 9):
        _note(m, repo, f"n{t}", t)
    _obey(m, repo, 2)
    _note(m, repo, "n9", 9)
    _note(m, repo, "n10", 10)
    view = m.list_view(repo)
    assert _grains(view) == [4, 4, 1, 1]
    out = m.fold_request(repo, 3, nodes=view)
    assert out
    id_a, id_b = RUN.search(out).groups()
    ids = [node.id for node in view]
    assert {m.resolve_id(id_a, ids), m.resolve_id(id_b, ids)} == {view[0].id, view[1].id}
