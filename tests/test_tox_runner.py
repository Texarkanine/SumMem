"""Tox runner contract: declared CPythons and pytest on tests/."""

from __future__ import annotations

from configparser import ConfigParser

from conftest import ROOT


def _ini(path):
    """Read an INI file without interpolating tox {posargs} braces."""
    parser = ConfigParser(interpolation=None)
    read = parser.read(path)
    assert read, f"missing {path}"
    return parser


def test_tox_env_list_is_non_eol_cpython_from_3_11():
    """tox.ini env_list is exactly py311–py314 (no py310)."""
    env_list = [
        name.strip()
        for name in _ini(ROOT / "tox.ini")["tox"]["env_list"].split(",")
        if name.strip()
    ]
    assert env_list == ["py311", "py312", "py313", "py314"]


def test_tox_skips_packaging_the_project():
    """tox.ini [testenv] package is skip (no hatchling/sdist)."""
    assert _ini(ROOT / "tox.ini")["testenv"]["package"] == "skip"


def test_tox_commands_run_pytest_with_posargs():
    """tox.ini [testenv] commands run pytest and forward {posargs}."""
    commands = _ini(ROOT / "tox.ini")["testenv"]["commands"].split()
    assert commands[0] == "pytest"
    assert "{posargs}" in commands


def test_pytest_collects_from_tests_directory():
    """pytest.ini testpaths is tests."""
    assert _ini(ROOT / "pytest.ini")["pytest"]["testpaths"] == "tests"
