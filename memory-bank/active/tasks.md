# Task: multi-store-filing rework 2: single `--path` with git `:/` + PR #104 fixes

* Task ID: multi-store-filing
* Complexity: Level 2
* Type: simple enhancement (breaking CLI change, pre-1.0) + review fixes

Replace `--root` xor `--path` with one `--path`, required on `note`, `nap`, `zoom`, `recall` and `surgery.py`. A path starting with `:/` is relative to the git root, and `:/` alone means the root. Any other path is relative to `$PWD`. Every printed path is in `:/` form. The `Run:` path is shell-quoted. The resolver refuses unknown `:` prefixes and paths or stores outside the repository. The design is in `creative/creative-store-flag-scheme.md` (with its plan amendments: bare `wake` = `--path .` as today; resolver refusals exit 1).

## Test Plan (TDD)

### Behaviors to Verify

- B1: `note --path :/ "x"` run from a subdirectory → note lands in the root store; stdout ``Saved to `:/` ``.
- B2: `note --path :/pkg/f.py "x"` run from a sibling directory, with `pkg` started → lands in the `pkg` store; ``Saved to `:/pkg` ``.
- B3: `note --path pkg/f.py "x"` from the root (relative to `$PWD`) → the `pkg` store, as today; ack ``Saved to `:/pkg` ``.
- B4: `note "x"` (no flag) → exit 2, one stderr line naming `--path` and `:/`, nothing written; the same for `nap`, `zoom`, `recall`, `surgery.py`.
- B5: `note --root "x"` → argparse rejects it (exit 2), nothing written.
- B6: `--path :x` and `--path :(top)` → exit 1, `unknown path prefix: …`, nothing written.
- B7: `--path :/../outside` → exit 1, `outside the repository: …`, nothing written.
- B8: a `.summem` symlink to a directory outside the repository (POSIX only) → `note --path :/ "x"` exits 1 with one stderr line and no traceback, and nothing is written there.
- B9: a fold request for a child store prints `Run: … nap --path :/pkg …`; for the root, `nap --path :/ …`.
- B10: a child store at `team docs` → the `Run:` line carries `--path ':/team docs'`; `shlex.split` of that line, run through `m.main` from a *different* subdirectory, folds that store (closes the `Run:` cwd hole and the space hole together).
- B11: root wake catalog lines read `N: :/dogfood`; `wake --path :/dogfood` pulls that store from any directory.
- B12: `start :/newdir` creates the store and prints `There is a store in :/newdir.`; `start :/../x` → exit 1, outside the repository.
- B13: `migrate.py --path :/` limits the rewrite to the root store (via the shared resolver).
- B14: `surgery.py --path :/ --contains T` excises from the root store; `surgery.py --root …` is rejected.
- B15: the odd-arity heal test (`tests/test_heal_view.py`) plants a nap that partially overlaps a neighbour, so heal takes the split branch; the 50-call cap still holds; every original leaf is reachable; `assert_unique_cover` passes.
- B16 (round trip, creative rule 4): every printed path (`Saved to`, `Run:` after `shlex.split`, catalog line, `start`) passed back as `--path` from the root, a child dir, and a sibling dir selects the same store. One parametrized test in `tests/test_scopes.py`; `_input_path`/`_root_path` are a parse/format pair.
- Regression: bare `wake` from the root and from a child-store subdirectory behaves as today; `-h`/`--help` stays side-effect-free.

### Test Infrastructure

- Framework: pytest via tox (`tox -e py311`; final `tox run-parallel`)
- Test location: `tests/`
- Conventions: in-process `m.main([...])` unit suites (`test_cli.py`, `test_scopes.py`, `test_fold.py`, `test_surgery.py`, `test_migrate.py`, `test_heal_view.py`) stay separate from child-process binary suites (`test_path_walkup_and_catalog.py`); helpers in `tests/gitutil.py` (`_FOLD_RUN`); the `summem` fixture, never `load_summem`.
- New test files: none

## Implementation Plan

