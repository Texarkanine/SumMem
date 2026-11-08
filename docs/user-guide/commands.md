# Commands

Agents run these commands as `.summem/summem <command>`. They learn them from the how-to that root `wake` prints.

```text
summem wake    [--path PATH]                    print this store's view
summem note    [--path PATH] TEXT               record one line
summem nap     [--path PATH] ID-A ID-B CAPTION  fold two ids of the same grain
summem zoom    [--path PATH] ID                 open a nap to its children
summem recall  [--path PATH] PATTERN            search remembered text
summem start <path>                             create a store in that directory
summem init                                     print the agent prompt
summem version                                  print this script's version
```

That table is what `.summem/summem -h` prints. For one command's options, run `.summem/summem <command> -h`.

## Choosing a store with `--path`

Every command except `start`, `init`, and `version` takes `--path`. It names a file or directory. SumMem walks up from there to the nearest directory that has a store, and uses that store. Without `--path`, the walk starts in the current directory.

A repository has one store at its root until someone runs `start`. See [Stores and Settings](stores.md).

## Reading a memory line

`wake`, `zoom`, and `recall` print memories in the same two forms:

| Line | What it is |
|---|---|
| `x1 2026-11-06: Docs build with properdocs.` | A **note**: one memory, with the UTC day it was written. |
| `x2 44cf08be: Test with tox -e py311; ...` | A **nap**: a summary of 2 memories, with its id. |

The number after `x` is the **grain**: how many original notes the line stands for. A nap's id is printed as the shortest prefix that is unique in that list, at least 8 characters long. Copy ids from what SumMem printed. Do not type a line number or a range.

## `wake`

Prints the memory list. Agents run it once, at the start of a session.

At the repository root, `wake` prints up to three sections, then a final line:

```text
== SumMem Usage ==
...how-to for agents...

== Additional SumMem Catalogs ==
1: ./pkg/a

== Project-root Memories ==
x1 2026-11-06: Run tests with tox -e py311.
You are up to speed.
```

- **SumMem Usage** is the how-to for agents. It comes from the script, so a newer script brings a newer how-to.
- **Additional SumMem Catalogs** lists the other stores in the repository, if there are any. `1:` is how many notes that store holds. These lines are not commands.
- **Project-root Memories** is the root store's list. It is left out while the store is empty.

`wake --path <dir>` prints only the nearest store's list for that path, with no how-to and no catalog.

`wake` never changes a file and never refuses to print. If the list is over its wake budget, for example right after a merge, `wake` prints all of it. The next `note` or `nap` folds it back.

## `note TEXT`

Records one line and prints `Saved.`

The text must be a single line, at most 280 bytes of UTF-8 by default. Accented and other non-ASCII characters take 2 or more bytes. The limit is the store's `ENTRY_CHARS` setting.

If the list is now over its wake budget, `note` then asks for a nap:

```text
Saved.

Summarize these two into one line of at most 280 characters.
Keep what has lasting effect, drop what does not. Invent nothing.

  g
  h

Run: .summem/summem nap --path dogfood 3fc87382 fa6da6a9 "<your line>"
```

The `Run:` line is the exact command to run, with the summary in place of `<your line>`. When more than one fold is needed, the request ends with a count of how many remain after this one.

Recording text that the store already holds still prints `Saved.` The store still holds that memory once, not twice.

## `nap ID-A ID-B CAPTION`

Folds two memories into one summary. Use the ids from the `Run:` line, and write a summary of the two lines it quoted. The summary has the same length limit as a note.

```console
$ .summem/summem nap --path dogfood 3fc87382 fa6da6a9 "g & h"
Saved.

Nothing left to compress.
```

After `Saved.`, `nap` prints either the next fold request or `Nothing left to compress.`

SumMem asks for one pair at a time: the oldest memory that has another of the same grain later in the list, with the nearest such memory. `nap` also accepts any other two memories of the same grain with no memory of that grain between them. [Troubleshooting](troubleshooting.md) lists what it refuses.

## `zoom ID`

Opens a nap one level, into the two memories under it:

```console
$ .summem/summem zoom --path dogfood cfbf987a
x1 2026-08-19: g
x1 2026-08-19: h
```

Zoom into a printed child nap to go further down.

## `recall PATTERN`

Searches remembered text with a [Python regular expression](https://docs.python.org/3/library/re.html#regular-expression-syntax). It searches note text and nap summaries, including those inside naps. It does not search the grain, the id, or the date.

```console
$ .summem/summem recall --path dogfood 'c|f'
x4 01b18901: a, b, c, d
x2 abd13ab8: e & f
x2 bbd5a70e: c & d
x1 2026-08-19: c
x1 2026-08-19: f
```

The search is case-sensitive. Start the pattern with `(?i)` to ignore case. No match prints nothing.

## `start <path>`

Creates a store in a directory that already exists. It prints `There is a store in ./path.` whether the store is new or already there, and it does not rewrite an existing config. A path that is not a directory fails with `not a directory: ./path`. See [Stores and Settings](stores.md).

## `init`

Prints the activation block for `AGENTS.md`, with a short instruction above it. See [Quickstart](quickstart.md) and [What to Remember](what-to-remember.md).

## `version`

Prints the script's version, such as `0.12.2`.

## Outside a repository

`wake`, `note`, `nap`, `zoom`, `recall`, and `start` need a git repository, and fail with `not in a repository` outside one. `init`, `version`, and `-h` work anywhere.
