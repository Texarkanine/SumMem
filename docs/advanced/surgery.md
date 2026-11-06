# Emergency Surgery

`surgery.py` removes one note from a store. Use it when a memory must not exist at all: personal data already in git, a wall of duplicates, or a badly formatted line. For a memory that is only wrong, record a new note that corrects it instead.

`surgery.py` is in the root of the SumMem repository. It is not a `summem` command and is not part of an install. Do not delete store files by hand instead: the script is the only writer.

## Clean the tip, then the history

Deleting the note's file is not enough. Its text can also sit inside the `.tree` file of any nap that folded it, and `zoom` and `recall` would still find it there.

1. Run `surgery.py` on the **tip of a branch**, so that no store file at the tip holds the text any more.
2. Commit that tip.
3. If the text must also leave git history, rewrite the history yourself. GitHub's guide [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) covers the tools and the steps.

`surgery.py` does step 1 only. It never rewrites git history.

## What it does

1. **Opens naps.** Every nap whose `.tree` holds the note is opened into its children, from the top down, until the note is a loose file in `notes/` again. Opening a nap removes the nap and its summary.
2. **Deletes the note.** It removes that one note file.
3. **Tidies the list.** It runs the same repair that follows a merge, so no two lines in the list share a memory.

It never writes a summary, and it never deletes a nap as if it were a note. Notes with the same text are still separate files: name the one you mean.

## Run it

You need a clone of the SumMem repository and Python 3.11 or newer. Run it from the root of the repository you are repairing:

```text
python /path/to/SumMem/surgery.py version
python /path/to/SumMem/surgery.py [--path PATH] [--dry-run] --contains TEXT
python /path/to/SumMem/surgery.py [--path PATH] [--dry-run] NAME
```

- **`--contains TEXT`** picks the note whose text contains `TEXT`. It searches note text only, loose or inside naps, never nap summaries. If more than one note matches, give `NAME` instead.
- **`NAME`** is the note's file name in `notes/`, or a unique prefix of it. If you give both, `NAME` picks the file and its text must contain `TEXT`.
- **`--path`** picks the store, the same way it does for `summem`.
- **`--dry-run`** prints what it would do and changes nothing.

Always start with `--dry-run`. It prints each nap it would open, in order, then the note it would delete. Here, in the `dogfood` store after the walk on [How SumMem Works](../how-it-works/index.md#a-walk-through-one-store), the note `g` sits inside the `g & h` nap:

```console
$ python /path/to/SumMem/surgery.py --path dogfood --dry-run --contains g
20260819T213123Z-5e64febd8268823c-cfbf987aa25d8492-2-8f8111f124e6075e
20260819T213123Z-5e64febd8268823c
```

`surgery.py version` prints the same version string as `summem version`; the two are released together. Use a `surgery.py` at least as new as your `summem`. Nothing checks this for you, so compare the two.

## Aftercare

Opening naps removes their summaries and leaves more lines in the list. `surgery.py` does not write new summaries.

If the list is now over its wake budget, `surgery.py` ends by printing the same fold request that `note` would print, with a `Run:` line. `wake` does not ask for folds, so this is the easiest way to start them. After you commit the clean tip:

1. Give the `Run:` line to an agent, or run it yourself with a summary of the two quoted lines.
2. Each `nap` prints `Saved.`, then the next request or `Nothing left to compress.` Repeat until it says `Nothing left to compress.`
3. Commit the new files.

You may also leave the extra lines. The next `note` will ask for the same folds.

Then check that the text is gone. This should print nothing:

```bash
.summem/summem recall 'the removed text'
```
