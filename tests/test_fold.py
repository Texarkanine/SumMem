"""Equal-grain fold request when the view exceeds WAKE_LINES."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from conftest import dated_leaf, load_summem
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


def _equal_grain_pair(nodes):
    """Return the oldest adjacent same-leaf-count file ids, or None."""
    for i in range(len(nodes) - 1):
        if nodes[i].leaves == nodes[i + 1].leaves:
            return nodes[i].id, nodes[i + 1].id
    return None


def test_nap_stem_inherits_left_child_seq_prefix(tmp_path):
    """Nap stem is {left.stamp}-{left.rand}-{leafset}-2 from the left child's filename."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    pa = m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    pb = m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    leafset = m.leafset_id([m.note_digest(pa.read_bytes()), m.note_digest(pb.read_bytes())])
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    stem = f"{pa.name}-{leafset}-2"
    naps = repo / ".summem" / "naps"
    assert (naps / f"{stem}.summ").is_file()
    assert (naps / f"{stem}.tree").is_file()


def test_same_second_nap_stays_in_left_slot(tmp_path):
    """Four notes in one UTC second: napping the oldest two leaves grains [2, 1, 1]."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    rng = Random(0)
    for text in ("a", "b", "c", "d"):
        m.write_note(repo, text, now, rng)
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    assert [n.leaves for n in m.list_view(repo)] == [2, 1, 1]


def test_equal_grain_pair_returns_two_oldest_ids_when_all_ones(tmp_path):
    """equal_grain_pair returns the two oldest ids when every file is a 1."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(("alpha", "beta", "gamma"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    assert _equal_grain_pair(nodes) == (nodes[0].id, nodes[1].id)


def test_equal_grain_pair_returns_none_for_16_plus_1(tmp_path):
    """A 16-pack plus a later note has no equal-grain pair."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "n")
    _fold_loose_notes(m, repo, "pack")
    m.write_note(repo, "later", datetime(2026, 1, 1, 0, 1, 0, tzinfo=UTC), Random(99))
    assert _equal_grain_pair(m.list_view(repo)) is None


def test_equal_grain_pair_returns_two_8s_not_16_plus_8(tmp_path):
    """Two 8-packs beside an older 16-pack yield the two 8s."""
    m = load_summem()
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


def test_equal_grain_pair_returns_two_1s_not_2_plus_1(tmp_path):
    """Grains 2, 1, 1 yield the two 1s, not 2+1."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    for i, text in enumerate(("a", "b", "c", "d"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    m.write_nap(repo, nodes[0].id, nodes[1].id, "pair")
    nodes = m.list_view(repo)
    assert [node.leaves for node in nodes] == [2, 1, 1]
    assert _equal_grain_pair(nodes) == (nodes[1].id, nodes[2].id)


def test_equal_grain_pair_duplicate_ids_when_same_text(tmp_path):
    """Two identical notes are requested as (id, id)."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    m.write_note(repo, "same", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "same", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    assert nodes[0].id == nodes[1].id
    assert _equal_grain_pair(nodes) == (nodes[0].id, nodes[1].id)


def test_over_budget_note_prints_saved_when_16_plus_1(tmp_path, monkeypatch, capsys):
    """WAKE_LINES=1, a 16-pack plus a new note prints Saved. and no fold request."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    _add_notes(m, repo, 16, 0, "n")
    _fold_loose_notes(m, repo, "pack")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    assert m.main(["note", "later"]) == 0
    out = capsys.readouterr().out
    assert out == "Saved.\n"
    assert "Run:" not in out
    assert "Compress these two" not in out


