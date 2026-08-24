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

## QA Results

**Result:** PASS

Advisories (do not block):

- `docs/architecture/index.md` Identity still says wake prints a unique prefix of the id. Pack-only, as after tree-schema. The invariant this rework named was updated.
- `projectbrief.md` use-cases still show parenthetical days. The Rework section is the current contract; that history is not product copy.
