# Task: summ-caption-suffix

* Task ID: summ-caption-suffix
* Complexity: Level 2
* Type: simple enhancement

Rename nap caption files from `.sum` to `.summ` so they do not collide with checksum files. The store directory stays `.summem/`. `NapChild.sum` (caption text in the children JSON) does not change. The consumer `find … -exec` recipe is verified in a temp tree and goes in the PR body only.

## Test Plan (TDD)

### Behaviors to Verify

- [Nap writes `.summ`]: `write_nap` of two adjacent notes → returns `{stem}.summ`, that file holds the caption, `{stem}.tree` is unchanged
- [View groups `.summ` + `.tree`]: `list_view` after a nap → one nap node whose `sum_path` is the `.summ` file
- [Missing `.summ`]: `{stem}.tree` with no caption file → still one view node, empty caption
- [Conflict-marked `.summ`]: `.summ` containing `<<<<<<<` → still one view node, empty caption
- [Leftover `.sum` is not a caption]: `{stem}.tree` plus only `{stem}.sum` → empty caption (old suffix is ignored)
- [Failed `.tree` write leaves no caption]: injected replace failure on `.tree` → no `.summ` and no `.tree` left
- [Same-children different captions]: two nappers of the same pair → identical `.tree` bytes, different `.summ` bytes, dest names end in `.summ`
- [Proof: caption conflict]: two nappers of the same pair → conflict names end in `.summ`

### Test Infrastructure

- Framework: pytest via `tox` (`pytest.ini` `testpaths = tests`)
- Test location: `tests/`
- Conventions: `test_*.py` load repo-root `summem` via `conftest.load_summem`; store tests use `gitutil.init_repo` + `tmp_path`
- New test files: none (retarget existing suffix pins; add the leftover-`.sum` case to `tests/test_view.py`)

## Implementation Plan

### 1. Caption suffix — executable

- Files: `summem`; `tests/test_nap.py`; `tests/test_view.py`; `tests/test_wake.py`; `tests/test_fold.py`; `tests/test_cli.py`; `tests/test_zoom.py`; `tests/test_zipper.py`; `tests/test_proof_conflict.py`

1. Stub tests: retarget existing `.sum` globs, dest paths, and docstrings that mean the caption file to `.summ`; add empty `test_view_ignores_leftover_sum_caption` in `tests/test_view.py`. Do not change `NapChild.sum` / `kid.sum` (caption text).
2. Stub interface: no new functions. The suffix sites in `summem` stay as they are until the red run (`list_view` suffix set + `files.get`, `rematerialize_child`, `write_nap` dest and docstring).
3. Write tests and run red: assertions use `.summ` / `*.summ`; leftover-`.sum` case plants `{stem}.sum` beside `{stem}.tree` and expects empty caption. `tox -e py311 -- tests/test_view.py tests/test_nap.py` (and the other retargeted files) fail because production still writes `.sum`.
4. Write code and run green: those three `summem` sites write and read `.summ`. `path.suffix` for `.summ` is `.summ`; `path.stem` is unchanged. Do not dual-read `.sum`.

### 2. Rename committed store captions — prose/policy

- Files: `.summem/naps/*.sum`; `dogfood/.summem/naps/*.sum`
- No tests: prose/policy artifact

1. After the script change is green on `tmp_path` tests, `git mv` each committed `{stem}.sum` to `{stem}.summ` (four files). Do not run an unverified `find` against this working tree.
2. Confirm `tox -e py311` still passes and a root/dogfood wake still prints captions.

### 3. Documentation — prose/policy

- Files: `README.md`; `docs/architecture/index.md`
- No tests: prose/policy artifact

1. README: the example `git st` path and the “`.sum` contains our summary” bullet become `.summ`.
2. Architecture naps section: name the on-disk pair as `.summ` (caption) and `.tree` (children). Do not rewrite archives or `NapChild.sum` schema docs.

### 4. Consumer find recipe — prose/policy

- Files: none in-repo (recipe is PR-body only)
- No tests: prose/policy artifact

1. In a temp directory, plant: nested `.summem/naps/*.sum`, a checksum `other.sum` outside any store, a `.summem/summem` script, and an already-present `{stem}.summ`. Run the candidate `find … -exec` there.
2. Required properties: only direct children of `*/.summem/naps/` named `*.sum` are renamed; checksums and the driver are untouched; dest is `${f%.sum}.summ`; rename is same-directory `mv` (atomic on one filesystem); existing dest is not clobbered (`mv -n` or an existence check). Verify those properties before keeping the command.
3. Keep the verified command for the draft PR body. Do not add it to README or the script.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest / tox / `tmp_path` store fixtures
- GNU or BSD `find` + `mv -n` on the machine that runs the consumer recipe (document that in the PR body)

## Challenges & Mitigations

- [Rename `NapChild.sum` by mistake]: treat only the caption *file suffix* as in scope; JSON key `sum` and `ViewNode.sum_path` stay
- [Find matches checksums]: never `-name '*.sum'` from the repo root; require a path that is a direct child of `.summem/naps/`
- [Find clobbers or half-renames]: same-dir `mv`, no-clobber, verify in a temp tree first; this repo’s four files are `git mv` after that
- [Committed captions left as `.sum`]: step 2 is in the same change as the script; otherwise this repo’s wakes lose captions
- [Dual-read “for compatibility”]: out of scope; the find recipe is the upgrade path

## Pre-Mortem

- [We changed the children-file schema because a field is named `sum`]: already covered by Challenge 1; preflight should fail the plan if any step edits `dumps_tree` / `NapChild`
- [The find recipe is written from the repo root with a loose `*.sum` and eats checksums in the wild]: already covered by Challenge 2; step 4 must demonstrate a planted `other.sum` surviving
- [We ship the recipe in README “so people can find it”]: operator said PR body / squash-merge `BREAKING CHANGES:` footer only — step 4 forbids an in-repo copy
- [We keep reading `.sum` so dogfood still wakes, and the break never lands]: already covered by Challenge 5; step 2 renames this repo instead

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

✅ PASS (advisories, not blocking)

- **KISS / YAGNI:** Three literal `.summ` sites, no `CAPTION_SUFFIX` helper (preflight advisory honored).
- **Completeness:** Script, tests, four `git mv` captions, README, and architecture pair bullets match the plan. `NapChild.sum` untouched. No dual-read of `.sum`.
- **Regression:** `_unlink_node` still follows `sum_path`; `surgery.py` does not hardcode the suffix.
- **Documentation:** Planned docs updated; archives not rewritten; find recipe not shipped in-repo.
- **Advisory:** find command is PR-body only and is not copied into memory-bank; leftover `{stem}.sum` is an ignored orphan on unlink.
