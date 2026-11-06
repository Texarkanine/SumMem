# Upgrading

SumMem is one file. To upgrade, replace it.

## Replace the script

1. Copy the newer [`summem`](https://github.com/Texarkanine/SumMem/blob/main/summem) over `.summem/summem` in the repository root, as in the [Quickstart](quickstart.md#set-up-a-repository).
2. Check the version:

    ```bash
    .summem/summem version
    ```

3. Commit the new script.

Only the root has a copy of the script, so there is nothing to update in other stores.

You can skip versions: install the newest script over any older one. If the store has naps in an older format, rewrite them as described in [Older nap files](#older-nap-files).

## What changes for agents

The how-to that root `wake` prints comes from the script, so agents pick up new instructions in their next session.

Your activation block in `AGENTS.md` does not change. To see whether the starting block is different in the new version, compare your block with what `.summem/summem init` prints. If you want the change, copy it in by hand, and keep your own edits to the write rule.

## Older nap files

Some releases changed the format of nap file names. The script does not read naps whose names are in an older format: they disappear from `wake` until they are rewritten. Notes are not affected.

Look at the nap names in each `.summem/naps/` folder. A current name has five parts separated by `-`, and the third part is 16 hex characters:

```text
20260819T213123Z-5e64febd8268823c-cfbf987aa25d8492-2-8f8111f124e6075e.tree
```

If any name has four parts, or a 64-character third part, rewrite them with `migrate.py`. It is in the SumMem repository and is not part of an install.

1. Clone the SumMem repository, at the release you are installing.
2. From your repository's root, run its `migrate.py` with Python 3.11 or newer:

    ```bash
    python /path/to/SumMem/migrate.py
    ```

    It rewrites old naps in every store in the repository. To rewrite only one store, add `--path <dir>`. It prints nothing when there is nothing to rewrite.

3. Check that `wake` lists the naps again, then commit the result.

`migrate.py` loads the `summem` script next to it in the clone, so use the clone that matches the script you installed. Do not rename nap files by hand: the new names hold hashes of the files' contents.
