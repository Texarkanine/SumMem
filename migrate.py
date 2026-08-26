#!/usr/bin/env python3

# Copyright (C) 2026 Texarkanine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Rename complete four-part SumMem nap pairs to five-part stems. Not a shipped CLI command."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path


def load_summem():
    """Load sibling repo-root `summem` via SourceFileLoader (no .py suffix)."""
    script = Path(__file__).resolve().parent / "summem"
    loader = SourceFileLoader("summem", str(script))
    spec = importlib.util.spec_from_loader("summem", loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load summem")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["summem"] = mod
    spec.loader.exec_module(mod)
    return mod


def _four_part_stem(stem: str) -> tuple[str, str, str, int] | None:
    """Return stamp, rand, leafset, grain for a pre-variant nap stem, or None."""
    parts = stem.split("-")
    if len(parts) != 4:
        return None
    stamp, rand, leafset, leaves_s = parts
    if len(stamp) != 16 or len(rand) != 16 or len(leafset) != 64 or not leaves_s.isdigit():
        return None
    if any(c not in "0123456789abcdef" for c in rand + leafset):
        return None
    return stamp, rand, leafset, int(leaves_s)


def _migrate_store(m, parent) -> bool:
    """Rename complete four-part pairs under *parent*. Return True if an incomplete pair was skipped."""
    naps = Path(parent) / ".summem" / "naps"
    if not naps.is_dir():
        return False
    stems: dict[str, dict[str, Path]] = {}
    for path in naps.iterdir():
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix not in (".summ", ".tree"):
            continue
        stems.setdefault(path.stem, {})[path.suffix] = path
    incomplete = False
    for stem, files in stems.items():
        four = _four_part_stem(stem)
        if four is None:
            continue
        stamp, rand, leafset, grain = four
        tree_path = files.get(".tree")
        sum_path = files.get(".summ")
        if tree_path is None or sum_path is None:
            sys.stderr.write(f"incomplete pair: {stem}\n")
            incomplete = True
            continue
        tree_bytes = tree_path.read_bytes()
        caption_bytes = sum_path.read_bytes()
        dest = m.nap_stem(f"{stamp}-{rand}", leafset, grain, tree_bytes, caption_bytes)
        if dest == stem:
            continue
        dest_tree = naps / f"{dest}.tree"
        dest_summ = naps / f"{dest}.summ"
        if dest_tree.exists() or dest_summ.exists():
            continue
        tree_path.replace(dest_tree)
        sum_path.replace(dest_summ)
    return incomplete


def main(argv: list[str] | None = None) -> int:
    """Rewrite complete four-part nap pairs. Return 0 on success, 1 on skip or error."""
    m = load_summem()
    m.require_python()
    args_list = list(argv) if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="migrate.py")
    parser.add_argument("--path", help="limit rewrite to this store")
    try:
        args = parser.parse_args(args_list)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)
    try:
        if args.path:
            parents = [m.resolve_parent(Path.cwd(), args.path)]
        else:
            root = m.find_store_parent(Path.cwd())
            parents = m.started_stores(root)
    except ValueError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    incomplete = False
    for parent in parents:
        incomplete = _migrate_store(m, parent) or incomplete
    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
