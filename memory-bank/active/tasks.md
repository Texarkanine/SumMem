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

## Status

- [x] Component analysis complete
- [x] Open questions resolved
- [ ] Test planning complete (TDD)
- [ ] Implementation plan complete
- [ ] Technology validation complete
- [ ] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
