# What to Remember

The activation block at the top of `AGENTS.md` is how a repository turns SumMem on. It also sets the **write rule**: what agents in this repository should remember. You own that rule and may change it.

## The block

`.summem/summem init` prints the starting block:

```markdown
# Project Memory

Shared memory for this repository is managed through SumMem.

## At Session Start: Activating SumMem (mandatory)

Run `python .summem/summem wake` from the repository root. If you can see a prior project-root SumMem wake in this conversation's history, do not run it again.

## While Working: Register Memories

When something matches the write rule below, record it with SumMem's `note`.

One short line another contributor needs to work on this repository: gotchas, norms, failed approaches, lore and tribal knowledge, etc. Not merely "news" - e.g. that a PR opened, checks passed, or a task completed. Personal, machine-local, and user preference facts stay out. Skip if nothing qualifies or it is already remembered.
```

It has two jobs:

- **At Session Start** tells the agent to wake SumMem once per session. The second sentence stops an agent from loading the memory twice in one conversation.
- **While Working** holds the write rule: the last paragraph.

## Change the write rule

Edit the last paragraph to fit the repository. For example, you might add the kinds of fact your team keeps losing, or name what must never be written down.

Keep the **At Session Start** section as it is. Do not copy command syntax into the block. Agents learn the commands from the how-to that root `wake` prints, and that how-to comes from the script. If the block also explained the commands, a newer script and your copy could disagree.

SumMem never rewrites your block. Copying in a newer script changes the how-to on `wake`, not `AGENTS.md`. To see whether the starting block has changed in a new version, compare your block with what `init` prints.

## What stays out

Everything an agent notes is committed to git. Everyone who can read the repository can read it, and it stays in the history.

So the starting rule keeps these out:

- **Personal facts**, such as people's names or details about their lives.
- **Machine-local facts**, such as a home directory path or "on this machine". These are wrong on every other clone.
- **User preferences**, which belong to one person, not the repository.
- **News**, such as "the PR opened" or "the tests passed". It is true for a moment and then just takes up a line.

The rule also says "one short line another contributor needs". A memory should still be true and useful to someone who clones the repository next year.

If a wrong memory gets in, the normal fix is a new note that corrects it. If a memory must not exist at all, for example because it holds personal data, see [Emergency Surgery](../advanced/surgery.md).
