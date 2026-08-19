# Task: tree-schema

* Task ID: tree-schema
* Complexity: Level 2
* Type: simple enhancement

Clean-cut `.tree` JSON (`c` + `type: note|nap`, no `v`) and undated wake lines. Python keeps `Tree.kids`. Ignore unknown JSON fields. Do not dual-read `kids`/`k`. Reject missing or unsupported child `type`.

## Test Plan (TDD)

### Behaviors to Verify

- Dump one note: `dumps_tree` → `{"c":[{"name":"…","text":"hello","type":"note"}]}\n` (no `v`/`kids`/`k`)
- Dump nested nap: children use `type:nap` / `type:note`; nested object is `{c:[…]}` only
- Round-trip: `loads_tree(dumps_tree(t)) == t` for mixed note+nap trees
- Unknown fields: `loads_tree` of a valid tree plus extra keys (including leftover `v`/`kids` on an object that already has `c` and `type`) succeeds and matches the known fields
- Clean cut: `loads_tree(b'{"kids":[],"v":1}\n')` raises (no `c`)
- Missing child `type`: `loads_tree` of `{c:[{name,text}]}` raises (do not infer note vs nap)
- Unsupported child `type`: `loads_tree` of `{c:[{"type":"pack",…}]}` raises (do not fall through to nap)
- Wake note: `hello` not `YYYY-MM-DD: hello`
- Two notes: lines are exactly `first` and `second` (today `endswith(": first")`)
- Lone expanded note: line is exactly `solo` (`tests/test_wake_expand.py`, today `endswith(": solo")`)
- Wake pack (`leaves>1`): `xN <prefix>: caption` with no date
- Wake pack missing caption: `xN <prefix>:`
- Identical-note nap: line still contains `x2` and ends with `twins` without a date (`tests/test_nap.py`)
- Fold/nap prompt lines inherit `format_wake_line` (indented undated captions)

### Test Infrastructure

- Framework: pytest via `uv run --python 3.11 --with pytest pytest` (`pytest.ini`)
- Test location: `tests/`
- Conventions: `test_*.py`, `load_summem()` from `conftest.py`, docstring names the behavior
- New test files: none — extend `tests/test_codec.py`; rewrite assertions in `tests/test_wake.py`, `tests/test_wake_expand.py`, `tests/test_nap.py`, `tests/test_fold.py`

## Implementation Plan

### 1. Canonical tree codec — executable

- Files: `tests/test_codec.py`, `.summem/summem`

1. Stub tests: add `test_loads_tree_ignores_unknown_fields`, `test_loads_tree_rejects_kids_key_without_c`, `test_loads_tree_rejects_child_missing_type`, `test_loads_tree_rejects_unknown_type` (empty bodies). Keep existing dump/round-trip names.
2. Stub interface: `Tree` without `v`; `_tree_dict` / `_tree_from_dict` still present, signatures unchanged. Do not change dump/load behavior in this step.
3. Write tests and run red: golden bytes use `c`/`type`; unknown-field fixture includes `"v":1` and `"kids":[]` beside a real `"c"`; old-only `{"kids":[],"v":1}` raises; child without `type` raises; child `"type":"pack"` raises; nested dump has no `"v"` / `"kids"` / `"k"`.
4. Write code and run green: `_tree_dict` emits `{c:[…]}` with `type: note|nap`; `_tree_from_dict` reads `c` and `type`, ignores other keys; `type == "note"` → `NoteChild`, `type == "nap"` → `NapChild`, anything else (missing or unknown) raises `ValueError` (no `else` → nap). Drop `Tree.v`.

### 2. Undated wake lines — executable

- Files: `tests/test_wake.py`, `tests/test_wake_expand.py`, `tests/test_nap.py`, `tests/test_fold.py`, `.summem/summem`

1. Stub tests: no new cases; rewrite the existing line assertions listed above.
2. Stub interface: `format_wake_line` signature unchanged.
3. Write tests and run red:
   - `test_wake.py`: two notes `== ["first", "second"]`; single note `== "hello"`; pack `== f"x2 {prefix}: pair"`; mixed pack+note has no dates; missing caption `== f"x2 {prefix}:"`; newest-four `== [f"n{i}" for i in range(7, 11)]`
   - `test_wake_expand.py`: `test_lone_note_does_not_split` → `== "solo"`
   - `test_nap.py`: pack line `== f"x2 {prefix}: pair"`; twins line has `x2` and `endswith("twins")` without `YYYY-MM-DD`
   - `test_fold.py`: prompts contain `  c\n` / `  d\n` (and alpha/beta, a/b), not `  2026-01-01: …`
   - `xN` still only when `leaves > 1`
4. Write code and run green: `format_wake_line` drops `_day_from_stamp` (keep the helper; catalog stats still use it).

### 3. Contract prose — prose/policy

- Files: `VISION.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Schema lines: Tree `{c}`; note `type=note`, `name`, `text`; nap `type=nap`, `id`, `sum`, `tree`. Unknown fields ignored. Missing or unsupported `type` is an error. No `v`.
2. Wake: note is `text`; pack is `xN <prefix>: caption`. Heading/body that say “dated lines” become undated (still never positional ranges).
3. Leave `tests/test_zipper.py` `{"v":1}` fixture as-is: after ignore-unknown it still lacks `c`, so `leaf_digests` stays `None`.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing pytest / `json` / `hashlib` only

## Challenges & Mitigations

- Golden JSON key order: `json.dumps(..., sort_keys=True)` already locks order (`c`; child `id`/`name`/`sum`/`text`/`tree`/`type`). Write expected bytes from that rule, not from hand-waved order.
- `{"v":1}` zipper fixture: still invalid without `c`; do not add a dual-read just to keep that blob special.
- Catalog `store_stats` still prints a date: out of scope; do not strip `_day_from_stamp`.
- Stale `endswith(": …")` assertions outside the obvious date literals: enumerated in step 2 (`test_wake.py` two-note sort, `test_wake_expand.py` solo, `test_nap.py` twins).

## Pre-Mortem

- Wake date removed only on some files, others still expect `: caption`: step 2 lists every remaining `YYYY-MM-DD` / `endswith(": …")` wake assertion in `test_wake.py`, `test_wake_expand.py`, `test_nap.py`, and `test_fold.py`.
- Dual-read of `kids` sneaks in “to be nice”: clean-cut test in step 1 (`kids` without `c` raises) is the guard.
- Unknown `type` still becomes a nap via `else`: `test_loads_tree_rejects_unknown_type` plus an explicit `ValueError` branch (no nap fallback).
- Proofs fail on payload identity: they compare via `dumps_tree` or behavior, not old literals (only `test_codec.py` byte-locks). No extra step.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
