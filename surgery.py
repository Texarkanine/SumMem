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

"""Emergency zipper excision of one raw SumMem note. Not a shipped CLI command."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path

__version__ = "0.7.0"  # x-release-please-version


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


def _collect_notes(m, parent) -> list[tuple[str, str]]:
    """Return unique ``(filename, text)`` pairs for loose and nested notes."""
    found: dict[str, str] = {}
    for node in m.list_view(parent):
        if node.kind == "note":
            found.setdefault(node.name, node.caption)
            continue
        if node.kind != "nap" or node.tree_path is None or not node.tree_path.is_file():
            continue
        try:
            tree = m.loads_tree(node.tree_path.read_bytes())
        except m._TREE_PARSE_ERRORS:
            continue
        for child in m._note_children(tree):
            found.setdefault(child.name, child.text)
    return list(found.items())


def locate_note(m, parent, *, contains: str | None = None, name: str | None = None) -> str:
    """Return the filename of the unique target note.

    *contains* matches ``NoteChild.text`` / loose note text only, never nap
    captions. *name* is a filename or unique prefix of one. Raise
    ``ValueError`` when the target is missing, ambiguous, or a nap.
    """
    notes = _collect_notes(m, parent)
    if name:
        exact = [(note_name, text) for note_name, text in notes if note_name == name]
        hits = exact if len(exact) == 1 else [
            (note_name, text) for note_name, text in notes if note_name.startswith(name)
        ]
        if len(hits) != 1:
            raise ValueError("unknown note" if not hits else "ambiguous note")
        note_name, text = hits[0]
        if contains and contains not in text:
            raise ValueError("unknown note")
        return note_name
    if contains:
        hits = [(note_name, text) for note_name, text in notes if contains in text]
        if not hits:
            raise ValueError("unknown note")
        if len(hits) > 1:
            raise ValueError("ambiguous note")
        return hits[0][0]
    raise ValueError("unknown note")


def _tree_has_note(m, tree, note_name: str) -> bool:
    """Return True if *tree* (nested) contains a NoteChild named *note_name*."""
    return any(child.name == note_name for child in m._note_children(tree))


def _naps_containing(m, parent, note_name: str):
    """Return view naps whose trees embed *note_name*, in ``list_view`` order."""
    hits = []
    for node in m.list_view(parent):
        if node.kind != "nap" or node.tree_path is None or not node.tree_path.is_file():
            continue
        try:
            tree = m.loads_tree(node.tree_path.read_bytes())
        except m._TREE_PARSE_ERRORS:
            continue
        if _tree_has_note(m, tree, note_name):
            hits.append(node)
    return hits


def plan_break_out(m, parent, note_name: str) -> list[str]:
    """Return nap stems to split, in ``list_view`` filename order, until *note_name* is loose."""
    view: list[tuple[str, str, object | None]] = []
    seen: set[str] = set()
    for node in m.list_view(parent):
        if node.kind == "note":
            view.append(("note", node.name, None))
            seen.add(node.name)
            continue
        if node.kind != "nap" or node.tree_path is None or not node.tree_path.is_file():
            continue
        try:
            tree = m.loads_tree(node.tree_path.read_bytes())
        except m._TREE_PARSE_ERRORS:
            continue
        view.append(("nap", node.name, tree))
        seen.add(node.name)
    chain: list[str] = []
    while True:
        containing = [
            item for item in view if item[0] == "nap" and item[2] is not None and _tree_has_note(m, item[2], note_name)
        ]
        if not containing:
            break
        containing.sort(key=lambda item: item[1])
        _kind, nap_name, tree = containing[0]
        chain.append(nap_name)
        view = [item for item in view if item[1] != nap_name]
        seen.discard(nap_name)
        for kid in tree.kids:
            if isinstance(kid, m.NoteChild):
                kid_name = kid.name
                kid_row = ("note", kid_name, None)
            else:
                kid_name, _, _ = m.child_nap_stem(kid)
                kid_row = ("nap", kid_name, kid.tree)
            if kid_name in seen:
                continue
            view.append(kid_row)
            seen.add(kid_name)
        view.sort(key=lambda item: item[1])
    return chain


def excise_note(m, parent, note_name: str, *, dry_run: bool = False) -> list[str]:
    """Break out containing naps, unlink the loose note, then ``heal_view``.

    *dry_run* returns the rematerialize chain including *note_name* and writes
    nothing. Never calls ``write_nap``.
    """
    names = {item for item, _text in _collect_notes(m, parent)}
    if note_name not in names:
        raise ValueError("unknown note")
    chain = plan_break_out(m, parent, note_name)
    result = [*chain, note_name]
    if dry_run:
        return result
    while True:
        hits = _naps_containing(m, parent, note_name)
        if not hits:
            break
        node = hits[0]
        child, _digests = m._as_child(node)
        for kid in child.tree.kids:
            m.rematerialize_child(parent, kid)
        m._unlink_node(node)
    loose = next((node for node in m.list_view(parent) if node.kind == "note" and node.name == note_name), None)
    if loose is None:
        raise ValueError("unknown note")
    m._unlink_node(loose)
    m.heal_view(parent)
    return result


def _usage() -> str:
    return """\
Emergency zipper excision of one raw SumMem note. Not a shipped command.

  surgery.py version
  surgery.py [--path PATH] [--dry-run] --contains TEXT
  surgery.py [--path PATH] [--dry-run] NAME

NAME is a notes/ filename or unique prefix. --contains matches note text only.
If both are given, NAME selects the file and TEXT must appear in it.
version prints this script's version (lockstep with summem; not enforced).
"""


def main(argv: list[str] | None = None) -> int:
    """Run emergency surgery. Return 0 on success, 2 on usage, 1 on validation."""
    m = load_summem()
    m.require_python()
    args_list = list(argv) if argv is not None else sys.argv[1:]
    if args_list[:1] == ["version"]:
        if args_list[1:]:
            sys.stderr.write(_usage())
            return 2
        sys.stdout.write(f"{__version__}\n")
        return 0
    parser = argparse.ArgumentParser(prog="surgery.py")
    parser.add_argument("--path", help="aim at this file or directory")
    parser.add_argument("--contains", help="unique substring of the note text")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the rematerialize chain and write nothing",
    )
    parser.add_argument("name", nargs="?", help="note filename or unique prefix")
    try:
        args = parser.parse_args(args_list)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)
    if not args.contains and not args.name:
        sys.stderr.write(_usage())
        return 2
    try:
        parent = m.resolve_parent(Path.cwd(), args.path)
    except ValueError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    try:
        note_name = locate_note(m, parent, contains=args.contains, name=args.name)

        def mutate():
            return excise_note(m, parent, note_name, dry_run=args.dry_run)

        if args.dry_run:
            chain = mutate()
        else:
            chain = m.with_store_lock(parent, mutate)
    except ValueError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    sys.stdout.write("".join(f"{item}\n" for item in chain))
    if not args.dry_run:
        nap = m.fold_request(parent, m.knobs(parent)["WAKE_LINES"])
        if nap:
            sys.stdout.write("\n" + nap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
