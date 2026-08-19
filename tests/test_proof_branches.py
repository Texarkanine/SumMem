"""First proof 6: disjoint branch packs merge, then nap the two neighbors."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from conftest import load_summem
from gitutil import fold_ids, git, init_repo, zoom_reaches

UTC = timezone.utc


def test_two_branch_packs_merge_then_nap_neighbors(tmp_path):
    """Two disjoint packs merge clean; wake is two lines; nap of those ids zooms both sides."""
    m = load_summem()
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
    lines = [line for line in m.wake_text(main).splitlines() if line]
    assert len(lines) == 2
    ids = [line.split()[0] for line in lines]
    parent = m.write_nap(main, ids[0], ids[1], "both packs")
    wake = m.wake_text(main)
    assert len(wake.splitlines()) == 1
    assert "(8 notes," in wake
    nap_id = wake.splitlines()[0].split()[0]
    zoom_reaches(main, nap_id, "A0")
    zoom_reaches(main, nap_id, "B0")
    assert parent.is_file()
