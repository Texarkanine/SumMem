"""Concurrent same-block folds union as distinct five-part stems, then zipper."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta, timezone
from random import Random

from conftest import SCRIPT, load_summem
from gitutil import git, init_repo, reaches, zoom_reaches

UTC = timezone.utc


def _run(args, cwd, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            result.stderr.decode("utf-8", "replace") or result.stdout.decode("utf-8", "replace")
        )
    return result


def _commit(repo, message: str) -> None:
    git(["add", "-A"], repo)
    git(["commit", "-m", message], repo)


def _unmerged(repo) -> list[str]:
    out = git(["diff", "--name-only", "--diff-filter=U"], repo).stdout.decode("utf-8")
    return [line for line in out.splitlines() if line]


def _nap_nodes(m, repo):
    return [node for node in m.list_view(repo) if node.kind == "nap"]


def _scan_markers(repo) -> None:
    store = repo / ".summem"
    if not store.is_dir():
        return
    for path in store.rglob("*"):
        if not path.is_file() or path.name.startswith("."):
            continue
        raw = path.read_bytes()
        assert b"<<<<<<<" not in raw
        assert b">>>>>>>" not in raw


def _assert_pairs_match_stems(m, repo) -> None:
    naps = repo / ".summem" / "naps"
    if not naps.is_dir():
        return
    for tree in naps.glob("*.tree"):
        summ = tree.with_suffix(".summ")
        if not summ.is_file():
            continue
        parsed = m._parse_nap_stem(tree.stem)
        assert parsed is not None
        tag = parsed[4]
        if not tag:
            continue
        assert tag == m.variant_tag(tree.read_bytes(), summ.read_bytes())


def _two_notes_on_main(m, main):
    m.write_note(main, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(main, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    _commit(main, "two notes")
    return [node.id for node in m.list_view(main)]


def _worktrees(main, tmp_path, names):
    trees = []
    for name in names:
        dest = tmp_path / name
        git(["worktree", "add", "-b", name, str(dest)], main)
        trees.append(dest)
    return trees


def test_identical_pair_bytes_share_a_stem(tmp_path):
    """Same tree and caption produce one stem; git merge keeps a single pair."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "pair")
    m.write_nap(wt_b, ids[0], ids[1], "pair")
    _commit(wt_a, "pair a")
    _commit(wt_b, "pair b")
    stems_a = {p.stem for p in (wt_a / ".summem" / "naps").glob("*.tree")}
    stems_b = {p.stem for p in (wt_b / ".summem" / "naps").glob("*.tree")}
    assert stems_a == stems_b
    assert len(stems_a) == 1
    merged = git(["merge", "--no-edit", "nap-b"], wt_a, check=False)
    assert merged.returncode == 0
    assert _unmerged(wt_a) == []
    assert len(_nap_nodes(m, wt_a)) == 1
    _scan_markers(wt_a)
    _assert_pairs_match_stems(m, wt_a)


def test_note_heals_equal_variants(tmp_path):
    """CLI note after a twin merge zipper-collapses to one complete pair."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "ours caption")
    m.write_nap(wt_b, ids[0], ids[1], "theirs caption")
    _commit(wt_a, "ours")
    _commit(wt_b, "theirs")
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    assert len(_nap_nodes(m, wt_a)) == 2
    noted = _run([sys.executable, str(SCRIPT), "note", "gamma"], wt_a)
    assert noted.returncode == 0
    naps = _nap_nodes(m, wt_a)
    assert len(naps) == 1
    assert naps[0].tree_path.is_file() and naps[0].sum_path.is_file()
    assert reaches(m, wt_a, "alpha") and reaches(m, wt_a, "beta")
    assert reaches(m, wt_a, "gamma")


def test_nap_heals_equal_variants(tmp_path):
    """CLI nap after a twin merge heals first, then folds the remaining notes."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(("alpha", "beta", "gamma", "delta"), start=1):
        m.write_note(main, text, base + timedelta(seconds=i), Random(i))
    _commit(main, "four notes")
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "ours caption")
    m.write_nap(wt_b, ids[0], ids[1], "theirs caption")
    _commit(wt_a, "ours")
    _commit(wt_b, "theirs")
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    assert len(_nap_nodes(m, wt_a)) == 2
    napped = _run([sys.executable, str(SCRIPT), "nap", ids[2], ids[3], "later"], wt_a)
    assert napped.returncode == 0
    naps = _nap_nodes(m, wt_a)
    assert len(naps) == 2
    grains = sorted(node.leaves for node in naps)
    assert grains == [2, 2]
    for text in ("alpha", "beta", "gamma", "delta"):
        assert reaches(m, wt_a, text)


