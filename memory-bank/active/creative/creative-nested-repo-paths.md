# Architecture Decision: Paths into Nested Repositories

## Requirements & Constraints

1. **No surprising or plainly wrong results.** A memory should land in the repository that the person's change will be pushed to.
2. **Lean driver.** The script is pasted into every consumer repository, so the fix should be the fewest lines that work.
3. **Printed paths can be pasted back** (`creative-store-flag-scheme.md` rule 4).
4. Existing product rule (`productContext.md`): outside a repository, store commands fail.

Operator evidence: memories written into a submodule or a vendored checkout (for example, ffmpeg cloned into a C project) almost never get pushed. One change that commits to two repositories is not a real workflow.

## Components

- `find_store_parent(dir)`: the nearest directory above `dir` that has `.git`. A submodule's `.git` file also counts.
- `resolve_parent(cwd, path)`: resolves the path, walks up to the nearest store, and refuses a store outside the root.
- `_input_path`: parses `:/`; for now it also holds the `:/..` containment check.

## Options Evaluated

- **A. Keep today's behaviour and document it.** The path picks the nested repository's store. Printed `:/` is relative to that repository.
- **B. Refuse (git's rule).** The repository of the current directory is the repository. A path whose own repository is a different one is refused with one line.
- **C. Look past the nested repository.** Walk up past the nested repository to the outer repository's store, with printed paths relative to the outer root.

## Analysis

| | A: keep | B: refuse | C: look past |
|---|---|---|---|
| Memory lands where it is pushed | No: it goes into a repository nobody pushes | Yes, or nothing is written | Yes |
| Printed paths can be pasted back | Only from inside the nested repository | Yes: one repository per command | Yes, but the nested repository's own `.summem` would need skipping |
| Driver code | 0 | About 2 lines, and it replaces the `:/..` check | A repository check on every walk step |
| Precedent | None | git: `Pathspec is in submodule` | None |

Key insights:

- With B, one comparison (the target's repository root must equal the current directory's) also catches `:/../x`. That case is "not this repository" too. So the separate containment check in `_input_path` goes away, and the net code change is about zero.
- C is the friendliest in theory, but it has to work out store ownership per directory. The operator's evidence says the case is too rare to pay for that.
- Someone who really wants to write into the submodule can `cd` into it. Inside the submodule, B works normally, because that submodule is now the repository.

## Decision

### Choice Pre-Mortem

- *Callers run store commands from outside any repository, passing an absolute `--path`.* Checked: `productContext.md` already says store commands fail outside a repository, so B makes the code match the stated rule.
- *A vendored repository that is not a submodule is something people expect to annotate from the outer repository.* Checked against the operator's evidence: those notes would not be pushed anyway. The refusal tells them where to run the command.
- *Tests pass an absolute path while their current directory is somewhere else.* This is not a product premise. The two affected test calls would `chdir` first.

**Selected**: B, refuse (git's rule)
**Rationale**: Memories land only in the repository the person is working in, so nothing is written where it would never be pushed (constraint 1). One comparison replaces the existing `:/..` check, so the driver gets no bigger (constraint 2). Every printed `:/` means the same repository as the command (constraint 3).
**Tradeoff**: You can no longer write into a nested repository's store from the outer repository; you `cd` into it first.

## Implementation Notes

- `resolve_parent`: `root = find_store_parent(cwd)`. After resolving the target, if `find_store_parent(origin) != root`, raise `ValueError` with ``not in this repository: `<arg>` ``. Keep the store-symlink check.
- `_input_path`: drop its `is_relative_to` check; `:/..` now fails the same comparison. `start` uses the same comparison in place of its own `outside the repository` check.
- One error message for every case: ``not in this repository: `<arg>` `` (exit 1). Update the troubleshooting row, and replace the nested-repository bullet in `commands.md` with the refusal.
- Tests: a submodule-style nested repository (`git init` inside the outer repository) refuses `--path :/vendor/lib/x` and `--path vendor/lib/x` from the outer repository and writes nothing; the same note works when run from inside `vendor/lib`. Update `:/../x` and outside-start assertions to the new message.
