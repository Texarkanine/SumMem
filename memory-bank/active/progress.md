# Progress

Replace the bare `note is too long` rejection with an OptMem-style ratchet for `note` and `nap`, and apply the same rule to other CLI errors that only complain when a next step is known and not obvious.

**Complexity:** Level 2

## 2026-08-20 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated and confirmed intent for [SumMem#16](https://github.com/Texarkanine/SumMem/issues/16) plus a bounded pass over other CLI errors
    - Determined Level 2
* Decisions made
    - Note and nap length ratchets are must-ship; other errors are a secondary walk, not a rewrite of every string
    - Do not invent a next step when we do not know one
* Insights
    - `require_entry` already serves both `note` and `nap`; one message change covers the primary path
    - OptMem's crib is `Too long: %d bytes, limit %d. Accented characters cost 2 bytes. Compress it further.`

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan: length ratchet in `require_entry`, then a closed table of other CLI errors
    - Mapped tests onto existing files; no new test module; no new dependency
* Decisions made
    - Footer interpolates the store limit, not a hardcoded 280
    - Empty stays a problem-only `Empty.`; multi-line gets a next step
    - `unknown id`, `ambiguous id`, `not adjacent`, and range tokens get one next step each
    - `unreadable pack`, `overlapping packs`, `invalid pattern`, `not in a repository` stay problem-only
    - No architecture-page edit
* Insights
    - Existing proofs already lock substrings (`unknown id`, the range token); keep those phrases
    - `require_entry` is the single write path for both commands

## 2026-08-20 - PREFLIGHT - FAIL (fixable)

* Work completed
    - [Preflight](1b1f8b7c-d52d-4955-891e-a5fc3b443028) judged the first plan; first line of `.preflight-status` was `FAIL (fixable)`
* Decisions made
    - Do not build on that plan
* Insights
    - `require_entry` is shared; “note each line” is false for nap
    - `unknown id` is two causes: identity miss vs missing `.tree`

## 2026-08-20 - PLAN - COMPLETE

* Work completed
    - Rewrote the plan against those two findings and the cheap advisories
* Decisions made
    - Multi-line next step is merge-only
    - Wake hint only on `resolve_id`, `_adjacent_nodes`, and `zoom_text`’s final raise
    - Leave `note is empty`
    - Assert 94 × `你` → `282`; extend the existing CLI note leak test; new CLI nap-overlong test; drain `capsys` per tight-store failure
* Insights
    - A unique-string table is the wrong key when one phrase has two causes

## 2026-08-20 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the Level 2 plan against `summem` call sites and existing tests
    - First line of `.preflight-status`: `FAIL (fixable)`
* Decisions made
    - TDD encoding, conventions, and the must-ship `require_entry` length path are acceptable
    - Plan must change before build: multi-line next step is note-only inside shared `require_entry`; `unknown id` next step must not attach to missing-tree raises
* Insights
    - `unknown id` is one string and two causes (identity miss vs missing `.tree`)
    - `tests/test_cli.py::test_note_error_text_omits_store_paths_and_git` already owns the CLI over-long note path
