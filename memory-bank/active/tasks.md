# Task: note-membership

* Task ID: note-membership
* Complexity: Level 3
* Type: enhancement

Retarget shipped `note` membership so agents record lore and tree-affecting in-flight work, not process telemetry, in as few words as will carry it.

## Component Analysis

### Affected Components
- `prompt_text()` in `summem`: committed `AGENTS.md` bootstrap — note duty and stay-out. Must not grow into a lecture. Today: “a fact another contributor would still need.”
- `how_to_text()` in `summem`: root-wake Usage — versioned membership. Today: “designs, decisions, invariants” plus clone-portability (“even when cloned on another machine”).
- `AGENTS.md`: lockstep prefix with `prompt_text()`.
- `tests/test_init.py`: bootstrap/how-to invariants. Bootstrap currently **forbids** `clone`; how-to currently **requires** `another machine`. Those pins encode the old split, not a store contract.
- OptMem global rule (out of repo): constraint only — do not name it; change it only if SumMem cannot carry the test.

### Cross-Module Dependencies
- `init_text()` wraps `prompt_text()`; no extra membership copy.
- Root `wake` prepends `how_to_text()`; pulls omit it. `WAKE_LINES` does not count Usage.
- `test_scopes.py` compares wake stdout to `how_to_text()` by identity — changing the function does not break those tests.

### Boundary Changes
- Agent-facing prompt contract only. No CLI verbs, store, or nap `fold_request` change.
- Deliberate invariant retarget in `test_init.py` if the new probe uses “this clone” on the bootstrap.

### Invariants & Constraints
- Must preserve writer-only + untracked clause.
- Must preserve wake-usage split (small bootstrap, versioned how-to).
- Must not name OptMem, Niko, or `memory-bank/`.
- Must not restore `must still be true after a fresh clone`.
- Must keep write-time-true gotchas legal.
- Membership language must not add a Register Memories lecture (sentence count ≤ today).

## Open Questions

- [x] Membership wording and placement → Resolved: work-in-this-clone probe on both surfaces; how-to carries genre + denylist + skip-if-nothing; OptMem untouched (see `memory-bank/active/creative/creative-membership-wording.md`)

## Test Plan (TDD)

### Behaviors to Verify

- Bootstrap probe: `prompt_text()` → contains `work in this clone`
- How-to probe: `how_to_text()` → contains `work in this clone`
- Bootstrap stays lecture-free: `prompt_text()` → no `another machine`, no `must still be true after a fresh clone`
- How-to drops portability lecture: `how_to_text()` → still has `clone`, does not require `another machine`, still no `must still be true after a fresh clone`
- Lockstep: this repo’s `AGENTS.md` starts with `prompt_text().strip()`
- Writer-only unchanged: existing `test_prompt_text_notes_are_part_of_the_work` still passes

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`
- Test location: `tests/`
- Conventions: `test_*.py`; `summem` fixture loads repo-root driver; iterate with `tox -e py311 -- tests/test_init.py`
- New test files: none

### Integration Tests

- None — `test_scopes.py` already asserts root wake stdout begins with `how_to_text()` by identity

## Implementation Plan

### 1. Membership language — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text`, `how_to_text`), `AGENTS.md`
- Creative ref: `memory-bank/active/creative/creative-membership-wording.md`
- [x] Complete

1. Stub tests: no new cases. Leave `prompt_text()` / `how_to_text()` signatures unchanged.
2. Stub interface: none.
3. Write tests and run red: in `test_prompt_text_invariants`, remove `assert "clone" not in lower`; add `assert "work in this clone" in lower`; keep `another machine` and `must still be true after a fresh clone` out. In `test_how_to_text_is_the_usage_section`, remove `assert "another machine" in lower`; add `assert "work in this clone" in lower`; keep `assert "clone" in lower`. Run `tox -e py311 -- tests/test_init.py::test_prompt_text_invariants tests/test_init.py::test_how_to_text_is_the_usage_section tests/test_init.py::test_agents_md_starts_with_prompt_text` — red on the new pin and lockstep.
4. Write code and run green: set `prompt_text()` Register Memories body and `how_to_text()` note paragraph to the sentences in the creative Implementation Notes. Copy `prompt_text()` onto the `AGENTS.md` prefix. Re-run `tox -e py311 -- tests/test_init.py`.

### 2. Persistent docs — prose/policy

- Files: none
- No tests: prose/policy artifact
- Creative ref: same
- [x] Complete (no-op)

1. Do not edit `productContext.md`, `README.md`, or OptMem. The product picture is still “learned a fact”; the README already says gotchas. OptMem stays unnamed and unedited.

## Technology Validation

No new technology - validation not required

## Challenges & Mitigations

- Phrase tests on denylist examples (PR / checks / archived) become change-detectors: do not add them; pin only `work in this clone`
- `(mandatory)` still read as “emit a note every session”: how-to line “Skip if nothing qualifies or it is already remembered” is the counterweight; do not drop the heading
- Existing wake notes few-shot the old genre: out of scope — do not rewrite the store
- Bootstrap without the denylist if an agent notes before wake: accepted; session-start wake is already mandatory

## Pre-Mortem

- Agents still tweet because bootstrap still says “would still need”: already covered — the probe lands on both surfaces
- Density rejected because Register Memories grew: creative counted sentences (4 = today) and forbade When/What headings
- Write-time gotchas become illegal because we restored eternal currency: we did not; the denylist is events, not truth-over-time
- Next wording tweak is blocked by pins on “PR opened”: already covered by Challenge 1
- Products couple because we edited OptMem or named it: non-goal; SumMem carries the test alone

## Status

- [x] Component analysis complete
- [x] Open questions resolved
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
