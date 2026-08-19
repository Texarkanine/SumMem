# Milestones: file-backend

## Cross-milestone invariants and constraints

- Agents never write the store. The script is the only writer.
- Ingest commutes: two notes are two paths. No next id. No shared mutable index.
- Sequence is in the filename, not in `git log`. Zoom is a property of `HEAD`.
- Wake never refuses to print.
- The agent interface does not mention store files, hashes as paths, or git.
- Personal and machine facts stay out of the repository.
- A scope is a started directory, not a package manifest. Walk-up never creates a store.
- Missing config means script defaults. Knobs live in the store, not the environment.
- Phase 1 freezes store layout and leaf-set hashing. Later milestones do not invent a second identity scheme.
- `ROADMAP.md` "Later" stays out: other backends, harness hooks, aligned cover, pack-size cap, agent prompt or Cursor rule, filled `README.md`.
- A missing piece of `VISION.md` is unfinished work, not a reason to shrink the contract.

## Execution Order

Sequential. No parallel milestones.

- [x] Implement ingest: Python 3 CLI, git-root store auto-create, `note` and wait-free `wake` of loose notes, first proof 1, freeze store layout and leaf-set hashing
- [ ] Implement single-store memory: `nap`, `zoom`, `recall`, left-fold of adjacent view nodes, first proofs 2-6
- [ ] Address issue #1 - https://github.com/Texarkanine/SumMem/issues/1
- [ ] Implement scopes: `start`, `--path` walk-up, root-wake catalog, per-store config, first proofs 7-8

## Scope estimates

- Ingest — L3: new package, CLI, store I/O, and a worktree merge proof; freezes layout for the rest of the L4.
- Single-store memory — L3: one store subsystem (`nap`/`zoom`/`recall`/fold) and proofs 2-6; design is already in `VISION.md`.
- Scopes — L2: addressing and catalog on an existing CLI; must not change identity or the `HEAD` zoom rule.
