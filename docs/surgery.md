# Emergency surgery

`surgery.py` is an emergency tool at the SumMem repository root. It is **not** a shipped `summem` command and does not belong in a normal install. Reach for it after a real store mess: a sensitive sentence already in git, a wall of duplicates, a misformatted line.

Agents never `rm` `notes/` or `.tree`. This script is the writer.

## Tip, then history

A traditional history rewrite that purges the original `notes/` blob is not enough. That sentence can still occupy a spot inside a nap `.tree` at the tip. Zoom and recall would still owe it.

1. Run `surgery.py` on the **tip of a branch** so `HEAD` no longer contains the sentence in any store file (`notes/` or remaining `.tree` payloads).
2. Commit that tip.
3. Rewrite git history yourself to purge leftover blobs.

`surgery.py` does step 1 only. It does not rewrite git history.

## What it does

Zipper-shaped whole-note excision:

1. **Break out** until the target is a loose `notes/` file (rematerialize along every view nap whose tree still embeds that filename).
2. **Unlink** that one raw note.
3. **Zip again** with `heal_view` so the remaining view is a unique cover.

It must not write nap captions. It must not delete a nap as if it were a leaf. Identical-text notes are different files: address the one you mean.

## How to run it

From a clone of this repository, with Python 3.11+:

```text
./surgery.py [--path PATH] [--dry-run] --contains TEXT
./surgery.py [--path PATH] [--dry-run] NAME
```

`--path` aims at a started store the same way `summem` does.

`--contains` matches **note text** only (loose or nested). It does not treat a nap caption as a delete target. If two notes share the same text, the match is ambiguous: pass `NAME` (the `notes/` filename, or a unique prefix of it). If both `--contains` and `NAME` are given, `NAME` selects the file and `TEXT` must appear in it.

`--dry-run` prints the rematerialize chain (nap stems in split order, then the note filename) and writes nothing.

## Aftercare

Excision can invalidate captions. `surgery.py` will not nap those back up. Leaving the hole is allowed; the next honest worker will hit a wall of nap requests. It is polite for the surgeon to finish them.

After you commit the clean tip, run an agent in that repository:

1. `.summem/summem wake` (skip if a root wake is already in the conversation).
2. When `note` or the wake listing asks for a nap, `.summem/summem nap` the two adjacent ids with a caption that is true of the **surviving** children. Do not invent filenames. Do not patch `.tree` bytes.
3. Repeat until wake no longer asks.

The files the script writes are part of the work; do not leave them untracked.
