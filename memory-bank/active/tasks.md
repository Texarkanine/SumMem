# Current Task: dated-leaf-wake

**Complexity:** Level 1

## Fix

Parentheses on leaf wake lines were a human “not an id” marker. Agents get one grammar: `xN TOKEN: body`. Drop the parens.

- `format_wake_line` / `dated_leaf` now emit `x1 YYYY-MM-DD: text`
- Prompt and briefing name the same shape
- `tox` 272 passed py311–py314

## Files

- `summem`
- `tests/conftest.py`
- `tests/test_wake.py` (docstrings)
- `docs/agents-prompt.md`
- `AGENTS.md`
- `memory-bank/systemPatterns.md`
- `docs/architecture/index.md`
