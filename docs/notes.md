# Notes

Things that are not true of the tree yet, and that we did not replace with a different design. Not a backlog contract.

## Not this backend

- A second on-disk backend (sqlite or otherwise). The agent commands stay the same if that happens. Store roles in [Architecture](architecture/index.md) must still exist.
- Harness hooks as the way memory loads. They may nag. Session start is still the `AGENTS.md` prompt and a root `wake`.

## Not this fold

- OptMem’s aligned `cover(T)` after merge: tile the sorted leaf sequence with aligned power-of-two blocks and rebuild `[0, 8192)` over interleaved pasts. This backend requests equal-grain adjacent **view nodes** and may expand a nap in memory when the view is short. After a long-lived merge it does not re-cover.
- A pack-size cap: never fold past *N* original notes per `.tree` (256 was a reasonable first *N*). View-node **count** stays on the order of `WAKE_LINES`. File **size** is where lifetime `T` shows up. GitHub warns around 50–100 MB; at ~280 bytes per note that is hundreds of thousands of notes in one block.
- Hot margin: how close to “now” a block may be before the script will nap it. The script has `ENTRY_CHARS` and `WAKE_LINES` only. Nap of a sealed pair is the agent’s job when the fold request prints.
