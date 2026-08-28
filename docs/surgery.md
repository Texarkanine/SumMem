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
./surgery.py version
./surgery.py [--path PATH] [--dry-run] --contains TEXT
./surgery.py [--path PATH] [--dry-run] NAME
```

`./surgery.py version` prints the same string as `summem version`. They advance in lockstep. Prefer a surgery that matches your `summem`, or a newer surgery; do not use an older surgery on a newer `summem`. This is not enforced — compare the two prints.

`--path` aims at a started store the same way `summem` does.

`--contains` matches **note text** only (loose or nested). It does not treat a nap caption as a delete target. If two notes share the same text, the match is ambiguous: pass `NAME` (the `notes/` filename, or a unique prefix of it). If both `--contains` and `NAME` are given, `NAME` selects the file and `TEXT` must appear in it.

`--dry-run` prints the rematerialize chain (nap stems in split order, then the note filename) and writes nothing. It does not print a fold request.

## Aftercare

Excision can invalidate captions. `surgery.py` will not nap those back up. After a real excision (not `--dry-run`), if the view is still over budget, stdout includes the same first fold request `note` would print (`Compress these two` / `Run: .summem/summem nap …`). Feed that to an agent; each successful `nap` prints `Saved.` then either the next pair or `Nothing left to compress.` `wake` does not demand a nap, so without this print you would have to `note` something else to start the cascade.

Leaving the hole is allowed; the next honest `note` will also print a fold request. It is polite for the surgeon to finish the naps.

After you commit the clean tip, run an agent in that repository:

1. If surgery printed a fold request, feed that `Run:` line to the agent (or run it yourself). Caption the surviving children. Do not invent filenames. Do not patch `.tree` bytes.
2. Each `nap` prints `Saved.` then either the next pair or `Nothing left to compress.` Repeat until the idle line.
3. `.summem/summem wake` still shows the view; it will not demand a nap.

The files the script writes are part of the work; do not leave them untracked.
