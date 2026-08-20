"""Live coverage collection: pytest-cov measures the no-suffix shebang."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

_NARROW = "tests/test_version.py::test_version_prints_script_version"


def _sf_paths(lcov_text: str) -> list[str]:
    return [
        line.removeprefix("SF:").strip()
        for line in lcov_text.splitlines()
        if line.startswith("SF:")
    ]


def _clean_cov_env(tmp_path: Path) -> dict[str, str]:
    """Drop parent coverage/pytest-cov state so a nested --cov cannot share files."""
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("COV_") or key.startswith("COVERAGE_"):
            del env[key]
    env.pop("PYTEST_ADDOPTS", None)
    env["COVERAGE_FILE"] = str(tmp_path / ".coverage")
    return env


def test_cov_summem_emits_lcov_with_summem_sf(tmp_path):
    """pytest --cov=summem writes lcov whose SF includes summem, not tests-only."""
    dest = tmp_path / "lcov.info"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            _NARROW,
            "--cov=summem",
            f"--cov-report=lcov:{dest}",
        ],
        cwd=ROOT,
        env=_clean_cov_env(tmp_path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert dest.is_file(), f"missing {dest}"
    sf = _sf_paths(dest.read_text(encoding="utf-8"))
    assert sf, "lcov has no SF: entries"
    assert any(Path(p).name == "summem" for p in sf), sf
    assert not all("tests/" in p.replace("\\", "/") for p in sf), sf


def test_default_pytest_does_not_write_lcov(tmp_path):
    """A narrow pytest without --cov does not write coverage/lcov.info."""
    watched = ROOT / "coverage" / "lcov.info"
    existed = watched.exists()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", _NARROW],
        cwd=ROOT,
        env=_clean_cov_env(tmp_path),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (tmp_path / "lcov.info").exists()
    if not existed:
        assert not watched.exists()
