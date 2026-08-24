# Project Brief

## User Story

As an agent using `summem zoom`, I want `named_ids` to treat a children file whose child is not a mapping the same way other tree readers do, so a corrupt sibling pack does not abort the command with an `AttributeError` traceback.

## Use-Case(s)

### Use-Case 1

A view nap's `.tree` is valid JSON but a child in `c` is not a mapping. `zoom` / `recall` of other ids still work. Zoom of that pack is `unreadable pack`, not a traceback.

## Requirements

1. As described in https://github.com/Texarkanine/SumMem/issues/40
2. `named_ids` catches `_TREE_PARSE_ERRORS` (includes `AttributeError`), same as the other tree readers

## Constraints

1. Surgical edit in `named_ids` only; do not reformat `summem`
2. TDD: failing test first
3. Do not recreate VISION.md or ROADMAP.md
4. Do not create `memory-bank/active/milestones.md`

## Acceptance Criteria

1. A tree whose child is not a mapping does not make `named_ids` raise
2. `zoom_text` / `recall_text` still survive that file; `summem zoom` does not abort with a traceback
3. Existing `{not json` skip/unreadable-pack tests still pass
