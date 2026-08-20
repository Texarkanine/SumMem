# Current Task: empty-root-header

**Complexity:** Level 1

## Fix

- **Broke:** Root wake with a catalog always printed `== Project-root memories ==`. Empty `wake_text` left the closer under that header like a memory.
- **Why:** `if cat:` concatenated the header unconditionally.
- **Changed:** Print the memories header only when `cat` and `doc` are both non-empty. Empty extra-store list still omits both headers. Pull wakes unchanged.
- **Files:** `summem`, `tests/test_scopes.py`, `VISION.md`
