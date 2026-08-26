# Active Context

## Current Task: nap-variant-stems
**Phase:** ARCHIVE - IN-PROGRESS

## What Was Done

- Five-part nap stems shipped: `variant_tag` / `nap_stem` / `child_nap_stem`, shared `_write_pair`, union-then-zipper, sibling `migrate.py`. This clone's root and dogfood stores are five-part.
- Post-QA: `child_nap_stem` shared by rematerialize and surgery; clobber and serialize-once tests repaired; `started_stores` lists the git root only when `.summem` is a directory.
- Operator clean break after reflect: `_parse_nap_stem` is five-part only. Unmigrated four-part files are invisible. `migrate.py._four_part_stem` is the only four-part reader. Happy-path migrate fully rewrites complete pairs; incomplete pairs stay on disk and exit 1.
- Draft PR #62 on `fix-the-hole`. Title `feat!: five-part nap stems so same-block folds merge [#61]`. Body closes #61, supersedes #59, and has a `BREAKING CHANGE:` migrate footer for Release Please. `tox` 349 green on py311–py314.

## Next Step

- Run `/niko-archive` to create the archive document and finalize. Then mark PR #62 ready and squash-merge so the `BREAKING CHANGE:` footer lands in the release notes.
