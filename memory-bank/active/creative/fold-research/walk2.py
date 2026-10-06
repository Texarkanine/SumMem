import importlib.util, json, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("walk", str(Path(__file__).with_name("walk.py")))
src = Path(__file__).with_name("walk.py").read_text().split("for name, rule in")[0]
ns = {}
exec(src, ns)


def rule_equal(g):
    for i in range(len(g) - 1):
        if g[i] == g[i + 1]:
            return i, i + 1, 0


def rule_v2(g):
    dup = sorted({x for x in g if g.count(x) > 1})
    if not dup:
        return None
    idx = [k for k, x in enumerate(g) if x == dup[0]][:2]
    return idx[0], idx[1], sum(g[idx[0] + 1 : idx[1]])


def rule_r2(g):
    for i in range(len(g) - 1):
        if g[i] < 2 * g[i + 1]:
            return i, i + 1, 0


def fold_any(g, i, j):
    return g[:i] + [g[i] + g[j]] + g[i + 1 : j] + g[j + 1 :]


out = {}
rules = {"today": rule_equal, "r2": rule_r2, "v2": rule_v2, "v1": ns["rule_v1"], "pull": ns["ranked"](True), "score": ns["ranked"](False)}
for name, rule in rules.items():
    g = [16, 8, 4, 2, 1, 4, 2, 1, 2, 1]
    steps = [{"note": 0, "grains": list(g), "pair": None, "jump": 0}]
    for note in range(1, 7):
        g = g + [1]
        while len(g) > 10:
            c = rule(g)
            if c is None:
                steps.append({"note": note, "grains": list(g), "pair": None, "jump": None, "stuck": True})
                break
            i, j, jump = c
            steps.append({"note": note, "grains": list(g), "pair": [i, j], "jump": jump})
            g = fold_any(g, i, j)
    steps.append({"note": "end", "grains": list(g), "pair": None, "jump": 0})
    out[name] = steps
json.dump(out, open(sys.argv[1], "w"))
for k, v in out.items():
    print(k, [ (s["note"], s["pair"], s["jump"]) for s in v if s["pair"] or s.get("stuck")][:8], "end", v[-1]["grains"])
