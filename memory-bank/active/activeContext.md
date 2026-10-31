# Active Context

## Current Task: fold-grain-as-child
**Phase:** QA - COMPLETE (FAIL)

## What Was Done
- Fold grain is the digest count from `_as_child`, or 0 when that call raises `ValueError`.
- A hand-edited parsing tree is no longer requested at its filename grain. Wake still lists that filename grain.
- `tox -e py311`: 421 passed.

## Next Step
- BLOCKED. Two ways make `fold_request` and `nap` agree, and they are not the same product. Do not pick one here.
    - `write_nap` treats grain as the digest count and drops the filename `leaves` check. A filename-2 row with 4 digests can then fold with a real 4-pack.
    - `_fold_grains` marks a stem whose digest count differs from the filename as ineligible. That row is never requested, including when `nap` would accept two rows that lie the same way.
