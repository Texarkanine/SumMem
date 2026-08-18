# Project Brief

## User Story

As an agent working in a git repository, I want a script that records one immutable note per fact and wakes a wait-free listing of those notes so that two writers can add two files and a normal git merge keeps both.

## Use-Case(s)

### Record a fact

An agent that learned something runs `.summem/summem note`. The script writes one short immutable file at the git-root store. The agent does not invent filenames or edit store files.

### Session start (root, loose notes)

An agent wakes the repository's root memory once by running `.summem/summem wake` and reads a listing of loose notes, each with a content id. Wake never refuses to print.

### Concurrent writers

Two worktrees or agents each `note` once. A normal git merge has zero conflicts and both notes appear in the view.

## Requirements

1. Implement Phase 1 (ingest) of the first file backend as specified in `VISION.md` and sequenced in `ROADMAP.md`.
2. Ship one shebang Python 3.11+ script at `.summem/summem`. That path is the brand and the ride-along driver. No installable package, no hatchling, no `src/` layout, no console entry on `PATH`.
3. Auto-create the git-root store on first `wake` or `note`: `.summem/config.toml` (commented template), `.summem/notes/`, and `.summem/summem` itself if the driver is missing (copy the running file, do not overwrite an existing driver).
4. `note` writes one immutable file: UTC name from `datetime.now(timezone.utc)` (or an injected UTC `now`), at most 280 bytes, temp file plus rename.
5. `wake` prints a wait-free listing of loose notes, each with a content id. Empty output is a valid wake. Reconfigure stdout/stderr to UTF-8 so non-ASCII notes do not crash on a latin-1 locale.
6. Freeze store layout and leaf-set hashing so later milestones do not invent a second identity scheme: note-byte digest, sorted hex join with no delimiter, leaf-set id, and canonical `.tree` bytes — including nested nap children — even though this milestone does not write naps.
7. Put failing compatibility-vector tests in place before the codec implementation. Those vectors are the executable format contract reused by the single-store milestone.
8. Satisfy first proof 1 in `VISION.md`.
9. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git. `.summem/summem` is the tool path (like `~/.optmem/memo`), not a leaked store file.
10. Refuse to run on Python older than 3.11.

## Constraints

1. Out of this milestone: `nap`, `zoom`, `recall`, `start`, `--path`, root catalog, cover, config knobs beyond internal defaults, and every item under `ROADMAP.md` "Later".
2. No actor, lease, lock, shared mutable index, or custom merge driver.
3. Sequence is in the filename, not in `git log`. Time is UTC. A `Z` suffix without a UTC clock is a defect.
4. Wake never refuses to print.
5. Personal and machine facts stay out of the repository.
6. Walk-up never creates a store. This milestone only auto-creates the git root.
7. Missing config means script defaults. `tomllib` reads only; defaults are a commented template string.
8. Store directory is `.summem/` (not `.mem/`). Config path is `.summem/config.toml`. The driver is `.summem/summem`. Nested stores later are data only; they do not each get a copy of the driver.
9. Hashing is SHA-256 from `hashlib`. Do not call `sha256sum`, `openssl`, or `git hash-object`.
10. First proofs 2–8 belong to later milestones. Do not implement them here.
11. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.
12. This is milestone 1 of L4 `file-backend`. Do not mark that L4 complete.
13. Tests live outside the script. The product stays one file.

## Acceptance Criteria

1. Compatibility-vector tests exist and failed before the codec was written: note-byte digests, sorted leaf-set ids, and nested canonical `.tree` bytes. Chinese (and any UTF-8) notes hash as file bytes; `ensure_ascii=False` is part of the `.tree` contract.
2. First proof 1: two worktrees each `.summem/summem note` once, merge, zero conflicts, two notes in the view.
3. `note` of a line over 280 bytes is rejected. `note` assigns time and name; the caller does not. 280 is UTF-8 bytes, not characters.
4. First `wake` or `note` in a git repo creates `.summem/config.toml` as a commented template, a `notes/` directory, and installs `.summem/summem` if it was missing. An existing driver is never overwritten.
5. `wake` prints each loose note with a 64-hex content id and never mentions `notes/`, `naps/`, hashes as paths, or git.
6. `.summem/summem` exposes `wake` and `note` only. It is a shebang file (`#!/usr/bin/env python3`) and executable.

## Rework

Operator rejected the hatchling / `src/` / PATH console-entry plan (2026-08-18). Product is one shebang script. `.summem/` is the brand; the driver is `.summem/summem`, sibling to data, matching `~/.optmem/memo` beside `~/.optmem/memory`. UTC clock, UTF-8 stdout, and 280-byte (not character) limit were confirmed.
