# Reading

Three commands read a store: `wake` lists it, `zoom` opens one nap, and `recall` searches it. None of them writes a file, takes the lock, or waits on a writer.

## Wake

`wake` is how memory enters an agent's context. The activation block in `AGENTS.md` makes the agent run it once, at the repository root, at the start of a session. Harness hooks are not the load mechanism; they may remind, but the activation block and a root `wake` are what loads memory.

A root `wake` prints, in order:

1. `== SumMem Usage ==`: the agent how-to, from the script. A newer script brings a newer how-to without touching `AGENTS.md`.
2. `== Additional SumMem Catalogs ==`: one `N: ./path` line per other store, when there are any. `N` counts the notes in that store's filenames. These lines are not commands; the how-to explains how to pull one.
3. `== Project-root Memories ==`: the root store's view, when it is not empty.
4. `You are up to speed.`

**The root pushes; other stores pull.** Only the root's memories load at session start. Other stores are advertised in the catalog and loaded on demand with `wake --path <dir>`, which prints only that store's view: no how-to, no catalog, no header. Loading every store at session start would make a large monorepo's wake unbounded.

The catalog is a walk of the working tree that honors git's ignore rules, built fresh on each root `wake`. It is not a committed index.

`wake` never blocks and never refuses to print. Over budget it lists every row. A missing or conflict-marked caption prints its grain and id with no caption. A broken children file only stops that row from [expanding](view-and-folding.md#expand), silently.

## Memory lines

`wake`, `zoom`, and `recall` print rows in one format:

| Row | Line |
|---|---|
| Note | `x1 2026-11-06: text`, with the UTC day from the filename |
| Nap | `x4 01b18901: caption`, with a unique prefix of the content id and no date |

A nap has no single date, and a range such as `#16-31` would describe one listing and be wrong after the next merge. So rows are named only by content id. Stored ids are 16 hex characters. Each listing prints the shortest prefix that is unique among the ids it can name, at least 8 characters. `nap` and `zoom` accept such a prefix, and reject anything shaped like a position or range.

A fold request is different: it quotes the two rows' text only, with no grain or id, and puts the ids on its `Run:` line.

## Zoom

`zoom <id>` prints the two children of one nap, one level down. The id may be a view row or a nap nested inside one, so repeated zooms walk down to the notes.

Zoom reads only children files in the current checkout. Every sentence a zoom can still owe is in a file at the tip, so squash-merges and shallow clones lose nothing, and an older commit is never consulted.

## Recall

`recall <pattern>` searches with a regular expression. It matches the text of notes and the captions of naps, including notes and captions nested inside children files. It does not match a row's grain, id, or date.

So the view answers everyday questions with captions standing in for their children, and `recall` reaches the original sentences when a caption is not enough.

## Unreadable children files

`zoom` and `recall` read children files. When one cannot be read, they print `skipped a pack` once on standard error and still print whatever other naps answered. `wake` stays silent about it.

## Cost

`zoom` and `recall` parse each view children file at most once per command. They work out unique prefixes once per command: they sort the distinct ids and compare each with its neighbors, so printing a line is a lookup. Uniqueness is among distinct ids, so two rows that share an id still share one prefix.
