# Troubleshooting

## Things that look wrong but are not

| What you see | Why |
|---|---|
| `start` printed nothing. | That is success. Check with root `wake`: the new store appears in the catalog. |
| Two `wake` lines have the same id. | Two branches summarized the same memories in different words. The next `note` or `nap` keeps one. See [Working with Git](git.md#merges). |
| `wake` prints more lines than `WAKE_LINES`. | Usually right after a merge. `wake` never drops lines. The next `note` or `nap` asks for folds until the list fits. |
| An agent noted something the store already had, and still got `Saved.` | The store holds each memory once, so it removed one of the two files. The memory was not lost. |
| `wake` shows fewer naps after an upgrade. | The naps have names in an older format. See [Upgrading](upgrading.md#older-nap-files). |
| `recall` printed nothing. | No match. `recall` is case-sensitive; start the pattern with `(?i)` to ignore case. |

## Agents do not use SumMem

- **The block is not at the top of `AGENTS.md`.** Put the block that `init` prints at the very top. See [Quickstart](quickstart.md).
- **The agent only reads some other instructions file.** Import `AGENTS.md` from that file, for example with `@AGENTS.md` at the top of `CLAUDE.md`, or copy the block there.
- **The agent's tool will not run the command.** Some agent tools ask before running a command, or block commands they do not know. Allow `python .summem/summem` and `.summem/summem`.
- **Python is too old.** See `SumMem needs Python 3.11 or newer` below.

## Memory files were left out of a commit

Agents are told to commit the files SumMem writes, but they can miss some. Check `git status` for untracked files under `.summem/`, and commit them with the work they belong to.

## Error messages

Error messages go to standard error, and the command exits with a non-zero status. Most are meant for the agent, and say what to do next.

| Message | Command | Meaning |
|---|---|---|
| `SumMem needs Python 3.11 or newer` | any | The Python that ran the script is older than 3.11. Both `python` and `python3` must be 3.11 or newer. |
| `not in a repository` | `wake`, `note`, `nap`, `zoom`, `recall`, `start` | The command ran outside a git repository. |
| `Too long: N bytes, limit L. …` | `note`, `nap` | The text is longer than the store's `ENTRY_CHARS`, counted in bytes of UTF-8. |
| `One line only. Merge the lines.` | `note`, `nap` | The text has a line break. |
| `note is empty` | `note`, `nap` | There is no text. |
| `unknown id. Copy an id from wake.` | `nap`, `zoom` | No line in the current list has that id. After a merge, the next write may have tidied that line away; run `wake` again for current ids. |
| `ambiguous id. Give a longer prefix.` | `nap`, `zoom` | More than one id starts with what was typed. |
| `not a content id: …. Copy an id from wake.` | `nap`, `zoom` | What was typed is not an id. Line numbers and ranges such as `0-3` are not ids. |
| `not two rows` | `nap` | The two ids name the same line. |
| `not the same grain` | `nap` | The two lines stand for different numbers of notes. Use the ids from the `Run:` line. |
| `not a power of two` | `nap` | Folding these two would make a nap whose grain is not 2, 4, 8, and so on. Use the ids from the `Run:` line. |
| `a nearer row of that grain sits between them` | `nap` | The fold must use the nearest line of that grain. Use the ids from the `Run:` line. |
| `overlapping packs` | `nap` | The two lines share some of the same memories. |
| `unknown id` | `nap`, `zoom` | The nap's `.tree` file is missing, so it cannot be folded or opened. Check whether it was left out of a commit. |
| `unreadable pack` | `nap`, `zoom` | The nap's `.tree` file is not in the expected format, usually because it was edited by hand. Restore the committed version from git. |
| `skipped a pack` | `zoom`, `recall` | One nap's `.tree` file could not be read. The other results are still printed. |
| `invalid pattern` | `recall` | The pattern is not a valid regular expression. |
| `cannot lock` | `note`, `nap` | SumMem could not take the lock on this machine. Run the command again. |