### 1. Resolver: `:/` anchor, prefix reservation, containment — executable

- Files: `summem` (`resolve_parent`, new `_input_path`), `tests/test_scopes.py`

1. Stub tests in `tests/test_scopes.py`: B1, B2, B3, B6, B7, B8 (with `skipif(os.name == "nt")`).
2. Stub interface: `_input_path(cwd, arg) -> Path`, with a docstring: `:/rel` → `find_store_parent(cwd) / rel`, resolved; any other leading `:` raises `ValueError("unknown path prefix: …")`; other values resolve against `cwd` (absolute paths are accepted). Outside the root raises `ValueError("outside the repository: …")`.
3. Write the tests and run them red.
4. Write the code and run it green. `resolve_parent` uses `_input_path` when it gets a `path_arg`. After choosing the store parent, it checks that `(parent / ".summem").resolve()` is inside the root; if not, it raises `ValueError("store outside the repository: …")`. Existing callers (`wake`, `migrate.py`) inherit this.

### 2. One required `--path`, `:/` output, quoted `Run:` — executable

- Files: `summem` (`_select_store`, `_store_flag_error`, `_root_path`, `_fold_store_flag`, `main` argparse, `start` branch, `catalog_text`), `tests/gitutil.py` (`_FOLD_RUN`), and every test file that uses `--root` (19 files, about 150 occurrences)

1. Stub tests: B4, B5, B9, B12 and B16 in `tests/test_cli.py` / `tests/test_scopes.py`; B10 in `tests/test_fold.py`; B11 in `tests/test_path_walkup_and_catalog.py`.
2. Stub interface: `_select_store(cwd, path_arg, cmd)` (drop `root_flag`).
3. Modify the existing tests: mechanically replace `"--root"` with `"--path", ":/"`; expected `nap --root` with `nap --path :/`; ``Saved to `./x/.summem` `` with ``Saved to `:/x` ``; catalog `N: ./x` with `N: :/x`; `There is a store in ./x.` with `:/x`. Update `_FOLD_RUN` to `' nap --path (\'[^\']*\'|\S+) (\S+) (\S+) "'` (with the group indices fixed). Write the new tests and run red.
4. Write code and run green:
   - `_root_path` returns `:/` + rel (the root is `:/`).
   - `Saved to` formats `parent`, not `parent/.summem`.
   - `_fold_store_flag` returns `"--path " + shlex.quote(":/" + rel)`; a non-git fallback returns `--path :/`.
   - `catalog_text` uses `_root_path`.
   - Remove the `--root` argparse option.
   - `start` resolves its target with `_input_path` (containment first) and only then formats `not a directory:` / `There is a store in` with `_root_path`.
   - `_store_flag_error` reads `pass --path <file> (nearest store; :/ is the project root)`, with `<store>` for the other commands.

### 3. `surgery.py` on the new selector — executable

- Files: `surgery.py` (`_usage`, argparse, `_select_store` call), `tests/test_surgery.py`

1. Stub the B14 tests.
2. Stub interface: none (`m._select_store` signature from step 2).
3. Replace `--root` in the tests, write B14, run red.
4. Drop the `--root` argument, call `m._select_store(Path.cwd(), args.path, "surgery")`, and update `_usage` to `surgery.py --path STORE …` / `:/`. Run green.

### 4. `migrate.py` accepts `:/` — executable

- Files: `tests/test_migrate.py` (no production change expected: it already calls `resolve_parent`)

1. Stub the B13 test.
2. Stub interface: none.
3. Write the B13 test and run it; it should be green after step 1. If it fails, fix it in `migrate.py`.
4. Confirm the help string `limit rewrite to this store` still holds.

### 5. Odd-arity heal test overlap — executable (test fix)

- Files: `tests/test_heal_view.py::test_heal_odd_arity_finishes_under_iteration_cap`

