"""Apply the research prototype of the middle-orphans plan to a COPY of the driver.

Usage: python prototype_plan.py <path-to-a-copy-of-summem>

Never point this at the repository's own `summem`. It rewrites the file in place.

What it changes (the prototype the plan was measured against):
  1. fold_request picks the oldest row that has a same-grain row anywhere below it,
     paired with the nearest one.
  2. _adjacent_nodes accepts a pair of the same grain with no row of that grain
     between them, and refuses unequal grains.
  3. expand_frontier sorts rows by their seconds stamp after each split.

Known differences from the plan (the build must not copy these):
  - The grain refusal sits in the pair check, before children are loaded, so
    four error-order tests fail ("unknown id" / "unreadable pack" lose to
    "not the same grain"). The plan checks grain after loading children.
  - The sort key is the seconds stamp only. The plan carries the oldest
    note's full `stamp-rand` so same-second rows keep a stable order.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
s = path.read_text()


def sub(old, new):
    global s
    if s.count(old) != 1:
        raise SystemExit(f"anchor not found exactly once:\n{old}")
    s = s.replace(old, new)


sub(
    """    for i in range(len(nodes) - 1):
        if nodes[i].leaves == nodes[i + 1].leaves:
            left, right = nodes[i], nodes[i + 1]
            break
""",
    """    for i in range(len(nodes) - 1):
        j = next((j for j in range(i + 1, len(nodes)) if nodes[j].leaves == nodes[i].leaves), None)
        if j is not None:
            left, right = nodes[i], nodes[j]
            break
""",
)
sub(
    """            if abs(ia - ib) == 1:
                lo, hi = (ia, ib) if ia < ib else (ib, ia)
                return nodes[lo], nodes[hi]
    raise ValueError("not adjacent. Nap two ids that sit next to each other in wake.")""",
    """            lo, hi = (ia, ib) if ia < ib else (ib, ia)
            if nodes[lo].leaves != nodes[hi].leaves:
                raise ValueError("not the same grain")
            if any(nodes[k].leaves == nodes[lo].leaves for k in range(lo + 1, hi)):
                continue
            return nodes[lo], nodes[hi]
    raise ValueError("not adjacent. Nap two ids that sit next to each other in wake.")""",
)
sub(
    """        frontier = [*frontier[:idx], *kids, *frontier[idx + 1 :]]
    return frontier""",
    """        frontier = [*frontier[:idx], *kids, *frontier[idx + 1 :]]
        frontier.sort(key=lambda row: row.stamp)
    return frontier""",
)
path.write_text(s)
print(f"patched {path}")
