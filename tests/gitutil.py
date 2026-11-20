"""Git helpers for store and proof tests."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from importlib.machinery import SourceFileLoader
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "summem"
UTC = timezone.utc


def _load_driver():
    """Load repo-root summem without importing conftest."""
    name = "summem_gitutil"
    existing = sys.modules.get(name)
    if existing is not None:
        return existing
    loader = SourceFileLoader(name, str(SCRIPT))
    spec = importlib.util.spec_from_loader(name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load summem")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _find_nap_child(m, tree, cid: str):
    """Return the NapChild named *cid* under *tree*, or None."""
    for child in tree.kids:
        if isinstance(child, m.NoteChild):
            continue
        if child.id == cid:
            return child
        found = _find_nap_child(m, child.tree, cid)
        if found is not None:
            return found
    return None


def _tree_for_id(m, parent, cid: str):
    """Return the children tree of *cid* (view nap or nested NapChild), or None."""
    errors = m._TREE_PARSE_ERRORS
    for node in m.list_view(parent):
        if node.kind != "nap" or node.tree_path is None or not node.tree_path.is_file():
            continue
        try:
            loaded = m.loads_tree(node.tree_path.read_bytes())
        except errors:
            continue
        if node.id == cid:
            return loaded
        found = _find_nap_child(m, loaded, cid)
        if found is not None:
            return found.tree
    return None


def _nap_child_ids(m, parent, cid: str) -> list[str]:
    """Return direct NapChild ids of one zoom level for *cid*, or empty."""
    tree = _tree_for_id(m, parent, cid)
    if tree is None:
        return []
    return [child.id for child in tree.kids if isinstance(child, m.NapChild)]


def init_repo(path: Path) -> Path:
    """Create a git repo at *path* with a local author and an empty commit."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "SumMem Test"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "summem@test.invalid"], cwd=path, check=True)
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "init"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    return path


def git(args, cwd, check=True):
    """Run git in *cwd*. Raise AssertionError on failure when *check* is true."""
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            result.stderr.decode("utf-8", "replace") or result.stdout.decode("utf-8", "replace")
        )
    return result


def fold_ids(m, repo, ids, caption: str) -> str:
    """Balanced pairwise fold of *ids* until one nap id remains.

    *ids* must be a power-of-two count. Each level naps disjoint pairs, so
    every pack written has a power-of-two grain.
    """
    remaining = list(ids)
    count = len(remaining)
    if count < 2 or count & (count - 1) != 0:
        raise ValueError(f"fold_ids needs a power-of-two id count, got {count}")
    step = 0
    while len(remaining) > 1:
        nxt = []
        for i in range(0, len(remaining), 2):
            before = {node.id for node in m.list_view(repo)}
            m.write_nap(repo, remaining[i], remaining[i + 1], f"{caption}-{step}")
            after = [node.id for node in m.list_view(repo)]
            created = [cid for cid in after if cid not in before]
            if len(created) != 1:
                raise AssertionError(f"fold_ids expected one new nap, got {created}")
            nxt.append(created[0])
            step += 1
        remaining = nxt
    return remaining[0]


_FOLD_RUN = re.compile(r" nap --path (?:'[^']*'|\S+) (\S+) (\S+) " '"')


def break_children(node, how: str) -> None:
    """Remove or corrupt a nap row's children file.

    ``missing`` unlinks it. Any other *how* writes ``not a tree``.
    """
    if how == "missing":
        node.tree_path.unlink()
    else:
        node.tree_path.write_bytes(b"not a tree\n")


def plant_pack(m, repo, left, right, caption: str) -> None:
    """Write a nap of two view rows with no pairing policy.

    This builds a shape a legacy store can already hold. It does not apply
    the nap pair rule, and it unlinks both rows.
    """
    child_l, digs_l = m._as_child(left)
    child_r, digs_r = m._as_child(right)
    tree_bytes = m.dumps_tree(m.Tree(kids=[child_l, child_r]))
    caption_bytes = m.note_file_bytes(caption)
    digests = digs_l + digs_r
    stem = m.nap_stem(m._seq_prefix(left.name), m.leafset_id(digests), len(digests), tree_bytes, caption_bytes)
    m._write_pair(m.ensure_store(repo) / "naps", stem, tree_bytes, caption_bytes)
    m._unlink_node(left)
    m._unlink_node(right)


def obey_folds(m, repo, budget: int, cap: int = 500):
    """Heal, then nap every requested pair until fold asks for nothing.

    Every pack this writes has a power-of-two grain. Return the view.
    """
    for step in range(cap):
        view = m.heal_view(repo)
        out = m.fold_request(repo, budget, nodes=view)
        if not out:
            return view
        match = _FOLD_RUN.search(out)
        if match is None:
            raise AssertionError(f"fold request had no Run line: {out!r}")
        id_a, id_b = match.groups()
        ids = [node.id for node in view]
        written = m.write_nap(repo, m.resolve_id(id_a, ids), m.resolve_id(id_b, ids), f"fold {step}", nodes=view)
        grain = m._parse_nap_stem(written.stem)[3]
        grains = [node.leaves for node in view]
        assert grain & (grain - 1) == 0, f"fold wrote a {grain}-pack; grains {grains}"
    raise AssertionError("fold requests did not finish")


