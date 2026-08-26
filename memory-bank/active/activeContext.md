# Active Context

## Current Task: nap-variant-stems
**Phase:** BUILD - COMPLETE

## What Was Done

- Implemented five-part nap stems: `variant_tag` / `nap_stem`, dual-read parse, `write_nap` and rematerialize share `_write_pair`.
- Heal already kept the lex-greatest equal-set stem; pinned that, including four-part losing to five-part.
- Concurrent union proofs in `tests/test_nap_variants.py`; caption-conflict merge is now a clean union.
- Sibling `migrate.py` hashes on-disk pair bytes and rewrites complete four-part pairs. This clone's root and dogfood stores were migrated.
- Atlas, `systemPatterns.md`, and `productContext.md` now describe union-then-zipper. Dry-run on migrate stayed out (advisory, not a planned unit).

## Next Step

- QA review will now run automatically.
