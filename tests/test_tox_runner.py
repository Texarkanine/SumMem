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


def test_coverage_env_collects_summem_lcov():
    """[testenv:coverage] uses --cov=summem and writes lcov under COVERAGE_DIR."""
    commands = _ini(ROOT / "tox.ini")["testenv:coverage"]["commands"]
    assert "--cov=summem" in commands
    assert "lcov:{env:COVERAGE_DIR:coverage}/lcov.info" in commands
    assert "{posargs}" in commands


def test_default_tox_commands_have_no_cov():
    """[testenv] commands do not pass --cov; coverage is not in env_list."""
    commands = _ini(ROOT / "tox.ini")["testenv"]["commands"]
    assert "--cov" not in commands
    env_list = [
        name.strip()
        for name in _ini(ROOT / "tox.ini")["tox"]["env_list"].split(",")
        if name.strip()
    ]
    assert "coverage" not in env_list


def test_tox_pytest_does_not_set_basetemp():
    """pytest keeps its default basetemp; an explicit path is a cross-checkout clobber."""
    testenv = _ini(ROOT / "tox.ini")["testenv"]["commands"]
    assert "--basetemp" not in testenv
    coverage = _ini(ROOT / "tox.ini")["testenv:coverage"]["commands"]
    assert "--basetemp" not in coverage


def test_tox_deps_include_pytest_xdist():
    """[testenv] deps includes pytest-xdist."""
    deps = [
        line.strip()
        for line in _ini(ROOT / "tox.ini")["testenv"]["deps"].splitlines()
        if line.strip()
    ]
    assert "pytest-xdist" in deps


def test_tox_commands_enable_xdist():
    """[testenv] commands pass -n auto --maxprocesses=4."""
    commands = _ini(ROOT / "tox.ini")["testenv"]["commands"].split()
    n = commands.index("-n")
    assert commands[n + 1] == "auto"
    assert "--maxprocesses=4" in commands


def test_coverage_env_runs_serial():
    """[testenv:coverage] commands do not pass -n."""
    tokens = _ini(ROOT / "tox.ini")["testenv:coverage"]["commands"].split()
    assert "-n" not in tokens


