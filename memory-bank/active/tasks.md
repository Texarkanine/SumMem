# Task: prompt-membership

* Task ID: prompt-membership
* Complexity: Level 2
* Type: simple enhancement

Split the baked SumMem Register Memories paragraph in `prompt_text()` so the mandatory-note workflow and the clone-portability membership test are separate sentences. Lockstep `AGENTS.md`. No store or CLI change. Design record: `memory-bank/active/creative/creative-note-membership.md`.

Operator after blocking preflight: the new wording is policy. `init` printing `prompt_text()` is not a reason to assert on the sentences. Cut the planned phrase tests. Do not add change-detectors.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

Existing tests that must stay green (not new work, not new assertions):

- `test_agents_md_starts_with_prompt_text` — lockstep of `AGENTS.md` prefix to `prompt_text()` (contract across files, not a wording snapshot)
- `test_prompt_text_invariants` / `test_init_prints_paste_recipe_and_prompt` — current activation contract; new prose must not drop `personal`, `contributor`, `.summem/summem`, etc.

### Test Infrastructure

- Framework: pytest / `tox`
- Test location: `tests/test_init.py`
- Conventions: do not add phrase, heading, or checklist asserts on `prompt_text()`
- New test files: none

## Implementation Plan

### 1. Baked prompt membership — prose/policy

- Files: `summem` (`prompt_text()`), `AGENTS.md`
- No tests: prose/policy artifact

1. Rewrite the Register Memories body in `prompt_text()` per the creative: workflow (when to note) in one sentence; membership as its own sentence ending on clone-portability (true after a fresh clone on another machine; personal, machine-local, and preference facts stay out). Nap-if-asked stays. Do not name OptMem. Do not quote the leaked uv/rc3 line. Do not add a denylist or a wake reminder. Keep words the existing invariants already require (`personal`, `contributor`, `.summem/summem`).
2. Copy the new `prompt_text()` prefix into `AGENTS.md`. Do not edit the Agent context section below the baked block.
3. Run `tests/test_init.py`, then full `tox`, so lockstep and current invariants stay green.

## Technology Validation

No new technology - validation not required

## Dependencies

- `test_agents_md_starts_with_prompt_text` (edit `prompt_text()` and `AGENTS.md` together)
- Creative decision B in `memory-bank/active/creative/creative-note-membership.md`

## Challenges & Mitigations

- New prose drops a word an existing invariant requires: keep `personal`, `contributor`, and `.summem/summem` in the rewrite; the existing test is the check, not a new one.
- Overlong prompt: few short sentences. Do not take the preflight advisory (new `When to note` / `What belongs` headings) unless the operator asks; this replan stays on the creative’s sentence split.
- Branch vs #14: do not rewrite git-add / “tool manages them” lines unless they sit inside the sentences we split.

## Pre-Mortem

- Someone adds `assert "clone" in prompt` during build to “be safe”: do not; that is the change-detector this replan cuts.
- A later spawn still says “document this machine’s gap”: accepted creative tradeoff; not this task.
- Lockstep test fails because only one of `summem` / `AGENTS.md` was edited: already covered — copy the prefix in the same step.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
