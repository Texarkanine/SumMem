# Product Context

`VISION.md` is the design contract for this product. These sections are the business subset of that contract. A working tree that lacks a capability named here is unfinished work, not a different product.

## Target Audience

- Coding agents that work in a git repository and need a shared, decaying memory of what that tree has learned
- Operators who decide which directories get their own memory, especially in a monorepo
- Concurrent writers who do not share a process or a cross-clone lock: several agents on one machine, several jobs on one PR, several worktrees. A same-machine flock of `naps/` on one mutating invocation is not a committed object and is not an actor.

This product is not a single-actor local diary (that is OptMem, including its machine-global store). It is not task-scoped working documentation that is archived when a task ends (that is Niko's `memory-bank/`).

## Use Cases

- An agent starts a session, wakes the repository's root memory once, reads a bounded decaying view of what the repo has learned, and sees a catalog of other started memories it may pull when it works under those paths.
- An agent that learned a fact records one short line through the script. It does not invent filenames or edit store files.
- When asked to compact, the agent supplies a summary for a sealed block the script already identified. The original sentences remain recoverable.
- An agent searches remembered text word for word, or opens a summary back to its original sentences — including after a squash-merge, from a fresh clone of the branch tip.
- An operator (or an agent only when asked) starts a memory in a chosen directory so later commands under that path resolve there instead of rolling up.
- Many writers record facts at the same time. A normal git merge keeps all of them.

## Key Benefits

- Many writers can add facts without a cross-clone lock or a next-id.
- The view stays bounded as the log grows: recent facts stay verbatim, older facts collapse to one-line summaries.
- Squash-merge and shallow clones do not erase the sentences a later zoom still owes.
- Extra memories are opt-in directories, not inferred packages.
- The agent-facing commands can stay stable if the on-disk backend is replaced.

## Success Criteria

The product succeeds when the proofs in `VISION.md` under "First proof" hold. Those proofs are the acceptance bar for the first file backend: concurrent notes merge cleanly; same-block naps conflict only on the caption; originals survive squash onto `main`; positional ids are rejected; long-lived branches union then fold lazily; a path flag resolves to the nearest started store; root wake catalogs other stores and a pull prints only that store.

A missing proof is unfinished work, not a reason to drop the criterion.

## Key Constraints

- Agents never write the store. They run a script. The script owns every file.
- There is no actor, lease, or cross-clone lock. A scope is a directory that opted in. Same-machine flock of `naps/` on one mutating invocation is not a committed object.
- Personal and machine facts stay out of the repository.
- SumMem is not Niko's `memory-bank/` and must not be folded into it.
- Wake never refuses to print. "Cannot wake, go nap first" is a defect.
- The agent interface does not mention store files, hashes as paths, or git.
- A scope is not a package manifest. `start` is how a directory becomes a store.
- The git root auto-creates on first `wake` or `note`. Other stores appear only via `start`. Outside a repository, store commands fail. Help still prints.
