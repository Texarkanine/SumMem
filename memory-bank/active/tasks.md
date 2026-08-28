# Task: fold-pack-captions

* Task ID: fold-pack-captions
* Complexity: Level 2
* Type: simple enhancement

When `fold_request` quotes two packs (grain > 1), each source line is the caption only. Grain and content-id stay on wake and on the `Run:` line. Leaf-pair quotes stay dated wake lines.

## Test Plan (TDD)

### Behaviors to Verify

- Pack-pair quotes: four notes folded into two x2 packs plus one extra note, budget 2 → `fold_request` quoted lines are `  {caption}` for each pack, not `x2 <prefix>: {caption}`
- Pack-pair `Run:`: that same prompt still contains `nap {prefix_a} {prefix_b} `
- Pack-pair wake unchanged: `wake_text` of the same store still contains `x2 <prefix>: {caption}` for each pack
- Empty pack caption: two packs whose `.summ` files are missing, plus one extra note, budget 2 → quoted lines are indented blanks (caption empty), not reconstructed `xN <prefix>:` lines; `Run:` still has both prefixes
- Leaf-pair quotes unchanged: existing `test_fold_request_mentions_remaining` still expects dated `x1 YYYY-MM-DD:` lines

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`
- Test location: `tests/`
- Conventions: `test_*.py`; helpers `init_repo` from `gitutil`, `dated_leaf` from `conftest`; `summem` fixture loads repo-root driver; iterate with `tox -e py311 -- tests/test_fold.py::…`
- New test files: none

## Implementation Plan

### 1. fold_request pack quotes — executable

- Files: `tests/test_fold.py`, `summem` (`fold_request`)

1. Stub tests: `test_fold_request_pack_pair_quotes_captions_only` and `test_fold_request_empty_pack_caption_is_blank_quote` in `tests/test_fold.py` (empty bodies)
2. Stub interface: no new public function. `fold_request` already emits the two quoted lines; leave its signature unchanged
3. Write tests and run red:
    - Pack-pair: write a,b,c,d,i; nap a+b as `e & f`, nap c+d as `g & h`; `fold_request(repo, 2)` contains `  e & f\n` and `  g & h\n`; does not contain `x{n} {prefix}:` for either pack; `Run:` contains both `short_id` prefixes; `wake_text` still has `x2 {prefix}: e & f` and `x2 {prefix}: g & h`
    - Empty caption: same two-pack plus extra-note setup, unlink both `.summ` files; quoted block is two indented empty lines; fold text does not contain `x2 {prefix}:`; `Run:` still has both prefixes
    - Do not retarget `test_fold_request_mentions_remaining` (leaf-pair dated lines)
4. Write code and run green: in `fold_request`, for each quoted node use `node.caption` when `node.kind != "note"` and `node.leaves > 1`; otherwise keep `format_wake_line`. Do not change `format_wake_line`. Then `tox -e py311 -- tests/test_fold.py`

### 2. Atlas listing contract — prose/policy

- Files: `docs/architecture/index.md`
- No tests: prose/policy artifact

1. In Zoom and recall, stop saying listings including fold share `format_wake_line` for pack lines. Wake, recall, and zoom still share that grammar. Fold quotes pack captions without grain or prefix; ids stay on the `Run:` line. Fold still calls `short_id` for that `Run:` line.
2. Do not add a change-detector test on the atlas.

### 3. Briefing fold quote — prose/policy

- Files: `memory-bank/systemPatterns.md`
- No tests: prose/policy artifact

1. In How This System Works, add that `fold_request` quotes pack captions without grain or prefix (ids live on `Run:`). Leave the wake `xN <prefix>:` grammar as-is.
2. Do not add a change-detector test on the briefing.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `fold_request` / `format_wake_line` / `short_id` in `summem`
- `write_nap` cannot create an empty caption (`require_entry`); the empty-caption case uses a missing `.summ`, matching `test_wake_missing_sum_prints_id_and_grain_without_caption`
- `note`, `nap`, and `surgery.py` print `fold_request` as-is; they need no separate printers

## Challenges & Mitigations

- Changing `format_wake_line` would strip grain and hash from wake, recall, and zoom: fold_request is the only production edit; existing `tests/test_wake.py` pack-line tests stay the regression net
- A “prefix not in prompt” assertion would fail because `Run:` still has prefixes: assert absence of the `xN {prefix}:` token, not of the prefix itself
- `write_nap("", …)` cannot seed an empty caption: unlink `.summ` after a real nap, as wake tests already do

## Pre-Mortem

- The quoted lines were “fixed” by changing `format_wake_line`, so wake listings lost ids: already covered by Challenge 1; the executable step names `fold_request` only
- Leaf-pair quotes were stripped of dates because the condition used `leaves > 1` without keeping notes on `format_wake_line`: the branch is `kind != "note" and leaves > 1`; leaf regression is an existing green test, not a retarget
- Empty captions were treated as out of scope and fold reconstructed `xN prefix:`: already covered by Challenge 3 and the second test

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
