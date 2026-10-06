"""One writer under today's rule: which shapes are reachable at a given budget?"""
from collections import Counter


def single_writer(n_max, budget):
    g, shapes = [], {}
    for n in range(1, n_max + 1):
        g.append(1)
        while len(g) > budget:
            i = next((i for i in range(len(g) - 1) if g[i] == g[i + 1]), None)
            if i is None:
                break
            g[i : i + 2] = [2 * g[i]]
        shapes[n] = list(g)
    return shapes


def head_stats(g):
    head = [x for x in g if x > 1]
    c = Counter(head)
    return max(c.values(), default=0), sum(1 for v in c.values() if v > 1), len(g) - len(head)


for budget in (10, 32):
    shapes = single_writer(5000, budget)
    worst_copies = max(head_stats(s)[0] for s in shapes.values())
    worst_dups = max(head_stats(s)[1] for s in shapes.values())
    ascents = sum(1 for s in shapes.values() for k in range(len(s) - 1) if s[k] < s[k + 1])
    min_tail = min(head_stats(s)[2] for n, s in shapes.items() if n > budget)
    print(f"budget {budget}: over 5,000 notes -> most copies of one grain >= 2: {worst_copies}; "
          f"most duplicated grains at once: {worst_dups}; walls ever: {ascents}; fewest loose notes once full: {min_tail}")
    gap = next((n for n, s in shapes.items() if 64 in s and 32 not in s and 16 not in s and n > 64), None)
    if gap:
        print(f"   e.g. after {gap} notes: {shapes[gap]}  (a 64 with no 32 or 16 below it)")
