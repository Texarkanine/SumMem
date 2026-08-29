# Project Brief

## User Story

As a contributor, I want a newly recorded note to stay in the view even when its text already lives inside an older pack, so that a later `note` or `nap` does not silently delete a line I was just told was `Saved.`

## Use-Case(s)

### Use-Case 1

Two distinct notes fold into a grain-2 pack. Later, another agent records a line whose text matches one already inside that pack. The next `note` or `nap` runs `heal_view`. The new note file must still exist.

### Use-Case 2

Two loose notes with identical text are napped. The resulting pack must not claim grain 2 while holding a one-member leaf set. Heal from that state must not delete a third, never-napped copy.

## Requirements

1. Fix [issue #77](https://github.com/Texarkanine/SumMem/issues/77): `heal` must not delete a loose note whose text already sits inside a pack.
2. Napping two identical notes must not produce a pack whose grain disagrees with its leaf set.
3. A note written after its text was folded still exists after the next `note`.
4. Choose which layer to make honest. The issue lists three non-equivalent options (per-file identity, multiset heal, nap-reject overlap); they are not interchangeable.

## Constraints

1. Agents never write the store. The script remains the only writer.
2. Do not invent a repair in CLI output. If a note is kept, the agent is not told a story; if a note cannot be kept, do not print `Saved.`
3. The issue's three options are not equivalent: nap-reject alone does not stop trigger 1; per-file identity needs a `migrate.py` pass; multiset heal keeps content identity but leaves `leafset_id` and `leaf_digests` in disagreement unless that disagreement is also closed.
4. Personal and machine facts stay out of the repository.

## Acceptance Criteria

1. After a normal fold, a later `note` whose text matches a packed leaf remains on disk and in the view after the next mutating command's heal.
2. Grain and the pack's leaf membership tell the same story (either by changing identity so grain equals `|leaf set|`, or by counting multiplicity honestly everywhere overlap is decided).
3. A test covers: a note written after its text was folded still exists after the next `note`.
