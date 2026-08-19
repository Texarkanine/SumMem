"""First proof 4: three packs, squash onto main, clone still zooms."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta, timezone
from random import Random

from conftest import SCRIPT, load_summem
from gitutil import fold_ids, git, init_repo, zoom_reaches

UTC = timezone.utc


def test_three_packs_squash_clone_zooms_originals(tmp_path):
    """100 notes folded as 40/30/30, squashed to main; a clone zooms one original per pack."""
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
    fold_ids(m, main, ids[0:40], "A")
    fold_ids(m, main, ids[40:70], "B")
    fold_ids(m, main, ids[70:100], "C")
    git(["add", "-A"], main)
    git(["commit", "-m", "three naps"], main)
    git(["checkout", "main"], main)
    squashed = git(["merge", "--squash", "packed"], main)
    assert squashed.returncode == 0
    git(["commit", "-m", "squash packs"], main)
    clone = tmp_path / "clone"
    git(["clone", str(main), str(clone)], main)
    wake = subprocess.run(
        [sys.executable, str(SCRIPT), "wake"],
        cwd=clone,
        capture_output=True,
        check=True,
    )
    out = wake.stdout.decode("utf-8")
    lines = [line for line in out.splitlines() if line]
    assert len(lines) == 3
    grains = [line.split("  ", 1)[1] for line in lines]
    assert any(g.startswith("(40 notes,") for g in grains)
    assert sum(1 for g in grains if g.startswith("(30 notes,")) == 2
    nap_ids = [line.split()[0] for line in lines]
    zoom_reaches(clone, nap_ids[0], "n000")
    zoom_reaches(clone, nap_ids[1], "n040")
    zoom_reaches(clone, nap_ids[2], "n070")
    log = git(["log", "--pretty=%s"], clone).stdout.decode("utf-8")
    assert "n000" not in log
    assert "n040" not in log
    assert "n070" not in log
    assert "n099" not in log
