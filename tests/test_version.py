"""CLI: version prints the in-script release version."""

from __future__ import annotations

import json

from conftest import ROOT, load_summem


def test_version_prints_script_version(capsys):
    """main(['version']) exits 0 and prints __version__ plus a newline."""
    m = load_summem()
    assert m.main(["version"]) == 0
    assert capsys.readouterr().out == f"{m.__version__}\n"


def test_version_outside_repository_writes_nothing(tmp_path, monkeypatch, capsys):
    """version outside a repository exits 0 and creates no store."""
    m = load_summem()
    monkeypatch.chdir(tmp_path)
    assert m.main(["version"]) == 0
    capsys.readouterr()
    assert not (tmp_path / ".summem").exists()


def test_version_rejects_extra_args():
    """version with an extra token exits nonzero."""
    m = load_summem()
    assert m.main(["version", "x"]) != 0


def test_version_rejects_path_flag(capsys):
    """version --path is rejected; version -h does not list --path."""
    m = load_summem()
    assert m.main(["version", "--path", "."]) != 0
    capsys.readouterr()
    assert m.main(["version", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" not in text


def test_help_before_version_prints_version_help(capsys):
    """-h version prints version help, not top-level-only usage."""
    m = load_summem()
    catalog = m.usage_text()
    assert m.main(["-h", "version"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert captured.out
    assert "{wake,note" not in text
    assert catalog.strip() not in text


def test_version_line_has_release_please_marker():
    """Repo-root summem __version__ carries x-release-please-version."""
    text = (ROOT / "summem").read_text(encoding="utf-8")
    version_lines = [
        line for line in text.splitlines() if line.lstrip().startswith("__version__")
    ]
    assert version_lines, "no __version__ assignment in summem"
    assert any("x-release-please-version" in line for line in version_lines)


def test_version_matches_release_please_manifest():
    """summem.__version__ equals the Release Please manifest root version."""
    m = load_summem()
    manifest = json.loads((ROOT / ".release-please-manifest.json").read_text(encoding="utf-8"))
    assert manifest["."] == m.__version__


def test_release_config_generic_extra_file_is_summem():
    """release-please generic extra-files targets repo-root summem."""
    config = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))
    extra_files = config["packages"]["."]["extra-files"]
    generic_paths = {ef.get("path") for ef in extra_files if ef.get("type") == "generic"}
    assert "summem" in generic_paths
    assert ".summem/summem" not in generic_paths

