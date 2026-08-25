# Task: catalog-ls-files

* Task ID: catalog-ls-files
* Complexity: Level 2
* Type: simple enhancement

Replace `catalog_text`'s Python `os.walk` plus per-store `git check-ignore` with one `git ls-files --cached --others --exclude-standard` filtered for `.summem/config.toml`. Catalog output, pull omission, and ignore semantics stay the same. No committed catalog index.

## Test Plan (TDD)

### Behaviors to Verify

- Root wake catalogs another started store: `start pkg` then root `wake` → `== Additional SumMem Catalogs ==` and `./pkg`, not pull commands (existing `test_root_wake_catalogs_other_store`, `test_root_wake_catalog_is_labeled_paths_not_commands`)
- Empty root with a child store: root `wake` → Usage + `catalog_text` + footer, no Project-root header (existing `test_empty_root_omits_project_root_header`)
- Pull omits catalog: `wake --path pkg` → no catalog header, no Usage, no Project-root header (existing `test_pull_wake_omits_catalog_and_root_notes`)
- `.git/info/exclude` store omitted: exclude `secret/.summem`, start `secret` and `pkg` → `./pkg` present, `./secret` absent (existing `test_ignored_store_omitted_from_catalog`)
- `.gitignore` store omitted: ignore `hidden/.summem`, start `hidden` and `pkg` → `./pkg` present, `./hidden` absent (new `test_gitignore_store_omitted_from_catalog`)
- Python does not walk for catalog: monkeypatch `os.walk` to raise; `start pkg` then `catalog_text` / root `wake` → still lists `./pkg` (new `test_catalog_does_not_os_walk`)
- Sentinel is `config.toml`: a child `.summem/` directory with no `config.toml` → not listed (new `test_catalog_requires_config_toml_sentinel`)
- Untracked started store still lists: `start` without `git add` then root `wake` → `./pkg` (covered by existing start-then-wake tests; `--others` is required or they go red)

### Test Infrastructure

- Framework: pytest via tox (`py311`–`py314`)
- Test location: `tests/`
- Conventions: `tests/test_scopes.py` is the in-process catalog suite (`load_summem`, `init_repo`, `capsys`); process-level twin is `tests/test_path_walkup_and_catalog.py` (no change unless it goes red)
- New test files: none

## Implementation Plan

### 1. Catalog tests — executable

- Files: `tests/test_scopes.py`

1. Stub tests: add empty `test_catalog_does_not_os_walk`, `test_gitignore_store_omitted_from_catalog`, `test_catalog_requires_config_toml_sentinel`
2. Stub interface: no new public functions; `catalog_text(git_root, resolved_parent)` signature stays
3. Write tests and run red:
    - `test_catalog_does_not_os_walk`: `monkeypatch.setattr(m.os, "walk", lambda *a, **k: (_ for _ in ()).throw(AssertionError("os.walk")))`; start `pkg`; assert `./pkg` in root wake / `catalog_text`
    - `test_gitignore_store_omitted_from_catalog`: write `.gitignore` with `hidden/.summem`, start `hidden` and `pkg`, assert catalog has `./pkg` only
    - `test_catalog_requires_config_toml_sentinel`: mkdir `bare/.summem` with no `config.toml`, start `pkg`, assert `./pkg` and not `./bare`
4. Write code and run green: see step 2

### 2. `catalog_text` enumeration — executable

- Files: `summem`

1. Stub tests: (done in step 1)
2. Stub interface: keep `catalog_text`; delete `_ignored_store` once unused
3. Write tests and run red: (done in step 1; existing ignore/catalog tests stay green until the walk is removed, then the new walk/sentinel tests go green with the replacement)
4. Write code and run green:
    - `catalog_text`: if `resolved_parent` is not the git root, return `""` (unchanged)
    - One `subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=root, capture_output=True)`
    - Split stdout on NUL; keep paths whose POSIX form is `.summem/config.toml` or ends with `/.summem/config.toml`
    - Store parent is that path with `/.summem/config.toml` removed; skip the root store
    - Sort parents; emit `== Additional SumMem Catalogs ==` plus `./path` lines (unchanged)
    - If `git ls-files` fails, return `""` (wake never refuses)
    - Remove `_ignored_store`

### 3. Atlas / README — prose/policy

- Files: `docs/architecture/index.md` Scopes; `README.md` only if needed
- No tests: prose/policy artifact

1. Re-read Scopes: "The catalog is a walk of the tree that honors git ignore. It is not a committed index."
2. Leave both files unchanged unless that sentence becomes false. `git ls-files --exclude-standard` is still a walk that honors git ignore, not a committed index.

## Technology Validation

No new technology - validation not required. `git ls-files --cached --others --exclude-standard` is already how ignore is defined; tests already spawn git repos.

## Dependencies

- Existing `subprocess` + git (already used by `_ignored_store` and store resolution)
- Existing catalog tests in `tests/test_scopes.py`

## Challenges & Mitigations

- Untracked stores after `start`: `--others` is required; existing start-then-wake tests fail without it
- `--cached` alone would miss new stores and would list a tracked-then-ignored file; `--exclude-standard` applies to `--others`, matching current `check-ignore` on untracked stores
- Pathspec vs filter-in-Python: avoid `**` pathspec portability; one full `ls-files` plus a suffix filter is the issue's equivalent and still does not Python-walk ignored trees
- Atlas wording: do not rewrite Scopes to name `ls-files` unless "walk" would be read as "Python os.walk" after the change — default is leave it

## Pre-Mortem

- Catalog silently drops uncommitted `start`ed stores because someone used `--cached` only: already covered by Challenge 1; existing tests are the tripwire
- `os.walk` monkeypatch test is treated as a change-detector and deleted: the acceptance criterion is "Python does not walk"; keep the test; it goes red if a walk is reintroduced
- Sibling #50/#51 touch other functions in `summem`; this branch only edits `catalog_text` / `_ignored_store` so merge conflicts stay local to those lines

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [x] QA

## QA Results

- PASS: implementation matches the plan and acceptance criteria.
- One NUL-delimited `git ls-files` enumeration replaces the Python walk and per-store ignore checks.
- Catalog output, pull omission, ignored-store handling, untracked stores, root exclusion, and the `config.toml` sentinel are preserved.
- No KISS, DRY, YAGNI, completeness, regression, integrity, or documentation blockers found.
- Full tox matrix passed: 287 tests on Python 3.11, 3.12, 3.13, and 3.14.
