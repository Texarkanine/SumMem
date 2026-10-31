# Active Context

## Current Task: fold-grain-as-child
**Phase:** BUILD - COMPLETE

## What Was Done
- Fold grain is the digest count from `_as_child`, or 0 when that call raises `ValueError`.
- A hand-edited parsing tree is no longer requested at its filename grain. Wake still lists that filename grain.
- `tox -e py311`: 421 passed.

## Next Step
- Level 1 QA.
