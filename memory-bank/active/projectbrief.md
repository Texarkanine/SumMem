# Project Brief

## User Story

As an agent waking a repository that has only the git-root store, I want `== Project-root Memories ==` above a non-empty document so those lines are obviously labeled.

## Use-Case(s)

### Root-only store with memories

A consumer repo (no additional catalogs) has root notes. Root `wake` prints the memories header, then the document, then the footer.

### Catalog plus memories

A repo with other started stores and a non-empty root document still prints catalog first, then the memories header, then the document.

### Empty root document

A cataloged repo with no root notes still omits the memories header. Pull wakes stay unlabeled.

## Requirements

1. Print `== Project-root Memories ==` when the root decaying document is non-empty, whether or not a catalog exists.
2. Omit that header when the root document is empty.
3. Leave catalog heading and pull-wake behavior unchanged.

## Constraints

1. Do not invent a new header string. Keep `== Project-root Memories ==`.
2. Do not label `wake --path` (pull) output with the project-root header.

## Acceptance Criteria

1. Root `wake` with notes and no catalog includes `== Project-root Memories ==` above those notes.
2. Root `wake` with notes and a catalog still includes the header between catalog and document.
3. Root `wake` with an empty root document still omits the header.
4. `wake --path` on a child store still omits `== Project-root Memories ==`.
