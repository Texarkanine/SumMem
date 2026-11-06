# Stores and Settings

A **store** is a directory's memory: a `.summem/` folder with notes, naps, and a settings file. Most repositories need only one.

## The root store

The store at the repository root is created on the first `wake`, `note`, `nap`, `zoom`, or `recall`. Until someone starts another store, every note from anywhere in the repository goes there.

The root store is the one agents load at the start of a session, because the block in `AGENTS.md` runs the root `wake`.

## More stores

In a monorepo, or any repository where one directory has its own concerns, give that directory its own store:

```bash
.summem/summem start packages/api
```

`start` creates `packages/api/.summem/config.toml`, and creates the directory too if it does not exist. It prints nothing when it succeeds. Running it on a directory that already has a store changes nothing.

Only the root needs a copy of the script. Every store is used through the root's `.summem/summem`.

### Which store a command uses

A command uses one store. It starts from `--path`, or from the current directory, and walks up toward the repository root. The first directory on the way that has a store is the one it uses.

So, with stores at the root and at `packages/api`:

| Command | Store |
|---|---|
| `.summem/summem note "…"` | root |
| `.summem/summem note --path packages/api/src/db.py "…"` | `packages/api` |
| `.summem/summem note --path packages/web/app.js "…"` | root, because `packages/web` has no store |

Walking up never creates a store. Only the root, and directories you `start`, ever have one.

### How agents find other stores

The root `wake` lists the other stores in a catalog, and its how-to tells agents how to use them:

```text
== Additional SumMem Catalogs ==
1: ./pkg/a
```

`1:` is how many notes that store holds. Agents do not load these stores at the start of a session. When an agent works under one of these paths, the how-to tells it to run `wake --path <path>` for that store, and to record notes there with `note --path <file>`.

The root's memories are pushed into every session. Other stores are pulled only when they are needed. That keeps the start of a session short in a large monorepo.

## Settings

Each store has a committed `config.toml`. A new store gets this template:

```toml
# SumMem per-store settings. Missing values take the script's defaults.
# ENTRY_CHARS = 280
# WAKE_LINES = 32
```

Remove the `#` from a line and change the value to set it for that store.

| Setting | Default | What it controls |
|---|---|---|
| `WAKE_LINES` | 32 | The list's cap. When a store holds more lines than this, `note` and `nap` ask for folds. When it holds fewer, `wake` may open recent naps to fill the space, without changing any file. |
| `ENTRY_CHARS` | 280 | The longest note or nap summary, in bytes of UTF-8. |

A smaller `WAKE_LINES` means a shorter wake and more folding. A larger one keeps more memories word for word, at the cost of a longer wake in every session.

Settings live only in this file. SumMem does not read environment variables for them, and it never rewrites the file once it exists.
