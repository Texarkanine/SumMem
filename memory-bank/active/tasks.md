# Task: dated-leaf-wake

* Task ID: dated-leaf-wake
* Complexity: Level 2
* Type: simple enhancement

Print each loose note on `wake` as `x1 (YYYY-MM-DD): text` from the filename stamp. Leave nap lines `xN <prefix>: caption` with no date. One printer (`format_wake_line`) feeds wake, expand, recall’s view pass, and `fold_request`.

## Test Plan (TDD)

### Behaviors to Verify

- Leaf wake line: write a note at a known UTC instant → wake prints `x1 (YYYY-MM-DD): <exact stored text>` and does not put the day after the colon as body.
- Day source: stamp `20260824T123005Z` → `_day_from_stamp` returns `2026-08-24` (UTC calendar date, not local).
- Two leaves: two notes → two prefixed lines, sorted by filename as today.
- Nap unchanged: pack with `leaves > 1` → `xN <prefix>: caption` (or `xN <prefix>:`) and the line contains no `YYYY-MM-DD`.
- Grain-1 pack: `kind != "note"` and `leaves <= 1` → caption only (today’s behavior), not a dated `x1`.
- Fold prompt: over-budget leaf pair → `fold_request` body lines are the same leaf shape (`  x1 (…): text`), not bare text.
- Date is not an id: `resolve_id("2026-08-24", view_ids)` → `unknown id` (hyphens are not a content-id prefix).
- Empty note caption: dated leaf with no text → `x1 (YYYY-MM-DD):` (same trailing-colon convention as a captionless pack).
- [Edge] Missing/conflict `.sum` on a pack → still grain + prefix, still no date.
- [Edge] Under-budget expand of a nested `NoteChild` → printed child uses that child’s `name` stamp, `kind == "note"`.
- [Edge] Recall of a loose note still matches the stored sentence (substring); view-line match may include the new prefix.
- [Regression] `zoom` of a pack still prints children; zoom of a leaf still prints `{id}  {text}` (zoom is not `format_wake_line`).
- [Regression] Wake still omits `notes/`, `naps/`, and `git`; still never prints `Run:`.

### Test Infrastructure

- Framework: pytest via `tox` (`tox.ini` `py311`–`py314`, `package = skip`)
- Test location: `tests/`
- Conventions: `test_<area>.py`, `load_summem()` + `init_repo`, explicit `datetime(..., tzinfo=UTC)` and `Random` for notes; monkeypatch `WAKE_LINES` when the window matters
- New test files: none

## Implementation Plan

### 1. Dated leaf printer — executable

- Files: `summem` (`_day_from_stamp`, `format_wake_line`); `tests/test_wake.py`; `tests/test_wake_expand.py`; `tests/test_fold.py`

1. Stub tests: in `tests/test_wake.py` add empty `test_day_from_stamp_formats_utc_calendar_date`, `test_wake_line_is_dated_grain_for_a_note` (replace `test_wake_line_is_text_for_a_note`), `test_wake_pack_line_has_no_date`, `test_format_wake_line_grain1_pack_is_undated_caption`, `test_resolve_id_rejects_hyphenated_day`. Keep using `tests/test_wake.py` for printer unit cases. In `tests/test_fold.py` stub no new names; existing fold-body cases will be rewritten in step 3.
2. Stub interface: add `_day_from_stamp(stamp: str) -> str` with project-style docstring; leave the body empty / `raise NotImplementedError`. Do not change `format_wake_line` yet.
3. Write tests and run red:
    - `_day_from_stamp("20260824T123005Z") == "2026-08-24"`
    - `write_note(..., datetime(2026, 8, 18, 12, 30, 5, tzinfo=UTC), ...)` → `wake_text` line `x1 (2026-08-18): hello`; stored bytes still `hello\n`
    - two-note sort test expects `x1 (2026-01-01): first` / `second`
    - `test_wake_prints_at_most_wake_lines_newest` expects `x1 (2026-01-01): n{i}`
    - mixed view: nap line unchanged, `gamma` → `x1 (2026-01-01): gamma`
    - pack tests already exact-match `x2 {prefix}: pair` — add `assert not re.search(r"\d{4}-\d{2}-\d{2}", pack_line)`
    - grain-1: build a `ProjectedNode(kind="nap", leaves=1, stamp=..., caption="solo")` (or the smallest real nap fixture if one exists) → `format_wake_line` returns `solo`
    - `resolve_id("2026-08-24", [64-hex ids])` raises `unknown id`
    - `test_lone_note_does_not_split` expects `x1 (2026-01-01): solo`
    - fold CLI tests that assert `  alpha\n` / `  beta\n` / `  a\n` / `  b\n` / `  c\n` / `  d\n` become `  x1 (` … `): alpha\n` (and siblings). Do not hardcode `date.today()`; match the prefix/suffix so a midnight UTC run is not a flake.
