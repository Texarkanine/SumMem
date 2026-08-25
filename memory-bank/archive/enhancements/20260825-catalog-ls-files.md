---
task_id: catalog-ls-files
complexity_level: 2
date: 2026-08-25
status: completed
---

# TASK ARCHIVE: catalog-ls-files

## SUMMARY

Root-wake catalog enumerates other started stores with one `git ls-files -z --cached --others --exclude-standard` filtered on `.summem/config.toml`. Output stays `== Additional SumMem Catalogs ==` plus `./path` lines. Pulls still omit the catalog. No committed index. Closes #49.

## REQUIREMENTS

- One git enumeration that honors every ignore source, including `.git/info/exclude`
- Sentinel is `.summem/config.toml` (`ensure_store` always writes it)
- Catalog output and pull omission unchanged
- A large ignored tree is not walked by Python
- Stay in lane: `catalog_text`, `_ignored_store`, catalog tests; atlas/README only if the documented walk became false

## IMPLEMENTATION

Level 2. Replaced `os.walk` plus per-store `git check-ignore` (`_ignored_store`) with one `subprocess.run` of `git ls-files -z --cached --others --exclude-standard`. Filter paths that are `.summem/config.toml` or end with `/.summem/config.toml`; skip the root store; sort; emit the same header and `./path` lines. `--others` keeps untracked `start` stores. Git failure returns empty catalog (wake never refuses). Atlas/README unchanged: Scopes is still a walk that honors git ignore, not a committed index.

- [`summem`](../../../summem): `catalog_text`; `_ignored_store` deleted
- [`tests/test_scopes.py`](../../../tests/test_scopes.py): `test_catalog_does_not_os_walk`, `test_gitignore_store_omitted_from_catalog`, `test_catalog_requires_config_toml_sentinel`; existing catalog/pull/exclude tests kept

## TESTING

TDD: two of three new tests red on the walk (no-`os.walk`, sentinel); gitignore was already green. Preflight PASS. `/niko-qa` PASS, no advisories. `uvx --with tox tox`: 287 passed on py311, py312, py313, py314.

## LESSONS LEARNED

- `--cached` alone would silently drop every uncommitted `start`. `--others --exclude-standard` is the old `check-ignore` contract for untracked stores.
- A new ignore-source test can pass before the rewrite. The walk-ban and sentinel tests were the ones that could only go green after the hole closed.

## PROCESS IMPROVEMENTS

Nothing notable — clean L2 execution.

## TECHNICAL IMPROVEMENTS

If catalog had always been "ask git for the tree," `_ignored_store` would never have existed.

## NEXT STEPS

None. Sibling shards (#50 recall/zoom, #51 heal) do not share this function.
