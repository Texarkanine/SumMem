# Project Brief

## User Story

As an agent starting a session, I want root wake to catalog other started stores with one git enumeration so a repository with a large ignored tree does not pay a Python walk plus per-store `check-ignore` on the critical path.

## Use-Case(s)

### Use-Case 1

Root `wake` lists every other started, non-ignored store as `./path` under `== Additional SumMem Catalogs ==`.

### Use-Case 2

A store ignored by `.gitignore`, `.git/info/exclude`, or another git-ignore source does not appear. A pull (`wake --path`) still prints no catalog.

## Requirements

As described in https://github.com/Texarkanine/SumMem/issues/49:

1. Replace `catalog_text`'s `os.walk` plus per-candidate `_ignored_store` (`git check-ignore`) with one `git ls-files --cached --others --exclude-standard` (or equivalent that honors every git-ignore source, including `.git/info/exclude`).
2. Filter that listing for `.summem/config.toml` (`ensure_store` always writes it; that file is the sentinel).
3. Catalog output stays `== Additional SumMem Catalogs ==` plus `./path` lines.
4. A pull still prints no catalog.
5. No committed catalog index.

## Constraints

1. Stay in lane: `catalog_text`, `_ignored_store`, catalog tests, and atlas/README only if the documented catalog walk would become false.
2. Do not touch heal, recall, zoom, `short_id`, dataclasses, skip-heal markers, or `note`/`nap` bodies.
3. Atlas Scopes: the catalog remains a walk that honors git ignore, not a committed index.

## Acceptance Criteria

1. Root wake still lists every other started, non-ignored store as a path, and nothing else.
2. Ignored stores (`.gitignore`, `.git/info/exclude`, and other git-ignore sources) stay out.
3. A repository with a large ignored tree is not walked by Python for this catalog.
4. Pull wake still omits Usage, catalog, and the Project-root header.
5. No committed catalog index.
