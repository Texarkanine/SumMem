# Active Context

## Current Task: fold-grain-as-child
**Phase:** BUILD - IN-PROGRESS

## What Was Done
- Operator decided the fork: `write_nap` treats grain as the digest count. Remove `left.leaves != right.leaves`. `len(digs_l) != len(digs_r)` is the same-grain check.
- A stem whose filename grain disagrees with its digest count stays eligible when that count is a power of two, and it may fold with a truthful row of that count.
- Wake still lists `node.leaves`. The OSError advisory stays outside this issue.

## Next Step
- Failing test for that pair, then the `write_nap` change.
