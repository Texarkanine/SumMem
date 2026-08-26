"""Disjoint branch packs merge, then nap the two neighbors."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from gitutil import assert_unique_cover, fold_ids, git, init_repo, reaches, zoom_reaches

UTC = timezone.utc


def test_two_branch_packs_merge_then_nap_neighbors(tmp_path, monkeypatch, summem):
    """Two disjoint packs merge clean; wake is two lines; nap of those ids zooms both sides."""
    m = summem
    main = init_repo(tmp_path / "main")
    base = datetime(2026, 1, 1, tzinfo=UTC)

    git(["checkout", "-b", "side-a"], main)
    texts_a = [f"A{i}" for i in range(4)]
    for i, text in enumerate(texts_a):
        m.write_note(main, text, base + timedelta(seconds=i), Random(i))
    ids_a = [node.id for node in m.list_view(main) if node.kind == "note"]
    fold_ids(m, main, ids_a, "pack-a")
    git(["add", "-A"], main)
    git(["commit", "-m", "pack a"], main)

    git(["checkout", "main"], main)
    git(["checkout", "-b", "side-b"], main)
    texts_b = [f"B{i}" for i in range(4)]
    for i, text in enumerate(texts_b):
        m.write_note(main, text, base + timedelta(seconds=10 + i), Random(100 + i))
    ids_b = [node.id for node in m.list_view(main) if node.kind == "note"]
    fold_ids(m, main, ids_b, "pack-b")
    git(["add", "-A"], main)
    git(["commit", "-m", "pack b"], main)

    git(["checkout", "main"], main)
    merged_a = git(["merge", "--no-edit", "side-a"], main)
    merged_b = git(["merge", "--no-edit", "side-b"], main)
    assert merged_a.returncode == 0
    assert merged_b.returncode == 0
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    lines = [line for line in m.wake_text(main).splitlines() if line]
    assert len(lines) == 2
    ids = [node.id for node in m.list_view(main)]
    parent = m.write_nap(main, ids[0], ids[1], "both packs")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    wake = m.wake_text(main)
    assert len(wake.splitlines()) == 1
    assert "x8 " in wake
    assert "both packs" in wake
    nap_id = m.list_view(main)[0].id
    zoom_reaches(main, nap_id, "A0")
    zoom_reaches(main, nap_id, "B0")
    assert parent.is_file()


def test_two_branch_overlapping_packs_heal_on_next_mutate(tmp_path, monkeypatch, summem):
    """Two branches nap overlapping-but-unequal packs; merge then CLI note leaves a unique cover."""
    m = summem
    repo = init_repo(tmp_path / "main")
    base = datetime(2026, 1, 1, tzinfo=UTC)
    m.write_note(repo, "A", base, Random(1))
    m.write_note(repo, "B", base + timedelta(seconds=1), Random(2))
    git(["add", "-A"], repo)
    git(["commit", "-m", "base notes"], repo)

    git(["checkout", "-b", "side-d"], repo)
    m.write_note(repo, "D", base + timedelta(seconds=2), Random(3))
    notes = [n for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "ab")
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "abd")
    git(["add", "-A"], repo)
    git(["commit", "-m", "pack abd"], repo)

    git(["checkout", "main"], repo)
    git(["checkout", "-b", "side-e"], repo)
    m.write_note(repo, "E", base + timedelta(seconds=3), Random(4))
    notes = [n for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, notes[0].id, notes[1].id, "ab")
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "abe")
    git(["add", "-A"], repo)
    git(["commit", "-m", "pack abe"], repo)

    git(["checkout", "main"], repo)
    merged_d = git(["merge", "--no-edit", "side-d"], repo)
    merged_e = git(["merge", "--no-edit", "side-e"], repo)
    assert merged_d.returncode == 0
    assert merged_e.returncode == 0
    monkeypatch.chdir(repo)
    assert m.main(["note", "later"]) == 0
    assert_unique_cover(m, repo)
    for sentence in ("A", "B", "D", "E"):
        assert reaches(m, repo, sentence), sentence
