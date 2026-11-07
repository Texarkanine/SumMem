# Not Yet

Things that are not true of SumMem yet, and that were not replaced with a different design. This is not a backlog or a promise.

## Not this backend

- A second on-disk backend, such as SQLite. If that happens, the agent commands stay the same, and every store role in [Architecture](index.md) must still exist.
- Harness hooks as the way memory loads. Hooks may remind. Session start is still the activation block in `AGENTS.md` and a root `wake`.

## Not this host

- Native Windows as a supported host. There is no clone-portable command that both `cmd.exe` and a Unix shell will run. The committed first wake is `python .summem/summem wake`. Root-wake Usage and `Run:` lines are host-specific: bare `.summem/summem` on Unix, `python .summem/summem` on Windows. Spec: [windows-compat-audit](https://github.com/Texarkanine/SumMem/blob/main/memory-bank/archive/enhancements/20260909-windows-compat-audit.md). Its Unix-only `AGENTS.md` wake and `sys.executable` recipes are superseded.

## Not this fold

- **Re-grouping after a merge.** After a long-lived merge, SumMem keeps whatever grouping the merge left, heals overlaps, and folds forward oldest pair first. It does not rebuild one canonical grouping of all notes, such as aligned power-of-two blocks over the notes in time order. [Why Memories Converge](../how-it-works/why-memories-converge.md#what-does-not-converge) argues why leaving the grouping unconverged is safe.
- **A nap size cap**: never fold past *N* original notes in one children file (256 was a reasonable first *N*). The number of rows stays near `WAKE_LINES`; the size of the oldest children file is where a store's lifetime shows up. GitHub warns at around 50–100 MB per file. At about 280 bytes per note, that is hundreds of thousands of notes in one nap.
- **A hot margin**: how close to "now" a block may be before the script will fold it. The script has only `ENTRY_CHARS` and `WAKE_LINES`. Folding a requested pair is the agent's job when the fold request prints.
