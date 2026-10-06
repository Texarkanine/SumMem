"""Replay the operator's [16, 8, 4, 2, 1, 4, 2, 1, 2, 1] example under each rule (grains only)."""


def inversions(g):
    return sum(1 for p in range(len(g)) for q in range(p + 1, len(g)) if g[p] < g[q])


def cands(g, smaller_gap):
    out = []
    for j in range(len(g)):
        i = next((i for i in range(j - 1, -1, -1) if g[i] == g[j]), None)
        if i is None or (smaller_gap and any(g[k] > g[j] for k in range(i + 1, j))):
            continue
        out.append((i, j, sum(g[i + 1 : j])))
    return out


def fold(g, i, j):
    return g[:i] + [2 * g[i]] + g[i + 1 : j] + g[j + 1 :]


def rule_v1(g):
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            if g[j] == g[i]:
                return i, j, sum(g[i + 1 : j])


def ranked(smaller_gap):
    def pick(g):
        c = cands(g, smaller_gap)
        return min(c, key=lambda c: (inversions(fold(g, c[0], c[1])), c[2], c[0])) if c else None
    return pick


def show(g, i=None, j=None):
    return "[" + ", ".join(f"*{x}*" if k in (i, j) else str(x) for k, x in enumerate(g)) + "]"


for name, rule in (("v1 (oldest pair)", rule_v1), ("pull-back only", ranked(True)), ("score", ranked(False))):
    g = [16, 8, 4, 2, 1, 4, 2, 1, 2, 1]
    print(f"== {name} ==")
    for note in range(1, 7):
        g = g + [1]
        while len(g) > 10:
            c = rule(g)
            if c is None:
                print("   stuck", g)
                break
            i, j, jump = c
            print(f"   note {note}: {show(g, i, j)} jump {jump}")
            g = fold(g, i, j)
    print("   end", g, "walls", sum(1 for k in range(len(g) - 1) if g[k] < g[k + 1]))
