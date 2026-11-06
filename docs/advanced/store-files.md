# Store Files

This page describes the files in a store, so you can read them when you debug. Do not write them. The script is the only writer: it names files after hashes of their contents, and a hand edit breaks that.

## Layout

```text
.summem/
├── summem            the script (root store only)
├── config.toml       settings for this store
├── notes/            one file per loose note
│   └── 20261106T202132Z-e91a47e5764f37af
└── naps/             two files per nap
    ├── 20261106T202124Z-ff0d65ba54340356-44cf08be43ed30e1-2-cfe9001b6d8f3ed3.summ
    └── 20261106T202124Z-ff0d65ba54340356-44cf08be43ed30e1-2-cfe9001b6d8f3ed3.tree
```

A store started with `start` has the same layout without the script. `__pycache__/` can appear next to the script when Python imports it; ignore it in git.

The **view**, the list that `wake` prints, is every loose note plus every nap, sorted by file name.

## Notes

A note's name is the UTC time it was written, then 16 random hex characters:

```text
20261106T202132Z-e91a47e5764f37af
```

The file holds the note's text and one newline. A note is never edited. When it is folded into a nap, its file is deleted and its text lives on in the nap's `.tree` file.

## Naps

A nap is two files that share a name. The name has five parts:

```text
20260819T213123Z-5e64febd8268823c-cfbf987aa25d8492-2-8f8111f124e6075e
```

1. `20260819T213123Z`: the time of the nap's oldest note.
2. `5e64febd8268823c`: that note's random part.
3. `cfbf987aa25d8492`: the nap's **id**, a hash of the original notes under it. `wake` prints a prefix of it.
4. `2`: the grain, how many original notes the nap stands for.
5. `8f8111f124e6075e`: a hash of the `.tree` and `.summ` contents. Two writers who word a summary differently get different file names here.

The first two parts put the nap where its oldest note sat in the list. [Why It Converges](../how-it-works/theory.md#a-naps-filename) explains why the fields are in this order.

### The `.summ` file

One line: the summary that `wake` prints.

### The `.tree` file

One line of JSON holding the nap's two children. A child is either a note, with its file name and text, or a nap, with its id, its summary, and its own two children. Nesting ends at notes, so the file holds the text of every original note under the nap.

Shown spread out:

```json
{
  "c": [
    {
      "id": "95cfbdf35bf0f5a6",
      "sum": "a & b",
      "tree": {
        "c": [
          {"name": "20260819T213039Z-6a413c0ef89642f7", "text": "a", "type": "note"},
          {"name": "20260819T213041Z-e6b29f4e23f5e9f7", "text": "b", "type": "note"}
        ]
      },
      "type": "nap"
    },
    {
      "id": "bbd5a70eb1da487f",
      "sum": "c & d",
      "tree": {
        "c": [
          {"name": "20260819T213042Z-15df7e536c1292b0", "text": "c", "type": "note"},
          {"name": "20260819T213043Z-1f108ca444236c2c", "text": "d", "type": "note"}
        ]
      },
      "type": "nap"
    }
  ]
}
```

To read one, use a JSON tool such as [`jq`](https://jqlang.org/). For example, this prints every original note under a nap:

```bash
jq -r '.. | objects | select(.type == "note") | .text' .summem/naps/<name>.tree
```

## Ids

A nap's id is the first 16 hex characters of a SHA-256 hash. SumMem hashes each original note file, sorts those hashes, joins them, and hashes the result. The id depends only on which notes are under the nap. It does not depend on the summary's words or on how the notes were grouped. [Architecture](../architecture/index.md#identity) has the exact rules.

Two notes with the same text have the same hash, so the store keeps only one of them.

## What is not in the store

- **No index.** Nothing lists the files. The file names and their contents are all there is.
- **No lock file.** The lock that stops two writes at once on one machine is held on the `naps/` folder, or on a file outside the repository. It is never committed.
- **No history.** SumMem never reads git history. Everything `zoom` and `recall` need is in the files at the tip of the branch.
