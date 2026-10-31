"""Equal-grain fold request when the view exceeds WAKE_LINES."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from random import Random

import pytest
from conftest import dated_leaf
from gitutil import fold_ids, init_repo

UTC = timezone.utc


def _add_notes(m, repo, count, offset, prefix):
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i in range(count):
        m.write_note(
            repo,
            f"{prefix}{i}",
            base + timedelta(seconds=offset + i),
            Random(offset + i),
        )


def _fold_loose_notes(m, repo, caption):
    ids = [node.id for node in m.list_view(repo) if node.kind == "note"]
    return fold_ids(m, repo, ids, caption)


def _max_note_depth(m, tree, depth=1) -> int:
    deepest = 0
    for child in tree.kids:
        if isinstance(child, m.NoteChild):
            deepest = max(deepest, depth)
        else:
            deepest = max(deepest, _max_note_depth(m, child.tree, depth + 1))
    return deepest


def _equal_grain_indices(grains):
    """Return the oldest adjacent equal-grain index pair, or None."""
    for i in range(len(grains) - 1):
        if grains[i] == grains[i + 1]:
            return i, i + 1
    return None


def _equal_grain_pair(nodes):
    """Return the oldest adjacent same-leaf-count file ids, or None."""
    pair = _equal_grain_indices([node.leaves for node in nodes])
    if pair is None:
        return None
    return nodes[pair[0]].id, nodes[pair[1]].id


def test_nap_stem_inherits_left_child_seq_prefix(tmp_path, summem):
    """Nap stem inherits the left child's {stamp}-{rand} and ends with the pair digest."""
    m = summem
    repo = init_repo(tmp_path / "r")
    pa = m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    pb = m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    leafset = m.leafset_id([m.note_digest(pa.read_bytes()), m.note_digest(pb.read_bytes())])
    tree = m.Tree(
        kids=[
            m.NoteChild(name=pa.name, text="alpha"),
            m.NoteChild(name=pb.name, text="beta"),
        ]
    )
    tree_bytes = m.dumps_tree(tree)
    caption_bytes = m.note_file_bytes("pair")
    stem = m.nap_stem(pa.name, leafset, 2, tree_bytes, caption_bytes)
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.summ").is_file()
    assert (naps / f"{stem}.tree").is_file()
    parsed = m._parse_nap_stem(stem)
    assert parsed is not None
    stamp, rand, got_leafset, grain, tag = parsed
    assert f"{stamp}-{rand}" == pa.name
    assert got_leafset == leafset
    assert grain == 2
    assert tag == m.variant_tag(tree_bytes, caption_bytes)


def test_write_nap_serializes_tree_once(tmp_path, monkeypatch, summem):
    """write_nap calls dumps_tree once for a two-note fold."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    orig = m.dumps_tree
    calls = {"n": 0}

    def wrapped(tree):
        calls["n"] += 1
        return orig(tree)

    monkeypatch.setattr(m, "dumps_tree", wrapped)
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    assert calls["n"] == 1


def test_same_second_nap_stays_in_left_slot(tmp_path, summem):
    """Four notes in one UTC second: napping the oldest two leaves grains [2, 1, 1]."""
    m = summem
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = Random(0)
    for text in ("a", "b", "c", "d"):
        m.write_note(repo, text, now, rng)
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    assert [n.leaves for n in m.list_view(repo)] == [2, 1, 1]


def test_equal_grain_pair_returns_two_oldest_ids_when_all_ones(tmp_path, summem):
    """equal_grain_pair returns the two oldest ids when every file is a 1."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(("alpha", "beta", "gamma"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    assert _equal_grain_pair(nodes) == (nodes[0].id, nodes[1].id)