1. Stub: rewrite the test body plan in its docstring: the one-kid nap wraps a multi-leaf child, and a neighbour shares some but not all of its leaves with the three-kid nap.
2. Stub interface: none.
3. Implement the test. Prove the split branch ran with an observable outcome: the overlapping nap's files on disk change (payload names before != after), not a call count on `rematerialize_child`. Keep the 50-call cap. Assert `reaches` for every leaf and `assert_unique_cover`. Run it.
4. Production code: none expected. If heal loops or loses a leaf, this is a real bug: stop and report (circuit breaker).

### 6. Agent-facing text — executable output, prose content

- Files: `summem` (`how_to_text`, `usage_text`, `wake --path` help), `surgery.py` `_usage`
- No tests that pin wording (`techContext.md` rule). The command forms in B4 and B11 are already covered.

1. `how_to_text`: "Every store command takes `--path`: a path from where you stand, or `:/path` from the repository root, as in git. `:/` is the root store." All examples use `:/`; catalog line form `N: :/path`.
2. `usage_text`: `note --path FILE TEXT`, `nap --path STORE …`, and so on, plus one `:/` line.

### 7. Docs — prose/policy

- Files: `docs/user-guide/{commands,quickstart,stores,troubleshooting,upgrading}.md`, `docs/advanced/surgery.md`, `docs/architecture/{store,wake}.md`, `docs/how-it-works/{index,no-conflicts}.md`, plus anything a sweep finds, `memory-bank/productContext.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Sweep `docs/` and `memory-bank/*.md` with `grep -rnE -- '--root|Saved to `\./|N: \./|store in \./'`; replace `--root` with `--path :/` and `./x` output examples with `:/x`; explain `:/`, the prefix reservation, the `./:name` escape and the containment refusal once, in `commands.md` and `stores.md`.
2. `commands.md:148`: a store command with no `--path` exits 2 before any repository check (PR #104 item 6).
3. `upgrading.md`: `--root` is removed; use `--path :/`. `commands.md`: one sentence that a relative path into a nested repository uses that repository, as before.
4. Run `properdocs build --strict`.

### 8. Supersede the stale project memory — prose/policy

- Files: `.summem/` (via the script only)
- No tests: prose/policy artifact

1. `.summem/summem note --path :/ "…"` stating that note, nap, zoom, recall and surgery.py require `--path` (`:/` = repo root, git syntax; `--root` removed), printed paths are `:/` form and pasteable, and the `Run:` path is shell-quoted. This supersedes note `20261119T200011Z-420729d3` (notes are grow-only; never edit it).
2. Do any nap the note requests.

## Technology Validation

No new technology. `shlex` and `Path.is_relative_to` are stdlib on the 3.11 floor. Validation is not required.

## Dependencies

- Steps 1 and 2 come before 3 and 4 (the shared resolver and selector).
- `tests/gitutil.py::_FOLD_RUN` must change in step 2, or every fold-driving test breaks.

## Challenges & Mitigations

- The mass `--root` test rewrite hides behaviour changes: do it with one scripted replace, then read every remaining failure by its error, not by file (OUTCOME #307).
- `shlex.quote` uses POSIX quoting; Windows `cmd` doesn't understand single quotes. PowerShell and bash do. The path is quoted only when it contains unsafe characters, so ordinary paths print bare. Accept this and note it in `commands.md`.
- Some tests call `m.main` with an absolute `--path` while cwd is elsewhere. `_input_path` takes the root for non-`:/` paths from the target, as today (`find_store_parent(origin)`), so this keeps working.
- The `Saved to` format changes from `./x/.summem` to `:/x`: 36 test assertions. Covered by the mechanical replace in step 2.

## Pre-Mortem

- The wrong premise, "bare `wake` = `:/`", would have changed session start from child directories: already amended to `--path .` (today's behaviour).
- The symlink check placed in formatting instead of the resolver would bring back the PR #104 crash: step 1 puts it in `resolve_parent`, and B8 pins it.
- The odd-arity test passes without hitting the split branch again (the same vacuity): step 5 asserts that `rematerialize_child` is called.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
