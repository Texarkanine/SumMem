# Task: tree-schema

* Task ID: tree-schema
* Complexity: Level 2
* Type: simple enhancement

Clean-cut `.tree` JSON (`c` + `type: note|nap`, no `v`) and undated wake lines. Python keeps `Tree.kids`. Ignore unknown JSON fields. Do not dual-read `kids`/`k`.

## Test Plan (TDD)

### Behaviors to Verify

- Dump one note: `dumps_tree` → `{"c":[{"name":"…","text":"hello","type":"note"}]}\n` (no `v`/`kids`/`k`)
- Dump nested nap: children use `type:nap` / `type:note`; nested object is `{c:[…]}` only
- Round-trip: `loads_tree(dumps_tree(t)) == t` for mixed note+nap trees
- Unknown fields: `loads_tree` of a valid tree plus extra keys (including leftover `v`/`kids` on the same object that already has `c` and `type`) succeeds and matches the known fields
- Clean cut: `loads_tree(b'{"kids":[],"v":1}\n')` raises (no `c`)
- Wake note: `hello` not `YYYY-MM-DD: hello`
- Wake pack (`leaves>1`): `xN <prefix>: caption` with no date
- Wake pack missing caption: `xN <prefix>:`
- Fold/nap prompt lines inherit `format_wake_line` (indented undated captions)

### Test Infrastructure

- Framework: pytest via `uv run --python 3.11 --with pytest pytest` (`pytest.ini`)
- Test location: `tests/`
- Conventions: `test_*.py`, `load_summem()` from `conftest.py`, docstring names the behavior
- New test files: none — extend `tests/test_codec.py` and rewrite assertions in `tests/test_wake.py`, `tests/test_nap.py`, `tests/test_fold.py`

## Implementation Plan

### 1. Canonical tree codec — executable

- Files: `tests/test_codec.py`, `.summem/summem`

1. Stub tests: add `test_loads_tree_ignores_unknown_fields` and `test_loads_tree_rejects_kids_key_without_c` (empty bodies). Keep existing dump/round-trip names.
2. Stub interface: `Tree` without `v`; `_tree_dict` / `_tree_from_dict` still present, signatures unchanged.
3. Write tests and run red: golden bytes use `c`/`type`; unknown-field fixture includes `"v":1` and `"kids":[]` beside a real `"c"`; old-only `{"kids":[],"v":1}` raises; nested dump has no `"v"` / `"kids"` / `"k"`.
4. Write code and run green: `_tree_dict` emits `{c:[…]}` with `type: note|nap`; `_tree_from_dict` reads `c` and `type`, ignores other keys; drop `Tree.v`.

### 2. Undated wake lines — executable

- Files: `tests/test_wake.py`, `tests/test_nap.py`, `tests/test_fold.py`, `.summem/summem`

1. Stub tests: no new cases; existing note/pack/missing-caption/over-budget/prompt tests already cover the lines.
2. Stub interface: `format_wake_line` signature unchanged.
3. Write tests and run red: note `== "hello"`; pack `== f"x2 {prefix}: pair"`; missing caption `== f"x2 {prefix}:"`; newest-four notes `== [f"n{i}" for i in range(7, 11)]`; fold prompts `  c\n` / `  d\n` (no date). `xN` still only when `leaves > 1`.
4. Write code and run green: `format_wake_line` drops `_day_from_stamp` (keep the helper; catalog stats still use it).

### 3. Contract prose — prose/policy

- Files: `VISION.md`, `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. Schema lines: Tree `{c}`; note `type=note`, `name`, `text`; nap `type=nap`, `id`, `sum`, `tree`. Unknown fields ignored. No `v`.
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

## Pre-Mortem

- Wake date removed only on packs, notes still dated: already covered by rewriting every `test_wake.py` / `test_fold.py` dated assertion in step 2.
- Dual-read of `kids` sneaks in “to be nice”: clean-cut test in step 1 (`kids` without `c` raises) is the guard.
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
