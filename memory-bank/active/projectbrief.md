# Project Brief

## User Story

As an agent using SumMem, I want `recall` to match nested nap captions that have left the view, and I want `zoom`/`recall` to tell me when they skip an unreadable sibling pack, so a folded caption is still findable and a corrupt `.tree` in the same store is not invisible.

## Use-Case(s)

### Use-Case 1 — nested caption recall

As described in [SumMem#8](https://github.com/Texarkanine/SumMem/issues/8): after a nap is itself folded, its caption (`NapChild.sum`) lives only in the parent children file. Everyday recall searches the view; deep recall already reads original note sentences from children files. `recall` of that inner caption text currently misses it because `_note_children` yields only `NoteChild` rows.

### Use-Case 2 — sibling pack warning

As described in [SumMem#7](https://github.com/Texarkanine/SumMem/issues/7): `zoom_text` and `recall_text` catch `_TREE_PARSE_ERRORS` and raise `unreadable pack` only for the pack the agent asked for. A sibling pack in the same view is `continue`d with no message. The command can succeed while a corrupt children file in the same store stays invisible.

## Requirements

1. `recall_text` matches nested nap captions as well as loose-note / view captions and original note sentences ([#8](https://github.com/Texarkanine/SumMem/issues/8)).
2. Recall output still omits store paths and git.
3. When zoom or recall skips a sibling pack because the children file is unreadable, print one agent-safe line on stderr (no paths, no traceback), e.g. that a pack was skipped ([#7](https://github.com/Texarkanine/SumMem/issues/7)).
4. Do not fail zoom or recall if another pack still answered.

## Constraints

1. Do not change wake listing. Wake stays wait-free and silent on degrade.
2. Do not search payloads that are not captions or original notes.
3. Do not invent a lock. No Windows-specific IO.
4. Do not change note/nap identity, `ensure_store`, or place the driver.
5. Agent CLI: no store paths, hashes-as-paths, or git in user-facing output.
6. Do not edit tox/pytest runner files, README Developing, or techContext Testing Process.
7. Do not recreate VISION/ROADMAP. Living contract is README, `docs/architecture/index.md`, `docs/notes.md`, persistent `memory-bank/`.
8. Do not expand into sqlite, hooks, `cover(T)`, or leftover `docs/notes.md` items.
9. TDD for executable behavior. Tests: `uv run --python 3.11 --with pytest pytest`.

## Acceptance Criteria

1. A nested nap caption that has left the view is found by `recall` of that caption text.
2. Existing recall of view captions and original note sentences still works.
3. Recall stdout still omits `notes/`, `naps/`, and git.
4. Zoom of a nested id still succeeds when another view nap has an unreadable children file, and stderr has one agent-safe skip line (no paths, no traceback).
5. Recall that still matches another pack after skipping an unreadable sibling children file succeeds, with the same style of stderr line.
6. Zoom of the asked-for pack that is itself unreadable still raises/exits `unreadable pack` (existing behavior).
7. Wake is unchanged (no new warning).