def zoom_reaches(cwd: Path, start_id: str, sentence: str, bound: int = 200) -> None:
    """Repeatedly zoom from *start_id* until *sentence* appears, or fail."""
    m = _load_driver()
    pending = [start_id]
    seen = 0
    while pending:
        cid = pending.pop(0)
        seen += 1
        if seen > bound:
            raise AssertionError(f"zoom bound exceeded looking for {sentence!r}")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "zoom", "--path", ".", cid],
            cwd=cwd,
            capture_output=True,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr.decode("utf-8", "replace"))
        out = result.stdout.decode("utf-8")
        if sentence in out:
            return
        pending.extend(_nap_child_ids(m, cwd, cid))
    raise AssertionError(f"did not reach {sentence!r}")


def assert_unique_cover(m, repo) -> None:
    """Fail unless every pair of view nodes has disjoint leaf-sets, including two notes."""
    nodes = m.list_view(repo)
    rows = [(n, m.leaf_digests(n)) for n in nodes]
    for i, (a, sa) in enumerate(rows):
        for b, sb in rows[i + 1 :]:
            if sa is None or sb is None:
                continue
            assert sa.isdisjoint(sb), (a.name, b.name, sa & sb)


def reaches(m, repo, sentence: str) -> bool:
    """Return True if in-process zoom from any view id can reach *sentence*."""
    pending = [n.id for n in m.list_view(repo)]
    seen: set[str] = set()
    while pending:
        cid = pending.pop()
        if cid in seen:
            continue
        seen.add(cid)
        try:
            out = m.zoom_text(repo, cid)
        except ValueError:
            continue
        if sentence in out:
            return True
        pending.extend(_nap_child_ids(m, repo, cid))
    return False


COMMAND_ONLY = ("tomllib", "fcntl", "subprocess", "dataclasses", "argparse")

_IMPORT_PROBE = r"""
import builtins
import importlib.util
import json
import sys
from importlib.machinery import SourceFileLoader

watched = ("tomllib", "fcntl", "subprocess", "dataclasses", "argparse")
from_driver = {name: False for name in watched}
real_import = builtins.__import__

def tracked(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".", 1)[0]
    if root in from_driver and globals and globals.get("__name__") == "summem_probe":
        from_driver[root] = True
    return real_import(name, globals, locals, fromlist, level)

builtins.__import__ = tracked
path, *cmd = sys.argv[1:]
loader = SourceFileLoader("summem_probe", path)
spec = importlib.util.spec_from_loader("summem_probe", loader)
mod = importlib.util.module_from_spec(spec)
sys.modules["summem_probe"] = mod
spec.loader.exec_module(mod)
code = mod.main(cmd)
sys.stdout.write("\n")
sys.stdout.write(json.dumps(from_driver))
raise SystemExit(0 if code is None else code)
"""


def fresh_imported(cmd: list[str]) -> tuple[int, dict[str, bool]]:
    """Run *cmd* in a new interpreter and report modules the driver itself imported.

    3.14's pathlib imports fcntl, so sys.modules is the wrong oracle.
    """
    result = subprocess.run(
        [sys.executable, "-c", _IMPORT_PROBE, str(SCRIPT), *cmd],
        capture_output=True,
        text=True,
    )
    payload = result.stdout.splitlines()[-1] if result.stdout.splitlines() else ""
    imported = json.loads(payload)
    return result.returncode, imported


def write_notes(m, repo, texts, start: int = 1) -> list[Path]:
    """Write *texts* as deterministic sequential notes beginning at second *start*."""
    paths = []
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i, text in enumerate(texts):
        paths.append(
            m.write_note(repo, text, base + timedelta(seconds=start + i), Random(start + i))
        )
    return paths


def payload_names(repo: Path) -> set[str]:
    """Return non-hidden filenames across notes/ and naps/ in *repo*'s root store."""
    names: set[str] = set()
    for folder in ("notes", "naps"):
        root = repo / ".summem" / folder
        if not root.is_dir():
            continue
        names.update(p.name for p in root.iterdir() if p.is_file() and not p.name.startswith("."))
    return names


def plant_nap(m, repo, kids, caption: str):
    """Materialize a NapChild built from *kids* and *caption* into *repo*."""
    tree = m.Tree(kids=list(kids))
    digests = m._digests_of_tree(tree)
    child = m.NapChild(id=m.leafset_id(digests), sum=caption, tree=tree)
    m.rematerialize_child(repo, child)
    return child


def balanced_4(m, repo, texts, cap_ab: str, cap_cd: str, cap_p: str, start: int):
    """Write four notes and fold them into a balanced 4-pack returning the parent ViewNode."""
    paths = write_notes(m, repo, texts, start=start)
    names = {p.name for p in paths}
    nodes = [n for n in m.list_view(repo) if n.name in names]
    m.write_nap(repo, nodes[0].id, nodes[1].id, cap_ab)
    c = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[2])
    d = next(n for n in m.list_view(repo) if n.kind == "note" and n.caption == texts[3])
    m.write_nap(repo, c.id, d.id, cap_cd)
    ab = next(n for n in m.list_view(repo) if n.caption == cap_ab)
    cd = next(n for n in m.list_view(repo) if n.caption == cap_cd)
    m.write_nap(repo, ab.id, cd.id, cap_p)
    return next(n for n in m.list_view(repo) if n.caption == cap_p)


GIT_CONVENTION_KEY = "as in git"


def git_free(text: str) -> bool:
    """True if *text* names git only as the ``as in git`` convention key (productContext CLI rule)."""
    return "git" not in text.lower().replace(GIT_CONVENTION_KEY, "")
