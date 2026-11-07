# The Store

A **store** is a `.summem/` directory of immutable files: notes, naps, and one settings file. Every fact the store can produce is spelled out in one of those files at the tip of the branch.

## Why the store is files

Two writers who each learned a fact must be able to record it at the same time, on different machines, without a shared counter or a lock that spans clones. Two new files is a merge git already knows how to do. One append-only log with a next id is not: both writers pick the same next slot.

Git is also not a clock, and not an archive of deleted sentences. A squash-merge keeps only the files that exist at the branch tip. Anything a later `zoom` must still see has to be in one of those files.

So SumMem has no primary writer. It has files, and a listing of the facts in those files that gets shorter as the facts age. That listing is the [view](wake.md#the-view).

## Notes

A **note** is one immutable file holding one line of text, up to the store's length limit. There is no edit. A retraction is a new note. Rewriting a note is the one way to create a real content conflict, and the script never does it.

The filename is the writer's time in UTC plus 16 random hex characters. Sorting by filename is the order. Git-add date, squash commit time, and `git log` are the wrong clock.

A note is written to a temporary path and renamed into place.

## Naps

A **nap** stands for two view rows of the same grain, with a one-line summary. It is two files that share a name:

- The **caption** (`.summ`) is the summary: one line, with the same length limit as a note. `wake` prints it.
- The **children file** (`.tree`) holds the two rows it replaced, down to the text of every original note. `zoom` and deep `recall` read it.

A fold writes the new nap first, then removes the files of the two rows it replaced. Those files leave the working tree only after the nap's children file, which holds their memories, exists on disk.

## Nap names

A nap's name does two jobs. It holds everything `wake` needs to list the nap without opening its children file. And it changes whenever the nap's bytes change, so two writers never write different bytes to one path.

```text
20260819T213123Z-5e64febd8268823c-cfbf987aa25d8492-2-8f8111f124e6075e
```

| | Field | Why it is in the name |
|---|---|---|
| 1 | `20260819T213123Z`, the UTC time of the nap's oldest note | Sorting by name is the order. The nap sorts where its oldest note sorted, not at the time of the fold. |
| 2 | `5e64febd8268823c`, that note's random suffix | Notes from the same second keep their order, and the nap sorts exactly where its oldest note did. |
| 3 | `cfbf987aa25d8492`, the **content id** | The public id: `wake` prints a prefix of it, and `nap` and `zoom` take one. It comes from the notes alone, so two writers who fold the same notes name the same id. See [Identity](#identity). |
| 4 | `2`, the grain | `wake` prints `x2` without opening the children file. Folding does not trust this field: it counts the notes in the children file. |
| 5 | `8f8111f124e6075e`, the **variant tag** | A hash of the children file's bytes and the caption's bytes. Agents never see or type it. |

Fields 1 to 4 are fixed by which notes the nap holds. Only the variant tag differs between two naps of the same notes, and it differs exactly when their bytes do:

- Two writers who write the same nap, byte for byte, write the same path. Git sees one file.
- Two writers who fold the same notes with different captions write two paths. At grain 4 and above, different nested captions or a different grouping also change the children file, and so the tag. Git keeps both files without a conflict.

The next heal keeps the nap whose name sorts last ([Same content id](merges-and-healing.md#same-content-id)). The two names differ only in the variant tag, and the tag is a hash of each nap's files. So sorting the names compares hashes of what the naps contain. The survivor does not depend on which writer was first or which branch merged last, and every clone that has both naps keeps the same one. [Why It Converges](../how-it-works/why-it-converges.md#a-max-register-for-captions) shows why that choice is safe.

### How the name got here

Each change below broke stores written before it.

| Release | Change | Why |
|---|---|---|
| 0.7.0 | Captions renamed from `.sum` to `.summ` ([#47](https://github.com/Texarkanine/SumMem/issues/47)) | `.sum` is a common suffix for checksum files. |
| 0.8.0 | Variant tag added, from four fields to five ([#61](https://github.com/Texarkanine/SumMem/issues/61)) | With four fields, two writers who folded the same notes with different captions wrote different bytes to one path. Git reported an add/add conflict on `.summ`, and at grain 4 and above on `.tree` too. Resolving the two files from different sides left a caption that did not describe its children. |
| 0.9.0 | Content id shortened from 64 hex to 16 ([#67](https://github.com/Texarkanine/SumMem/issues/67)) | A grain-2 name was 122 characters, too long for some file systems once a clone sits deep in a directory tree: eCryptfs allows about 143 bytes per name, and Windows drives traditionally 260 characters per path. 16 hex is 64 bits; a 1% chance of any collision in one store takes about 600 million ids. |

The script does not read the older names at all. `migrate.py` rewrites four-field names and 64-hex ids, including the ids nested in children files: see [Upgrading](../user-guide/upgrading.md#older-nap-files). The `.sum` rename was a one-line `find` in the 0.7.0 release notes.

## Identity

A row's **content id** is a hash of the original notes it stands for, never of its caption.

1. Hash each original note's file bytes with SHA-256.
2. Sort those hashes and join them with no delimiter.
3. Hash the join, and keep the first 16 hex characters. That is the **leaf-set id**, the content id that names the row.

The script computes both hashes itself, with the Python standard library. It does not shell out, and it does not use git's hasher: either would change the id when the machine or the repository's hash function changes.

Two notes with the same text have the same id. They are one memory, and [heal](merges-and-healing.md#a-note-held-twice) leaves it in one row.

## The children file

The children file is a JSON document holding exactly two children. A child is either a note, with its filename and text, or a nap, with its content id, its caption, and that nap's own two children. Nesting stops at notes.

Folding equal grains builds a balanced binary tree, so 2048 original notes are eleven naps deep. Every original sentence still lives in that one file: the file grows with grain, not deeper without bound.

Unknown fields are ignored. A child with a missing or unknown kind is an error; the kind is never guessed from other keys. There is no version field.

The document is deterministic. The same children in the same order, with the same nested captions and grouping, dump to the same bytes. The converse does not hold: the same content id, folded in a different grouping or with different nested captions, gives different bytes, and so a different variant tag.

## Settings

Each store has a committed `config.toml` with two settings: the length limit (`ENTRY_CHARS`) and the [wake budget](wake.md#the-wake-budget) (`WAKE_LINES`). Missing values use the script's defaults.

Settings are not environment variables. The script writes the file only when it is missing, so `start` on an existing store leaves it alone.

## More than one store

A command uses **one** store. It walks from the work path, `--path` or the current directory, toward the git root, and takes the first directory that already has a store. A work path that is a file starts the walk at its directory.

The git root gets a store on the first store command. Every other store is created with `start`. The script never parses workspace manifests, and walking up never creates a store, so an empty package stays empty even when someone records a note from deep inside it.

Agents learn about the other stores from the catalog in a [root wake](wake.md#a-root-wake).
