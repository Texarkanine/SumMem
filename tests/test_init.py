"""CLI: init prints the baked agent prompt."""

from __future__ import annotations

from gitutil import git_free


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


def test_init_rejects_path_flag(summem):
    """init --path is rejected."""
    assert summem.main(["init", "--path", "."]) != 0


def test_how_to_text_notes_are_part_of_the_work(summem):
    """how_to_text() treats script-written files as part of your work, not a separate git procedure."""
    m = summem
    text = m.how_to_text()
    lower = text.lower()
    assert "part of your work" in lower
    assert "untracked" in lower
    assert "git add" not in text
    assert git_free(lower)
    assert "own commit" not in lower
    assert "the tool manages them" not in text
    assert "invent filenames" in lower
    assert "rewrite" in lower
    assert "the only writer" in lower
    assert "notes/" not in text
    assert "naps/" not in text


def test_how_to_text_is_the_usage_section(monkeypatch, summem):
    """how_to_text() is the root-wake Usage section: header, taught verbs, no runbook."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    text = m.how_to_text()
    lower = text.lower()
    assert text.startswith("== SumMem Usage ==")
    assert text.endswith("\n")
    assert m.AGENT_BIN in text
    assert "note" in lower
    assert "asks for a nap" in lower
    assert "before your next action" in lower
    assert "already stored" not in lower
    assert "do not retry" not in lower
    assert "two older view nodes" not in lower
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
    assert git_free(lower)
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


def test_how_to_text_catalog_is_opt_in(monkeypatch, summem):
    """Default Usage omits catalog how-to; catalog=True appends the pull recipe."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    base = m.how_to_text()
    cataloged = m.how_to_text(catalog=True)
    assert "catalog" not in base.lower()
    assert "wake --path" not in base
    assert "Listed catalog lines" in cataloged
    assert "`N:`" in cataloged
    assert "count" in cataloged
    assert "leaf grain" not in cataloged
    assert "the `./` token" not in cataloged
    assert "not commands" in cataloged
    assert f"{m.AGENT_BIN} wake --path <path>" in cataloged
    assert f"{m.AGENT_BIN} note --path" in cataloged
    assert "walks up" in cataloged
    assert cataloged.startswith(base)
    assert "had no catalog" not in cataloged


def test_agent_invoke_uses_python_on_nt(monkeypatch, summem):
    """When the host cannot exec AGENT_BIN, agent_invoke prefixes python plus AGENT_BIN."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    assert m.agent_invoke() == m.AGENT_BIN
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: True)
    assert m.agent_invoke() == f"python {m.AGENT_BIN}"
    assert m.sys.executable not in m.agent_invoke()


def test_how_to_text_uses_agent_invoke(monkeypatch, summem):
    """On a host that needs an interpreter prefix, Usage recipes use agent_invoke()."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: True)
    invoke = m.agent_invoke()
    text = m.how_to_text()
    assert f"`{invoke} note" in text
    assert f"`{m.AGENT_BIN} note" not in text
    prompt = m.prompt_text()
    assert f"`{m.AGENT_BIN}`" not in prompt
    assert m.sys.executable not in prompt
    assert m.sys.executable not in text


def test_prompt_text_bootstrap_wake_is_python(monkeypatch, summem):
    """prompt_text names SumMem, then python AGENT_BIN wake; no invoke-path intro."""
    m = summem
    for needs in (True, False):
        monkeypatch.setattr(m, "_host_needs_interpreter", lambda n=needs: n)
        prompt = m.prompt_text()
        assert "invoked as" not in prompt
        assert f"`{m.AGENT_BIN}`" not in prompt
        assert f"`python {m.AGENT_BIN} wake`" in prompt
        assert m.sys.executable not in prompt
        assert "only work on Windows" not in prompt


def test_init_text_is_host_agnostic(monkeypatch, capsys, summem):
    """init_text is identical across host invoke modes and matches main(['init'])."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: True)
    windows = m.init_text()
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    posix = m.init_text()
    assert windows == posix
    assert m.sys.executable not in windows
    assert f"`python {m.AGENT_BIN} wake`" in windows
    assert m.main(["init"]) == 0
    assert capsys.readouterr().out == windows


def test_init_text_separates_recipe_from_prompt_at_divider(summem):
    """init_text separates the starting-rule recipe from prompt_text() at ---."""
    m = summem
    recipe, sep, rest = m.init_text().partition("---")
    assert sep == "---"
    assert "starting write rule" in recipe.lower()
    assert rest.lstrip() == m.prompt_text()


def test_how_to_text_always_explains_path_and_root_anchor(monkeypatch, summem):
    """Base how_to_text() always includes --path :/ and --path command forms even without a catalog."""
    m = summem
    monkeypatch.setattr(m, "_host_needs_interpreter", lambda: False)
    base = m.how_to_text()
    assert f"{m.AGENT_BIN} note --path" in base
    assert f"{m.AGENT_BIN} note --path :/" in base
    assert f"{m.AGENT_BIN} recall --path :/" in base
    assert f"{m.AGENT_BIN} zoom --path :/" in base
    assert "walks up" in base
    assert "wake --path" not in base
