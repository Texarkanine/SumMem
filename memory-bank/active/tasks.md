# Task: multi-store-filing rework 5

* Complexity: Level 1

## Fix

- **Change:** `_input_path` takes the root from `$PWD` and refuses any target whose own repository differs (outside it, or a nested repository) with ``not in this repository: `<arg>` ``. That one check replaces the `:/..` check and `start`'s own check. A symlinked store reports ``store is not in this repository: `<parent>` ``, formatting the parent so the symlink is never resolved.
- **Tests:** a nested repository is refused from the outer repository (both `:/` and relative forms, plus `start`) and works from inside it; existing refusal assertions now expect the new message.
- **Docs:** `commands.md` bullet, troubleshooting rows, `architecture/store.md`, `systemPatterns.md`.
- **Verify:** `tox run-parallel` py311–py314 OK (467 tests); `properdocs build --strict` clean.
