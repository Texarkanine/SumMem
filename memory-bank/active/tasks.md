# Task: entry-gate-split

* Task ID: entry-gate-split
* Complexity: Level 2
* Type: simple enhancement

Implement the disjoint split in `memory-bank/active/creative/creative-entry-gate-split.md`: write rule (WHAT/WHEN) lives only in `prompt_text()` / the `init`-emitted `AGENTS.md` prefix; command recipes (HOW) live only in `how_to_text()` / root-wake Usage. Neither surface restates the other. This repo dogfoods the shipped default via lockstep; consumers may edit the prefix.

Standalone creative already resolved the architecture. This plan does not re-open it.


## Test Plan (TDD)

### Behaviors to Verify

- Prefix is the write rule: `prompt_text()` contains the membership probe, genre list, denylist, personal/machine stay-out, and skip-if-nothing-qualifies, plus session-start `{AGENT_BIN} wake` and skip-if-prior-project-root-wake → those tokens present; `(mandatory)` only on the wake heading
- Prefix is not a recipe book: `prompt_text()` → `{AGENT_BIN}` occurs once, on the wake line; `{AGENT_BIN} note` absent; `wake --path`, `x1 YYYY-MM-DD`, `== SumMem Usage ==`, `You are up to speed.`, writer-only (`invent filenames`, `the only writer`, `part of your work`) absent
- Usage is recipes only: `how_to_text()` → `{AGENT_BIN} note "…"`, nap already-stored / do-not-retry, recall/zoom grammar, `wake --path`, writer-only paragraph present
- Usage is not a write rule: `how_to_text()` → `work on this repository`, `personal`, `PR opened`, `Skip if nothing qualifies`, `already remembered` absent
- Disjointness: write-rule phrases listed above are absent from `how_to_text()`; mechanical phrases (writer-only, `wake --path`, pack grammar) are absent from `prompt_text()`
- Lockstep: this repo's `AGENTS.md` starts with `prompt_text()` (dogfood of the shipped default, not a consumer contract)
- `init` recipe: `main(['init'])` stdout contains `prompt_text()` and tells the operator the block is a starting write rule they may edit, and not to copy command syntax into the prefix; `paste` still absent; `init` still writes nothing
- Root wake unchanged except Usage body: empty root wake is still `how_to_text()` plus footer (existing `tests/test_scopes.py` equality)

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` (`testpaths = tests`)
- Test location: `tests/test_init.py` (prompt contract); `tests/test_scopes.py` (root-wake assembly — no pin changes expected; it compares full `how_to_text()`)
- Conventions: one behavior per test; docstrings state the contract; leftover-pin class from wake-usage-prompt — name every assert that must move, not only the new ones
- New test files: none

## Implementation Plan

### 1. Agent prompt contract — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text`, `how_to_text`, `init_text`), `AGENTS.md`

1. Stub tests: retarget `test_prompt_text_invariants` (write-rule pins in, recipe forbids; `{AGENT_BIN}` once on wake); retarget `test_prompt_text_notes_are_part_of_the_work` onto `how_to_text()` (or rename); drop `work on this repository` from `test_how_to_text_is_the_usage_section` and add forbids; add `test_prompt_and_how_to_are_disjoint`; extend `test_init_prints_recipe_and_prompt` for the editable-template recipe; comment `test_agents_md_starts_with_prompt_text` that lockstep is this repo's default, not a consumer contract. Empty bodies / failing asserts only.
2. Stub interface: none. `prompt_text`, `how_to_text`, and `init_text` already exist with the right signatures.
3. Write tests and run red: `tox -e py311 -- tests/test_init.py`. Expected red: prefix still has `{AGENT_BIN} note` and writer-only; Usage still has membership; `init` recipe still lacks editability; disjointness fails. Lockstep stays green until `prompt_text()` changes.
4. Write code and run green: rewrite `prompt_text()` (wake handoff + write rule + `note` as verb name, no argv, no writer-only, drop `(mandatory)` from Register Memories); rewrite `how_to_text()` (note argv records one short line; nap/retry; recall/zoom; catalog; writer-only); rewrite `init_text()` operator wrapper; copy the new prefix into `AGENTS.md`. Re-run `tox -e py311 -- tests/test_init.py`, then `tox -e py311` for leftover pins elsewhere.

### 2. Briefing — prose/policy

- Files: `memory-bank/systemPatterns.md`, `docs/architecture/index.md`, `memory-bank/productContext.md`, `README.md`
- No tests: prose/policy artifact

1. `systemPatterns.md`: bootstrap owns the write rule; Usage must not repeat it; writer-only is Usage; `{AGENT_BIN}` in the prefix is the wake handoff only.
2. `docs/architecture/index.md`: change-surface row "what an agent is allowed to know or type" — writer-only is Usage, not the activation block. Invariant "Personal and machine facts stay out" remains product intent / shipped default; the prefix is repo policy the script does not parse.
3. `memory-bank/productContext.md`: "activation block treats the files the script wrote as part of your work" → that sentence is Usage, not the activation block.
4. `README.md` Quick Start step 2: insert is a starting write rule the operator may edit; command syntax comes from root wake.

## Technology Validation

No new technology - validation not required

## Dependencies

- Creative decision in `memory-bank/active/creative/creative-entry-gate-split.md` (already resolved)
- Existing `tests/test_init.py` and `tests/test_scopes.py`
- This repo's `AGENTS.md` prefix lockstep

## Challenges & Mitigations

- Leftover pins (wake-usage-prompt first preflight FAIL): named every `test_init.py` assert to retarget above; `test_scopes.py` compares full `how_to_text()` so it follows the new body. After green `test_init.py`, run full `tox -e py311` before calling build done.
- Shared-constant hoist (note-membership advisory, later rejected): keep two prompt functions as direct strings. Do not factor a `MEMBERSHIP_PROBE`.
- Agents fail to bind "record" to `{AGENT_BIN} note "…"`: prefix names the verb `note` without argv. If QA finds silent non-noting, tighten the duty sentence; do not put argv back.
- `init` recipe leaking into `prompt_text()`: demotion stays in `init_text()` only. `test_init_prints_recipe_and_prompt` checks editability on the stdout prefix before `prompt_text()`; `prompt_text()` forbids "you may edit".

## Pre-Mortem

- Leftover membership in Usage would make consumer prefix edits fake: the disjointness test is the fence; Challenge 1 covers missing pins.
- Briefing still teaches writer-only as activation: step 2 exists so the atlas and productContext do not lie after the move.
- Treating lockstep as a consumer contract and "fixing" a foreign `AGENTS.md`: the test docstring states dogfood-only; do not add a foreign-repo lockstep test.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
