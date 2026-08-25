# Task: slobac-audit-ratchet

Rework: pin `test_zoom_expanded_child_id` so zoom cannot ignore `child.id`.

## What broke

The nap-branch oracle `any(b{i} in out or eight-b-{i} in out)` stayed green on this fixture's `wake_text` and on `x2 00b0aaaa: eight-a-0` (`b0` in the hex).

## Why

The first non-file frontier child is the `eight-b-4` nap. Its zoom is two public wake lines, not "any token from the right 8-pack."

## What changed

`tests/test_wake_expand.py` — `test_zoom_expanded_child_id` now asserts

- `child.kind == "nap"`
- `out.splitlines() == [f"x5 {short_id}: eight-b-3", dated_leaf(..., "b5")]`

from `child.tree.kids` plus `named_ids` / `short_id` / `dated_leaf`. No product change.

## Files

- `tests/test_wake_expand.py`
