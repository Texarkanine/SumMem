"""CLI note/nap/wake healing, .tree single-parse boundary, and frontier projection."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from gitutil import (
    assert_unique_cover,
    init_repo,
    payload_names,
    plant_nap,
    plant_pack,
    write_notes,
    zoom_reaches,
)


def _fold_balanced(m, repo, texts, caption, start):
    paths = write_notes(m, repo, texts, start=start)
    remaining = [n.id for n in m.list_view(repo) if n.name in {p.name for p in paths}]
    step = 0
    while len(remaining) > 1:
        nxt = []
        for i in range(0, len(remaining) - 1, 2):
            before = {n.id for n in m.list_view(repo)}
            m.write_nap(repo, remaining[i], remaining[i + 1], f"{caption}-{step}")
            created = [cid for cid in [n.id for n in m.list_view(repo)] if cid not in before]
            nxt.extend(created)
            step += 1
        if len(remaining) % 2:
            nxt.append(remaining[-1])
        remaining = nxt
    return remaining[0]


def _over_budget_naps(m, repo):
    """Grain-4 nap, grain-2 nap, broken grain-2 nap; WAKE_LINES = 2."""
    _fold_balanced(m, repo, ["A", "B", "C", "D"], "abcd", start=1)
    _fold_balanced(m, repo, ["E", "F"], "ef", start=10)
    _fold_balanced(m, repo, ["G", "H"], "gh", start=20)
    next(n for n in m.list_view(repo) if n.caption == "gh-0").tree_path.write_bytes(b"{not json")
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 2\n", encoding="utf-8")


def _count_tree_reads(monkeypatch) -> Counter:
    counts: Counter = Counter()
    real = Path.read_bytes

    def spy(self):
        if self.suffix == ".tree":
            counts[self] += 1
        return real(self)

    monkeypatch.setattr(Path, "read_bytes", spy)
    return counts


def _plant_abd_abe(m, repo):
    write_notes(m, repo, ["A", "B", "D"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    ab = next(n for n in m.list_view(repo) if n.kind == "nap")
    d = next(n for n in m.list_view(repo) if n.kind == "note")
    plant_pack(m, repo, ab, d, "abd")
    abd = m.list_view(repo)[0]
    abd_tree = m.loads_tree(abd.tree_path.read_bytes())
    e_note = m.NoteChild(name="20260101T000010Z-eeeeeeeeeeeeeeee", text="E")
    plant_nap(m, repo, [abd_tree.kids[0], e_note], "abe")
    return abd


def test_cli_note_reads_each_children_file_once(tmp_path, monkeypatch, capsys, summem):
    """One note reads each .tree at most once, through heal, its relist, and the fold scan.

    Contract: the driver runs inside agent turns, so a command never parses the
    same children file twice. The store has a grain-4 nap, a grain-2 nap, a
    broken grain-2 nap, and a loose note heal must drop, and it is over budget.
    """
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _over_budget_naps(m, repo)
    dup = write_notes(m, repo, ["A"], start=30)[0]
    write_notes(m, repo, ["x", "y"], start=40)
    counts = _count_tree_reads(monkeypatch)
    assert m.main(["note", "--path", ":/", "z"]) == 0
    assert "Run:" in capsys.readouterr().out
    assert not dup.exists()
    assert max(counts.values(), default=0) <= 1, counts


def test_cli_nap_reads_each_children_file_once(tmp_path, monkeypatch, capsys, summem):
    """One nap reads each .tree at most once, through heal, the nearer-row check, and the next fold request.

    Contract as for note. The new pack's children file counts too.
    """
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _over_budget_naps(m, repo)
    write_notes(m, repo, ["x", "y", "z"], start=40)
    id_a, id_b = re.search(r' nap --path :/ (\S+) (\S+) "', m.fold_request(repo, 2)).groups()
    counts = _count_tree_reads(monkeypatch)
    assert m.main(["nap", "--path", ":/", id_a, id_b, "xy"]) == 0
    assert "Run:" in capsys.readouterr().out
    assert max(counts.values(), default=0) <= 1, counts


def test_heal_to_8_2_1_empty_fold_request_wake_projects(tmp_path, monkeypatch, summem):
    """Heal to grains 8,2,1: fold_request is empty at budget 2; wake lists all three and expands when short."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _fold_balanced(m, repo, [f"a{i}" for i in range(8)], "eight", start=1)
    write_notes(m, repo, ["b0", "b1"], start=100)
    ids = [n.id for n in m.list_view(repo) if n.kind == "note"]
    m.write_nap(repo, ids[0], ids[1], "two")
    write_notes(m, repo, ["c0"], start=200)
    m.heal_view(repo)
    grains = sorted(n.leaves for n in m.list_view(repo))
    assert grains == [1, 2, 8]
    assert m.fold_request(repo, 2) == ""
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 3
    monkeypatch.setattr(m, "WAKE_LINES", 4)
    lines = [line for line in m.wake_text(repo).splitlines() if line]
    assert len(lines) == 4


