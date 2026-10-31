# Active Context

## Current Task: fold-grain-as-child
**Phase:** BUILD - COMPLETE

## What Was Done
- Operator chose digest-count grain for `nap`. `write_nap` no longer compares filename `leaves`. Unequal digest counts are `not the same grain`.
- A filename-2 row with 4 digests is requested with a real 4-pack, and `nap` accepts it. Wake still lists `x2` and `x4`.
- `tox -e py311`: 422 passed.

## Next Step
- Level 1 QA.
