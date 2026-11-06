# The Store

A **store** is a `.summem/` directory of immutable files: notes, naps, and one settings file. Every fact the store can produce is spelled out in one of those files at the tip of the branch.

## Why the store is files

Two writers who each learned a fact must be able to record it at the same time, on different machines, without a shared counter or a lock that spans clones. Two new files is a merge git already knows how to do. One append-only log with a next id is not: both writers pick the same next slot.

Git is also not a clock, and not an archive of deleted sentences. A squash-merge keeps only the files that exist at the branch tip. Anything a later `zoom` must still see has to be in one of those files.

So SumMem has no primary writer. It has files, and a listing of the facts in those files that gets shorter as the facts age. That listing is the [view](view-and-folding.md#the-view).

## Notes

A **note** is one immutable file holding one line of text, up to the store's length limit. There is no edit. A retraction is a new note. Rewriting a note is the one way to create a real content conflict, and the script never does it.

The filename is the writer's time in UTC plus 16 random hex characters. Sorting by filename is the order. Git-add date, squash commit time, and `git log` are the wrong clock.

A note is written to a temporary path and renamed into place.

## Naps

A **nap** stands for two view rows of the same grain, with a one-line summary. It is two files that share a name:

- The **caption** (`.summ`) is the summary: one line, with the same length limit as a note. `wake` prints it.
- The **children file** (`.tree`) holds the two rows it replaced, down to the text of every original note. `zoom` and deep `recall` read it.

The shared name has five parts:

1. The UTC time of the nap's oldest note.
2. That note's random suffix.
3. The 16-hex **content id** of the notes the nap stands for.
4. The grain.
5. A 16-hex **variant tag**: a hash of the children file's bytes and the caption's bytes.

The first two parts make the nap sort where its oldest note sorted, not at the time of the fold. Agents never see or type the variant tag. The public id is the third part.

A fold writes the new nap first, then removes its two children. The children leave the working tree only after the nap's children file exists on disk.

Names in two older formats are not read at all: four parts, or five parts whose third part is 64 hex. `migrate.py` rewrites both, along with the ids nested in their children files. See [Upgrading](../user-guide/upgrading.md#older-nap-files).

## Identity

A row's **content id** is a hash of the original notes it stands for, never of its caption.

1. Hash each original note's file bytes with SHA-256.
2. Sort those hashes and join them with no delimiter.
3. Hash the join, and keep the first 16 hex characters. That is the **leaf-set id**, the content id that names the row.

The script computes both hashes itself, with the Python standard library. It does not shell out, and it does not use git's hasher: either would change the id when the machine or the repository's hash function changes.

Two notes with the same text have the same id. They are one fact. [Merges and Healing](healing.md#same-text) keeps one file.

## The children file

The children file is a JSON document holding exactly two children. A child is either a note, with its filename and text, or a nap, with its content id, its caption, and that nap's own two children. Nesting stops at notes.

Folding equal grains builds a balanced binary tree, so 2048 original notes are eleven naps deep. Every original sentence still lives in that one file: the file grows with grain, not deeper without bound.

Unknown fields are ignored. A child with a missing or unknown kind is an error; the kind is never guessed from other keys. There is no version field.

The document is deterministic. The same children in the same order, with the same nested captions and grouping, dump to the same bytes. The converse does not hold: the same content id, folded in a different grouping or with different nested captions, gives different bytes, and so a different variant tag.

## Settings

Each store has a committed `config.toml` with two settings: the length limit (`ENTRY_CHARS`) and the [wake budget](view-and-folding.md#the-wake-budget) (`WAKE_LINES`). Missing values use the script's defaults.

Settings are not environment variables. The script writes the file only when it is missing, so `start` on an existing store leaves it alone.

## More than one store

A command uses **one** store. It walks from the work path, `--path` or the current directory, toward the git root, and takes the first directory that already has a store. A work path that is a file starts the walk at its directory.

The git root gets a store on the first store command. Every other store is created with `start`. The script never parses workspace manifests, and walking up never creates a store, so an empty package stays empty even when someone records a note from deep inside it.

How other stores reach an agent is in [Reading](reading.md#wake).
