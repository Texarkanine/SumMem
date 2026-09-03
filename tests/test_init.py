"""CLI: init prints the baked agent prompt."""

from __future__ import annotations

from pathlib import Path

from conftest import ROOT


def test_init_prints_recipe_and_prompt(capsys, summem):
    """main(['init']) exits 0 and prints the insert recipe plus prompt_text()."""
    m = summem
    prompt = m.prompt_text()
    assert m.main(["init"]) == 0
    out = capsys.readouterr().out
    assert "AGENTS.md" in out
    assert "docs/agents-prompt.md" not in out
    assert prompt
    assert prompt in out
    recipe = out.split(prompt, 1)[0]
    assert "starting write rule" in recipe.lower()
    assert "you may edit" in recipe.lower()
    assert "command syntax" in recipe.lower()
    assert "you may edit" not in prompt.lower()
    assert "---" in recipe
    assert "---" not in prompt
    assert recipe.rstrip().endswith("---")
    assert "paste" not in out.lower()
    assert "AGENTS.md or CLAUDE.md" not in out


def test_usage_init_line_does_not_say_paste(summem):
    """usage_text() init catalog line does not tell the operator to paste."""
    m = summem
    lines = [
        ln
        for ln in m.usage_text().splitlines()
        if f"{m.CLI_NAME} init" in ln
    ]
    assert lines
    assert "paste" not in lines[0].lower()


def test_init_outside_repository_writes_nothing(tmp_path, monkeypatch, capsys, summem):
    """init outside a repository exits 0 and creates neither a store nor AGENTS.md."""
    m = summem
    monkeypatch.chdir(tmp_path)
    assert m.main(["init"]) == 0
    capsys.readouterr()
    assert not (tmp_path / ".summem").exists()
    assert not (tmp_path / "AGENTS.md").exists()


def test_init_rejects_extra_args(summem):
    """init with an extra token exits nonzero."""
    m = summem
    assert m.main(["init", "x"]) != 0


def test_init_rejects_path_flag(capsys, summem):
    """init --path is rejected; init -h does not list --path."""
    m = summem
    assert m.main(["init", "--path", "."]) != 0
    capsys.readouterr()
    assert m.main(["init", "-h"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert "--path" not in text


def test_help_before_init_prints_init_help(capsys, summem):
    """-h init prints init help, not top-level-only usage."""
    m = summem
    catalog = m.usage_text()
    assert m.main(["-h", "init"]) == 0
    captured = capsys.readouterr()
    text = captured.out + captured.err
    assert captured.out
    assert "{wake,note" not in text
    assert catalog.strip() not in text


def test_how_to_text_notes_are_part_of_the_work(summem):
    """how_to_text() treats script-written files as part of your work, not a separate git procedure."""
    m = summem
    text = m.how_to_text()
    lower = text.lower()
    assert "part of your work" in lower
    assert "untracked" in lower
    assert "git add" not in text
    assert "git" not in lower
    assert "own commit" not in lower
    assert "the tool manages them" not in text
    assert "invent filenames" in lower
    assert "rewrite" in lower
    assert "the only writer" in lower
    assert "notes/" not in text
    assert "naps/" not in text


def test_agents_md_starts_with_prompt_text(summem):
    """This repo's AGENTS.md prefix is prompt_text(); consumers may edit theirs.

    A prompt_text() change that is not copied onto AGENTS.md must fail. Tweaking
    the write rule and updating both files must not.
    """
    m = summem
    agents = Path(ROOT, "AGENTS.md").read_text(encoding="utf-8")
    prompt = m.prompt_text().strip()
    assert agents.startswith(prompt)


def test_how_to_text_is_the_usage_section(summem):
    """how_to_text() is the root-wake Usage section: header, taught verbs, no runbook."""
    m = summem
    text = m.how_to_text()
    lower = text.lower()
    assert text.startswith("== SumMem Usage ==")
    assert text.endswith("\n")
    assert m.AGENT_BIN in text
    assert "note" in lower
    assert "already stored" in lower
    assert "do not retry" in lower
    assert f'{m.AGENT_BIN} note' in text
    assert "invent filenames" in lower
    assert "the only writer" in lower
    assert "part of your work" in lower
    assert "work on this repository" not in lower
    assert "personal" not in lower
    assert "pr opened" not in lower
    assert "skip if nothing qualifies" not in lower
    assert "already remembered" not in lower
    assert "x1 YYYY-MM-DD" in text
    assert "zoom" in lower
    assert "zoom target" in lower
    assert "recall" in lower
    assert "wake --path" not in text
    assert "catalog" not in lower
    assert "git" not in lower
    assert "notes/" not in text
    assert "naps/" not in text
    assert "Run:" not in text
    assert "must still be true after a fresh clone" not in text
    assert "== Project-root Memories ==" not in text
    assert "== Additional SumMem Catalogs ==" not in text
    assert "wake --path pkg" not in text


def test_how_to_text_is_not_operator_help(summem):
    """how_to_text() is not usage_text(); agent bin vs operator catalog name."""
    m = summem
    how_to = m.how_to_text()
    usage = m.usage_text()
    assert how_to != usage
    assert ".summem/summem" in how_to
    assert "summem" in usage
    assert ".summem/summem" not in usage


def test_prompt_and_how_to_are_disjoint(summem):
    """Usage does not restate the write rule; the prefix does not teach recipes."""
    m = summem
    prompt = m.prompt_text()
    how_to = m.how_to_text().lower()
    lower = prompt.lower()
    for phrase in (
        "work on this repository",
        "personal",
        "pr opened",
        "skip if nothing qualifies",
        "already remembered",
    ):
        assert phrase not in how_to
    for phrase in (
        "invent filenames",
        "the only writer",
        "part of your work",
        "x1 yyyy-mm-dd",
    ):
        assert phrase in how_to
        assert phrase not in lower
    assert "wake --path" not in how_to
    assert "wake --path" not in lower
    assert "catalog" not in how_to
    assert f"{m.AGENT_BIN} note" not in prompt
    assert f"{m.AGENT_BIN} nap" not in prompt
    assert "== SumMem Usage ==" not in prompt


def test_how_to_text_catalog_is_opt_in(summem):
    """Default Usage omits catalog how-to; catalog=True appends the pull recipe."""
    m = summem
    base = m.how_to_text()
    cataloged = m.how_to_text(catalog=True)
    assert "catalog" not in base.lower()
    assert "wake --path" not in base
    assert "Listed catalog lines" in cataloged
    assert f"{m.AGENT_BIN} wake --path <path>" in cataloged
    assert cataloged.startswith(base)
    assert "had no catalog" not in cataloged
