# Why SumMem Converges

This page explains why many agents can write to one memory, on different machines, with no lock between them, and never disagree about what the repository learned.

It starts with a shoebox and ends with a homomorphism. Each section assumes only the ones above it. Terms link out the first time they appear.

The [Architecture](architecture/index.md) page says what the pieces are. This page says why the arrangement is safe.

## The problem

Two agents learn something at the same moment, in two clones, on two machines. Both must be able to record it. Neither can wait for the other.

The usual answer is a lock, or one writer everyone else defers to. SumMem has neither, and cannot have them: the clones may be on different laptops, or on a CI runner, and they meet only when someone merges a branch.

The second problem is size. A memory that only grows is unreadable by the thousandth fact. So the store has to shrink its own listing while it grows its own contents.

Shrinking is where most designs get hurt. Two agents who each tidy up, alone, usually produce two tidyings that fight.

## A shoebox of receipts

Start here. No code yet.

Keep every receipt in a box. Never throw one away.

When the box gets crowded, staple a batch together and write one line on the front of the batch. You have not lost a receipt. Pull the staple and they all come back. The box reads shorter and holds the same money.

Now give two people their own box and let them staple their own batches. Tip both boxes into one. You may find a receipt loose *and* inside somebody else's stapled bundle. Throw away the loose copy. You have lost nothing, because the loose one and the stapled one are the same receipt.

That is the whole design. Two people tidy at the same time, in different rooms, and never argue — because tidying does not change what the box is worth.

Three sentences carry over into the rest of this page:

- A receipt is a **note**.
- A stapled bundle with a line on the front is a **nap**.
- Tipping the boxes together is a **git merge**.

## The pieces, exactly

**A note** is one immutable file holding one line of text. There is no edit and no delete. A retraction is a new note. The filename carries the moment it was written, in UTC, plus random characters so two writers never pick the same name.

**A nap** is two files that share a name:

- the caption (`.summ`), one line, which is what `wake` prints;
- the children file (`.tree`), which holds the full text of every note underneath it.

The word *summary* misleads here. The caption summarises. The nap does not. A nap carries every original sentence inside it, spelled out. It is a bundle, not a précis.

You can check this in the code. `_digests_of_dict` ([`summem:558`](../summem)) rebuilds each note's identity from the text stored in the `.tree`, using the same encoding a loose note gets. A note inside a bundle and the same note loose are indistinguishable. That fact is what the rest of this page rests on.

**The view** is the current listing: every loose note, plus every nap, sorted by filename. **Grain** is how many original notes a listed item stands for.

## Counting, first pass