def test_reversed_merge_order_same_survivor(tmp_path):
    """Healing after A←B versus B←A keeps the same lex-greatest stem."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "ours caption")
    m.write_nap(wt_b, ids[0], ids[1], "theirs caption")
    _commit(wt_a, "ours")
    _commit(wt_b, "theirs")
    stem_a = next((wt_a / ".summem" / "naps").glob("*.tree")).stem
    stem_b = next((wt_b / ".summem" / "naps").glob("*.tree")).stem
    git(["branch", "merge-ab", "nap-a"], main)
    git(["branch", "merge-ba", "nap-b"], main)
    ab = tmp_path / "ab"
    ba = tmp_path / "ba"
    git(["worktree", "add", str(ab), "merge-ab"], main)
    git(["worktree", "add", str(ba), "merge-ba"], main)
    assert git(["merge", "--no-edit", "nap-b"], ab, check=False).returncode == 0
    assert git(["merge", "--no-edit", "nap-a"], ba, check=False).returncode == 0
    m.heal_view(ab)
    m.heal_view(ba)
    survivor_ab = _nap_nodes(m, ab)[0].name
    survivor_ba = _nap_nodes(m, ba)[0].name
    assert survivor_ab == survivor_ba == max(stem_a, stem_b)


def test_three_variants_merge_then_heal(tmp_path):
    """Three same-block captions merge without conflict and heal to one pair."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b, wt_c = _worktrees(main, tmp_path, ("nap-a", "nap-b", "nap-c"))
    for tree, caption in ((wt_a, "one"), (wt_b, "two"), (wt_c, "three")):
        m.write_nap(tree, ids[0], ids[1], caption)
        _commit(tree, caption)
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    assert git(["merge", "--no-edit", "nap-c"], wt_a, check=False).returncode == 0
    assert _unmerged(wt_a) == []
    assert len(_nap_nodes(m, wt_a)) == 3
    m.heal_view(wt_a)
    left = _nap_nodes(m, wt_a)
    assert len(left) == 1
    assert reaches(m, wt_a, "alpha") and reaches(m, wt_a, "beta")


def test_triple_worker_one_two_four(tmp_path):
    """Three workers fold 1→2→4 with different captions; merge unions; next note heals to one pack."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    base = datetime(2026, 1, 1, tzinfo=UTC)
    texts = ("A", "B", "C", "D")
    for i, text in enumerate(texts, start=1):
        m.write_note(main, text, base + timedelta(seconds=i), Random(i))
    _commit(main, "four notes")
    ids = [node.id for node in m.list_view(main)]
    workers = _worktrees(main, tmp_path, ("w1", "w2", "w3"))
    captions = (
        ("ab1", "cd1", "p1"),
        ("ab2", "cd2", "p2"),
        ("ab3", "cd3", "p3"),
    )
    for tree, (ab, cd, parent) in zip(workers, captions):
        m.write_nap(tree, ids[0], ids[1], ab)
        m.write_nap(tree, ids[2], ids[3], cd)
        nap_ids = [node.id for node in _nap_nodes(m, tree)]
        m.write_nap(tree, nap_ids[0], nap_ids[1], parent)
        _commit(tree, parent)
    assert git(["merge", "--no-edit", "w2"], workers[0], check=False).returncode == 0
    assert git(["merge", "--no-edit", "w3"], workers[0], check=False).returncode == 0
    assert _unmerged(workers[0]) == []
    assert len(_nap_nodes(m, workers[0])) == 3
    _scan_markers(workers[0])
    noted = _run([sys.executable, str(SCRIPT), "note", "extra"], workers[0])
    assert noted.returncode == 0
    naps = _nap_nodes(m, workers[0])
    assert len(naps) == 1
    assert naps[0].leaves == 4
    for text in texts:
        assert reaches(m, workers[0], text)


def test_sequence_prefix_order(tmp_path):
    """Distinct timestamps keep sequence-prefix order; variants of one block differ only at the tag."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(("a1", "a2", "b1", "b2"), start=1):
        m.write_note(main, text, base + timedelta(seconds=i), Random(i))
    _commit(main, "four notes")
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "a-one")
    m.write_nap(wt_a, ids[2], ids[3], "b-pair")
    m.write_nap(wt_b, ids[0], ids[1], "a-two")
    m.write_nap(wt_b, ids[2], ids[3], "b-pair")
    _commit(wt_a, "a")
    _commit(wt_b, "b")
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    naps = _nap_nodes(m, wt_a)
    assert len(naps) == 3
    parsed = [m._parse_nap_stem(node.name) for node in naps]
    assert all(row is not None for row in parsed)
    a_rows = [row for row in parsed if row[4] and row[0] == "20260101T000001Z"]
    b_rows = [row for row in parsed if row[0] == "20260101T000003Z"]
    assert len(a_rows) == 2
    assert len(b_rows) == 1
    assert naps[0].name < naps[1].name < naps[2].name
    stamp_a, rand_a, leaf_a, grain_a, tag_a = a_rows[0]
    stamp_b, rand_b, leaf_b, grain_b, tag_b = a_rows[1]
    assert (stamp_a, rand_a, leaf_a, grain_a) == (stamp_b, rand_b, leaf_b, grain_b)
    assert tag_a != tag_b
    assert f"{stamp_a}-{rand_a}" < f"{b_rows[0][0]}-{b_rows[0][1]}"


