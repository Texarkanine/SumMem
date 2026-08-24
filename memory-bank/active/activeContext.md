# Active Context

## Current Task: agent-display-unify
**Phase:** PREFLIGHT - COMPLETE (FAIL (fixable))

## What Was Done
- Level 2 plan: zoom and recall print `format_wake_line` (leaves dated, packs `short_id` among `named_ids`); recall matches caption/text only; prompt membership sentence loses the eternal-currency reading.
- 64-hex is on-disk identity. Agent stdout uses unique prefixes; longest print is only what `short_id` needs.
- Preflight judged the plan FAIL (fixable): TDD order and conventions hold; `tests/gitutil.py` plus leftover `{id}  text` zoom/nap assertions are not in the plan.

## Next Step
- Re-plan: retarget `reaches` / `zoom_reaches` and remaining `{id}  text` zoom/nap tests, then spawn `/niko-preflight` again.
