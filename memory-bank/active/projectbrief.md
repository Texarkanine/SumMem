# Project Brief

## User Story

As an operator of a SumMem clone that may sit in a deep path (worktrees, `/mnt/c/Users/…`, eCryptfs), I want stored nap leaf-set ids to be 16 hex so pair basenames stay well under Linux `NAME_MAX` and Windows traditional `MAX_PATH`, without mixing 16-hex view ids with 64-hex nested `.tree` ids.

## Use-Case(s)

### Use-Case 1

An agent wakes, notes, naps, zooms, and recalls against this clone. Public addressing stays unique-prefix of the (now 16-hex) leaf-set field. Agents never see or type the variant tag.

### Use-Case 2

An operator runs sibling `migrate.py` once against a store that still has four-part stems, five-part stems with 64-hex leaf-set fields, or both. Complete pairs become five-part with 16-hex leaf-set ids (nested `.tree` ids rewritten, variant recomputed). A second run is a no-op. Incomplete pairs print and exit 1. Dest-exists skips silently.

### Use-Case 3

This repository's root and `dogfood` stores are rewritten in the same change so committed naps match the driver that lists them.

## Requirements

As specified in [SumMem #67](https://github.com/Texarkanine/SumMem/issues/67):

1. Store the public leaf-set id as the first 16 hex of the existing SHA-256 (`leafset_id(...)[:16]`). Still compute the full digest; do not change the hash algorithm.
2. Target stem: `{seq-prefix}-{leafset16}-{grain}-{variant16}`. Seq, grain, and the 16-hex variant tag stay.
3. The driver writes and parses **only** this form. Four-part stems and five-part stems whose leaf-set field is 64 hex are not view nodes.
4. New folds and rematerialized children always write that form. `write_nap` / `child_nap_stem` stay one serialize-then-name path.
5. `migrate.py` one pass consumes whichever old form it finds: 4-part 64-hex and 5-part 64-hex become 5-part 16-hex (rewrite nested tree ids 64→16, recompute `variant_tag`); 5-part 16-hex left alone; incomplete pair prints and exits 1; dest already exists skips silently.
6. Filename-only truncate is not enough: truncate every stored leaf-set id, including JSON `id` fields, so `list_view` and `_index_tree` agree.
7. `migrate.py` remains the only old-stem reader (sibling script, not a `summem` verb, no `__version__`).
8. Atlas, `systemPatterns.md` (“Filenames and `.tree` identity stay 64 hex”), and the #61 path-length “do not shorten” sentence update to 16 hex stored / unique-prefix displayed.
9. This clone's root and `dogfood` stores are rewritten in the same change.
10. Wake / nap / zoom / recall still address by unique prefix of the (now 16-hex) leaf-set field. `short_id` floor 8 unchanged.

## Constraints

1. Breaking change, same clean-break class as #61: no dual-read of 64-hex stems in the driver.
2. Not this issue: shortening seq, grain, note rands, or the 16-hex variant tag; Base32 / other encodings; a new `summem migrate` verb; changing `short_id` floor 8.
3. After `/niko-reflect`: open a **non-draft** PR (so automated reviewers activate) via the GitHub PR skill. Include a copyable conventional-commit `BREAKING CHANGE:` footer in the PR body.

## Acceptance Criteria

1. `_parse_nap_stem` accepts only five-part stems with `len(leafset) == 16` (variant stays 16 hex). `leafset_id` still SHA-256, stored as `[:16]`.
2. New folds and rematerialized children always write that form.
3. `migrate.py` converts complete 4-part and 5-part-64 pairs to 5-part-16 as specified; second run is a no-op; `--path` and default-all-started-stores unchanged.
4. This clone's root and `dogfood` stores are rewritten in the same change.
5. Wake / nap / zoom / recall still address by unique prefix of the (now 16-hex) leaf-set field. Agents never see or type the variant tag.
6. Atlas, `systemPatterns.md`, and the #61 path-length sentence update to 16 hex stored / unique-prefix displayed.
7. `tox` py311–py314 green.
