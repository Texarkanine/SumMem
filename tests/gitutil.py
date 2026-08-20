"""Git helpers for store and proof tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "summem"


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
    """Pairwise-fold the oldest two ids in *ids* until one nap id remains."""
    remaining = list(ids)
    step = 0
    while len(remaining) > 1:
        before = {node.id for node in m.list_view(repo)}
        m.write_nap(repo, remaining[0], remaining[1], f"{caption}-{step}")
        after = [node.id for node in m.list_view(repo)]
        created = [cid for cid in after if cid not in before]
        remaining = created + remaining[2:]
        step += 1
    return remaining[0]


def zoom_reaches(cwd: Path, start_id: str, sentence: str, bound: int = 200) -> None:
    """Repeatedly zoom from *start_id* until *sentence* appears, or fail."""
    pending = [start_id]
    seen = 0
    while pending:
        cid = pending.pop(0)
        seen += 1
        if seen > bound:
            raise AssertionError(f"zoom bound exceeded looking for {sentence!r}")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "zoom", cid],
            cwd=cwd,
            capture_output=True,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr.decode("utf-8", "replace"))
        out = result.stdout.decode("utf-8")
        if sentence in out:
            return
        for line in out.splitlines():
            child = line.split()[0]
            if child != cid:
                pending.append(child)
    raise AssertionError(f"did not reach {sentence!r}")


def assert_unique_cover(m, repo) -> None:
    """Fail unless every nap/note pair in the view has disjoint leaf-sets. Two notes may share a digest."""
    nodes = m.list_view(repo)
    rows = [(n, m.leaf_digests(n)) for n in nodes]
    for i, (a, sa) in enumerate(rows):
        for b, sb in rows[i + 1 :]:
            if sa is None or sb is None:
                continue
            if a.kind == "note" and b.kind == "note":
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
        for line in out.splitlines():
            child = line.split()[0]
            if child != cid:
                pending.append(child)
    return False
