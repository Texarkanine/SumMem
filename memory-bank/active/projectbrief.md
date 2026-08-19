# Project Brief

## User Story

As an agent working in a git repository, I want `WAKE_LINES` to choose how many lines wake prints, and I want fold requests to name equal-grain pairs so `HEAD` stays a short power-of-two tree, so that raising the budget reveals more detail from trees already on disk, and rebuild, zoom, and later surgery stay `O(log n)`.

## Use-Case(s)

### Raise the budget

A store was napped down to two 512-leaf files while the budget was 2. The operator sets `WAKE_LINES` to 32. Wake does not rewrite the store. It expands the newest pack in memory until it has 32 lines (or the tree runs out). New notes then occupy those slots as native 1s and the cracking stops.

### Over-budget note

An agent records a note that makes **file** count exceed `WAKE_LINES`. The script writes the note and prints one equal-grain pair (two 1s or two 8s, never 16+1). It does not write a nap. It does not refuse to wake.

### Catch-up chain

The agent naps the requested pair. Children leave the directory. If **file** count is still over `WAKE_LINES`, that `nap` prints the next equal-grain pair.

### Long stream

A long stream of `note` plus requested `nap`s leaves on-disk grains that are powers of two, plus unmerged 1s. It does not leave one nap of size `T - WAKE_LINES + 1`. Depth of the oldest pack is `O(log leaves)`.

### Explicit nap after merge

Binary `nap <id-a> <id-b>` still folds two adjacent **view files**. After a long-lived merge, the agent may nap adjacent packs. Wake may print finer lines than those files. The request printer does not re-tile interleaved leaves into an aligned `[0, 8192)`.

## Requirements

1. Address [Texarkanine/SumMem#1](https://github.com/Texarkanine/SumMem/issues/1): equal-grain fold so the caption tree stays `O(log n)`.
2. `WAKE_LINES` is a view-time projection. Raising it must be able to print more lines from existing `.tree` payloads without writing children back out. See `memory-bank/active/creative/creative-wake-projection.md` (operator amendment: unlink + in-memory expand).
3. Keep binary `nap <id-a> <id-b> "…"`. Do not invent a second identity. Do not nap `k` children at once. The CLI table does not grow.
4. Change which pair is requested: only two adjacent view files with the same leaf count. Never 16+1. `fold_request` keys off file count, not printed-line count.
5. Nap filenames carry the leftmost child's `{stamp}-{rand}`. Leaf-set id stays identity. Stem is `{stamp}-{rand}-{leafset}-{leaves}`. Do not open `.tree` to sort.
6. Catch-up after a successful `nap` if file count is still over budget. `note` still prints at most one pair after a write.
7. Expand algorithm: while printed frontier `< WAKE_LINES`, from the right, replace the first nap that has two kids with those kids. Repeat. In memory only. Stop when the budget is met or no nap will split. A lone note never splits.
8. `write_nap` still unlinks children. Disk file count may stay on the order of the budget. That is not the wake listing.
9. `zoom` of an expanded line’s id already walks ancestor trees. This milestone does not teach `write_nap` to fold two in-tree-only ids.
10. Production fold tests refuse a 16+1 request and accept two 8s. Proof 4 helper packs are 64/32/4.
11. Surgical contract updates: `VISION.md` stems, equal-grain requests, and wake-as-projection (may open `.tree` when the directory is shorter than the budget). Year-later file count is the directory, not the printed cut.
12. Binary `nap`, leaf-set identity, write-once `.tree`, wait-free wake, and "zoom is a property of `HEAD`" stay.

## Constraints

1. Out of this milestone: redaction, flatten-to-leaves, full aligned `cover(T)` rebuild after merge, scopes, pack-size cap, harness hooks, `write_nap` of virtual ids, parsing `config.toml`.
2. Do not reopen single-store from zero. `write_nap`, `zoom`, `recall`, and proofs 2, 3, and 5 stay.
3. One shebang file at `.summem/summem`. No package, no second identity.
4. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git.
5. Sub-run of L4 `file-backend`. Do not mark that L4 complete. Do not start issue #2.
6. Tests live outside the script.
7. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Acceptance Criteria

1. Two 8-leaf naps on disk, `WAKE_LINES=4`, no extra notes → wake prints 4 lines (left 8 kept, right 8 split until the budget fills). No new store files.
2. The same store with `WAKE_LINES=2` → two lines, the two `.sum` captions. No `.tree` parse required.
3. Two 8-leaf naps plus two later notes, `WAKE_LINES=4` → four file lines, no expand.
4. 1024-equivalent shape (tested at small grain): raise budget above file count → more lines; add enough 1s to meet the budget → expand stops.
5. Long stream of `note` + requested `nap`s, including same-second notes: on-disk grains are powers of two plus remainder 1s, not a 17. Parent of two same-second notes stays in the left child's slot (`[2, 1, 1]`).
6. Depth of a 16-leaf equal-grain pack is `<= 4`. Request printer never names 16+1; it does name two adjacent 8s.
7. Proofs 2, 3, 5 still pass. Proof 4 squash-clones and zooms originals with 64/32/4 packs (CLI wake pinned to 3 lines so expand does not hide the three files). Proof 6 still unions two packs; nap still folds the two **files**.
8. No redaction command. No flatten. No aligned `[0, 8192)` rebuild. No children written back when the budget rises.
