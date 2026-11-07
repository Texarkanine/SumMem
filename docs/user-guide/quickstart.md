# Quickstart

Set up SumMem in a repository in a few minutes.

## Prerequisites

- A git repository.
- **Python 3.11 or newer, as a requirement of your repository.** Every agent that works in the repository runs SumMem, on whatever machine it runs on. That includes other contributors' machines and CI. So everyone who works on the repository needs Python 3.11 or newer, available as both `python` and `python3`: the activation block runs `python .summem/summem wake`, and the script's first line asks for `python3`. If your repository does not already require Python 3.11, add it to the prerequisites in your contributing guide.
- Agents that read `AGENTS.md` and can run shell commands.

## Set up a repository

1. Put the [`summem`](https://github.com/Texarkanine/SumMem/blob/main/summem) script at `.summem/summem`, in the root of your repository, and make it executable:

    ```bash
    mkdir -p .summem
    curl -fsSL https://raw.githubusercontent.com/Texarkanine/SumMem/main/summem -o .summem/summem
    chmod +x .summem/summem
    ```

    To install a particular release, replace `main` in the URL with its tag from [Releases](https://github.com/Texarkanine/SumMem/releases).

2. Print the activation block:

    ```bash
    .summem/summem init
    ```

    `init` prints a short instruction, a `---` line, and then the block. Put everything below the `---` at the top of `AGENTS.md`. The block tells agents to wake SumMem at the start of each session, and says what this repository remembers. You may change what it remembers: see [What to Remember](what-to-remember.md).

    If your repository also has a `CLAUDE.md`, you do not need to copy the block into it. Put `@AGENTS.md` at the top of `CLAUDE.md` to import `AGENTS.md` instead, so both files share one copy.

3. Add this line to `.gitignore`:

    ```gitignore
    **/.summem/__pycache__/
    ```

4. Commit `.summem/summem`, `AGENTS.md`, and `.gitignore`.

The first `wake`, `note`, `nap`, `zoom`, or `recall` creates the store: `.summem/config.toml`, plus `.summem/notes/` and `.summem/naps/` for the memories. Commit those files as they appear.

## Check that it works

```console
$ .summem/summem wake
== SumMem Usage ==

`.summem/summem note "…"` records one short line.
...
You are up to speed.
```

A new store prints only the how-to and the last line. Start a new agent session. The agent should run the wake by itself, because `AGENTS.md` tells it to. After it records its first note, `wake` also prints a `== Project-root Memories ==` section.

## Optional: more stores

In a monorepo, `.summem/summem start packages/api` gives that directory its own memory. See [Stores and Settings](stores.md).

## What next

- [Commands](commands.md): what each command does and prints.
- [What to Remember](what-to-remember.md): change what the repository remembers.
- [Working with Git](git.md): what memory looks like in commits and pull requests.
