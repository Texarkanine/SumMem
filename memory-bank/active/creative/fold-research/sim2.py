"""Compare skip-fold orderings against today's rule and R2, using the real driver."""
import random
import sys
from pathlib import Path

sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
import importlib.util
spec = importlib.util.spec_from_file_location("sim", str(Path(__file__).with_name("sim.py")))
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)
m = sim.m


def any_pair(nodes, id_a, id_b):
    """Skip-fold nap: the two nodes need not be neighbors. Left is the older."""
    ia = next(i for i, n in enumerate(nodes) if n.id == id_a)
    ib = next(i for i, n in enumerate(nodes) if n.id == id_b and i != ia)
    lo, hi = sorted((ia, ib))
    return nodes[lo], nodes[hi]


m._adjacent_nodes = any_pair


def pick_v1(nodes, budget, _pred=None):
    """Oldest node that has a same-grain partner anywhere later; its oldest partner."""
    if len(nodes) <= budget:
        return None
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j].leaves == nodes[i].leaves:
                return nodes[i], nodes[j]
    return None


def pick_v2(nodes, budget, _pred=None):
    """Smallest grain that occurs twice; its two oldest nodes."""
    if len(nodes) <= budget:
        return None
    seen = {}
    for n in nodes:
        seen.setdefault(n.leaves, []).append(n)
    dup = sorted(g for g, ns in seen.items() if len(ns) > 1)
    if not dup:
        return None
    a, b = seen[dup[0]][:2]
    return a, b


real_pick = sim.pick


def use(picker):
    sim.pick = picker if picker is not None else real_pick


def tail_ones(d):
    g = sim.grains(d)
    k = 0
    while k < len(g) and g[-1 - k] == 1:
        k += 1
    return k


def single_writer(label, picker, pred, budget=32, steps=400):
    use(picker)
    d = sim.fresh(f"single-{label}")
    stats = {"naps": 0}
    for t in range(1, steps + 1):
        sim.note(d, t, stats, budget, pred)
    g = sim.grains(d)
    print(f"single writer {label:6}: {len(g)} nodes, verbatim recent notes {tail_ones(d)}, "
          f"loose notes {g.count(1)}, naps {stats['naps']}, grains {g[:8]}...")


if __name__ == "__main__":
    combos = [("equal", None, sim.equal), ("r2", None, sim.r2), ("v1", pick_v1, None), ("v2", pick_v2, None)]
    for label, picker, pred in combos:
        single_writer(label, picker, pred)
    print()
    for label, picker, pred in combos[2:]:
        use(picker)
        sim.scenario(pred, label)
    print()
    for budget in (8, 32):
        for label, picker, pred in combos[2:]:
            use(picker)
            sim.simulate(pred, label, writers=4, steps=1500, budget=budget, p_sync=0.08, seed=7)