def test_cli_note_and_nap_call_heal(tmp_path, monkeypatch, capsys, summem):
    """main(['note', ...]) and main(['nap', ...]) call heal; wake does not."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    calls = {"n": 0}
    real = m.heal_view

    def wrapped(parent):
        calls["n"] += 1
        return real(parent)

    monkeypatch.setattr(m, "heal_view", wrapped)
    assert m.main(["note", "--path", ":/", "hello"]) == 0
    assert m.main(["note", "--path", ":/", "world"]) == 0
    assert calls["n"] == 2
    ids = [n.id for n in m.list_view(repo)]
    assert m.main(["nap", "--path", ":/", ids[0], ids[1], "pair"]) == 0
    assert calls["n"] == 3
    calls["n"] = 0
    capsys.readouterr()
    assert m.main(["wake"]) == 0
    assert calls["n"] == 0


def test_cli_wake_on_overlapping_head_writes_nothing(tmp_path, monkeypatch, summem):
    """CLI wake on overlapping HEAD prints and adds no file; wake must not lock."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    before = payload_names(repo)
    locks = {"n": 0}
    real = m.with_store_lock

    def wrapped(parent, fn):
        locks["n"] += 1
        return real(parent, fn)

    monkeypatch.setattr(m, "with_store_lock", wrapped)
    assert m.main(["wake"]) == 0
    assert locks["n"] == 0
    assert payload_names(repo) == before


def test_cli_nap_overlapping_ids_exits_1_without_concat(tmp_path, monkeypatch, summem):
    """nap of two overlapping ids exits 1, does not concat, writes no new .summ sentence."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    ids = [n.id for n in m.list_view(repo)]
    assert m.main(["nap", "--path", ":/", ids[0], ids[1], "concat-caption"]) == 1
    sum_texts = []
    for path in (repo / ".summem" / "naps").glob("*.summ"):
        text = path.read_text(encoding="utf-8")
        if text.endswith("\n"):
            text = text[:-1]
        sum_texts.append(text)
    assert "concat-caption" not in sum_texts
    assert_unique_cover(m, repo)


def test_cli_note_text_inside_nap_exits_0_no_loose_note(tmp_path, monkeypatch, capsys, summem):
    """note of text already in a nap exits 0; that note does not remain in the view."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    write_notes(m, repo, ["A", "B"], start=1)
    ids = [n.id for n in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "ab")
    nap_id = m.list_view(repo)[0].id
    assert m.main(["note", "--path", ":/", "A"]) == 0
    assert capsys.readouterr().out == "Saved to `:/`\n"
    nodes = m.list_view(repo)
    assert all(n.kind == "nap" for n in nodes)
    assert not any(n.kind == "note" and n.caption == "A" for n in nodes)
    zoom_reaches(repo, nap_id, "A")


def test_cli_invalid_nap_caption_does_not_heal(tmp_path, monkeypatch, summem):
    """Invalid nap caption on an overlapping store exits nonzero and leaves payloads unchanged."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _plant_abd_abe(m, repo)
    ids = [n.id for n in m.list_view(repo)]
    before = payload_names(repo)
    calls = {"n": 0}
    real = m.heal_view

    def wrapped(parent):
        calls["n"] += 1
        return real(parent)

    monkeypatch.setattr(m, "heal_view", wrapped)
    assert m.main(["nap", "--path", ":/", ids[0], ids[1], ""]) != 0
    assert calls["n"] == 0
    assert payload_names(repo) == before
