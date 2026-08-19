# Project Brief

## User Story

As an agent working in a git repository, I want fold requests to name two adjacent view nodes of the same leaf count, and a short sequential nap chain while the view is over budget, so that `HEAD` stays a short power-of-two tree and rebuild, zoom, and later surgery stay `O(log n)` in the number of leaves.

## Use-Case(s)

### Over-budget note

An agent records a note that pushes the view over `WAKE_LINES`. The script writes the note and prints one equal-grain pair (two adjacent 1s, or two adjacent 8s, never 16+1). It does not write a nap. It does not refuse to wake.

### Catch-up chain

The agent naps the requested pair. If the view is still over `WAKE_LINES`, that `nap` prints the next equal-grain pair. The agent does them in sequence in one turn. Falling a handful of pairs behind is `O(k)` naps, not `O(T)`.

### Long stream

A long stream of `note` plus requested `nap`s leaves view grains that are powers of two, plus a remainder of unmerged 1s. It does not leave one nap of size `T - WAKE_LINES + 1`. Depth of the oldest pack is `O(log leaves)`.

### Explicit nap after merge

Binary `nap <id-a> <id-b>` still folds two adjacent view nodes the agent named. After a long-lived merge, the agent may nap adjacent packs. The request printer does not re-tile interleaved leaves into an aligned `[0, 8192)`.

## Requirements

1. Address [Texarkanine/SumMem#1](https://github.com/Texarkanine/SumMem/issues/1): equal-grain fold so rebuild stays `O(log n)`.
2. Keep binary `nap <id-a> <id-b> "…"`. Do not invent a second identity. Do not nap `k` children at once. The CLI table does not grow.
3. Change which pair is requested: only two adjacent view nodes with the same leaf count. Two 1s → 2, two 8s → 16. Never 16+1.
4. Catch-up is a chain, not one request per later `note`. After a successful `nap`, if the view is still over `WAKE_LINES`, print the next equal-grain pair. `note` still prints at most one pair after a write.
5. Wake stays wait-free. Boundedness comes from the files on disk being a short tree, not from wake truncating or refusing.
6. Production fold tests refuse a 16+1 request and accept two 8s. Proof 4's in-pack left-spines may remain a test helper; pack sizes in the squash proof must be reachable under equal-grain (powers of two, plus remainder).
7. Surgical contract updates: `VISION.md` "simpler equivalent" (oldest two / oldest *k*) is no longer the long-term fold; the year-later diagram is the fold rule. `ROADMAP.md` Later distinguishes equal-grain / short tree (this issue) from full aligned cover as a wake pretty-printer (still Later).
8. Binary `nap`, leaf-set identity, write-once `.tree`, wait-free wake, and "zoom is a property of `HEAD`" do not change.

## Constraints

1. Out of this milestone: redaction (no sibling script, no history rewrite, no new agent verb), flatten-to-leaves, full OptMem `cover(T, budget)`, scopes (`start`, `--path`, catalog), pack-size cap, harness hooks, and every other `ROADMAP.md` Later item.
2. Do not reopen single-store from zero. `write_nap`, `zoom`, `recall`, and proofs 2, 3, and 5 stay.
3. Do not add a package, hatchling, `src/` layout, a root-level `summem`, or a second identity scheme. Extend `.summem/summem`.
4. Missing config still means script defaults. This milestone does not parse `config.toml`.
5. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git.
6. This is a sub-run of L4 `file-backend`. Do not mark that L4 complete. Do not start issue #2 (prompt) from this L4.
7. Tests live outside the script. The product stays one file.
8. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Acceptance Criteria

1. A long stream of `note` + requested `nap`s produces view grains that are powers of two (plus a remainder of unmerged 1s), not one nap of size `T - WAKE_LINES + 1`.
2. Depth of the oldest pack is `O(log leaves)`, not `O(leaves)`.
3. Falling `k` pairs behind can be caught in one agent turn (`O(k)` sequential equal-grain naps, `k` on the order of a cover burst, not `O(T)`).
4. The request printer never names 16+1. It does name two adjacent 8s.
5. Binary `nap`, leaf-set identity, write-once `.tree`, wait-free wake, and zoom-from-`HEAD` still hold. First proofs 2, 3, 5, and 6 still pass. Proof 4 still squash-clones and zooms originals, with power-of-two pack sizes.
6. No redaction command ships. No flatten. No aligned `[0, 8192)` rebuild after merge.
