"""Git helpers for store and proof tests."""

from __future__ import annotations

import subprocess
from pathlib import Path


def init_repo(path: Path) -> Path:
    """Create a git repo at *path* with a local author and an empty commit."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "SumMem Test"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "summem@test.invalid"], cwd=path, check=True)
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "init"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    return path
