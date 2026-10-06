"""Does the listing keep one writer's shape guarantee with many writers?

One writer, today's rule: grains never go up, each grain >= 2 appears at most twice,
at most one grain is doubled at a time. Check every snapshot against that.

Usage: python sim4.py <summem> <workdir> <picker> <budget> <seed>
"""
import importlib.util
import random
import sys
from collections import Counter
from pathlib import Path

SUMMEM, WORK, PICKER, BUDGET, SEED = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
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


sim.pick = {"equal": pick_equal, "v1": pick_v1}[PICKER]


def one_writer_shapes(n_max, budget):
    g, out = [], {}
    for n in range(1, n_max + 1):
        g.append(1)
        while len(g) > budget:
            i = next((i for i in range(len(g) - 1) if g[i] == g[i + 1]), None)
            if i is None:
                break
            g[i : i + 2] = [2 * g[i]]
        out[n] = list(g)
    return out


REF = one_writer_shapes(1600, BUDGET)


def check(g):
    head = Counter(x for x in g if x > 1)
    walls = sum(1 for k in range(len(g) - 1) if g[k] < g[k + 1])
    copies = max(head.values(), default=0)
    dups = sum(1 for v in head.values() if v > 1)
    tail = 0
    while tail < len(g) and g[-1 - tail] == 1:
        tail += 1
    ok = walls == 0 and copies <= 2 and dups <= 1
    return ok, walls, copies, dups, tail


def run():
    rng = random.Random(SEED)
    stats = {"naps": 0}
    probe = sim.fresh(f"p4-{PICKER}-{BUDGET}-{SEED}")
    ws = [{"dir": sim.fresh(f"w4-{PICKER}-{BUDGET}-{SEED}-{i}"), "base": {}, "since": None} for i in range(4)]
    main = {}
    main_rows = []
    writer_rows = []
    recover = []
    for t in range(1, 1501):
        w = ws[rng.randrange(4)]
        nodes = sim.note(w["dir"], t, stats, BUDGET, None)
        g = [n.leaves for n in nodes]
        ok, *_ = check(g)
        writer_rows.append((ok,) + check(g)[1:])
        if w["since"] is not None:
            w["since"] += 1
            if ok:
                recover.append(w["since"])
                w["since"] = None
        if rng.random() < 0.08:
            main = sim.three_way(w["base"], main, sim.snapshot(w["dir"]))
            sim.restore(probe, main)
            nodes = sim.catch_up(probe, BUDGET, None, {"naps": 0})
            g = [n.leaves for n in nodes]
            n_notes = sum(g)
            ref = REF[n_notes]
            row = check(g)
            main_rows.append(row + (g == ref, check(ref)[4], len(g) <= BUDGET))
            sim.restore(w["dir"], main)
            w["base"] = dict(main)
            if not row[0]:
                w["since"] = 0

    def frac(rows, k):
        return sum(1 for r in rows if r[k]) / len(rows)

    worst = max(main_rows, key=lambda r: (r[2], r[3]))
    print(
        f"{PICKER:5} budget {BUDGET} seed {SEED}: main after {len(main_rows)} merges -> "
        f"keeps one-writer shape {frac(main_rows, 0):.0%}, same grains as one writer {frac(main_rows, 5):.0%}, "
        f"within budget {frac(main_rows, 7):.0%}; worst copies of one grain {max(r[2] for r in main_rows)}, "
        f"worst doubled grains {max(r[3] for r in main_rows)}, mean walls {sum(r[1] for r in main_rows) / len(main_rows):.1f}; "
        f"loose notes vs one writer (mean) {sum(r[4] for r in main_rows) / len(main_rows):.1f} vs "
        f"{sum(r[6] for r in main_rows) / len(main_rows):.1f}"
    )
    print(
        f"      writers after each note -> keep one-writer shape {frac(writer_rows, 0):.0%}; "
        f"notes to recover after a merge broke it: median {sorted(recover)[len(recover) // 2] if recover else '-'}, "
        f"max {max(recover) if recover else '-'} ({len(recover)} recoveries)"
    )


run()
