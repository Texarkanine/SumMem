# Project Brief

## User Story

As an agent starting a session, I want each nested store on the root-wake catalog to show its leaf grain in a tiny prefix so I can tell which catalogs have memories worth pulling, without a slow per-store walk.

## Use-Case(s)

### Use-Case 1

Root `wake` in a repo with nested stores prints catalog lines like `0: ./foo` and `15: ./dogfood`. Empty started stores stay listed. Digit widths are not padded.

### Use-Case 2

Two notes in `./pkg` are folded into one grain-2 nap. The catalog still prints `2: ./pkg`, using the nap stem’s encoded grain, not the now-empty `notes/` directory.

### Use-Case 3

Catalog discovery and grain both come from the single `git ls-files` pass root wake already runs. Wake does not `iterdir` each store, does not `list_view`/`heal`, and does not open `.tree` or `.summ` to count.

## Requirements

1. Catalog lines are `N: ./path` with a single space after the colon and no digit padding.
2. `N` is that store’s leaf grain from filenames in the catalog listing: each loose note is 1; each nap stem adds its encoded grain once (`.tree` and `.summ` are one stem).
3. Empty started stores print `0:`.
4. One `git ls-files` scan; counting is extra constant work on names already listed (`O(P)` with catalog discovery, `F ≤ P` parses).
5. Pulls (`wake --path`) stay document-only: no Usage, no catalog, no `xN` grain prefix on catalog lines (there is no catalog on a pull).
6. Usage’s catalog sentence must not claim the whole line is a path: the `./` token is the path. Do not add a `note --path <catalog>` recipe in this task.

## Constraints

1. Agent output stays silent on git, `notes/`, and `naps/`.
2. Catalog lines are not commands.
3. Do not reprint Usage on a pull.
4. Do not use pack grammar `xN` for the count.
5. `started_stores()` remains a `list[Path]` for migrate and existing tests; grain is a catalog concern, not a migrate API change.
6. The uncommitted root-Usage `note --path <catalog>` draft is out of scope.

## Acceptance Criteria

1. Root wake catalog matches `N: ./rel` with no padding; `0:` for an empty child store.
2. After folding two notes, catalog grain is `2`, not `0`.
3. `catalog_text` / root wake do not call `list_view` or `heal_view` to produce counts.
4. Existing catalog omission rules still hold (gitignore, pull omits catalog, root is not listed).
5. Catalog how-to still teaches `wake --path` and now identifies the `./` token as the path.
