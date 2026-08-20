"""CLI: init prints the baked agent prompt."""

from __future__ import annotations

from pathlib import Path

from conftest import ROOT, load_summem


def test_init_prints_paste_recipe_and_prompt(capsys):
    """main(['init']) exits 0 and prints the paste recipe plus prompt_text()."""
    m = load_summem()
    prompt = m.prompt_text()
    assert m.main(["init"]) == 0
    out = capsys.readouterr().out
    assert "AGENTS.md" in out
    assert prompt
    assert prompt in out
    assert "AGENTS.md or CLAUDE.md" not in out


def test_init_outside_repository_writes_nothing(tmp_path, monkeypatch, capsys):
    """init outside a repository exits 0 and creates neither a store nor AGENTS.md."""
    m = load_summem()
    monkeypatch.chdir(tmp_path)
    assert m.main(["init"]) == 0
    capsys.readouterr()
    assert not (tmp_path / ".summem").exists()
    assert not (tmp_path / "AGENTS.md").exists()


def test_init_rejects_extra_args():
    """init with an extra token exits nonzero."""
    m = load_summem()
    assert m.main(["init", "x"]) != 0


def test_init_rejects_path_flag(capsys):
    """init --path is rejected; init -h does not list --path."""
    m = load_summem()
    assert m.main(["init", "--path", "."]) != 0
    capsys.readouterr()
    assert m.main(["init", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" not in text


def test_help_before_init_prints_init_help(capsys):
    """-h init prints init help, not top-level-only usage."""
    m = load_summem()
    catalog = m.usage_text()
    assert m.main(["-h", "init"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert captured.out
    assert "{wake,note" not in text
    assert catalog.strip() not in text


def test_prompt_text_invariants():
    """prompt_text() names .summem/summem and wake rules; omits forbidden strings."""
    m = load_summem()
    prompt = m.prompt_text()
    lower = prompt.lower()
    assert "summem" in lower
    assert "wake" in lower
    assert "root" in lower
    assert "conversation" in lower
    assert "contributor" in lower
    assert "personal" in lower
    assert "before any other tool call" not in lower
    assert ".summem/summem" in prompt
    assert "AGENTS.md or CLAUDE.md" not in prompt
    assert "./summem/summem" not in prompt


def test_agents_md_starts_with_prompt_text():
    """This repo's AGENTS.md starts with prompt_text() so the paste does not drift."""
    m = load_summem()
    agents = Path(ROOT, "AGENTS.md").read_text(encoding="utf-8")
    prompt = m.prompt_text().strip()
    assert agents.startswith(prompt)
