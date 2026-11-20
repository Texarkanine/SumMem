# Task: multi-store-filing rework 4

* Complexity: Level 1

## Fix

- **Stale note:** deleted `.summem/notes/20261119T200011Z-420729d37491f5ab` (written on this branch; described `--root`). A newer note already records `--path`.
- **PowerShell:** `_root_path` double-quotes each typographic single quote (U+2018 to U+201B) outside the single-quoted run, so PowerShell can't read it as a closing quote. POSIX splitting is unchanged. Test: `test_printed_path_quoting_is_posix_and_powershell_safe`.
- **Docs (`commands.md`):** run the `Run:` line from the repository root (the script path is relative); nested repositories stay in their own repository, with no special code (operator ruling).
- **Verify:** `tox run-parallel` OK on py311–py314; `properdocs build --strict` clean.
