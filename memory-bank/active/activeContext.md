# Active Context

## Current Task: wake-omit-empty-catalog
**Phase:** BUILD - COMPLETE

## What Was Done
- Root wake with no other stores no longer mentions catalogs or `wake --path`.
- Root wake with catalogs still teaches catalog lines and `wake --path` via `how_to_text(catalog=True)`.
- Dropped “Ignore `--path` if the root wake had no catalog.”
- `tox -e py311`: 373 passed, 1 skipped.

## Next Step
- QA phase (`/niko-qa`).