Give every note a name that depends only on its contents: the [SHA-256](https://en.wikipedia.org/wiki/SHA-2) of its bytes. Two files with the same bytes get the same name. This is [content addressing](https://en.wikipedia.org/wiki/Content-addressable_storage), and it means we can talk about *which* notes a bundle holds without caring where the bundle came from.

Write `N` for every note that has ever been written.

Each item in the view stands for some collection of notes. A loose note stands for one. A bundle stands for all the notes inside it. Call that collection `leaves(v)`.

Now the question this page exists to answer:

> When two clones merge, do they end up remembering the same things?

To answer it we need to say what "what the store remembers" means, as a single object.

## The set that actually matters

A [set](https://en.wikipedia.org/wiki/Set_(mathematics)) is a collection with no order and no repeats.

Let `S` be a store: the finite collection of items currently in its view. Define

    L(S)  =  the union of leaves(v), for every v in S

`L(S)` is the set of notes the store can still produce. Call it **what the store means**.

Note what `L` throws away. It does not care how the notes are grouped into bundles. It does not care what the captions say. Two stores that grouped their notes completely differently can mean exactly the same thing.

That is the point. Convergence is a claim about `L`, not about files.

## Every operation, checked against `L`

Now run each thing SumMem does and watch `L`.

| Operation | What happens to the files | What happens to `L(S)` |
|---|---|---|
| `note` | one file appears | gains one note |
| `nap(a, b)` | `a` and `b` are deleted, a bundle holding both appears | **nothing** |
| heal, drop a covered item | one item is deleted | **nothing** |
| heal, unbundle then drop | one item becomes its children | **nothing** |
| git merge | the two file sets are unioned | `L(S₁) ∪ L(S₂)` |

Read the middle rows again. **Folding does not change what the store means.** Neither does healing. They move notes between groupings; they never add a fact and never lose one.

This is why `nap` deletes files without danger. It is not deleting notes. It is re-describing the same notes more compactly, and the notes are still spelled out inside the bundle it just wrote. `write_nap` ([`summem:710`](../summem)) writes the bundle before it unlinks either child ([`summem:728-730`](../summem)), so no moment exists where a sentence lives nowhere.

So across the whole system there is exactly one operation that changes `L`, and it only ever adds: `note`.

## Saying that properly

A [monotone](https://en.wikipedia.org/wiki/Monotonic_function) function never goes down. `L` is monotone: no operation shrinks it.

A structure where any two elements have a well-defined least upper bound is a [join-semilattice](https://en.wikipedia.org/wiki/Semilattice). Sets under union are the standard example: the join of two sets is their union.

The store's files form one such structure, joined by git's union of paths. The sets of notes form another, joined by union. And `L` carries one to the other:

    L(S₁ ∪ S₂)  =  L(S₁) ∪ L(S₂)

A map that turns the join on one side into the join on the other is a [semilattice homomorphism](https://en.wikipedia.org/wiki/Homomorphism). That single line is the whole convergence argument, and everything above was building the right vocabulary to state it.

Because union is [idempotent](https://en.wikipedia.org/wiki/Idempotence), [commutative](https://en.wikipedia.org/wiki/Commutative_property) and [associative](https://en.wikipedia.org/wiki/Associative_property) — merging twice is merging once, order does not matter, grouping does not matter — every clone that has seen the same notes agrees on `L`, no matter what order the merges happened in and no matter who folded what along the way.

That property is [strong eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency#Strong_eventual_consistency), and a structure with it is a [conflict-free replicated data type](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type), or CRDT.

**So: the notes form a grow-only set, and that set is a CRDT. The files are not. Compaction is invisible to the thing that converges.**

Naming the parts, for anyone comparing this to the CRDT literature:

- The notes are a [G-Set](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#G-Set_(Grow-only_Set)) — grow-only, no removes.
- Fold and heal are **compaction**, the standard state-based-CRDT move of shrinking a representation without touching the value it denotes. Compaction is not part of the join, and it is not required for correctness. It is allowed here for one reason only: it preserves `L`.

## The view is a partition

`L` tells us the store converges. It says nothing about what `wake` prints. That needs a second idea.

A [partition](https://en.wikipedia.org/wiki/Partition_of_a_set) of a set is a way of cutting it into pieces that do not overlap and that together cover everything.

After healing, the view is a partition of `L(S)`. Each listed item is one block. Its grain is the block's size. Its caption is a label on the block.

`heal_view` ([`summem:635`](../summem)) is what forces this. It loops until no two items share a note:

- if one block sits entirely inside another, drop the smaller;
- otherwise open the smaller block into its children and drop it.

Both moves preserve `L`, which is why heal is safe to run at any time, in any order, on any clone. `note` and `nap` run it ([`summem:1365`](../summem), [`summem:1418`](../summem)). `wake` never does — reading must not block on repair.

Git merge is the only thing that breaks the partition. It can land a bundle beside the very notes that bundle contains. Heal puts it right.

Fold, then, is: merge two adjacent blocks of equal size. Expand ([`summem:906`](../summem)) is: split a block, for display only, writing nothing back.

## Where a second, smaller CRDT hides

Two agents fold the same two notes and write different captions.

Same notes means the same leaf-set field in the filename, the same leftmost child, the same grain. Only the variant tag differs — a hash of the bundle's bytes and the caption's bytes ([`summem:421`](../summem)). Two filenames. Git unions them. Both appear in the view, briefly, as two rows with one id.

Heal settles it. The view is sorted by filename, and when two items cover the same notes, the earlier name loses. Since the names differ only in that trailing hash, the surviving caption is the one whose variant tag sorts highest.

That is a **max-register**: one value per key, chosen by taking the largest under a fixed [total order](https://en.wikipedia.org/wiki/Total_order). Maximum is idempotent, commutative and associative, so it is a real CRDT join, and every clone picks the same caption without asking anyone.

It resolves by content, not by clock. There is no last-write-wins here and there could not be — the clones have no shared clock, and the file timestamps a merge produces describe the merge, not the writing.

## What does not converge

Facts converge. Structure does not.

Two clones that have seen the same notes always agree on `L`. They need not agree on the partition. One may hold `ABCD` beside `EF` where the other holds `AB`, `CD` and `EF`. Both are correct: same notes, different cuts.

[Architecture](architecture/index.md) concedes this and rules the repair out of scope, and [Notes](notes.md) records the design that would close it.

Leaving it open is a judgement, not an oversight. Rebuilding one canonical grouping after every merge would mean rewriting bundles that are already correct, and it would still not settle the captions — two agents wrote two English sentences about the same pair of notes, and no rule picks the better one. SumMem picks one deterministically and keeps every original sentence reachable underneath it. The cut is cosmetic; the contents are not.

State it plainly: **strong eventual consistency on what is remembered, and none on how it is grouped or worded.**

## Where the theory leaks

One assumption above is doing more work than it can bear.

"Two notes with the same text are the same note" follows from content addressing. It is what lets heal drop a loose note it finds inside a bundle. It is also wrong about the world: an agent that records a sentence today, and an agent that recorded the same sentence in March, wrote two things, not one.

The code half-knows this. `leafset_id` ([`summem:99`](../summem)) hashes a sorted **list** and keeps repeats, so an item's identity counts duplicates. `leaf_digests` ([`summem:582`](../summem)) returns a **set**, so overlap does not. Identity is over a [multiset](https://en.wikipedia.org/wiki/Multiset); overlap is over a set. The two disagree, and heal trusts the second.

The consequence is a live defect: a note written after its text was folded is deleted by the next `note` or `nap`, with nothing said to the agent who wrote it. See [#77](https://github.com/Texarkanine/SumMem/issues/77).

Until that is settled, the honest version of the claim on this page is: **the store converges over the *set* of remembered notes.** Multiplicity is not preserved, and the architecture's promise that duplicate notes stay two listed items holds only while neither has been folded.
