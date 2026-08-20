"""First proof 4: three packs, squash onto main, clone still zooms."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from conftest import load_summem
from gitutil import fold_ids, git, init_repo, zoom_reaches

UTC = timezone.utc


def test_three_packs_squash_clone_zooms_originals(tmp_path, monkeypatch):
    """100 notes folded as 64/32/4, squashed to main; a clone zooms one original per pack."""
    m = load_summem()
    main = init_repo(tmp_path / "main")
    git(["checkout", "-b", "packed"], main)
    base = datetime(2026, 1, 1, tzinfo=UTC)
    texts = [f"n{i:03d}" for i in range(100)]
    for i, text in enumerate(texts):
        m.write_note(main, text, base + timedelta(seconds=i), Random(i))
        git(["add", ".summem"], main)
        git(["commit", "-m", text], main)
    ids = [node.id for node in m.list_view(main) if node.kind == "note"]
    assert len(ids) == 100
    fold_ids(m, main, ids[0:64], "A")
    fold_ids(m, main, ids[64:96], "B")
    fold_ids(m, main, ids[96:100], "C")
    git(["add", "-A"], main)
    git(["commit", "-m", "three naps"], main)
    git(["checkout", "main"], main)
    squashed = git(["merge", "--squash", "packed"], main)
    assert squashed.returncode == 0
    git(["commit", "-m", "squash packs"], main)
    clone = tmp_path / "clone"
    git(["clone", str(main), str(clone)], main)
    monkeypatch.setattr(m, "WAKE_LINES", 3)
    out = m.wake_text(clone)
    lines = [line for line in out.splitlines() if line]
    assert len(lines) == 3
    assert any(line.startswith("x64 ") for line in lines)
    assert any(line.startswith("x32 ") for line in lines)
    assert any(line.startswith("x4 ") for line in lines)
    nap_ids = [node.id for node in m.list_view(clone)]
    zoom_reaches(clone, nap_ids[0], "n000")
    zoom_reaches(clone, nap_ids[1], "n064")
    zoom_reaches(clone, nap_ids[2], "n096")
    log = git(["log", "--pretty=%s"], clone).stdout.decode("utf-8")
    assert "n000" not in log
    assert "n040" not in log
    assert "n070" not in log
    assert "n099" not in log
