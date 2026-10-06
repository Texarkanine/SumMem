"""Fold pickers judged on stranding AND chronological misordering, using the real driver.

Usage: python sim3.py <summem> <workdir> <picker> [budget] [seed]
"""
import importlib.util
import random
import sys
from datetime import timedelta
from pathlib import Path

SUMMEM, WORK, PICKER = sys.argv[1], sys.argv[2], sys.argv[3]
BUDGET = int(sys.argv[4]) if len(sys.argv) > 4 else 32
SEED = int(sys.argv[5]) if len(sys.argv) > 5 else 7
sys.argv = [sys.argv[0], SUMMEM, WORK]
spec = importlib.util.spec_from_file_location("sim", str(Path(__file__).with_name("sim.py")))
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)
m = sim.m


def any_pair(nodes, id_a, id_b):
    ia = next(i for i, n in enumerate(nodes) if n.id == id_a)
    ib = next(i for i, n in enumerate(nodes) if n.id == id_b and i != ia)
    lo, hi = sorted((ia, ib))
    return nodes[lo], nodes[hi]


m._adjacent_nodes = any_pair


def inversions(g):
    """Walls: pairs where an older row is finer than a newer row."""
    return sum(1 for p in range(len(g)) for q in range(p + 1, len(g)) if g[p] < g[q])


def candidates(g, smaller_gap):
    """(i, j): same grain, no row of that grain between; optionally every row between smaller."""
    out = []
    for j in range(len(g)):
        i = next((i for i in range(j - 1, -1, -1) if g[i] == g[j]), None)
        if i is None:
            continue
        if smaller_gap and any(g[k] > g[j] for k in range(i + 1, j)):
            continue
        out.append((i, j, sum(g[i + 1 : j])))
    return out


def ranked(g, cands):
    def key(c):
        i, j, jump = c
        after = g[:i] + [2 * g[i]] + g[i + 1 : j] + g[j + 1 :]
        return (inversions(after), jump, i)

    return min(cands, key=key) if cands else None


def pick_equal(nodes, budget, _p=None):
    if len(nodes) <= budget:
        return None
    for i in range(len(nodes) - 1):
        if nodes[i].leaves == nodes[i + 1].leaves:
            return nodes[i], nodes[i + 1]
    return None


def pick_v1(nodes, budget, _p=None):
    if len(nodes) <= budget:
        return None
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j].leaves == nodes[i].leaves:
                return nodes[i], nodes[j]
    return None


def _pick_ranked(smaller_gap):
    def pick(nodes, budget, _p=None):
        if len(nodes) <= budget:
            return None
        g = [n.leaves for n in nodes]
        best = ranked(g, candidates(g, smaller_gap))
        return None if best is None else (nodes[best[0]], nodes[best[1]])

    return pick


PICKERS = {
    "equal": pick_equal,
    "v1": pick_v1,
    "pull": _pick_ranked(True),
    "score": _pick_ranked(False),
}
sim.pick = PICKERS[PICKER]


def leaf_rows(d):
    rows = []
    for n in m.list_view(d):
        if n.kind == "note":
            rows.append(([n.name], n.leaves))
        else:
            tree = m.loads_tree(n.tree_path.read_bytes())
            rows.append((sorted(k.name for k in m._note_children(tree)), n.leaves))
    return rows


def misorder(d):
    """Newer-above-older leaf pairs across rows, and the worst displacement per leaf."""
    rows = leaf_rows(d)
    seq = [name for names, _ in rows for name in names]
    n = len(seq)
    rank = {name: r for r, name in enumerate(sorted(seq))}
    later_smaller = [0] * n
    tree = [0] * (n + 1)
    for pos in range(n - 1, -1, -1):
        r = rank[seq[pos]] + 1
        c, k = 0, r - 1
        while k > 0:
            c += tree[k]
            k -= k & -k
        later_smaller[pos] = c
        k = r
        while k <= n:
            tree[k] += 1
            k += k & -k
    pos = 0
    worst = 0
    worst_ratio = 0.0
    total = 0
    displaced = 0
    for names, grain in rows:
        for _ in names:
            d_x = later_smaller[pos]  # within-row leaves are sorted, so this counts later rows only
            total += d_x
            displaced += d_x > 0
            worst = max(worst, d_x)
            worst_ratio = max(worst_ratio, d_x / grain)
            pos += 1
    return total, displaced, worst, worst_ratio, n


