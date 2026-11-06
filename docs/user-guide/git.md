# Working with Git

SumMem's memory is ordinary files in git. It is shared the same way the code is: commits, branches, pull requests, and merges.

## Commit the files with the work

The files SumMem writes are part of the work that produced them. The how-to on `wake` tells agents not to leave them untracked. A memory that is never committed never reaches anyone else.

In a pull request, memory changes look like this:

- **A note** is one new file under `.summem/notes/`, holding one line of text.
- **A nap** adds two files under `.summem/naps/`, a `.summ` and a `.tree` with the same name, and deletes the note or nap files it folded.

Notes are plain text, so review them like any other change. Look for memories that should not be there: personal data, facts about one machine, or news. See [What to Remember](write-rule.md).

## Do not edit store files

Do not edit, rename, or delete files under `.summem/notes/` or `.summem/naps/` by hand, in review or anywhere else. The script is the only writer. Every guarantee SumMem makes depends on that.

- To correct a memory, record a new note that says what is true now.
- To remove a memory that must not exist, use [Emergency Surgery](../advanced/surgery.md).

`config.toml` is the exception. It is yours to edit. See [Stores and Settings](stores.md#settings).

## Merges

Merges do not conflict on memory files, however many agents wrote to the store. [Why Writers Never Conflict](../how-it-works/no-conflicts.md) shows why, with a real merge.

Right after a merge, `wake` can look untidy:

- **Two lines with the same id.** Two branches summarized the same memories in different words.
- **A summary next to part of itself.** One branch folded further than the other, so a nap and a smaller nap of some of the same memories are both listed.
- **More lines than the wake budget.** Both branches added memories.

All three are expected. The next `note` or `nap` on that branch tidies them, and asks for any folds that are needed. Nothing has been lost.

Do not add a custom merge driver or merge strategy for `.summem/`. Git's normal merge is the one SumMem is built for.

## Squash, rebase, and cherry-pick

All of these work. SumMem orders memories by their file names, which hold the time each memory was written. It does not use commit times or `git log`, so rewriting history does not reorder memories.

A squash-merge keeps only the files at the tip of the branch. Those files hold every original memory, so `zoom` and `recall` still work on the result.

## Parallel agents on one machine

Several agents can work in one checkout at once. When two of them change the store at the same moment, a lock on that machine makes the second wait until the first has finished. `wake` never waits.

Agents in separate checkouts or worktrees never wait on each other. Their memories meet when the branches merge, like the rest of their work.
