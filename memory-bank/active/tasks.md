# Task: surgery

* Task ID: surgery
* Complexity: Level 2
* Type: simple enhancement

Emergency-only repo-root `surgery.py` that zipper-excises one whole raw note at the branch tip. Spec: https://github.com/Texarkanine/SumMem/issues/28. Not a `summem` subcommand. Do not edit `summem`, `prompt_text()`, `docs/agents-prompt.md`, or `AGENTS.md`.


## Test Plan (TDD)

### Behaviors to Verify

- Locate unique `--contains`: a substring that matches exactly one `NoteChild.text` (loose or nested) → that note's filename.
- Locate by filename / seq prefix: a unique note name (loose or nested) → that filename.
- Ambiguous `--contains`: two notes share the same text → error; require filename/seq. Do not delete both. Do not address by leafset id alone.
- Nap-caption-only hit: `--contains` matches a `.sum` / `NapChild.sum` but no note text → not found (do not delete a nap as if it were a leaf).
- Unknown target: no matching note → error; store unchanged.
- Loose-note excise: target already in `notes/` → `_unlink_node` that note; sibling notes remain; `heal_view` runs; zoom/recall do not owe the sentence.
- Nested excise: target lives inside a nested `.tree` → break out by rematerializing along containing view naps (kids via `rematerialize_child`, then `_unlink_node` the nap) until the named file is loose; unlink that `NoteChild` only; remaining HEAD `.tree` files do not embed the sentence; sibling notes still zoom/recall; `write_nap` is never called.
- Overlapping packs: two view naps both embed the target → split every containing view nap before unlink (do not call `heal_view` during break-out); after unlink + `heal_view`, unique cover and no remaining `.tree` embeds the sentence.
- Dry-run: `--dry-run` prints the rematerialize chain (nap stems in split order, then the note name) and writes nothing (byte-identical store).
- Dry-run still validates: not-found / ambiguous fail the same way and write nothing.
- Lock: the mutating path runs under `with_store_lock`.
- CLI `--path`: aims at a started store the same way `resolve_parent` does.
- Driver load: `surgery.py` loads sibling `summem` via `SourceFileLoader` (same method as `tests/conftest.py`).
- Python floor: CLI calls `require_python` (3.11+).

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini` `package=skip`, `py311`–`py314`)
- Test location: `tests/`
- Conventions: `test_*.py`; `load_summem()` from `conftest.py`; `init_repo` / `assert_unique_cover` / `reaches` from `tests/gitutil.py`; plant naps with `write_note` + `write_nap` or `rematerialize_child` as in `tests/test_zipper.py`. Run under tox so `sys.executable` is 3.11+, never this machine's bare `python3` (3.10).
- New test files: `tests/test_surgery.py`

## Implementation Plan

### 1. Locate the target note — executable

- Files: `tests/test_surgery.py`, `surgery.py`

1. Stub tests: `tests/test_surgery.py` empty cases `test_contains_unique_nested_note`, `test_filename_locates_nested_note`, `test_contains_duplicate_text_requires_filename`, `test_contains_nap_caption_only_is_not_found`, `test_unknown_target_errors`.
2. Stub interface: `load_summem()` using `SourceFileLoader` on sibling `summem`; `locate_note(m, parent, *, contains: str | None, name: str | None) -> str` raising `ValueError`.
3. Write tests and run red: unique substring → filename; unique name/seq → filename; two identical texts + `--contains` → `ValueError`; substring only in a nap caption → `ValueError`; missing note → `ValueError`.
4. Write code and run green: walk `list_view` loose notes and nested `NoteChild` via `_note_children` / `loads_tree`; match text with `contains` and names with exact filename or unique prefix of `NoteChild.name`; never treat a nap stem as a delete target.

### 2. Break out, unlink, heal — executable

- Files: `tests/test_surgery.py`, `surgery.py`

1. Stub tests: empty cases `test_excise_loose_note`, `test_excise_nested_note_unzips_then_unlinks`, `test_excise_overlapping_packs_clears_remaining_trees`, `test_excise_does_not_call_write_nap`, `test_dry_run_prints_chain_and_writes_nothing`, `test_dry_run_unknown_writes_nothing`, `test_identical_text_deletes_only_named_file`.
2. Stub interface: `plan_break_out(m, parent, note_name: str) -> list[str]` (nap stems to split, in order); `excise_note(m, parent, note_name: str, *, dry_run: bool = False) -> list[str]` (chain including the note name).
3. Write tests and run red: loose unlink; nested path rematerializes until loose then unlinks; overlapping packs both lose the sentence in remaining `.tree` bytes; `write_nap` monkeypatch is never entered; dry-run stdout/return chain vs unchanged `_payload_names` and file bytes; duplicate text keeps the other file; after mutate, `assert_unique_cover`, `not reaches(m, repo, sentence)`, and `sentence not in m.recall_text(repo, re.escape(sentence))`.
4. Write code and run green: **while** a view nap's tree contains that `NoteChild.name`, rematerialize its immediate kids (`rematerialize_child`) and `_unlink_node` that nap (do **not** call `heal_view` in this loop — subset-drop would swallow the loose note back into a larger pack). Then `_unlink_node` the loose note. Then `heal_view(parent)` for a unique cover. Copy existing child captions on rematerialize; never call `write_nap`. `dry_run` uses `plan_break_out` only. Mutating `excise_note` is wrapped by `with_store_lock` from the CLI (unit may assume caller locks, or lock internally once).

### 3. `surgery.py` CLI — executable

- Files: `tests/test_surgery.py`, `surgery.py`

1. Stub tests: empty cases `test_main_contains_excises`, `test_main_dry_run`, `test_main_path_flag`, `test_main_usage_without_target`.
2. Stub interface: `main(argv: list[str] | None = None) -> int`; argparse `--path`, `--contains`, `--dry-run`, optional positional `name`; `require_python()`; `if __name__ == "__main__"`.
3. Write tests and run red: `main(["--contains", sentence])` after chdir into `init_repo` removes the sentence; `--dry-run` exit 0 and unchanged store; `--path` aims at a `start`ed store; missing address exit 2.
4. Write code and run green: load driver, `resolve_parent`, locate, lock+excise (skip lock on dry-run), print chain lines, map `ValueError` to stderr + exit 1. AGPL header and `python3` shebang like `summem`. Do not register anything in `summem` argparse / `usage_text` / `init`.

### 4. Operator docs — prose/policy

- Files: `docs/surgery.md`, `README.md`, `docs/index.md`
- No tests: prose/policy artifact

1. Write `docs/surgery.md`: this is not a shipped CLI; script is the only writer; workflow (1) run surgery on the **branch tip** so HEAD store files no longer embed the sentence, (2) commit that tip, (3) operator rewrites git history — `surgery.py` does not rewrite history; `--contains` / filename addressing; `--dry-run`; aftercare: surgery must not nap — leave the hole or run an agent (`wake` / `nap` via `.summem/summem`) to rebuild invalidated captions from surviving children.
2. Link that page from README Documentation and `docs/index.md`. Do not add surgery to the command table or `AGENTS.md`.

## Technology Validation

No new technology - validation not required. `surgery.py` is a shebang script that loads existing repo-root `summem` via `SourceFileLoader`. Suite remains `tox`. Do not add `surgery.py` to `tox -e coverage` `--cov=` (optional; default tox stays coverage-free).

## Dependencies

- Existing `summem` helpers: `list_view`, `rematerialize_child`, `_unlink_node`, `heal_view`, `_note_children`, `loads_tree`, `with_store_lock`, `resolve_parent`, `require_python` — call them; do not move or duplicate into `summem`.
- `tests/conftest.py` `load_summem` / `tests/gitutil.py` for the suite.
- Issue #27 sibling owns `summem` / prompt / `AGENTS.md`; this branch must not touch them.

## Challenges & Mitigations

- **`heal_view` during break-out swallows the target:** subset-drop unlinks a rematerialized loose note while a larger overlapping pack still embeds it. Mitigation: split containing view naps until no remaining view nap's tree has that name; only then unlink the loose note; only then `heal_view`.
- **One-path unzip leaves a second overlapping `.tree`:** Mitigation: loop all containing view naps, not a single ancestor path.
- **Invented zip:** Mitigation: tests monkeypatch `write_nap`; rematerialize copies existing child `.sum` text only.
- **Identical-text notes:** Mitigation: locate by filename/seq; `--contains` errors on collision.
- **Loading `summem`:** Mitigation: `SourceFileLoader` on `Path(__file__).resolve().parent / "summem"`, same as `tests/conftest.py`.

## Pre-Mortem

- Plan treated `heal_view` as targeted break-out of a named leaf: already covered by Challenge 1; walk belongs in `surgery.py`.
- “Zip again” implemented as `write_nap` with a fake caption: already covered by Challenge 3 and issue aftercare.
- Docs omitted how to run an agent to nap the hole: prose step 4 names `.summem/summem` wake/nap aftercare.
- Collision with #27 by “just adding a helper to `summem`”: files list is `surgery.py` + tests + operator docs only.

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

**Result:** PASS (advisories, none blocking)

Reviewed `surgery.py`, `tests/test_surgery.py`, and operator docs against the plan, brief, and issue #28.

- **KISS:** Repo-root script + locate / plan / excise / CLI. No extra store format. `plan_break_out` simulation is the dry-run walk the plan named.
- **DRY:** Calls `list_view`, `rematerialize_child`, `_unlink_node`, `heal_view`, `with_store_lock`, `resolve_parent`, `require_python`. Does not copy zipper logic into `summem`.
- **YAGNI:** No `write_nap`, no shipped CLI fold-in, no history rewrite, no `fold_request` aftercare print.
- **Completeness:** All planned tests and helpers are real. `--contains` / filename / dry-run / lock / `--path` / SourceFileLoader / `require_python` are implemented. Docs cover tip-then-rewrite and agent aftercare.
- **Regression:** `summem` CLI, `usage_text`, `AGENTS.md`, and `docs/agents-prompt.md` untouched. Surgery is not in the command table.
- **Integrity:** No TODOs, debug leftovers, or invented captions. Break-out does not call `heal_view`. Mutate locks; dry-run does not.
- **Documentation:** `docs/surgery.md` linked from README Documentation and `docs/index.md`.

Advisories: dual dry-run/mutate walks must stay filename-ordered; unreadable `.tree` files are skipped like `summem`; no `fold_request` print (correct).
