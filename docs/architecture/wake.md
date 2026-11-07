# Wake

`wake` is how memory enters an agent's context. It prints a store's memories, one line per row. The activation block in `AGENTS.md` makes every agent run it once, at the repository root, at the start of a session. `wake` never writes a file, never takes the lock, and never waits on a writer.

!!! note "What `wake` prints is not a list of files"

    It prints the rows of the view, and a row is not a file. Do not expect its output to match `ls` or `git status`.

- A nap is two files and one row. The memories inside a nap have no file of their own.
- When the list is short, `wake` opens some naps in memory and prints their children as rows. Those rows exist only inside a children file. See [Expand](#expand).
- When the store holds more rows than it aims for, `wake` still prints them all.
- Right after a merge, until the next `note` or `nap` [heals](merges-and-healing.md) the store, two rows can hold some of the same memories, or print with the same id.
- Two clones that hold the same memories can print different lists: the same facts, grouped and worded differently.

What does hold: every memory line that `wake` prints comes from a file at the tip of the branch.

## The view

The **view** is every loose note plus every nap in a store, sorted by filename. Each entry is one **row**. A nap counts as a row even when only one of its two files is present.

## Grain

**Grain** is how many original notes a row stands for. A loose note is grain 1. A nap that covers sixteen original notes is grain 16. Grain counts memories, not files.

`wake` reads a nap's grain from its [name](store.md#nap-names), so it can list the row without opening its children file.

## Memory lines

`wake` prints each row as one line. `zoom` and `recall` use the same format.

| Row | Line |
|---|---|
| Note | `x1 2026-11-06: text`, with the UTC day from the filename |
| Nap | `x4 01b18901: caption`, with a unique prefix of the content id and no date |

A nap has no single date, and a range such as `#16-31` would describe one listing and be wrong after the next merge. So rows are named only by content id. Stored ids are 16 hex characters. Each listing prints the shortest prefix that is unique among the ids it can name, at least 8 characters. `nap` and `zoom` accept such a prefix, and reject anything shaped like a position or range.

A nap whose caption is missing or holds conflict markers still prints: its grain and id, with no caption.

A fold request is not a memory line. It quotes the two rows' text only, with no grain or id, and puts the ids on its `Run:` line.

## The wake budget

The **wake budget** (`WAKE_LINES`, 32 by default) is the number of rows the view aims for. It is a target, not a hard cap.

- **Over budget**, every `note` and `nap` asks for the next [fold](folding.md#fold). Writers keep moving the view toward the budget.
- **A merge** can push the view far over budget in one step. `wake` still prints every row, and the next writes fold it back. The view reaches the budget eventually, not immediately.
- **Under budget**, `wake` fills the spare lines by [expanding](#expand) naps in memory. It writes nothing.

`wake` never drops rows to fit the budget, and never refuses to print. "Cannot wake, go nap first" would make every writer wait on someone else's fold.

## Expand

Under budget, `wake` opens the children file of the newest nap that can split, and prints its two children in its place. It repeats until the listing reaches the budget or nothing left will split. After each split it sorts the opened rows by each row's oldest note, so a newer child lands at its own date.

Expansion happens in memory and writes nothing. The expanded rows print with their ids, and `zoom` can open them. `nap` refuses them with `unknown id`, because no file holds them as a row. No fold request ever names one: requests are built from the rows on disk.

A nap whose children file is missing or unreadable does not split, and `wake` says nothing about it.

At or over budget, `wake` lists every row and opens no children file.

## A root wake

A root `wake` prints, in order:

1. `== SumMem Usage ==`: the agent how-to, from the script. A newer script brings a newer how-to without touching `AGENTS.md`.
2. `== Additional SumMem Catalogs ==`: one `N: ./path` line per other store, when there are any. `N` counts the notes in that store's filenames. These lines are not commands; the how-to explains how to load one.
3. `== Project-root Memories ==`: the root store's memory lines, when there are any.
4. `You are up to speed.`

**The root pushes; other stores pull.** Only the root's memories load at session start. Other stores are listed in the catalog and loaded on demand with `wake --path <dir>`, which prints only that store's memory lines: no how-to, no catalog, no header. Loading every store at session start would make a large monorepo's wake unbounded.

The catalog is a walk of the working tree that honors git's ignore rules, built fresh on each root `wake`. It is not a committed index.

Harness hooks are not how memory loads. They may remind an agent, but the activation block and a root `wake` are what load it.
