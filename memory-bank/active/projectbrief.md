# Project Brief

## User Story

As a contributor, I want the store’s meaning `L` to be a set of facts, so that two recordings of the same sentence are one leaf, heal can throw away a loose copy already inside a pack, and a nap cannot claim grain 2 for one fact.

## Use-Case(s)

### Use-Case 1

Two distinct notes fold into a grain-2 pack. Later, another agent records a line whose text matches one already inside that pack. The next `note` or `nap` runs `heal_view`. The new note file is gone. `L` is unchanged. `Saved.` still prints: the fact is in the store. This is the shoebox, not a defect.

### Use-Case 2

Two loose notes with identical text exist. Heal keeps one (later filename). `write_nap` of the pair without heal refuses overlap. No pack claims grain 2 with a one-member leaf set.

## Requirements

1. Fix [issue #77](https://github.com/Texarkanine/SumMem/issues/77) under the operator vote: `L` is a set of facts. Trigger 1 is intended.
2. Trigger 2: napping two identical notes must not produce a pack whose grain disagrees with its leaf set.
3. `note_digest` stays content-only. No migrate.
4. `Saved.` stays. Do not add an “already remembered” message.

## Constraints

1. Agents never write the store. The script remains the only writer.
2. Do not invent a repair in CLI output.
3. Recency-by-renoting a packed fact is out of scope.
4. Do not design around a broken third-party write rule that re-notes the same line.
5. Personal and machine facts stay out of the repository.

## Acceptance Criteria

1. After a normal fold, a later `note` whose text matches a packed leaf is absent after heal; zoom of the pack still reaches the sentence; CLI prints `Saved.`
2. Two loose identical notes, after heal, are one view node.
3. `write_nap` of two identical-text notes raises overlap and writes no pack.
4. Atlas and `docs/theory.md` describe trigger 1 as the shoebox, not as a leak.
