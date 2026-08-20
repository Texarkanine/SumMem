# Current Task: empty-root-header

**Complexity:** Level 1

## Fix

- **Broke:** Root wake with a catalog always printed `== Project-root memories ==`. Empty `wake_text` left the closer under that header like a memory.
- **Why:** `if cat:` concatenated the header unconditionally.
- **Changed:** Print the memories header only when `cat` and `doc` are both non-empty. Empty extra-store list still omits both headers. Pull wakes unchanged. Catalog heading is `== Additional SumMem Catalogs ==`. Config comment is settings/values; briefing and VISION match. `knobs()` unchanged.
- **Files:** `summem`, `tests/test_scopes.py`, `tests/test_proof_scopes.py`, `VISION.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`, `AGENTS.md`

## QA Result

- **Status:** PASS. 207 tests pass on Python 3.11.
- **Filter:** Operator ruled `VISION.md` and `ROADMAP.md` directional, not gospel. Lockstep findings against those two files do not block.
- **Verified:** Empty root omits the memories header; catalog and closer still print. Catalog heading consistent in code and tests. Settings wording lockstepped into `systemPatterns.md` and `techContext.md`; `knobs()` unchanged. `AGENTS.md` matches `prompt_text()`.
- **Advisories:** The wake branch nests three cases where two suffice. The two wake headers disagree on capitalization. `VISION.md` and `ROADMAP.md` still say "knobs" (discarded by the filter).
