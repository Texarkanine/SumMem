## SumMem

Shared memory for this repository. The driver is the `summem` file at the repository root (the directory that contains `.git`). `--path` aims at a store, not at that file. This block is how the repository opts in; the driver alone is not activation.

### At session start

1. If you can see a prior **root** SumMem wake in this conversation, skip these steps.
2. Run `summem wake` from the repository root, or `summem wake --path <root>`.
3. Do what it prints, to the end of its output.

### Notes

`summem note "…"` records one line, at most 280 bytes. Only durable public facts about this tree — what a stranger clone would need, and what is acceptable in git forever. Personal, machine, and preference facts stay out. If `note` asks for a nap, do that nap before your next action. Never edit store files.

### Other commands

- `summem recall <regex>` — search remembered text word for word
- `summem zoom <id>` — open a nap
- `summem wake --path <path>` — when you work under a cataloged path, pull that store if its wake is not already in this conversation
- `summem start <dir>` — only when asked to start a package memory

# Agent context

Tracked agent-facing project knowledge lives under `memory-bank/`. Prefer those files over inventing project facts.

## Persistent files

- `memory-bank/productContext.md` — business context: users, use cases, success criteria, constraints
- `memory-bank/systemPatterns.md` — architecture and naming patterns in use
- `memory-bank/techContext.md` — stack, tools, and how to work in this repo

## Archives

Completed work is summarized under `memory-bank/archive/<kind>/YYYYMMDD-<task-id>.md`.

## Active work

`memory-bank/active/` holds the current-task execution trace. If those files exist, an in-flight task may be underway — consult them before starting work that could collide.

## When to load

When the task needs project, architecture, or stack context, read the relevant persistent file(s). Do not load every memory-bank file on every chat.