4. Write code and run green: implement `_day_from_stamp` as `{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}`. Change `format_wake_line` so **only** `node.kind == "note"` prints `x1 ({day}): {caption}` (empty caption → trailing colon, no extra space). Leave the `leaves <= 1` branch as caption-only for non-notes. Packs with `leaves > 1` unchanged. Run `tox` (or `tox -e py311` while iterating, full `tox` before calling the unit done).

### 2. Briefing and zoom discriminator — prose/policy

- Files: `memory-bank/systemPatterns.md`; `docs/architecture/index.md`; `summem` (`prompt_text`); `docs/agents-prompt.md`; `AGENTS.md`
- No tests: prose/policy artifact

1. Rewrite the systemPatterns heading that says wake prints undated lines: leaves are `x1 (YYYY-MM-DD): text`; packs stay `xN <prefix>: caption` with no day; ranges stay forbidden.
2. Replace the architecture invariant “Wake prints undated lines, never ranges” with the same leaf/pack split.
3. In `prompt_text()`, keep `x<N> <hash>:` as the zoomable nap signal; add that a leaf is `x1 (YYYY-MM-DD):` and is not a zoom target. Copy the new `prompt_text()` into `docs/agents-prompt.md` and replace the `AGENTS.md` prefix so existing lockstep tests stay green.

## Technology Validation

No new technology - validation not required

## Dependencies

- `ViewNode.stamp` and `ProjectedNode.stamp` already exist (`YYYYMMDDTHHMMSSZ` from the filename).
- Nested expand already sets `kind="note"` and `stamp=child.name.split("-")[0]` in `_projected_child`.
- `docs/agents-prompt.md` and `AGENTS.md` must stay lockstep with `prompt_text()` (`tests/test_init.py`).

## Challenges & Mitigations

- Fold tests create notes via `main(["note", ...])`, so the day is “now” UTC. Mitigation: assert `  x1 (` and `): alpha\n` (etc.), not a hardcoded calendar day.
- Old exact strings (`"hello"`, `"  alpha\n"`) live in several files. Mitigation: grep `tests/` for `== "first"`, `== "hello"`, `== "gamma"`, `== "solo"`, and `  alpha\\n` / `  a\\n` / `  c\\n` before calling the unit green.
- `format_wake_line` currently treats `kind == "note" or leaves <= 1` as one branch. Mitigation: split the condition so grain-1 packs do not grow a date.
- Agents may try to `zoom` an `x1` line. Mitigation: prompt copy states leaves are not zoomable; `resolve_id` already rejects a hyphenated day.

## Pre-Mortem

- Plan failed because we restored the 2026-08-19 wake-listing shape (`YYYY-MM-DD:` on every line, including packs). Response: keep pack lines byte-stable except for tests that only check leaf rows; never prefix a pack with a day.
- Plan failed because fold-body tests were left asserting bare `  alpha\n`. Response: already a Challenge; treat those strings as part of the first executable unit, not a follow-up.
- Plan failed because `AGENTS.md` / `docs/agents-prompt.md` drifted from `prompt_text()`. Response: step 2 is copy-the-function-output, not a paraphrase.
- Plan failed because we dated zoom/recall nested `{id}  {text}` lines and broke zoom proofs. Response: do not touch `_zoom_note_line` or `_recall_nested`; only `format_wake_line`.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
