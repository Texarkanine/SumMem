# Task: heal-same-text

* Task ID: heal-same-text
* Complexity: Level 3
* Type: bug fix (identity)

Fix [issue #77](https://github.com/Texarkanine/SumMem/issues/77) under the operator’s vote: `L` is a set of facts. Trigger 1 (heal drops a packed-text loose note) is intended. Trigger 2 (napping two identical notes into grain 2 with one leaf) is the remaining lie. Close the theory “leak” as the shoebox, not as a second identity.

## Pinned Info

### Shoebox heal

Same bytes are one receipt. A loose copy next to a bundle that already holds those bytes is thrown away. Two loose copies collapse the same way.

```mermaid
graph TD
    classDef keep fill:#e8f5e9,stroke:#2e7d32;
    classDef drop fill:#ffebee,stroke:#c62828;

    Packed["nap already holds sentence S"] --> New["new note with text S"]
    New --> Heal["heal_view"]
    Heal --> DropNew["unlink new file; L unchanged"]:::drop
    Two["two loose notes, same bytes"] --> Heal2["heal_view"]
    Heal2 --> KeepNewer["unlink older filename; one view node"]:::keep
```

## Component Analysis

### Affected Components
- `_first_overlap` (`summem`): stop skipping note/note pairs. Same digest set → unlink the older (left, filename order).
- `write_nap`: reject any intersecting digest sets, not only when a nap is on one side.
- Tests that pin two identical notes surviving heal and napping via a repeated id: retarget. `tests/gitutil.py::assert_unique_cover` currently skips note/note; drop that skip in unit 1.
- Atlas Identity **and** Zipper (`docs/architecture/index.md`), `memory-bank/systemPatterns.md` wake-dates sentence, `docs/theory.md` leak section: `L` is a set of facts; trigger 1 is the shoebox. Zipper today says two loose notes that share text are skipped; that sentence goes.

### Cross-Module Dependencies
- CLI `note`/`nap` already call `heal_view` before fold. After the skip is gone, `fold_request` should not see two identical notes.
- Direct `write_nap` in tests can still pair two files if heal was not called; the reject closes that path.
- `test_heal_note_covered_by_nap_dropped` is rematerialize of the same name; must stay green.

### Boundary Changes
- No on-disk identity change. No migrate.
- `Saved.` unchanged: the fact is in `L`.
- View after a mutating command holds at most one node per content digest among notes (and a pack still covers that digest).

## Open Questions

- [x] Which layer to make honest → Resolved: keep content identity; trigger 1 intended; collapse loose copies on heal; `write_nap` rejects digest overlap. Operator vote 2026-08-29 (see `memory-bank/active/creative/creative-leaf-identity.md`)

## Test Plan (TDD)

### Behaviors to Verify

- Two loose notes with the same text, then `heal_view` → one file remains (later filename); `L` still has the sentence.
- After a grain-2 fold of two distinct notes, a later `write_note` of one packed sentence, then `heal_view` → that new file is gone; pack remains; zoom still reaches the sentence. (Trigger 1: intended. This is a pin, not a keep-the-file test.)
- Rematerialize a packed `NoteChild` then `heal_view` → file gone; pack remains; zoom still reaches. Unchanged.
- `write_nap` of two identical-text notes (no prior heal) → `ValueError` overlap; no pack written; both files still present until heal.
- CLI `note` of text already inside a pack → exit 0, stdout `Saved.`, no loose duplicate, zoom still reaches the packed sentence. This is `tests/test_zipper.py::test_cli_note_text_inside_nap_exits_0_no_loose_note`, not a new file.
- `fold_request` / CLI `nap` of two identical notes after heal: only one view node, so the old `(prefix, prefix)` nap path is gone.

### Test Infrastructure

- Framework: pytest via `tox -e py311` (iterate); `tox run-parallel` at end-of-work.
- Test location: `tests/`
- Conventions: `tmp_path` + `init_repo`; session `summem` fixture.
- New test files: none. Cases in `tests/test_zipper.py`, `tests/test_nap.py`, `tests/test_nap_reject.py` (or existing overlap tests in `tests/test_nap.py`). Retarget `test_cli_note_text_inside_nap_exits_0_no_loose_note`, `test_write_nap_identical_text_notes_still_concat`, `test_nap_two_identical_notes_by_repeated_id`, `test_identical_notes_nappable_after_heal_view`, `test_equal_grain_pair_duplicate_ids_when_same_text`, `test_fold_request_identical_notes_use_short_prefix`, `test_nap_accepts_prefix_of_identical_notes`.

### Integration Tests

- `test_zipper.py`: packed text + new same-text note + heal → file gone, zoom reaches. CLI: `test_cli_note_text_inside_nap_exits_0_no_loose_note` after packing A+B, `main(["note", "A"])`.
- `test_nap.py` / `test_nap_reject.py`: `write_nap` of two same-digest notes raises before write.

## Implementation Plan

### 1. Heal note/note overlap — executable — done

- Files: `summem`, `tests/test_zipper.py`, `tests/gitutil.py`
- Creative ref: `memory-bank/active/creative/creative-leaf-identity.md`

1. Stub tests: add `test_heal_two_identical_notes_keeps_newer` (two files → heal → one file, later stamp; then `assert_unique_cover`). Leave `test_two_identical_notes_stay` alone: it never calls `heal_view`. Change `test_identical_notes_nappable_after_heal_view` so it no longer requires both files after heal. Add `test_note_after_packed_text_is_healed_away` as a library pin (`write_note` + `heal_view`; file gone; zoom reaches). Retarget `tests/test_zipper.py::test_cli_note_text_inside_nap_exits_0_no_loose_note` (add `capsys`): after packing A+B, `main(["note", "A"])` returns 0, stdout is exactly `Saved.\n`, no loose note with caption `A`, `zoom_reaches` the remaining pack still finds `A`.
2. Stub interface: none. No new signatures. Removing the note/note skip is step 4, not a stub.
3. Write tests and run red: `tox -e py311 -- tests/test_zipper.py::test_heal_two_identical_notes_keeps_newer` (new; red until the skip is gone). Fill in the four CLI assertions on `test_cli_note_text_inside_nap_exits_0_no_loose_note` in this step; that case is a contract pin of intended trigger 1 and should stay green on current `note` (heal already drops the packed-text file and prints `Saved.`).
4. Write code and run green: remove the note/note skip in `_first_overlap`. In `tests/gitutil.py::assert_unique_cover`, delete `if a.kind == "note" and b.kind == "note": continue` and replace the docstring claim “Two notes may share a digest” with: after heal, every pair of view nodes has disjoint leaf-sets, including two notes.

### 2. `write_nap` rejects digest overlap for notes — executable — done

- Files: `summem`, `tests/test_nap.py`, `tests/test_nap_reject.py`, `tests/test_cli.py`
- Creative ref: `memory-bank/active/creative/creative-leaf-identity.md`

1. Stub tests: retarget `tests/test_nap.py::test_write_nap_identical_text_notes_still_concat` so a direct `write_nap` of two identical-text notes (no prior heal) raises `ValueError` on overlapping leaves, writes no `.summ` and no `.tree`, and **both** loose note files remain. Retarget `test_nap_two_identical_notes_by_repeated_id` and CLI `test_nap_accepts_prefix_of_identical_notes` (after heal there is one node; nap of one id twice still fails).
2. Stub interface: none.
3. Write tests and run red: the new reject case.
4. Write code and run green: drop the `left.kind == "nap" or right.kind == "nap"` conjunct. Keep the existing overlap error string if tests already pin `"overlapping packs"`; if that string is a lie for two notes, use one truthful overlap error and update those tests in this unit — do not add a second error family.

### 3. Fold listings and remaining same-id tests — executable — done

- Files: `tests/test_fold.py`, `tests/test_cli.py`
- Creative ref: `memory-bank/active/creative/creative-leaf-identity.md`

1. Stub tests: `test_equal_grain_pair_duplicate_ids_when_same_text` and `test_fold_request_identical_notes_use_short_prefix` become: after heal, one node, no `(id, id)` pair. If fold is invoked without heal, do not require a `(prefix, prefix)` Run line.
2. Stub interface: none unless `fold_request` still offers the pair because it lists before heal; mutating CLI heals first. Only change `fold_request` if a failing test shows it still pairs two identical notes that `list_view` can see.
3. Write tests and run red.
4. Write code and run green: only if fold still requests the collapsed pair; otherwise tests-only.

### 4. Atlas and theory — prose/policy — done

- Files: `docs/architecture/index.md`, `memory-bank/systemPatterns.md`, `docs/theory.md`
- No tests: prose/policy artifact
- Creative ref: `memory-bank/active/creative/creative-leaf-identity.md`

1. Identity: replace “Two notes with the same text share an id; they remain two view nodes.” Two notes with the same text share an id; heal keeps one. Packed coverage of a later copy is the shoebox.
2. Zipper: replace “Two loose notes that happen to share text are skipped.” They are not skipped; heal unlinks the older filename. Heal still runs before `nap` resolves ids; if that drop leaves a missing id, the command fails and does not fold.
3. `systemPatterns.md`: replace “two notes with the same text share an id, and adjacency must keep both.” After heal they are one view node; adjacency still needs two distinct ids when two nodes exist.
4. `docs/theory.md` leak section: not a leak. `L` is a set of facts. Heal dropping a packed-text loose note is the design. `note` of a duplicate does not grow `L`. The remaining hole was napping two copies; that path is closed.

## Technology Validation

No new technology - validation not required

## Challenges & Mitigations

- `test_heal_note_covered_by_nap_dropped` must stay: it is the same rule as trigger 1, with the packed child’s name. Do not special-case rematerialize.
- `assert_unique_cover` in `tests/gitutil.py` currently skips note/note and would stay blind to this bug class. Unit 1 drops that skip. Do not share `_first_overlap` with the helper: tests should not import a private walk just to avoid a six-line loop.
- Unlinking `left` of two grain-1 notes keeps the later filename only because `list_view` sorts by name. If a test plants names out of stamp order, “newer” is filename-newer, not clock-newer. Tests should use `write_note` stamps that match name order.
- Existing overlap error says `overlapping packs`. Two notes are not packs. Mitigation: one overlap error; update pinned substrings in this task rather than teach a second phrase.

## Pre-Mortem

- Shipped “keep the new file” tests from the issue’s write-up and fought the shoebox: the plan’s trigger-1 test pins deletion, not survival.
- Left the note/note skip, only rejected `write_nap`, then `fold_request` stuck at budget on `(id, id)`: unit 1 removes the skip so heal runs first on `note`/`nap`.
- Left `assert_unique_cover` skipping note/note so the shared helper stayed blind: unit 1 drops that skip.

## QA Findings (2026-08-29 — FAIL, build rework)

Production diff (4 lines) is clean: KISS/DRY/YAGNI, no debris, all four acceptance criteria pinned, `assert_unique_cover` now exercised post-heal, `tox -e py311` 371 passed / 1 skipped. Three blocking findings, all small and test/prose-local — no plan change required.

1. **Three test names assert the opposite of their bodies.** `test_write_nap_identical_text_notes_still_concat` (raises, writes nothing), `test_nap_accepts_prefix_of_identical_notes` (exit 1, `not adjacent`), `test_identical_notes_nappable_after_heal_view` (collapses to one node). Docstrings were retargeted; names were not. Rename each.
2. **`test_two_identical_notes_stay` docstring is now false.** "not unlinked by leaf-set helpers" — `_first_overlap` is a leaf-set helper and now unlinks one. Body is correct (no `heal_view`); scope the name and docstring to what it pins: `leaf_digests` reports the shared digest for both nodes.
3. **`docs/theory.md:241` is broken prose.** "Heal and that refuse make a duplicate list a path the view does not offer." Rewrite; re-anchor "a hash of a list" to `leafset_id` vs `leaf_digests`, whose asymmetry is still true and is why the refuse exists.

Advisories (non-blocking): `overlapping packs` wording for two loose notes is CLI-unreachable (both mutating commands heal first) and was a permitted plan choice; the planted-tree zoom/recall duplicate-date tests should say they cover pre-change packs. Full detail in `memory-bank/active/.qa-validation-status`.

## QA Findings (2026-08-29 — PASS)

The QA rework resolved all three blockers. Test names and docstrings now match their assertions, `docs/theory.md` coherently names the list-vs-set asymmetry between `leafset_id` and `leaf_digests`, and compatibility tests explicitly plant pre-change duplicate-child packs. No blocking semantic findings remain. `uvx --with tox tox run-parallel` passed on py311 and py314; py312 and py313 skipped because those interpreters are unavailable.

## Status

- [x] Component analysis complete
- [x] Open questions resolved
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS 2026-08-29)
- [x] Build
- [x] QA (FAIL 2026-08-29 — build rework: 3 blocking findings)
- [x] Build (rework: renamed 3 tests, scoped leaf_digests pin, theory sentence)
- [x] QA (PASS 2026-08-29)
