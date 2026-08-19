# Project Brief

## User Story

As an agent working in a git tree that may have more than one memory, I want commands to resolve to the nearest started store via `--path` or `$PWD`, and I want root wake to catalog the others so I can pull one, so that package memory is opt-in and child memory is advertised rather than stuffed into the root document.

## Use-Case(s)

### Regular repository

Nobody ran `start`. First `wake` or `note` still auto-creates the git-root store. Every command from a subdirectory rolls up there. Root wake has no other stores to list.

### Started package

An operator ran `start foo/packages/baz`. `note --path foo/packages/baz/fee.ts "…"` writes into that store. Work under an unstarted sibling rolls up to the nearest started ancestor, at least the git root.

### Pull is not a second root wake

Root wake prints the root document plus a catalog line per other started store. `wake --path foo/packages/baz/fee.ts` prints only that nearest store. It does not reprint root or the catalog.

### Per-store budget

`foo/packages/baz/.summem/config.toml` sets `WAKE_LINES = 8`. A pull of that store uses 8. Root still uses root's config. Missing names mean script defaults. Wake does not rewrite the file.

### Ignored store

A `.summem/` that git ignores (including via `.git/info/exclude`) is not a catalog entry.

## Requirements

1. Implement scopes as named in `memory-bank/active/milestones.md` and `ROADMAP.md` Phase 3: `start`, `--path` walk-up, root-wake catalog, per-store config, first proofs 7-8.
2. Every command except `start` takes optional `--path`. Walk from that path, or from `$PWD` if omitted, toward the git root. `--path` may be a file: walk from its parent directory. Take the first directory that already has a store.
3. Do not create a store because a command ran from a deep folder or passed a file under one. Git-root auto-create on first `wake` or `note` stays. `start <dir>` is the only way to create a store elsewhere, in that directory, with no walk-up.
4. Do not parse workspace manifests. A scope is a started directory.
5. Root wake (the resolved store is the git root) prints that store's decaying document and a computed catalog of every other started store: relative path, note count, latest date, and how to pull. The catalog is a tree walk that honors git ignore, including `.git/info/exclude`. It is not a committed index.
6. `wake --path` prints only the nearest store. It does not reprint root or the full catalog. Do not load every started store in the root wake.
7. `start <dir>` writes the same kind of store and default commented config that git-root auto-create writes, including a sibling driver. Missing knobs still mean script defaults. Wake and `note` do not rewrite config.
8. Load that store's `config.toml` with stdlib `tomllib`. Fill omitted names from built-in defaults. Knobs are not environment variables. Invert today's tests that `--path` is unknown and that `config.toml` is ignored.
9. Identity, binary `nap`, write-once `.tree`, wait-free wake, zipper-heal, and "zoom is a property of `HEAD`" stay.

## Constraints

1. Out of this milestone: other backends, harness hooks, aligned cover, pack-size cap, agent prompt or Cursor rule (issue #2), filled `README.md`, an explicit config CLI, a committed catalog index.
2. Do not reopen ingest, equal-grain, or zipper-heal from zero.
3. One shebang file at `.summem/summem`. No package, no second identity, no shared mutable index.
4. Agents never write store files. Wake listings and errors do not mention `notes/`, `naps/`, hashes as paths, or git.
5. Last sub-run of L4 `file-backend`. Do not mark that L4 complete until this milestone is reflected.
6. Tests live outside the script.
7. A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Acceptance Criteria

1. `note --path foo/packages/baz/fee.ts` writes into `foo/packages/baz` if that store exists, else the next ancestor (first proof 7).
2. Root wake lists other started stores. `wake --path` on one of them prints that store only, not root again (first proof 8).
3. `start <dir>` creates a store in that directory and does not create stores along the walk-up.
4. A command from an unstarted subdirectory of a git repo still uses (and may auto-create) the git-root store, not the subdirectory.
5. A store git ignores is omitted from the catalog.
6. A store's `WAKE_LINES` in `config.toml` bounds that store's wake. Another store's file does not.
7. `--path` omitted walks from `$PWD`. `--path` on a file walks from the file's directory.
8. Note identity, nap identity, and zoom-from-`HEAD` unchanged.
