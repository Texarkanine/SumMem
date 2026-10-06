"""Read-only: count packs whose grain is not a power of two, listed and nested, per store."""
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

m = SourceFileLoader("summem", sys.argv[1]).load_module()


def walk(tree, depth, out):
    n = 0
    for kid in tree.kids:
        if isinstance(kid, m.NoteChild):
            n += 1
        else:
            k = walk(kid.tree, depth + 1, out)
            out.append((k, depth + 1))
            n += k
    return n


for store in sys.argv[2:]:
    parent = Path(store).parent
    naps = Path(store) / "naps"
    if not naps.is_dir():
        continue
    try:
        view = m.list_view(parent)
    except Exception as exc:
        print(f"{parent}: unreadable ({exc.__class__.__name__})")
        continue
    listed_odd = [n.leaves for n in view if n.leaves & (n.leaves - 1)]
    nested = []
    deepest = 0
    old_stems = sum(1 for p in naps.iterdir() if p.suffix == ".tree" and m._parse_nap_stem(p.stem) is None)
    for n in view:
        if n.kind != "nap" or n.tree_path is None:
            continue
        out = []
        walk(m.loads_tree(n.tree_path.read_bytes()), 0, out)
        nested += [g for g, _ in out if g & (g - 1)]
        deepest = max([deepest] + [d for _, d in out])
    print(f"{parent}: rows {len(view)}, notes {sum(n.leaves for n in view)}, listed odd {listed_odd}, "
          f"nested odd {sorted(nested)[:12]}{'...' if len(nested) > 12 else ''} ({len(nested)}), "
          f"deepest nesting {deepest}, unmigrated old stems {old_stems}")
