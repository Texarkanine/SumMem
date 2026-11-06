# SumMem

**A committed, concurrent memory for agents working in a git repository.**

Put one Python script in your repository and a short block at the top of `AGENTS.md`. From then on, each agent that works in the repository starts its session with what earlier agents learned, and records what it learns. The memories are small files in git, so they travel with every clone, fork, and pull request.

## Why memory?

Many agents may work on one repository. They make decisions and find facts and gotchas. Then the session ends and all of it is gone, unless something keeps it.

### Why memory in the repository?

You can give *your* agent memory on *your* machine, through an MCP server or some other local tool. That does not help anyone else. Another contributor's agent still starts from nothing, and you still get changes that ignore how things are done here. What the repository has learned has to travel with the code.

### Why SumMem?

- **Lives in the repository.** Memories are files in git. There is no server and no account. Once you have the repository, you have the memory.
- **Many writers, no lock.** Every memory is a new file with its own name, so git merges never conflict on them. [Why writers never conflict](how-it-works/no-conflicts.md).
- **Bounded context.** Recent memories stay word for word. Older ones fold into one-line summaries, so waking up costs about the same in a young repository and an old one.
- **Nothing is lost.** Every summary keeps the original memories inside it. An agent can open a summary back up, or search the original text.
- **Scoped stores.** In a monorepo, give a package its own memory with one command.
- **Works with most agents.** Any agent that reads `AGENTS.md` and can run a shell command can use it.

## What an agent sees

At the start of each session the agent runs one command. After a short how-to, it reads the repository's memories:

```text
== Project-root Memories ==
x2 44cf08be: Test with tox -e py311; the script is the only writer of .summem.
x1 2026-11-06: Docs build with properdocs.
x1 2026-11-06: CI runs py311 to py314.
x1 2026-11-06: Release Please cuts tags from main.
You are up to speed.
```

An `x1` line is one memory, with the day it was written. An `x2` line is a summary of two memories. The agent can open it with the id after `x2`. [How SumMem works](how-it-works/index.md) walks through the whole cycle.

## Where to go from here

- See how it works: [How It Works](how-it-works/index.md)
- Find out why many writers never conflict: [Why Writers Never Conflict](how-it-works/no-conflicts.md)
- Set it up in a repository: [Quickstart](user-guide/quickstart.md)
- Change SumMem itself: [Architecture](architecture/index.md) and [Contributing](contributing/index.md)
