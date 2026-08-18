# Project Brief

## User Story

As an agent working in a git repository, I want a script-owned concurrent memory so that many writers can record facts, wake a decaying view, and recover original sentences after a squash-merge.

## Use-Case(s)

### Session start

An agent wakes the repository's root memory once, reads a bounded decaying view, and sees a catalog of other started memories it may pull.

### Record a fact

An agent that learned something runs `note`. The script writes one short immutable file. The agent does not invent filenames or edit the store.

### Compact and recover

When asked, the agent `nap`s a sealed block the script identified. Later `zoom` and `recall` still see the original sentences, including from a fresh clone after squash onto `main`.

### Concurrent writers

Two worktrees or agents record at the same time. A normal git merge keeps both facts.

### Aim at a directory

`start` opts a directory in. `--path` walks up to the nearest started store and does not create one.

## Requirements

1. Implement the first file backend as specified in `VISION.md`.
2. Sequence the work as the three phases in `ROADMAP.md`: ingest, single-store memory, scopes.
3. Satisfy first proofs 1–8 in `VISION.md`. Those proofs are the acceptance bar, not a change-detector on the vision document.
4. Agents never write the store. They run a script.
5. The agent interface (`wake`, `note`, `nap`, `recall`, `zoom`, `start`, optional `--path`) does not mention store files, hashes as paths, or git.
6. First implementation language is Python 3 with SHA-256 from `hashlib`.

## Constraints

1. Items listed under `ROADMAP.md` "Later" are out of this L4: sqlite or other backends, harness hooks, full OptMem aligned cover, pack-size cap, shipping an agent prompt or Cursor rule, a filled `README.md`.
2. No actor, lease, lock, shared mutable index, or custom merge driver.
3. Sequence is in the filename, not in `git log`. Zoom is a property of `HEAD`.
4. Wake never refuses to print.
5. Personal and machine facts stay out of the repository.
6. A scope is a started directory, not a package manifest.
7. Missing config means script defaults. Knobs live in the store, not the environment.
8. A missing implementation of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Acceptance Criteria

1. First proof 1: two worktrees each `note` once, merge, zero conflicts, two notes in the view.
2. First proof 2: both `nap` the same pair with different sentences; one conflict, on `.sum` only; either resolution wakes and zooms.
3. First proof 3: `<<<<<<<` in a `.sum` is skipped by wake; zoom still prints the leaves.
4. First proof 4: one hundred notes, fold to three naps, squash onto `main`; a fresh clone of `main` can `zoom` to an original sentence.
5. First proof 5: `nap` with a positional range, or with no content id, is rejected.
6. First proof 6: two long-lived branches with disjoint packs merge clean; wake prints both at pack grain; a following nap folds the two oldest neighbors into one parent.
7. First proof 7: `note --path foo/packages/baz/fee.ts` writes into `foo/packages/baz` if that store exists, else the next ancestor.
8. First proof 8: root wake lists other started stores; `wake --path` on one of them prints that store only, not root again.
