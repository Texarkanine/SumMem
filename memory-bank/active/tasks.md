# Task: catalog-grain-count

* Task ID: catalog-grain-count
* Complexity: Level 2
* Type: simple enhancement

Root-wake catalog lines become `N: ./path` (leaf grain from filenames in the existing `git ls-files` pass). Empty stores stay `0:`. No digit padding. Pulls unchanged. Catalog how-to names the `./` token as the path.

## Test Plan (TDD)

### Behaviors to Verify

- Empty child store: `start pkg` then root `wake` → catalog contains the line `0: ./pkg`
- One loose note: `note --path pkg` then root `wake` → catalog contains `1: ./pkg` and does not contain note text
- Folded pair: two notes then `nap` → catalog contains `2: ./pkg` and does not contain `0: ./pkg` for that store (grain from the nap stem, not empty `notes/`)
- Nap pair counted once: after that fold, grain is `2` not `4` (`.tree` and `.summ` share a stem)
- No digit padding: empty `./a` and ten notes in `./b` → lines `0: ./a` and `10: ./b` (not `0:  ./a`)
- Counting source: `catalog_text` → does not call `list_view` or `heal_view`
- Pull unchanged: `wake --path pkg` → no `== Additional SumMem Catalogs ==`, no `N: ./` catalog block
- How-to: `how_to_text(catalog=True)` → teaches `wake --path`, says catalog lines are not commands, identifies the `./` token as the path (the line is no longer “the path”)
- How-to default: `how_to_text()` → still omits catalog recipe
- Regression: gitignored store omitted; `os.walk` still unused; root store not listed; catalog how-to still absent when there are no nested stores

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` (`testpaths = tests`)
- Test location: `tests/`
- Conventions: behavior-named `test_*` functions, `summem` fixture, `init_repo` from `gitutil`, `monkeypatch.chdir` for CLI, `capsys` for wake stdout
- New test files: none

## Implementation Plan

### 1. Catalog grain lines — executable

- Files: `tests/test_scopes.py`, `summem`

1. Stub tests: retarget `test_catalog_count_preserves_folded_note_grain` (today it asserts `"(2 notes" not in out`). Add empty-store `0:`, one-note `1:`, no-padding `0:` vs `10:`, and `catalog_text` does not call `list_view`/`heal_view`. Keep existing `./pkg` substring asserts (they stay true as a suffix).
2. Stub interface: add `_listed_store_grains(git_root) -> dict[Path, int]` with an empty body / `{}` return; keep `started_stores() -> list[Path]`.
3. Write tests and run red: `tox -e py311 -- tests/test_scopes.py::test_catalog_count_preserves_folded_note_grain tests/test_scopes.py::test_catalog_empty_store_prints_zero_grain tests/test_scopes.py::test_catalog_one_note_prints_one_grain tests/test_scopes.py::test_catalog_does_not_pad_grain_width tests/test_scopes.py::test_catalog_text_does_not_list_view` (names may be shortened to match the stubs). Expect fail on missing `N:` lines.
4. Write code and run green: one `git ls-files -z --cached --others --exclude-standard` in `_listed_store_grains`. For each path containing `/.summem/`, take the store parent. `notes/<file>` → `+1`. `naps/<stem>.summ` or `.tree` → `_parse_nap_stem`, add grain once per stem. Other files (including `config.toml`) contribute `0` but still register the store. `started_stores` returns `sorted` keys, still adding the git root via `is_store` when `/.summem/` does not match root-relative `.summem/…`. `catalog_text` reads that dict once (do not call `started_stores` as well — that would double `ls-files`). Lines are `f"{n}: ./{rel}"`. Skip root. Then `tox -e py311 -- tests/test_scopes.py tests/test_path_walkup_and_catalog.py`.

### 2. Catalog how-to path token — executable

- Files: `tests/test_init.py`, `summem` (`how_to_text`)

1. Stub tests: extend `test_how_to_text_catalog_is_opt_in` (and any catalog-wake tests that pin `"Listed catalog lines are paths"`) so catalog Usage says the `./` token is the path and that a leading `N:` is a count, not a command. Do not teach `note --path`. Drop the uncommitted `You can use add --path` sentence if it is still in the working tree.
2. Stub interface: none if `how_to_text(catalog=True)` already exists; only the catalog paragraph changes.
3. Write tests and run red: `tox -e py311 -- tests/test_init.py::test_how_to_text_catalog_is_opt_in`.
4. Write code and run green: rewrite the catalog how-to paragraph. Keep `wake --path <path>`. Run `tox -e py311 -- tests/test_init.py tests/test_scopes.py`.

### 3. Briefing — prose/policy

- Files: `memory-bank/systemPatterns.md`, `docs/architecture/index.md`, `README.md` (only if it still says catalog lines are paths-only)
- No tests: prose/policy artifact

1. Scopes / root-wake catalog: lines are `N: ./path` (filename grain), not bare paths and not pull commands. Still one git listing; still do not load every store’s view.
2. Surgical edit only where the current “paths only” sentence becomes false.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `_parse_nap_stem` for nap grain
- Existing `git ls-files` catalog enumeration (`started_stores` / catalog-ls-files)
- pytest / `tox -e py311` for iteration; `tox run-parallel` at end-of-work

## Challenges & Mitigations

- Double `ls-files` if `catalog_text` and `started_stores` each call the helper on one wake: `catalog_text` calls `_listed_store_grains` only; `started_stores` is for migrate and tests.
- Index vs worktree: `--cached` can still name a napped note whose worktree file is gone, so `N` can exceed the live view. Mitigation: count git-visible names, same source of truth as store discovery. Do not `stat` or `iterdir` to “fix” it.
- Same-leafset nap variants or leftover nested nap files: summing stem grains can exceed `|L|`. Mitigation: filename-only is the accepted approximation (opening `.tree` is forbidden). Tests cover the healed fold path (children unlinked, one stem).
- Four-part legacy nap stems: `_parse_nap_stem` returns `None`, so they add `0`. Mitigation: out of scope; `migrate.py` remains the old-stem reader.
- Digit padding by accident (`f"{n:3}"` or aligning `0:` to `10:`): an explicit `0:` vs `10:` test.
- Out-of-scope Usage draft (`note --path <catalog>`): do not keep it; this task only fixes the lying “line is a path” sentence.

## Pre-Mortem

- Plan fails because counting goes through `list_view`/`heal` “to be correct”: already covered by the boom-test in step 1; that would violate the O(P) constraint.
- Plan fails because catalog lines change but Usage still says the line is a path, so agents pass `15: ./dogfood` to `--path`: step 2 exists to close that.
- Plan fails by restoring per-store `store_stats` `iterdir` (original file-backend): slower and not the agreed source; helper must parse the ls-files loop.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA - PASS (no findings requiring build changes; see `.qa-validation-status`)
