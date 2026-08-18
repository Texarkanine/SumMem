# Project Brief

## User Story

As an agent working in a git repository, I want a script that naps sealed blocks into one-line captions, zooms those captions back to original sentences, and recalls remembered text word for word, so that a fresh clone of `main` after squash can still open every sentence the view still owes.

## Use-Case(s)

### Compact a sealed block

An agent supplies a one-line summary for a sealed block the script already identified. The script writes a nap pair keyed by leaf set, not by the sentence. Children leave the view only after the parent payload exists on disk.

### Session start (root, mixed view)

An agent wakes the repository's root memory once and reads the current view: loose notes plus nap captions, each with a content id. A missing or conflict-marked caption degrades. Wake never refuses to print.

### Open a summary

An agent runs `zoom` with a content id from wake and reads the block's two halves, down to raw notes. After squash onto `main`, a clone of the tip still zooms to originals.

### Search remembered text

An agent runs `recall` and searches the view word for word, including original sentences stored inside nap payloads.

### Concurrent nappers

Two writers nap the same leaves with different sentences. Git conflicts on the caption only. Either resolution still wakes and zooms. Two writers nap disjoint leaves: two pairs, no conflict.

## Requirements

1. Implement Phase 2 (single-store memory) of the first file backend as specified in `VISION.md` and sequenced in `ROADMAP.md`.
2. Extend the existing shebang driver at `.summem/summem`. Do not add a package, hatchling, `src/` layout, a root-level `summem`, or a second identity scheme. Call `leafset_id` and `dumps_tree` already in that file. The Sequence section's 8-character id is a picture, not the contract.
3. `nap <id-a> <id-b> "…"` accepts exactly two adjacent content ids a wake printed, plus a caption. `zoom <id>` accepts one id. A positional range, one id to `nap`, three ids, or no id, is rejected.
4. A nap is a pair: `.sum` caption (one line, at most 280 UTF-8 bytes) and `.tree` canonical payload. Identity is the leaf set, not the sentence. Same children produce the same id and the same payload bytes. Different wording produces the same id and a different caption.
5. A child may be a raw note or another nap. Fold writes a new pair. Children leave the view only after the parent payload exists on disk. Do not implement "nap only raw notes" and extend later. Proof 6 needs nap-of-naps.
6. `wake` prints the current view (loose notes plus nap pairs), wait-free. A missing or conflict-marked caption degrades to the content id without a caption; it does not block. Wake does not open `.tree`.
7. `recall` searches the view, and original sentences inside `.tree` files.
8. When the view is over `WAKE_LINES`, left-fold: nap the oldest adjacent view nodes. That is enough decay for the proofs. Aligned power-of-two `cover(T, budget)` is later.
9. Satisfy first proofs 2, 3, 4, 5, and 6 in `VISION.md`. Internal order: identity and conflict (2, 3, 5) before volume and longevity (4, 6).
10. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git.

## Constraints

1. Out of this milestone: `start`, `--path`, root catalog, committed config knobs, cover, and every item under `ROADMAP.md` "Later".
2. Missing config still means script defaults. This milestone does not parse `config.toml` and does not import `tomllib` unless a default must be read from disk — it must not.
3. No actor, lease, lock, shared mutable index, or custom merge driver.
4. Sequence is in the filename, not in `git log`. A nap file's sort key is the minimum child time, not when compaction ran. Zoom is a property of `HEAD`.
5. Wake never refuses to print.
6. Personal and machine facts stay out of the repository.
7. Store directory is `.summem/` (not `.mem/`). The driver is `.summem/summem`. Do not overwrite an existing driver. Nested stores later are data only.
8. Hashing is SHA-256 from `hashlib`. Do not call `sha256sum`, `openssl`, or `git hash-object`.
9. First proofs 1, 7, and 8 belong to other milestones. Do not re-implement ingest. Do not implement scopes.
10. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.
11. This is milestone 2 of L4 `file-backend`. Do not mark that L4 complete.
12. Tests live outside the script. The product stays one file.
13. This repo is not a store until a hook binds the driver. Do not commit this tree's `config.toml` / `notes/` / `naps/`.

## Acceptance Criteria

1. First proof 2: both `nap` the same pair with different sentences. One conflict, on `.sum` only. Either resolution wakes and zooms.
2. First proof 3: plant conflict markers in a `.sum`. Wake skips that caption. Zoom still prints the leaves.
3. First proof 4: one hundred notes on a branch, fold to three naps, squash onto `main`. A fresh clone of `main` can `zoom` to an original sentence. `git log` of the branch is gone.
4. First proof 5: `nap` with a positional range, or with no content id, is rejected.
5. First proof 6: two long-lived branches with disjoint packs merge clean. Wake prints both at pack grain. A following nap folds the two oldest neighbors into one parent.
6. `.summem/summem` exposes `wake`, `note`, `nap`, `zoom`, and `recall`. It still does not expose `start` or `--path`.
7. Nap-of-naps uses the same `leafset_id` / `dumps_tree` contract ingest froze, including nested `.tree` bytes.
