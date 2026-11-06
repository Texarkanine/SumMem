# The View and Folding

The store only grows. What an agent reads must not. The **view** is the listing `wake` prints, and **folding** keeps it near a fixed length by replacing two old rows with one nap.

## The view

The **view** is every loose note plus every nap in a store, sorted by filename. Each entry is one **view row**. A nap is two files and still one row. A nap counts as a row even when only one of its two files is present.

A row whose caption is missing or holds conflict markers still lists: its grain and id print, its caption does not. A row whose children file is missing or unreadable will not split.

## Grain

**Grain** is how many original notes a row stands for. A loose note is grain 1. A nap that covers sixteen original notes is grain 16.

Grain is the only size folding cares about. It is not the number of files.

`wake` prints the grain from the nap's filename. Folding counts the notes in the children file instead, and trusts that count even when the filename disagrees. A loose note is always grain 1, and the fold scan never opens its file.

## The wake budget

The **wake budget** (`WAKE_LINES`, 32 by default) is the number of view rows SumMem aims for. It is a target, not a hard cap.

- **Over budget**, every `note` and `nap` asks for the next fold. Writers keep moving the view toward the budget.
- **A merge** can push the view far over budget in one step. `wake` still prints every row, and the next writes fold it back. The view reaches the budget eventually, not immediately.
- **Under budget**, `wake` fills the spare lines by [expanding](#expand) naps in memory. It writes nothing.

`wake` never drops rows to fit the budget, and never refuses to print. "Cannot wake, go nap first" would make every writer wait on someone else's fold.

## Fold

```mermaid
flowchart TD
    Note["note: write a new file"] --> Over{"View over budget?"}
    Nap["nap: write the nap, then remove its children"] --> Over
    Over -->|yes| Pair["Request the oldest same-grain pair"]
    Over -->|no| Done["No request"]
```

When a write leaves the view over budget, the script requests one fold. The pair is:

- the **oldest** row whose grain is a power of two and that has another row of that grain anywhere later in the listing,
- paired with the **nearest** such later row.

The two rows need not be neighbors. The request quotes the two rows' text and prints a `Run:` line with their ids. The agent supplies the caption. `nap` writes the new nap, removes the two children, and, if the view is still over budget, requests the next pair.

`nap` accepts any pair that obeys the same rule, and refuses the rest:

- two rows whose notes overlap: `overlapping packs` (overlap is [healing's](healing.md) job);
- unequal grains: `not the same grain`;
- a grain that would not be a power of two: `not a power of two`;
- a same-grain row between them: `a nearer row of that grain sits between them`.

Every nap the script writes has a power-of-two grain. Folding never glues a sealed block to a single leftover note: an `x16` next to one `x1` waits for another `x1`.

Fold always removes the children. It does not keep them on disk because `wake` might expand them later.

### Rows that never fold

Two kinds of row stay listed but are never requested, and never count as the nearer row of their grain:

- a nap whose grain is not a power of two, written by an older driver;
- a nap whose children file is missing or unreadable, because `nap` could not fold it.

Without this, oldest-pair-first would request the same broken row on every `note`, and folding would stop.

## Walls

A **wall** is an older row sitting before a bigger, newer one, such as an `x1` before an `x4`.

One writer never builds a wall. Grains only fall from older rows to newer ones, each grain of 2 or more appears at most twice, and the oldest row with a twin is always the oldest pair of neighbors.

A merge builds them easily. Say `main` holds `x8 x4 x2 x1`. Two branches that never saw that `x1` each record and fold later notes. After the merge and the next folds:

```mermaid
flowchart LR
    classDef row fill:#f3e5f5,stroke:#7b1fa2;
    classDef stuck fill:#ffebee,stroke:#c62828;

    A["x8"]:::row --- B["x4"]:::row --- C["x2"]:::row --- D["x1"]:::stuck --- E["x4"]:::row
```

A late note stamped before an existing nap, a zipper reopen, [surgery](../advanced/surgery.md), or an old odd-grain nap can build the same shape.

A rule that only folds neighbors can never fold across a wall. The `x1` never meets another `x1`, because new notes land at the end and the `x4` after it only grows. That row and every older row stay in the view forever, over budget, with no request. Skipping to the nearest same-grain row is what lets these views heal.

### Why oldest pair first

Six rules were simulated on the real driver: 4 writers, 1,500 notes, merges after 8% of notes, budget 32, two seeds.

| Rule | Result |
|---|---|
| Neighbors only (the old rule) | Stalled over budget after most merges. |
| Fold unequal grains | Wrote packs of 3, 35, and 1,371 notes. |
| Skip, smallest grain first | Folded the newest notes first: no recent note stayed word for word. |
| Pull back, never jump a bigger row | Still stranded rows, and listed far more notes out of order, because a stranded row gets jumped again and again. |
| Fewest walls, any jump | Worked, with more notes out of order and fewer recent notes word for word. |
| **Skip, oldest pair first** | **Never stalled, kept recent notes word for word, and listed the fewest notes out of order.** |

On a view where grains never rise, oldest-pair-first is exactly the neighbors rule, so one writer sees the same folds as before. After a merge it keeps that one-writer shape most of the time.

The cost: a nap's notes are no longer guaranteed to be contiguous in time. At a budget of 32, about a tenth of notes list above an older note. Concurrent writers already broke strict order, since a merged branch's nap spans notes from `main`.

The guarantee is bounded, not absolute. With only power-of-two grains, a view where no two rows share a grain has at most ⌊log₂ N⌋ + 1 rows for N notes. Over a 32-row budget, a foldable pair exists until about 8.6 billion notes. This is argued and simulated, not proved; a seeded property test in the suite holds the line.

## Expand

Under budget, `wake` opens the children file of the newest expandable nap and lists its two children in its place, in memory. It repeats until the listing reaches the budget or nothing left will split. After each split it sorts the opened rows by each row's oldest note, so a newer child lands at its own date.

Expansion writes nothing. The expanded rows print with their ids, and `zoom` can open them, but `nap` takes only ids of rows that exist as files.

At or over budget, `wake` lists every row and opens no children file.
