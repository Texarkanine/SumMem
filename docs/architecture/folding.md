# Folding

The store only grows. What an agent reads must not. **Folding** keeps the [view](wake.md#the-view) near its [wake budget](wake.md#the-wake-budget) by replacing two old rows with one nap, whose caption an agent writes.

## Fold

When a write leaves the view over budget, the script asks for one fold, if a pair exists. The pair is:

- the **oldest** row whose grain is a power of two and that has another row of that grain anywhere later in the listing,
- paired with the **nearest** such later row.

```mermaid
flowchart TD
    Note(["note"]) --> WriteNote["Write the note, then heal"]
    Nap(["nap"]) --> WriteNap["Heal, write the nap, then remove the two rows' files"]
    WriteNote --> Over{"Is the view over budget?"}
    WriteNap --> Over
    Over -->|no| None(["No request"])
    Over -->|yes| Pair{"Is there a same-grain pair?"}
    Pair -->|no| None
    Pair -->|yes| Request(["Request the oldest same-grain pair"])
```

The two rows need not be neighbors. The request quotes the two rows' text and prints a `Run:` line with their ids. The agent supplies the caption. `nap` writes the new nap, removes the files of the two rows it replaced, and, if the view is still over budget, requests the next pair.

Folding counts a nap's grain from its children file, not from its name, and trusts that count even when the name disagrees. A loose note is always grain 1, and the fold scan never opens its file.

`nap` accepts any pair that obeys the same rule, and refuses the rest:

- two rows that hold some of the same memories: `overlapping packs` (overlap is [healing's](merges-and-healing.md) job);
- unequal grains: `not the same grain`;
- a grain that would not be a power of two: `not a power of two`;
- a same-grain row between them: `a nearer row of that grain sits between them`.

Every nap the script writes has a power-of-two grain. Folding never glues a sealed block to a single leftover note: an `x16` next to one `x1` waits for another `x1`.

Fold always removes the two rows' files. It does not keep them on disk because `wake` might [expand](wake.md#expand) the nap later: their memories are in the nap's children file.

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

A rule that only folds neighbors can never fold across a wall. The `x1` never meets another `x1`, because new notes land at the end and the `x4` after it only grows. That row and every older row stay in the view forever, over budget, with no request. Skipping to the nearest same-grain row is what lets these views shrink again.

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
