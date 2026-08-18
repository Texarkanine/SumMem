# Project Brief

## User Story

As an agent working in a git repository, I want a script that records one immutable note per fact and wakes a wait-free listing of those notes so that two writers can add two files and a normal git merge keeps both.

## Use-Case(s)

### Record a fact

An agent that learned something runs `note`. The script writes one short immutable file at the git-root store. The agent does not invent filenames or edit the store.

### Session start (root, loose notes)

An agent wakes the repository's root memory once and reads a listing of loose notes, each with a content id. Wake never refuses to print.

### Concurrent writers

Two worktrees or agents each `note` once. A normal git merge has zero conflicts and both notes appear in the view.

## Requirements

1. Implement Phase 1 (ingest) of the first file backend as specified in `VISION.md` and sequenced in `ROADMAP.md`.
2. Ship a Python 3.11+ package with a console entry so agents run a script, not edit files.
3. Auto-create the git-root store on first `wake` or `note`: `.summem/` plus a commented default `config.toml`.
4. `note` writes one immutable file: UTC name, at most 280 bytes, temp file plus rename.
5. `wake` prints a wait-free listing of loose notes, each with a content id. Empty output is a valid wake.
6. Freeze store layout and leaf-set hashing so later milestones do not invent a second identity scheme: note-byte digest, sorted hex join, leaf-set id, and canonical `.tree` bytes — including nested nap children — even though this milestone does not write naps.
7. Put failing compatibility-vector tests in place before the codec implementation. Those vectors are the executable format contract reused by the single-store milestone.
8. Satisfy first proof 1 in `VISION.md`.
9. Agents never write the store. The agent interface does not mention store files, hashes as paths, or git.

## Constraints

1. Out of this milestone: `nap`, `zoom`, `recall`, `start`, `--path`, root catalog, cover, config knobs beyond internal defaults, and every item under `ROADMAP.md` "Later".
2. No actor, lease, lock, shared mutable index, or custom merge driver.
3. Sequence is in the filename, not in `git log`.
4. Wake never refuses to print.
5. Personal and machine facts stay out of the repository.
6. Walk-up never creates a store. This milestone only auto-creates the git root.
7. Missing config means script defaults. `tomllib` reads only; defaults are a commented template string.
8. Store directory is `.summem/` (not `.mem/`). Config path is `.summem/config.toml`.
9. Hashing is SHA-256 from `hashlib`. Do not call `sha256sum`, `openssl`, or `git hash-object`.
10. First proofs 2–8 belong to later milestones. Do not implement them here.
11. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.
12. This is milestone 1 of L4 `file-backend`. Do not mark that L4 complete.

## Acceptance Criteria

1. Compatibility-vector tests exist and failed before the codec was written: note-byte digests, sorted leaf-set ids, and nested canonical `.tree` bytes.
2. First proof 1: two worktrees each `note` once, merge, zero conflicts, two notes in the view.
3. `note` of a line over 280 bytes is rejected. `note` assigns time and name; the caller does not.
4. First `wake` or `note` in a git repo creates `.summem/config.toml` as a commented template and a `notes/` directory.
5. `wake` prints each loose note with a content id and never mentions store paths, hashes as paths, or git.
6. Console entry `summem` exposes `wake` and `note` only.