def test_equal_grain_pair_returns_none_for_16_plus_1(tmp_path, summem):
    """A 16-pack plus a later note has no equal-grain pair."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "n")
    _fold_loose_notes(m, repo, "pack")
    m.write_note(repo, "later", datetime(2026, 1, 1, 0, 1, 0, tzinfo=UTC), Random(99))
    assert _equal_grain_pair(m.list_view(repo)) is None


def test_equal_grain_pair_returns_two_8s_not_16_plus_8(tmp_path, summem):
    """Two 8-packs beside an older 16-pack yield the two 8s."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "a")
    _fold_loose_notes(m, repo, "sixteen")
    _add_notes(m, repo, 8, 16, "b")
    _fold_loose_notes(m, repo, "eight-b")
    _add_notes(m, repo, 8, 24, "c")
    _fold_loose_notes(m, repo, "eight-c")
    nodes = m.list_view(repo)
    assert [node.leaves for node in nodes] == [16, 8, 8]
    assert _equal_grain_pair(nodes) == (nodes[1].id, nodes[2].id)


def test_equal_grain_pair_returns_two_1s_not_2_plus_1(tmp_path, summem):
    """Grains 2, 1, 1 yield the two 1s, not 2+1."""
    m = summem
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(("a", "b", "c", "d"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    nodes = m.list_view(repo)
    assert [node.leaves for node in nodes] == [2, 1, 1]
    assert _equal_grain_pair(nodes) == (nodes[1].id, nodes[2].id)


def test_equal_grain_pair_duplicate_ids_when_same_text(tmp_path, summem):
    """After heal, two identical notes are one view node; no (id, id) pair."""
    m = summem
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "same", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "same", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert _equal_grain_pair(nodes) is None


def test_over_budget_note_prints_saved_when_16_plus_1(tmp_path, monkeypatch, capsys, summem):
    """WAKE_LINES=1, a 16-pack plus a new note prints Saved. and no fold request."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "n")
    _fold_loose_notes(m, repo, "pack")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    assert m.main(["note", "later"]) == 0
    out = capsys.readouterr().out
    assert out == "Saved.\n"
    assert "Run:" not in out
    assert "Nothing left to compress." not in out


def test_under_budget_note_prints_saved(tmp_path, monkeypatch, capsys, summem):
    """Under-budget note exits 0 with stdout Saved. and no fold request."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "hello"]) == 0
    out = capsys.readouterr().out
    assert out == "Saved.\n"
    assert "Run:" not in out
    assert "Nothing left to compress." not in out


def test_long_stream_same_second_grains_are_powers_of_two(tmp_path, monkeypatch, summem):
    """24 same-second notes at budget 8 fold to power-of-two grains, never a 17."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.setattr(m, "WAKE_LINES", 8)
    now = datetime(2026, 1, 1, tzinfo=UTC)
    rng = Random(0)
    for i in range(24):
        m.write_note(repo, f"n{i}", now, rng)
        while len(m.list_view(repo)) > 8:
            pair = _equal_grain_pair(m.list_view(repo))
            if pair is None:
                break
            m.write_nap(repo, pair[0], pair[1], "fold")
    nodes = m.list_view(repo)
    grains = [node.leaves for node in nodes]
    assert len(nodes) <= 8
    assert all(g > 0 and g & (g - 1) == 0 for g in grains)
    assert any(g >= 4 for g in grains)
    assert 17 not in grains


def test_sixteen_leaf_pack_tree_depth_is_log(tmp_path, summem):
    """Sixteen 1s folded by equal_grain_pair produce NoteChild depth <= 4."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "n")
    while True:
        pair = _equal_grain_pair(m.list_view(repo))
        if pair is None:
            break
        m.write_nap(repo, pair[0], pair[1], "fold")
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    assert nodes[0].leaves == 16
    tree = m.loads_tree(nodes[0].tree_path.read_bytes())
    assert _max_note_depth(m, tree) <= 4


def test_nap_prints_saved_and_idle_when_at_or_under_budget(tmp_path, monkeypatch, capsys, summem):
    """A successful nap at or under file budget prints Saved. then Nothing left to compress."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    assert m.main(["nap", nodes[0].id, nodes[1].id, "pair"]) == 0
    assert capsys.readouterr().out == "Saved.\n\nNothing left to compress.\n"


def test_nap_prints_remaining_count_after_saved(tmp_path, monkeypatch, capsys, summem):
    """Five notes at budget 2: first nap prints Saved. then 1 compression remains after this one."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    for i, text in enumerate(("a", "b", "c", "d", "e"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    assert m.main(["nap", nodes[0].id, nodes[1].id, "pair"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Saved.\n\n")
    assert "1 compression remains after this one." in out
    assert "  c\n" in out
    assert "  d\n" in out
    assert "Nothing left to compress." not in out


def test_over_budget_note_requests_equal_grain_ones(tmp_path, monkeypatch, capsys, summem):
    """With WAKE_LINES=3, a fourth note prints the two oldest ids and writes no nap."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 3)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.write_note(repo, "gamma", datetime(2026, 1, 1, 0, 0, 3, tzinfo=UTC), Random(3))
    ids = [node.id for node in m.list_view(repo)]
    assert m.main(["note", "delta"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Saved.\n")
    assert "  alpha\n" in out
    assert "  beta\n" in out
    assert 'Run: .summem/summem nap ' in out
    assert '"<your line>"' in out
    pa = m.short_id(ids[0], ids)
    pb = m.short_id(ids[1], ids)
    assert f"nap {pa} {pb} " in out
    assert ids[0] not in out
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(notes) == 4
    naps = repo / ".summem" / "naps"
    assert list(naps.glob("*.summ")) == []
    assert list(naps.glob("*.tree")) == []


def test_default_wake_lines_is_32(summem):
    """Default WAKE_LINES is 32."""
    m = summem
    assert m.WAKE_LINES == 32


def test_config_toml_wake_lines_is_read(tmp_path, monkeypatch, capsys, summem):
    """A committed config.toml WAKE_LINES value is the store's budget."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 1\n", encoding="utf-8")
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    assert m.main(["note", "beta"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Saved.\n")
    assert out.index("Saved.") < out.index("Run:")
    assert "Run: .summem/summem nap " in out
    assert "Invent nothing." in out
    notes = [p for p in (repo / ".summem" / "notes").iterdir() if not p.name.startswith(".")]
    assert len(notes) == 2
    assert list((repo / ".summem" / "naps").glob("*.summ")) == []


def test_fold_request_reuses_nodes_and_entry_chars(tmp_path, monkeypatch, summem):
    """fold_request(nodes=..., entry_chars=...) does not list or parse knobs."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    for i, text in enumerate(("a", "b", "c"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    expected = m.fold_request(repo, 1)

    def boom(*_args, **_kwargs):
        raise AssertionError("fold_request must reuse nodes and entry_chars")

    monkeypatch.setattr(m, "list_view", boom)
    monkeypatch.setattr(m, "knobs", boom)
    out = m.fold_request(repo, 1, nodes=nodes, entry_chars=280)
    assert out == expected


def test_fold_request_mentions_remaining(tmp_path, monkeypatch, summem):
    """Five notes at budget 3: fold_request says compressions remain after this one."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 3)
    for i, text in enumerate(("a", "b", "c", "d", "e"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    out = m.fold_request(repo, 3)
    assert "1 compression remains after this one." in out
    assert "  a\n" in out
    assert "  b\n" in out
    assert "Run: .summem/summem nap " in out
    assert "Run: summem nap " not in out


def test_fold_request_identical_notes_use_short_prefix(tmp_path, monkeypatch, summem):
    """After heal, two identical notes are one node; fold_request has no (prefix, prefix) Run line."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    m.heal_view(repo)
    nodes = m.list_view(repo)
    assert len(nodes) == 1
    out = m.fold_request(repo, 1)
    assert out == ""
    assert "Run:" not in out
    cid = nodes[0].id
    prefix = m.short_id(cid, [cid])
    assert f"nap {prefix} {prefix} " not in out


def test_fold_request_uses_config_entry_chars(tmp_path, monkeypatch, summem):
    """A store ENTRY_CHARS value appears in the fold prompt."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    m.ensure_store(repo)
    (repo / ".summem" / "config.toml").write_text("ENTRY_CHARS = 140\n", encoding="utf-8")
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    out = m.fold_request(repo, 1)
    assert "140 characters" in out
    assert "280 characters" not in out


def test_fold_request_includes_path_when_cwd_misses_store(tmp_path, monkeypatch, summem):
    """Walk-up from $PWD is a different store: Run: includes --path to the folded store."""
    m = summem
    repo = init_repo(tmp_path / "r")
    nested = repo / "foo" / "packages" / "baz"
    nested.mkdir(parents=True)
    m.ensure_store(nested)
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(nested, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(nested, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    out = m.fold_request(nested, 1)
    assert "nap --path foo/packages/baz " in out


def test_fold_request_omits_path_when_cwd_selects_store(tmp_path, monkeypatch, summem):
    """Walk-up from $PWD already finds the folded store: Run: has no --path."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    repo = init_repo(tmp_path / "r")
    pkg = repo / "pkg"
    pkg.mkdir()
    m.ensure_store(pkg)
    nested = pkg / "src"
    nested.mkdir()
    monkeypatch.chdir(nested)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(pkg, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(pkg, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    out = m.fold_request(pkg, 1)
    assert " --path " not in out
    assert "Run: .summem/summem nap " in out


def test_fold_request_run_uses_agent_invoke(tmp_path, monkeypatch, summem):
    """On nt, fold_request Run: uses agent_invoke(), not a bare AGENT_BIN command."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: True)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    out = m.fold_request(repo, 1)
    invoke = m.agent_invoke()
    assert invoke == f"python {m.AGENT_BIN}"
    assert f"Run: {invoke} nap " in out
    assert "Run: .summem/summem nap " not in out
    assert m.sys.executable not in out


def test_fold_request_note_pair_quotes_text_only(tmp_path, monkeypatch, summem):
    """Two notes over budget: fold quotes note text; wake still has x1 and the day."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    ids = [node.id for node in nodes]
    pa = m.short_id(nodes[0].id, ids)
    pb = m.short_id(nodes[1].id, ids)
    out = m.fold_request(repo, 1)
    assert "  alpha\n" in out
    assert "  beta\n" in out
    assert dated_leaf("20260101T000001Z", "alpha") not in out
    assert dated_leaf("20260101T000002Z", "beta") not in out
    assert "x1 " not in out
    assert f"nap {pa} {pb} " in out
    wake = m.wake_text(repo)
    assert dated_leaf("20260101T000001Z", "alpha") in wake
    assert dated_leaf("20260101T000002Z", "beta") in wake


def test_fold_request_pack_pair_quotes_captions_only(tmp_path, monkeypatch, summem):
    """Two x2 packs over budget: fold quotes captions; wake still has grain and prefix."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    for i, text in enumerate(("a", "b", "c", "d", "i"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "e & f")
    m.write_nap(repo, ids[2], ids[3], "g & h")
    packs = [node for node in m.list_view(repo) if node.kind == "nap"]
    assert len(packs) == 2
    view_ids = [node.id for node in m.list_view(repo)]
    pa = m.short_id(packs[0].id, view_ids)
    pb = m.short_id(packs[1].id, view_ids)
    out = m.fold_request(repo, 2)
    assert "  e & f\n" in out
    assert "  g & h\n" in out
    assert f"x2 {pa}:" not in out
    assert f"x2 {pb}:" not in out
    assert f"nap {pa} {pb} " in out
    wake = m.wake_text(repo)
    assert f"x2 {pa}: e & f" in wake
    assert f"x2 {pb}: g & h" in wake


def test_fold_request_empty_pack_caption_is_blank_quote(tmp_path, monkeypatch, summem):
    """Missing .summ on two packs: fold quotes blank lines, not reconstructed xN prefix:."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    for i, text in enumerate(("a", "b", "c", "d", "i"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    ids = [node.id for node in m.list_view(repo)]
    m.write_nap(repo, ids[0], ids[1], "e & f")
    m.write_nap(repo, ids[2], ids[3], "g & h")
    for node in m.list_view(repo):
        if node.kind == "nap" and node.sum_path is not None:
            node.sum_path.unlink()
    packs = [node for node in m.list_view(repo) if node.kind == "nap"]
    assert len(packs) == 2
    view_ids = [node.id for node in m.list_view(repo)]
    pa = m.short_id(packs[0].id, view_ids)
    pb = m.short_id(packs[1].id, view_ids)
    out = m.fold_request(repo, 2)
    assert "\n  \n  \n\nRun:" in out
    assert f"x2 {pa}:" not in out
    assert f"x2 {pb}:" not in out
    assert f"nap {pa} {pb} " in out


_RUN = re.compile(r' nap(?: --path \S+)? (\S+) (\S+) "')


def _seal(m, repo, count, start, prefix):
    """Add *count* notes and, when there are at least two, fold only those notes."""
    before = {node.id for node in m.list_view(repo)}
    _add_notes(m, repo, count, start, prefix)
    new = [node.id for node in m.list_view(repo) if node.kind == "note" and node.id not in before]
    assert len(new) == count
    if count >= 2:
        fold_ids(m, repo, new, prefix)


def _named_pair(m, view, out):
    """Return the two full ids named on a fold request's Run: line."""
    id_a, id_b = _RUN.search(out).groups()
    ids = [node.id for node in view]
    return {m.resolve_id(id_a, ids), m.resolve_id(id_b, ids)}


def test_fold_request_skips_to_nearest_same_grain_row_across_a_wall(tmp_path, summem):
    """Grains 8, 4, 2, 1, 4 over budget: fold names the two 4s, not the neighbors."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _seal(m, repo, 8, 0, "a")
    _seal(m, repo, 4, 8, "b")
    _seal(m, repo, 2, 12, "c")
    _seal(m, repo, 1, 14, "d")
    _seal(m, repo, 4, 15, "e")
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [8, 4, 2, 1, 4]
    out = m.fold_request(repo, 4, nodes=view)
    assert _named_pair(m, view, out) == {view[1].id, view[4].id}


def test_fold_request_takes_oldest_row_with_a_twin_first(tmp_path, summem):
    """Grains 8, 1, 4, 1 at budget 3: fold names the two 1s."""
    m = summem
    repo = init_repo(tmp_path / "r")
    _seal(m, repo, 8, 0, "a")
    _seal(m, repo, 1, 8, "b")
    _seal(m, repo, 4, 9, "c")
    _seal(m, repo, 1, 13, "d")
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [8, 1, 4, 1]
    out = m.fold_request(repo, 3, nodes=view)
    assert _named_pair(m, view, out) == {view[1].id, view[3].id}


def test_run_line_for_a_skip_pair_is_accepted_by_nap(tmp_path, monkeypatch, capsys, summem):
    """A skip pair's Run: line, pasted into nap, exits 0 and prints Saved."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _seal(m, repo, 8, 0, "a")
    _seal(m, repo, 1, 8, "b")
    _seal(m, repo, 4, 9, "c")
    _seal(m, repo, 1, 13, "d")
    view = m.list_view(repo)
    out = m.fold_request(repo, 3, nodes=view)
    id_a, id_b = _RUN.search(out).groups()
    assert m.main(["nap", id_a, id_b, "the two ones"]) == 0
    assert capsys.readouterr().out.startswith("Saved.\n")


def _break_children(node, how):
    """Remove or corrupt a nap row's children file."""
    if how == "missing":
        node.tree_path.unlink()
    else:
        node.tree_path.write_bytes(b"not a tree\n")


@pytest.mark.parametrize("how", ["missing", "unreadable"])
def test_fold_request_skips_a_pack_whose_children_file_is_broken(tmp_path, monkeypatch, capsys, summem, how):
    """Grains 2, 1, 2, 1, 1 with the oldest 2's children file broken: fold names the two oldest 1s, and nap accepts them."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _seal(m, repo, 2, 0, "a")
    _seal(m, repo, 1, 2, "b")
    _seal(m, repo, 2, 3, "c")
    _seal(m, repo, 1, 5, "d")
    _seal(m, repo, 1, 6, "e")
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [2, 1, 2, 1, 1]
    _break_children(view[0], how)
    view = m.list_view(repo)
    out = m.fold_request(repo, 4, nodes=view)
    assert _named_pair(m, view, out) == {view[1].id, view[3].id}
    id_a, id_b = _RUN.search(out).groups()
    assert m.main(["nap", id_a, id_b, "the two ones"]) == 0
    assert capsys.readouterr().out.startswith("Saved.\n")


def test_fold_pair_matches_neighbors_rule_for_one_writer(summem):
    """One writer: _fold_pair matches the neighbors-only rule at every fold step."""
    m = summem
    for budget in range(1, 33):
        grains = []
        for _note in range(200):
            grains.append(1)
            while len(grains) > budget:
                old = _equal_grain_indices(grains)
                new = m._fold_pair(grains)
                assert new == old, (budget, grains, old, new)
                if old is None:
                    break
                i, j = old
                grains = grains[:i] + [grains[i] + grains[j]] + grains[j + 1 :]


def test_fold_pair_skips_non_power_of_two_rows(summem):
    """_fold_pair skips rows whose grain is not a power of two."""
    m = summem
    assert m._fold_pair([6, 6, 2, 1, 1]) == (3, 4)
    assert m._fold_pair([6, 6]) is None
    assert m._fold_pair([8, 1, 4, 1]) == (1, 3)


def test_fold_request_skips_a_pack_whose_digest_count_is_not_the_stem_grain(
    tmp_path, monkeypatch, capsys, summem
):
    """Grains 2, 1, 2, 1, 1 with the oldest 2's tree parsing at another digest count: fold names the two oldest 1s, and nap accepts them."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _seal(m, repo, 2, 0, "a")
    _seal(m, repo, 1, 2, "b")
    _seal(m, repo, 2, 3, "c")
    _seal(m, repo, 1, 5, "d")
    _seal(m, repo, 1, 6, "e")
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [2, 1, 2, 1, 1]
    tree = m.loads_tree(view[0].tree_path.read_bytes())
    extra = m.NoteChild(name="20260101T000000Z-eeeeeeeeeeeeeeee", text="extra")
    view[0].tree_path.write_bytes(m.dumps_tree(m.Tree(kids=[*tree.kids, extra])))
    view = m.list_view(repo)
    _child, digests = m._as_child(view[0])
    assert len(digests) != view[0].leaves
    x2_lines = [line for line in m.wake_text(repo).splitlines() if line.startswith("x2 ")]
    assert len(x2_lines) == 1
    assert x2_lines[0].endswith(": a-0")
    out = m.fold_request(repo, 4, nodes=view)
    assert _named_pair(m, view, out) == {view[1].id, view[3].id}
    id_a, id_b = _RUN.search(out).groups()
    assert m.main(["nap", id_a, id_b, "the two ones"]) == 0
    assert capsys.readouterr().out.startswith("Saved.\n")


def _rename_stem_grain(m, node, grain: int) -> None:
    """Point a nap pair's filename grain at *grain* and leave the children file bytes."""
    stamp, rand, leafset, _old, variant = m._parse_nap_stem(node.name)
    stem = f"{stamp}-{rand}-{leafset}-{grain}-{variant}"
    folder = node.tree_path.parent
    node.tree_path.rename(folder / f"{stem}.tree")
    node.sum_path.rename(folder / f"{stem}.summ")


def test_fold_request_folds_a_lying_filename_with_a_truthful_row(
    tmp_path, monkeypatch, capsys, summem
):
    """Filename grains 4 and 2, both with 4 digests: fold names that pair, nap accepts it, and wake still lists the filenames."""
    m = summem
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    _seal(m, repo, 4, 0, "a")
    _seal(m, repo, 4, 4, "b")
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [4, 4]
    _rename_stem_grain(m, view[1], 2)
    view = m.list_view(repo)
    assert [node.leaves for node in view] == [4, 2]
    assert [len(m._as_child(node)[1]) for node in view] == [4, 4]
    (repo / ".summem" / "config.toml").write_text("WAKE_LINES = 2\n", encoding="utf-8")
    assert [line.split(" ", 1)[0] for line in m.wake_text(repo).splitlines()] == ["x4", "x2"]
    out = m.fold_request(repo, 1, nodes=view)
    assert _named_pair(m, view, out) == {view[0].id, view[1].id}
    id_a, id_b = _RUN.search(out).groups()
    assert m.main(["nap", id_a, id_b, "the eights"]) == 0
    assert capsys.readouterr().out.startswith("Saved.\n")
    assert [node.leaves for node in m.list_view(repo)] == [8]

