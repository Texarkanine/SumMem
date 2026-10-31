# Project Brief

## User Story

As an agent folding this store, I want one bad row to drop out of the pair scan so that the other rows still fold.

## Use-Case(s)

### Use-Case 1

A loose note is listed, then its file disappears. Fold of the other rows continues. The scan keeps that note at `node.leaves` and does not open the note file. `OSError` stays on `_as_child` of the row actually being napped.

### Use-Case 2

A children file parses, and a note's text is not a string. That pack is grain 0, the same as an unreadable pack. Fold of the other rows continues. The digest path raises `ValueError` so the existing `_fold_grains` catch applies. Other exceptions are not swallowed.

## Requirements

1. [Pull request 95, discussion r4429688354](https://github.com/Texarkanine/SumMem/pull/95#discussion_r4429688354): inside `_fold_grains`, keep a note at `node.leaves`. A note is one digest. Do not open the note file during that scan. `OSError` stays on `_as_child` of the row actually being napped.
2. [Pull request 95, discussion r4430896236](https://github.com/Texarkanine/SumMem/pull/95#discussion_r4430896236): a children file that parses, whose note text is not a string, is an ineligible pack (grain 0). It must not abort fold of the other rows. Raise `ValueError` from that digest path. Do not catch every exception.

## Constraints

1. This is rework of pull request 95 on `feat/fold-grain-as-child`, issue 88. The operator approved the restatement in the invocation and said not to wait.
2. Tests first. Edit only this worktree.
3. The scan's existing `except ValueError` stays the fold skip. Do not widen it to every exception.

## Acceptance Criteria

1. Three listed notes, third file removed: `fold_request` names the first two, and `write_nap` of that pair writes a grain-2 nap. `_fold_grains` does not open note files. `_as_child` of the removed note raises `OSError`.
2. A parseable children file whose note text is not a string: `_as_child` raises `ValueError`, and `fold_request` names an eligible pair among the other rows. `nap` of that pair succeeds.