def test_squash_clone_zooms_after_heal(tmp_path):
    """Merge, heal, commit, squash; a fresh clone zooms every original note."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "ours caption")
    m.write_nap(wt_b, ids[0], ids[1], "theirs caption")
    _commit(wt_a, "ours")
    _commit(wt_b, "theirs")
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    m.heal_view(wt_a)
    _commit(wt_a, "healed")
    squashed = git(["merge", "--squash", "nap-a"], main, check=False)
    assert squashed.returncode == 0
    git(["commit", "-m", "squash"], main)
    clone = tmp_path / "clone"
    git(["clone", str(main), str(clone)], main)
    naps = _nap_nodes(m, clone)
    assert len(naps) == 1
    zoom_reaches(clone, naps[0].id, "alpha")
    zoom_reaches(clone, naps[0].id, "beta")


def test_no_conflict_markers_or_mismatched_pair(tmp_path):
    """After the merge scenario, no conflict markers and no cross-variant .tree/.summ pair."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    _two_notes_on_main(m, main)
    ids = [node.id for node in m.list_view(main)]
    wt_a, wt_b = _worktrees(main, tmp_path, ("nap-a", "nap-b"))
    m.write_nap(wt_a, ids[0], ids[1], "ours caption")
    m.write_nap(wt_b, ids[0], ids[1], "theirs caption")
    _commit(wt_a, "ours")
    _commit(wt_b, "theirs")
    assert git(["merge", "--no-edit", "nap-b"], wt_a, check=False).returncode == 0
    _scan_markers(wt_a)
    _assert_pairs_match_stems(m, wt_a)
    assert _unmerged(wt_a) == []


def test_legacy_four_part_wake_zoom_recall(tmp_path, monkeypatch):
    """A planted four-part pair still wakes, zooms, and recalls."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "pair")
    node = m.list_view(repo)[0]
    parsed = m._parse_nap_stem(node.name)
    assert parsed is not None
    stamp, rand, leafset, grain, tag = parsed
    assert tag
    four = f"{stamp}-{rand}-{leafset}-{grain}"
    naps = repo / ".summem" / "naps"
    (naps / f"{four}.tree").write_bytes(node.tree_path.read_bytes())
    (naps / f"{four}.summ").write_bytes(node.sum_path.read_bytes())
    node.tree_path.unlink()
    node.sum_path.unlink()
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    wake = m.wake_text(repo)
    prefix = m.short_id(leafset, [leafset])
    assert wake == f"x2 {prefix}: pair\n"
    zoom = m.zoom_text(repo, leafset)
    assert "alpha" in zoom and "beta" in zoom
    recall = m.recall_text(repo, "pair")
    assert "pair" in recall


def test_rematerialize_legacy_parent_writes_five_part_children(tmp_path):
    """NapChild kids rematerialized out of a four-part parent land on five-part stems."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(("A", "B", "C", "D"), start=1):
        m.write_note(repo, text, base + timedelta(seconds=i), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    m.write_nap(repo, ids[2], ids[3], "cd")
    nap_ids = [node.id for node in _nap_nodes(m, repo)]
    m.write_nap(repo, nap_ids[0], nap_ids[1], "abcd")
    parent = _nap_nodes(m, repo)[0]
    parsed = m._parse_nap_stem(parent.name)
    assert parsed is not None
    stamp, rand, leafset, grain, _tag = parsed
    four = f"{stamp}-{rand}-{leafset}-{grain}"
    naps = repo / ".summem" / "naps"
    tree_bytes = parent.tree_path.read_bytes()
    caption_bytes = parent.sum_path.read_bytes()
    parent.tree_path.unlink()
    parent.sum_path.unlink()
    (naps / f"{four}.tree").write_bytes(tree_bytes)
    (naps / f"{four}.summ").write_bytes(caption_bytes)
    inner = m.loads_tree(tree_bytes)
    for kid in inner.kids:
        assert isinstance(kid, m.NapChild)
        m.rematerialize_child(repo, kid)
        kid_bytes = m.dumps_tree(kid.tree)
        kid_caption = m.note_file_bytes(kid.sum)
        leftmost = next(m._note_children(kid.tree))
        leaves = len(m._digests_of_tree(kid.tree))
        stem = m.nap_stem(
            m._seq_prefix(leftmost.name), kid.id, leaves, kid_bytes, kid_caption
        )
        assert (naps / f"{stem}.tree").is_file()
        assert m._parse_nap_stem(stem)[4]
        assert four not in stem