def walls(d):
    g = sim.grains(d)
    return sum(1 for i in range(len(g) - 1) if g[i] < g[i + 1])


def young_main_big_branch():
    d = sim.fresh(f"young-{PICKER}")
    stats = {"naps": 0}
    for t in range(1, 6):
        m.write_note(d, f"main {t}", sim.EPOCH + timedelta(seconds=t), random.Random(t))
    sim.catch_up(d, 1, None, stats)
    for t in range(6, 14):
        m.write_note(d, f"branch {t}", sim.EPOCH + timedelta(seconds=t), random.Random(t))
    # The branch never saw main's five notes; it folds its own eight into one 8-pack.
    level = [n.id for n in m.list_view(d) if n.kind == "note" and n.name >= "20260101T000006Z"]
    while len(level) > 1:
        nxt = []
        for k in range(0, len(level), 2):
            before_ids = {n.id for n in m.list_view(d)}
            m.write_nap(d, level[k], level[k + 1], "b")
            nxt += [n.id for n in m.list_view(d) if n.id not in before_ids]
        level = nxt
    before = sim.grains(d)
    first = {n.name for n in m.list_view(d)[:2]}
    for t in range(100, 164):
        sim.note(d, t, stats, 4, None)
    left = [n.name for n in m.list_view(d) if n.name in first]
    print(f"young main + big branch: {before} -> {sim.grains(d)}; old rows still listed: {len(left)}")


def run():
    rng = random.Random(SEED)
    stats = {"naps": 0}
    probe = sim.fresh(f"p3-{PICKER}-{BUDGET}-{SEED}")
    ws = [{"dir": sim.fresh(f"w3-{PICKER}-{BUDGET}-{SEED}-{i}"), "base": {}} for i in range(4)]
    main = {}
    over = []
    wall_counts = []
    for t in range(1, 1501):
        w = ws[rng.randrange(4)]
        sim.note(w["dir"], t, stats, BUDGET, None)
        if rng.random() < 0.08:
            main = sim.three_way(w["base"], main, sim.snapshot(w["dir"]))
            sim.restore(probe, main)
            nodes = sim.catch_up(probe, BUDGET, None, {"naps": 0})
            over.append(max(0, len(nodes) - BUDGET))
            wall_counts.append(walls(probe))
            sim.restore(w["dir"], main)
            w["base"] = dict(main)
    for w in ws:
        main = sim.three_way(w["base"], main, sim.snapshot(w["dir"]))
    sim.restore(probe, main)
    sim.catch_up(probe, BUDGET, None, stats)
    total, displaced, worst, ratio, n = misorder(probe)
    g = sim.grains(probe)
    tail = 0
    while tail < len(g) and g[-1 - tail] == 1:
        tail += 1
    print(
        f"{PICKER:5} budget {BUDGET} seed {SEED}: final rows {len(g)}, walls {walls(probe)}, "
        f"merges left over budget {sum(1 for o in over if o)}/{len(over)}, mean walls after merge "
        f"{sum(wall_counts) / len(wall_counts):.1f}; misordered leaf pairs {total} "
        f"({displaced}/{n} notes listed above an older note, worst {worst} notes, worst/own-row {ratio:.1f}); "
        f"recent verbatim {tail}; naps {stats['naps']}; depth {sim.max_depth(probe)}"
    )


if __name__ == "__main__":
    if BUDGET == 32 and SEED == 7:
        sim.scenario(None, PICKER)
        young_main_big_branch()
    run()
