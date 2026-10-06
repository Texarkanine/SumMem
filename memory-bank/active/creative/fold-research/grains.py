import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path
s = SourceFileLoader("summem", sys.argv[1]).load_module()
for parent in sys.argv[2:]:
    nodes = s.list_view(Path(parent))
    g = [n.leaves for n in nodes]
    walls = [i for i in range(len(g) - 1) if g[i] < g[i + 1]]
    print(parent, "count", len(g), "total", sum(g))
    print("  grains", g)
    print("  ascents at", walls, "->", [(g[i], g[i + 1]) for i in walls])
