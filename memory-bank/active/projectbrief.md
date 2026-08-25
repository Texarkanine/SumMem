# Project Brief

## User Story

As an operator of SumMem stores, I want nap captions to use the `.summ` suffix instead of `.sum` so they do not collide with checksum files, while still reading as “summary” and “summem.”

## Use-Case(s)

### New naps write `.summ`

After this change, the script writes and reads caption files as `.summ`. A fresh nap pair is `{stem}.summ` + `{stem}.tree`.

### Existing stores keep working after rename

This repository’s committed captions (root and `dogfood/`) are renamed in the same change. Other consumer repos rename with a `find … -exec` recipe supplied in the PR body (not shipped as product docs); the operator will attach that recipe to a `BREAKING CHANGES:` footer on the squash-merge to `main`.

## Requirements

1. The script writes and reads nap captions as `.summ`.
2. Tests, proofs, comments, and in-repo documentation that name the caption suffix are updated.
3. Existing caption files under `.summem/naps/` and `dogfood/.summem/naps/` are renamed.
4. The PR body includes a `find … -exec` recipe that any consumer repo can run: it renames only SumMem caption files (including nested `.summem` stores), leaves real checksum `.sum` files and the `summem` script alone, and is atomic enough that a miss cannot half-rename or clobber.

## Constraints

1. The store directory remains `.summem/`. Only the caption suffix changes.
2. The migration recipe lives in the PR body, not as a shipped product command or README procedure.
3. The find recipe must be developed and verified in a temp tree (or after a commit), never against an uncommitted live store.

## Acceptance Criteria

1. A new nap writes `{stem}.summ` and the view/zoom/recall path still works.
2. No product path still writes or requires `.sum` captions.
3. This repo’s existing caption files are `.summ` on disk.
4. The draft PR body contains the verified find recipe for consumer migration.
