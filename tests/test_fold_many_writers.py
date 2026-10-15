"""Many writers: merges must not strand a row, and packs stay powers of two."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

import pytest

from gitutil import _nap_child_ids, obey_folds

UTC = timezone.utc


def _at(t: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=t)


def _files(repo):
    """Return note and nap bytes keyed by ``notes/name`` or ``naps/name``."""
    out = {}
    root = repo / ".summem"
    for sub in ("notes", "naps"):
        folder = root / sub
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if path.is_file() and not path.name.startswith("."):
                out[f"{sub}/{path.name}"] = path.read_bytes()
    return out


def _restore(m, repo, snap):
    """Replace the store's notes and naps with *snap*."""
    m.ensure_store(repo)
    root = repo / ".summem"
    for sub in ("notes", "naps"):
        folder = root / sub
        for path in folder.iterdir():
            if path.is_file():
                path.unlink()
    for rel, data in snap.items():
        (root / rel).write_bytes(data)


def _three_way(base, ours, theirs):
    """Merge immutable files the way git does: union of adds, drop a one-sided delete."""
    out = {}
    for name in set(ours) | set(theirs):
        in_o, in_t, in_b = name in ours, name in theirs, name in base
        if in_o and in_t:
            out[name] = ours[name]
        elif in_o and not in_b:
            out[name] = ours[name]
        elif in_t and not in_b:
            out[name] = theirs[name]
    return out


def _assert_no_stall(view, budget: int) -> None:
    """Over budget, no two power-of-two rows share a grain."""
    if len(view) <= budget:
        return
    grains = [node.leaves for node in view if node.leaves > 0 and node.leaves & (node.leaves - 1) == 0]
    assert len(grains) == len(set(grains)), [node.leaves for node in view]


def _reachable_text(m, repo) -> str:
    """Return every sentence zoom can reach from the view, in one walk."""
    pending = [node.id for node in m.list_view(repo)]
    seen: set[str] = set()
    chunks = []
    while pending:
        cid = pending.pop()
        if cid in seen:
            continue
        seen.add(cid)
        try:
            chunks.append(m.zoom_text(repo, cid))
        except ValueError:
            continue
        pending.extend(_nap_child_ids(m, repo, cid))
    return "\n".join(chunks)


def _assert_one_writer_shape(view) -> None:
    """No grain rises, each grain >= 2 appears at most twice, and only one grain is doubled."""
    grains = [node.leaves for node in view]
    assert all(grains[i] >= grains[i + 1] for i in range(len(grains) - 1)), grains
    counts: dict[int, int] = {}
    for grain in grains:
        if grain >= 2:
            counts[grain] = counts.get(grain, 0) + 1
    assert all(count <= 2 for count in counts.values()), counts
    assert sum(1 for count in counts.values() if count == 2) <= 1, counts


@pytest.mark.parametrize("seed", [7, 11])
def test_many_writers_never_strand_and_keep_powers_of_two(tmp_path, summem, seed):
    """Three writers, budget 6: no stall, no lost note, and the one-writer shape returns."""
    m = summem
    budget = 6
    steps = 200
    rng = Random(seed)
    main = tmp_path / "main"
    writers = [{"dir": tmp_path / f"w{i}", "base": {}} for i in range(3)]
    main_snap: dict = {}
    texts = []
    for t in range(1, steps + 1):
        writer = writers[rng.randrange(3)]
        text = f"note-{t:04d}"
        texts.append(text)
        m.write_note(writer["dir"], text, _at(t), Random(t))
        _assert_no_stall(obey_folds(m, writer["dir"], budget), budget)
        if rng.random() >= 0.08:
            continue
        main_snap = _three_way(writer["base"], main_snap, _files(writer["dir"]))
        _restore(m, main, main_snap)
        _assert_no_stall(obey_folds(m, main, budget), budget)
        main_snap = _files(main)
        _restore(m, writer["dir"], main_snap)
        writer["base"] = dict(main_snap)
    for writer in writers:
        main_snap = _three_way(writer["base"], main_snap, _files(writer["dir"]))
    _restore(m, main, main_snap)
    _assert_no_stall(obey_folds(m, main, budget), budget)
    found = _reachable_text(m, main)
    for text in texts:
        assert text in found, text
    view = None
    for t in range(steps + 1, steps + 65):
        m.write_note(main, f"quiet-{t:04d}", _at(1000 + t), Random(1000 + t))
        view = obey_folds(m, main, budget)
        _assert_no_stall(view, budget)
    _assert_one_writer_shape(view)
