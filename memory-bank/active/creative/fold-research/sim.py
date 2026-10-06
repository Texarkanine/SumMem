"""Middle-orphan reproduction and multi-writer simulation against the real driver.

Usage: python sim.py <path-to-summem> <workdir>
"""
import random
import shutil
import sys
from datetime import datetime, timedelta, timezone
from importlib.machinery import SourceFileLoader
from pathlib import Path

m = SourceFileLoader("summem", sys.argv[1]).load_module()
WORK = Path(sys.argv[2])
EPOCH = datetime(2026, 1, 1, tzinfo=timezone.utc)


def equal(a, b):
    return a == b


def r2(a, b):
    return a < 2 * b


def pick(nodes, budget, pred):
    if len(nodes) <= budget:
        return None
    for i in range(len(nodes) - 1):
        if pred(nodes[i].leaves, nodes[i + 1].leaves):
            return nodes[i], nodes[i + 1]
    return None


def catch_up(d, budget, pred, stats):
    """What an obedient agent does: heal, then nap every requested pair in sequence."""
    nodes = m.heal_view(d)
    while True:
        pair = pick(nodes, budget, pred)
        if pair is None:
            return nodes
        left, right = pair
        m.write_nap(d, left.id, right.id, f"c{stats['naps']}", nodes=nodes)
        stats["naps"] += 1
        nodes = m.heal_view(d)


def note(d, t, stats, budget, pred):
    m.write_note(d, f"note {t}", EPOCH + timedelta(seconds=t), random.Random(t))
    return catch_up(d, budget, pred, stats)


def grains(d):
    return [n.leaves for n in m.list_view(d)]


def depth(tree, at=1):
    out = 0
    for kid in tree.kids:
        out = max(out, at if isinstance(kid, m.NoteChild) else depth(kid.tree, at + 1))
    return out


def max_depth(d):
    best = 0
    for n in m.list_view(d):
        if n.kind == "nap":
            best = max(best, depth(m.loads_tree(n.tree_path.read_bytes())))
    return best


def leaf_texts(d):
    out = set()
    for n in m.list_view(d):
        if n.kind == "note":
            out.add(n.caption)
        else:
            out.update(k.text for k in m._note_children(m.loads_tree(n.tree_path.read_bytes())))
    return out


def fresh(name):
    d = WORK / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    m.ensure_store(d)
    return d


# ---------------------------------------------------------------- scenario
def scenario(pred, label):
    print(f"\n== Operator scenario, {label} ==")
    budget = 4
    stats = {"naps": 0}
    d = fresh(f"scenario-{label}")
    for t in range(1, 16):
        m.write_note(d, f"main {t}", EPOCH + timedelta(seconds=t), random.Random(t))
    catch_up(d, 1, equal, stats)
    print("main before merge   ", grains(d))
    # Writer B never saw `main 15` (foo); it noted twice later and napped its own pair.
    for t in (16, 17):
        m.write_note(d, f"B {t}", EPOCH + timedelta(seconds=t), random.Random(t))
    view = m.list_view(d)
    m.write_nap(d, view[-2].id, view[-1].id, "B pair", nodes=view)
    # Writer C noted twice later and did not nap.
    for t in (18, 19):
        m.write_note(d, f"C {t}", EPOCH + timedelta(seconds=t), random.Random(t))
    print("after merge         ", grains(d))
    nodes = catch_up(d, budget, pred, stats)
    print(f"after catch-up (budget {budget})", [n.leaves for n in nodes],
          "over budget, no pair" if len(nodes) > budget else "")
    for t in range(20, 52):
        note(d, t, stats, budget, pred)
    print("after 32 more notes ", grains(d), "naps", stats["naps"], "max depth", max_depth(d))


# --------------------------------------------------------------- simulation
def snapshot(d):
    out = {}
    for sub in ("notes", "naps"):
        for p in (d / ".summem" / sub).iterdir():
            if p.is_file():
                out[f"{sub}/{p.name}"] = p.read_bytes()
    return out


def restore(d, snap):
    for sub in ("notes", "naps"):
        for p in (d / ".summem" / sub).iterdir():
            p.unlink()
    for rel, data in snap.items():
        (d / ".summem" / rel).write_bytes(data)


def three_way(base, ours, theirs):
    """Whole-file add/delete merge: what git does for immutable, uniquely named files."""
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


def simulate(pred, label, *, writers, steps, budget, p_sync, seed):
    rng = random.Random(seed)
    stats = {"naps": 0}
    main_dir = fresh(f"sim-{label}-main")
    probe = fresh(f"sim-{label}-probe")
    ws = []
    for i in range(writers):
        ws.append({"dir": fresh(f"sim-{label}-w{i}"), "base": {}})
    main = {}
    worst_over = 0
    stuck_syncs = 0
    syncs = 0
    for t in range(1, steps + 1):
        w = ws[rng.randrange(writers)]
        note(w["dir"], t, stats, budget, pred)
        if rng.random() < p_sync:
            main = three_way(w["base"], main, snapshot(w["dir"]))
            # The next mutating command on main heals and catches up.
            restore(probe, main)
            nodes = catch_up(probe, budget, pred, {"naps": 0})
            over = len(nodes) - budget
            worst_over = max(worst_over, over)
            syncs += 1
            stuck_syncs += over > 0
            restore(w["dir"], main)
            w["base"] = dict(main)
    for w in ws:
        main = three_way(w["base"], main, snapshot(w["dir"]))
    restore(main_dir, main)
    nodes = catch_up(main_dir, budget, pred, stats)
    lost = {f"note {t}" for t in range(1, steps + 1)} - leaf_texts(main_dir)
    g = [n.leaves for n in nodes]
    print(
        f"{label:6} budget {budget:2} writers {writers}: final view {len(g):3} nodes "
        f"(over budget by {max(0, len(g) - budget):3}); syncs left over budget {stuck_syncs}/{syncs}; "
        f"worst overage {worst_over}; naps {stats['naps']}; max depth {max_depth(main_dir)}; "
        f"notes lost {len(lost)}"
    )
    print(f"       final grains {g}")


if __name__ == "__main__":
    scenario(equal, "equal")
    scenario(r2, "r2")
    print()
    for budget in (8, 32):
        for label, pred in (("equal", equal), ("r2", r2)):
            simulate(pred, label, writers=4, steps=1500, budget=budget, p_sync=0.08, seed=7)
