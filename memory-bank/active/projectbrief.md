# Project Brief

## User Story

As an agent that compacted on two long-lived branches, I want the next `note` or `nap` after those branches merge to zipper overlapping nap packs into a cover of unique leaves, so that shared prefix notes are not duplicated in a parent `.tree` and zoom still reaches every original.

## Use-Case(s)

### Prefix overlap after a D-vs-E fork

Main napped `{A,B,C,D}` while a feature napped `{A,B,C,E,…}`. Git merge adds both files. The next mutating command zippers the smaller pack against the other: drop subsets, rematerialize children from `.tree` where leaf-sets overlap, keep disjoint siblings. Typical result is a left spine of existing captions, no new agent sentences.

### Wake of a dirty HEAD

An overlapping merge is checked out. `wake` still prints and writes nothing. Heal waits for `note` or `nap`.

### Killed zipper

A crash leaves parent plus rematerialized children. The next mutating command drops the extra parent. No leaf is lost.

### Budget smaller than the healed spine

Heal leaves something like `8, 2, 1`. `WAKE_LINES=2` cannot equal-grain that. The request printer names no pair. Wake still projects to the budget.

## Requirements

1. Address [Texarkanine/SumMem#3](https://github.com/Texarkanine/SumMem/issues/3): zipper-heal overlapping nap leaf-sets after merge.
2. Zipper on `note` and `nap` only. Wake stays wait-free and does not rewrite the store.
3. At each node: keep if disjoint, drop if ⊆ the other, otherwise rematerialize the two children from `.tree` and recur. Worst case (scattered shared leaves) may flatten.
4. Mechanical rematerialize: copy `NapChild` / `NoteChild` bytes out, then unlink. Typical prefix overlap needs no new `.sum` text.
5. Remainder keeps its grain: a leftover 2-pack stays a 2-pack. Do not fold `8+1` or other unequal grains to force a cover.
6. After heal, if no adjacent equal-grain pair exists, print no fold request. Wake projection still bounds the listing.
7. `flock` this store on this machine for the mutating invocation only. Not a cross-worktree or cross-clone lock. Do not hold it waiting for a caption.
8. Crash order: write both children, then unlink the parent. Parent+children left behind is containment.
9. `write_nap` never concatenates overlapping packs.
10. Agent naps stay the existing interruptible equal-grain loop.
11. Binary `nap`, leaf-set identity, write-once `.tree`, wait-free wake, and "zoom is a property of `HEAD`" stay.

## Constraints

1. Out of this milestone: notes-stay / grow-only identity log; flatten as the normal path; aligned `[0, 8192)` rebuild; pack-size cap; `flock` across machines; zipper inside `wake`; scopes; issue #2 (agent prompt).
2. Do not reopen equal-grain from zero. Carry-stable stems, equal-grain requests, and in-memory wake expand stay.
3. One shebang file at `.summem/summem`. No package, no second identity.
4. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git.
5. Sub-run of L4 `file-backend`. Do not mark that L4 complete. Do not start scopes.
6. Tests live outside the script.
7. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Acceptance Criteria

1. Two branches that nap overlapping-but-unequal leaf-sets merge; next `note` or `nap` leaves a cover of unique leaves; zoom still reaches every original.
2. `write_nap` never concatenates overlapping packs.
3. Prefix overlap rematerializes `O(log N)` siblings, not `O(T)` notes; no new `.sum` text for those siblings.
4. Wake of an overlapping `HEAD` (no mutating command yet) still prints and writes nothing.
5. A killed zipper does not drop leaves. A second mutating command finishes the heal.
6. Binary `nap`, leaf-set identity, write-once `.tree`, wait-free wake unchanged.
