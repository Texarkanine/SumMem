# Merges and Healing

A git merge of two stores is the union of their files. Nothing in a store is ever edited, so the union never conflicts. It can, however, list the same notes more than once. **Healing** puts the view back into a clean state: no two rows share an original note. It never loses one.

## What a merge can leave

Three shapes, each from writers who did not see each other's work:

| Shape | How it happens |
|---|---|
| Two loose notes with the same text | Two writers recorded the same sentence. Their files differ only in name. |
| Two naps with the same content id | Two writers folded the same notes with different captions. Their variant tags differ, so git keeps both. |
| Two naps whose notes overlap | Two writers grouped some of the same notes differently. |

A loose note whose text already sits inside a nap is the first shape again: the same sentence, once loose and once folded.

## Heal

**Heal** is the repair for all three. It loops until no two rows share an original note:

```mermaid
flowchart TD
    Share["Two rows share original notes"] --> Sub{"One row's notes are a subset of the other's?"}
    Sub -->|yes| Drop["Remove the subset row"]
    Sub -->|no| Kids["Write the smaller nap's children back out as rows"]
    Kids --> Unlink["Remove the smaller nap"]
    Drop --> Share
    Unlink --> Share
```

Every step either removes a row whose notes are all still held elsewhere, or replaces a nap with its own children. No step changes which notes the store holds. [Why It Converges](../how-it-works/theory.md#what-each-operation-does-to-meaning) states that as a property, and [Why Writers Never Conflict](../how-it-works/no-conflicts.md#summaries-that-overlap) walks through both branches of the diagram with pictures.

The opening-up branch is also called the **zipper**: it unzips the smaller nap so the larger one can keep what they share.

### Same text

Two notes with the same text have the same content id, so each one's notes are a subset of the other's. Heal keeps the later filename. A loose note whose text is already inside a nap is dropped; the nap keeps it.

An agent that records a sentence the store already holds still hears `Saved.` The fact is in the store; the extra file is not.

Two copies of one sentence are one fact, so they can never fold together. A nap of them would claim grain 2 for one note. `nap` refuses any pair whose notes overlap.

### Same content id

Two naps with the same content id hold the same notes. Heal keeps the one whose filename sorts last. Their names differ only in the variant tag, so the survivor is chosen by content, not by who wrote last or merged last. Every clone that has both files keeps the same one. Its `.tree` and `.summ` are one pair and always survive together.

Until the next heal, `wake` can print both rows, with one id.

### Overlap

When two naps share some notes but neither holds all of the other's, heal opens the smaller one into its children and removes it. Repeated, this drops any child that is now a subset of the larger nap and keeps the rest.

## When heal runs

| Command | Heal |
|---|---|
| `note` | After writing the new note, before checking the budget. |
| `nap` | Before resolving the ids the agent passed. |
| `wake`, `zoom`, `recall` | Never. Reading never waits on a repair. |

Because `nap` heals first, an id the agent copied before a merge can disappear. Then `nap` fails with `unknown id` and folds nothing. The notes still live in the row that survived, and the next fold request names current ids.

## The lock

`note` and `nap` run heal, the fold scan, and the write under one lock on the machine. It is a lock on the store's `naps/` directory where the system allows one, and otherwise a lock file in the operating system's runtime directory. Neither is committed. Two clones never wait on each other; git merge remains the only coordination between them. `wake` never takes the lock.

While the lock is held, each children file is parsed at most once per command. Heal, the fold scan, and `nap` share that parse. A file the command writes is parsed again when next read. Nothing is cached outside the lock: tests call these functions directly and edit files between calls.

## What healing does not do

Heal makes the view clean, not canonical. Two clones that have seen the same notes may still group them differently: one may hold `ABCD` beside `EF` where the other holds `AB`, `CD`, and `EF`. Both are correct. Rebuilding one canonical grouping after every merge is [not this algorithm](not-yet.md#not-this-fold).