def test_under_budget_note_prints_saved(tmp_path, monkeypatch, capsys):
    """Under-budget note exits 0 with stdout Saved. and no fold request."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    assert m.main(["note", "hello"]) == 0
    out = capsys.readouterr().out
    assert out == "Saved.\n"
    assert "Run:" not in out
    assert "Compress these two" not in out


def test_long_stream_same_second_grains_are_powers_of_two(tmp_path, monkeypatch):
    """24 same-second notes at budget 8 fold to power-of-two grains, never a 17."""
    m = load_summem()
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


def test_sixteen_leaf_pack_tree_depth_is_log(tmp_path):
    """Sixteen 1s folded by equal_grain_pair produce NoteChild depth <= 4."""
    m = load_summem()
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


def test_nap_prints_remaining_ones_not_parent_plus_one(tmp_path, monkeypatch, capsys):
    """After napping two of four 1s at budget 2, stdout is the remaining two 1s."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    for i, text in enumerate(("a", "b", "c", "d"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    nodes = m.list_view(repo)
    assert m.main(["nap", nodes[0].id, nodes[1].id, "pair"]) == 0
    out = capsys.readouterr().out
    assert "Saved." not in out
    assert f"  {dated_leaf('20260101T000003Z', 'c')}\n" in out
    assert f"  {dated_leaf('20260101T000004Z', 'd')}\n" in out
    assert "Run: .summem/summem nap " in out
    assert "Invent nothing." in out


def test_nap_prints_nothing_when_at_or_under_budget(tmp_path, monkeypatch, capsys):
    """A successful nap at or under file budget prints nothing."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 2)
    m.write_note(repo, "alpha", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "beta", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    nodes = m.list_view(repo)
    assert m.main(["nap", nodes[0].id, nodes[1].id, "pair"]) == 0
    assert capsys.readouterr().out == ""


def test_over_budget_note_requests_equal_grain_ones(tmp_path, monkeypatch, capsys):
    """With WAKE_LINES=3, a fourth note prints the two oldest ids and writes no nap."""
    m = load_summem()
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
    assert out.index("Saved.") < out.index("Compress these two")
    assert "Compress these two into one line of at most 280 characters." in out
    assert "Invent nothing." in out
    assert f"  {dated_leaf('20260101T000001Z', 'alpha')}\n" in out
    assert f"  {dated_leaf('20260101T000002Z', 'beta')}\n" in out
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


def test_default_wake_lines_is_32():
    """Default WAKE_LINES is 32."""
    m = load_summem()
    assert m.WAKE_LINES == 32


def test_config_toml_wake_lines_is_read(tmp_path, monkeypatch, capsys):
    """A committed config.toml WAKE_LINES value is the store's budget."""
    m = load_summem()
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


def test_fold_request_reuses_nodes_and_entry_chars(tmp_path, monkeypatch):
    """fold_request(nodes=..., entry_chars=...) does not list or parse knobs."""
    m = load_summem()
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


def test_fold_request_mentions_remaining(tmp_path, monkeypatch):
    """Five notes at budget 3: fold_request says compressions remain after this one."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 3)
    for i, text in enumerate(("a", "b", "c", "d", "e"), start=1):
        m.write_note(repo, text, datetime(2026, 1, 1, 0, 0, i, tzinfo=UTC), Random(i))
    out = m.fold_request(repo, 3)
    assert "1 compression remains after this one." in out
    assert f"  {dated_leaf('20260101T000001Z', 'a')}\n" in out
    assert f"  {dated_leaf('20260101T000002Z', 'b')}\n" in out
    assert "Run: .summem/summem nap " in out
    assert "Run: summem nap " not in out


def test_fold_request_identical_notes_use_short_prefix(tmp_path, monkeypatch):
    """Two identical notes over budget emit 8-hex prefixes, not 64-hex ids."""
    m = load_summem()
    repo = init_repo(tmp_path / "r")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(m, "WAKE_LINES", 1)
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC), Random(1))
    m.write_note(repo, "hello", datetime(2026, 1, 1, 0, 0, 2, tzinfo=UTC), Random(2))
    cid = m.list_view(repo)[0].id
    out = m.fold_request(repo, 1)
    assert cid not in out
    prefix = m.short_id(cid, [cid, cid])
    assert len(prefix) == 8
    assert f"nap {prefix} {prefix} " in out


def test_fold_request_uses_config_entry_chars(tmp_path, monkeypatch):
    """A store ENTRY_CHARS value appears in the fold prompt."""
    m = load_summem()
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


def test_fold_request_includes_path_when_cwd_misses_store(tmp_path, monkeypatch):
    """Walk-up from $PWD is a different store: Run: includes --path to the folded store."""
    m = load_summem()
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


def test_fold_request_omits_path_when_cwd_selects_store(tmp_path, monkeypatch):
    """Walk-up from $PWD already finds the folded store: Run: has no --path."""
    m = load_summem()
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
