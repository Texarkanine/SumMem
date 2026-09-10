# Project Brief

## User Story

As an operator (and as agents running on native Windows), I want a complete audit of where SumMem will not work on Windows, each item paired with a recommended resolution and why that resolution is optimal, so a later implementation can follow a justified path instead of copying POSIX blindly or copying OptMem blindly.

## Use-Case(s)

### Use-Case 1

An agent on native Windows (Python 3.13 at `python` on this machine’s CMD) tries to run SumMem. The audit names every command or test path that will fail, and what to do instead.

### Use-Case 2

A later implementation task uses this audit as the decision record: lock fallback, invocation, paths, git, tests, and anything else found — each with a preferred fix and the rejected alternatives.

## Requirements

1. Audit SumMem (driver, helpers, tests, invocation, docs that claim portability) for native Windows breakage, not WSL-as-Linux.
2. Use [OptMem](https://github.com/VictorTaelin/OptMem) as the reference for Windows fallbacks already proven in the grandparent (`fcntl` optional, `msvcrt` lock, `.lock` opened append-not-truncate). Do not treat OptMem’s lock model as automatically correct for SumMem.
3. Probe native Windows CMD from this WSL session when that probe can confirm or refute a finding.
4. For each finding: what breaks, recommended resolution, and why that resolution is optimal (including why not the obvious alternative).
5. This run is the audit and recommendations. It does not implement the Windows port.

## Constraints

1. Do not implement Windows compatibility in this task.
2. Do not invent a cross-clone lock or a committed lock file. Product context: same-machine flock of `naps/` is not a committed object and is not an actor.
3. Personal and machine facts stay out of the repository store.
4. Findings must distinguish “will not run” from “works but tests assume POSIX” from “docs/docs-adjacent only.”

## Acceptance Criteria

1. Every native-Windows failure mode found in the driver, helpers, tests, and invocation is listed.
2. Each finding has a recommended resolution and a short optimality argument (why this, not the next-best option).
3. OptMem’s Windows path is used as evidence, not as a drop-in transplant, where SumMem’s git-tree store differs.
4. Windows CMD on this machine is used as a probe where it can ground a claim.
5. No product-code Windows port is shipped in this task.
