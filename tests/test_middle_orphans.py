"""Middle orphans: a node stranded beside a bigger newer node must still fold.

Fold requests name the oldest row that has a same-grain row below it, paired
with the nearest such row. A merge, a late note, a zipper reopen, or surgery
can leave an older node next to a bigger, newer one. That row must still fold.

These tests follow fold requests the way an agent does. They pin the outcome,
not which pair is requested. A fold never writes a pack whose grain is not a
power of two. A legacy pack like that stays listed; nothing opens it on disk.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import datetime, timedelta, timezone
from importlib.machinery import SourceFileLoader
from random import Random

from conftest import ROOT
from gitutil import fold_ids, git, init_repo, obey_folds, plant_pack

UTC = timezone.utc
RUN = re.compile(r' nap(?: --path \S+)? (\S+) (\S+) "')


def _at(t: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=t)


def _note(m, repo, text: str, t: int):
    return m.write_note(repo, text, _at(t), Random(t))


def _live(m, repo, budget: int, first: int, count: int):
    """Record *count* notes from second *first*, obeying fold requests after each."""
    view = None
    for t in range(first, first + count):
        _note(m, repo, f"later {t}", t)
        view = obey_folds(m, repo, budget)
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
    obey_folds(m, repo, 1)
    assert _grains(m.list_view(repo)) == [8, 4, 2]
    _commit(repo, "base")
    git(["branch", "side-b"], repo)
    git(["branch", "side-c"], repo)
    _note(m, repo, "foo", 15)
    _commit(repo, "foo")
    git(["checkout", "side-b"], repo)
    _note(m, repo, "concurrent B 16", 16)
    _note(m, repo, "concurrent B 17", 17)
    assert _grains(obey_folds(m, repo, 4)) == [8, 4, 2, 2]
    _commit(repo, "b")
    git(["checkout", "side-c"], repo)
    _note(m, repo, "concurrent C 18", 18)
    _note(m, repo, "concurrent C 19", 19)
    assert _grains(obey_folds(m, repo, 4)) == [8, 4, 2, 2]
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
    view = obey_folds(m, repo, 4)
    assert len(view) <= 4, f"over budget with no fold requested: grains {_grains(view)}"


def test_merged_branch_naps_do_not_strand_older_nodes(tmp_path, summem):
    """foo and the packs older than it fold once later notes arrive; none stay listed forever."""
    m = summem
    repo, stranded = _operator_merge(m, tmp_path)
    obey_folds(m, repo, 4)
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
    obey_folds(m, repo, 1)
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
    obey_folds(m, repo, 1)
    surgery.excise_note(m, repo, paths[2].name)
    view = m.list_view(repo)
    assert _grains(view) == [2, 1, 4]
    stranded = {node.name for node in view[:2]}
    _live(m, repo, 4, 100, 32)
    _assert_none_survive(m, repo, stranded)


def _plant_six(m, repo, start: int) -> str:
    """Plant one legacy 6-pack from six notes beginning at second *start*. Return its id."""
    for t in range(start, start + 4):
        _note(m, repo, f"n{t}", t)
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    fold_ids(m, repo, [node.id for node in notes], "four")
    for t in range(start + 4, start + 6):
        _note(m, repo, f"n{t}", t)
    notes = [node for node in m.list_view(repo) if node.kind == "note"]
    fold_ids(m, repo, [node.id for node in notes], "two")
    view = m.list_view(repo)
    four = next(node for node in view if node.leaves == 4)
    two = next(node for node in view if node.leaves == 2)
    already = {node.id for node in view if node.leaves == 6}
    plant_pack(m, repo, four, two, "six")
    return next(node.id for node in m.list_view(repo) if node.leaves == 6 and node.id not in already)


def _live_guard(m, repo, budget: int, first: int, count: int, forbidden: set[str]):
    """Record notes and obey folds. No request may name an id in *forbidden*."""
    view = None
    for t in range(first, first + count):
        _note(m, repo, f"later {t}", t)
        for step in range(500):
            view = m.heal_view(repo)
            out = m.fold_request(repo, budget, nodes=view)
            if not out:
                break
            id_a, id_b = RUN.search(out).groups()
            ids = [node.id for node in view]
            named = {m.resolve_id(id_a, ids), m.resolve_id(id_b, ids)}
            assert forbidden.isdisjoint(named), out
            written = m.write_nap(
                repo, m.resolve_id(id_a, ids), m.resolve_id(id_b, ids), f"fold {step}", nodes=view
            )
            grain = m._parse_nap_stem(written.stem)[3]
            assert grain & (grain - 1) == 0, grain
        else:
            raise AssertionError("fold requests did not finish")
    return view


def test_legacy_odd_pack_stays_listed_and_is_never_requested(tmp_path, summem):
    """A lone legacy 6-pack stays listed, is never requested, and 32 notes fit the budget."""
    m = summem
    repo = init_repo(tmp_path / "r")
    six = _plant_six(m, repo, 1)
    view = _live_guard(m, repo, 4, 100, 32, {six})
    assert six in {node.id for node in view}
    assert len(view) <= 4, _grains(view)
    assert _grains(view) == [6, 16, 8, 8]


def test_two_equal_legacy_odd_packs_are_never_paired(tmp_path, summem):
    """Two legacy 6-packs are never paired; both stay listed; 32 notes fit the budget."""
    m = summem
    repo = init_repo(tmp_path / "r")
    first = _plant_six(m, repo, 1)
    second = _plant_six(m, repo, 10)
    assert first != second
    view = _live_guard(m, repo, 4, 100, 32, {first, second})
    assert {first, second} <= {node.id for node in view}
    assert len(view) <= 4, _grains(view)
    assert _grains(view) == [6, 6, 16, 16]


def test_oldest_same_grain_pair_folds_before_newer_notes(tmp_path, summem):
    """Grains 4, 4, 1, 1 over budget: fold names the two 4s, so the newest notes stay verbatim."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for t in range(1, 9):
        _note(m, repo, f"n{t}", t)
    obey_folds(m, repo, 2)
    _note(m, repo, "n9", 9)
    _note(m, repo, "n10", 10)
    view = m.list_view(repo)
    assert _grains(view) == [4, 4, 1, 1]
    out = m.fold_request(repo, 3, nodes=view)
    assert out
    id_a, id_b = RUN.search(out).groups()
    ids = [node.id for node in view]
    assert {m.resolve_id(id_a, ids), m.resolve_id(id_b, ids)} == {view[0].id, view[1].id}
